import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './ProfilMembre.css';

const ProfilMembre = () => {
  const { memberId } = useParams();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Get API base URL from environment
  const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
  
  // Get current user from localStorage (simple auth check)
  const [currentUser, setCurrentUser] = useState(null);
  
  // Profile data
  const [memberProfile, setMemberProfile] = useState(null);
  const [memberStats, setMemberStats] = useState({});
  
  // Comments system
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [newRating, setNewRating] = useState(5);
  const [commentStats, setCommentStats] = useState({});
  
  // UI state
  const [showCommentForm, setShowCommentForm] = useState(false);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    if (token) {
      // Simple user object - in real app you'd decode the token
      setCurrentUser({ id: 'current_user_id', role: 'user' });
    }
    
    if (memberId) {
      fetchMemberProfile();
      fetchComments();
    }
  }, [memberId]);

  const fetchMemberProfile = async () => {
    try {
      setLoading(true);
      
      // Get member profile
      const profileResponse = await fetch(`${API_BASE_URL}/api/profiles/${memberId}`);
      if (profileResponse.ok) {
        const profileData = await profileResponse.json();
        setMemberProfile(profileData);
      } else {
        setError('Profil membre non trouvé');
        return;
      }

      // Get member stats
      try {
        const statsResponse = await fetch(`${API_BASE_URL}/api/profiles/${memberId}/stats`);
        if (statsResponse.ok) {
          const statsData = await statsResponse.json();
          setMemberStats(statsData);
        }
      } catch (statsError) {
        console.log('Stats non disponibles pour ce membre');
      }

    } catch (error) {
      console.error('Erreur chargement profil:', error);
      setError('Erreur lors du chargement du profil');
    } finally {
      setLoading(false);
    }
  };

  const fetchComments = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

      // Get comments
      const commentsResponse = await fetch(`${API_BASE_URL}/api/comments/user/${memberId}`, { headers });
      if (commentsResponse.ok) {
        const commentsData = await commentsResponse.json();
        setComments(commentsData);
      }

      // Get comment stats
      const statsResponse = await fetch(`${API_BASE_URL}/api/comments/stats/user/${memberId}`, { headers });
      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setCommentStats(statsData);
      }

    } catch (error) {
      console.error('Erreur chargement commentaires:', error);
      // Not critical - continue without comments
    }
  };

  const submitComment = async () => {
    if (!newComment.trim()) {
      alert('Veuillez écrire un commentaire');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        alert('Vous devez être connecté pour commenter');
        return;
      }

      const response = await fetch(`${API_BASE_URL}/api/comments/user`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          target_user_id: memberId,
          content: newComment,
          rating: newRating
        })
      });

      if (response.ok) {
        alert('Commentaire ajouté avec succès !');
        setNewComment('');
        setNewRating(5);
        setShowCommentForm(false);
        fetchComments(); // Refresh comments
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'Erreur lors de l\'ajout du commentaire');
      }

    } catch (error) {
      console.error('Erreur ajout commentaire:', error);
      alert('Erreur lors de l\'ajout du commentaire');
    }
  };

  const deleteComment = async (commentId) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce commentaire ?')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch(`${API_BASE_URL}/comments/user/${commentId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        alert('Commentaire supprimé');
        fetchComments(); // Refresh comments
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'Erreur lors de la suppression');
      }

    } catch (error) {
      console.error('Erreur suppression commentaire:', error);
      alert('Erreur lors de la suppression');
    }
  };

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, i) => (
      <span key={i} className={`star ${i < rating ? 'filled' : 'empty'}`}>
        ⭐
      </span>
    ));
  };

  const getGameDisplay = (game) => {
    const games = {
      'cs2': 'Counter-Strike 2',
      'lol': 'League of Legends',
      'wow': 'World of Warcraft',
      'sc2': 'StarCraft II',
      'minecraft': 'Minecraft'
    };
    return games[game] || game;
  };

  if (loading) {
    return (
      <div className="app">
        <Header />
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Chargement du profil...</p>
        </div>
        <Footer />
      </div>
    );
  }

  if (error) {
    return (
      <div className="app">
        <Header />
        <div className="error-container">
          <h2>❌ Erreur</h2>
          <p>{error}</p>
          <Link to="/communaute" className="btn-primary-pro">
            ← Retour à la communauté
          </Link>
        </div>
        <Footer />
      </div>
    );
  }

  if (!memberProfile) {
    return (
      <div className="app">
        <Header />
        <div className="error-container">
          <h2>👤 Profil non trouvé</h2>
          <p>Ce membre n'existe pas ou son profil n'est pas accessible.</p>
          <Link to="/communaute" className="btn-primary-pro">
            ← Retour à la communauté
          </Link>
        </div>
        <Footer />
      </div>
    );
  }

  const canDeleteComment = (comment) => {
    return (
      user && (
        comment.author_id === user.id || // Author can delete
        memberProfile.user_id === user.id || // Profile owner can delete
        user.role === 'admin' // Admin can delete
      )
    );
  };

  return (
    <div className="app">
      <Header />
      
      <main className="profil-membre-container">
        {/* Profile Header */}
        <section className="profile-header">
          <div className="profile-header-bg">
            <div className="profile-overlay"></div>
          </div>
          
          <div className="container-pro">
            <div className="profile-info-main">
              <div className="profile-avatar-large">
                {memberProfile.display_name.charAt(0).toUpperCase()}
              </div>
              
              <div className="profile-details">
                <h1 className="profile-name">{memberProfile.display_name}</h1>
                <p className="profile-bio">{memberProfile.bio || 'Aucune biographie renseignée'}</p>
                
                <div className="profile-stats-bar">
                  <div className="stat-item">
                    <span className="stat-value">Niv. {memberProfile.level || 1}</span>
                    <span className="stat-label">Niveau</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-value">{memberProfile.coins || 0}</span>
                    <span className="stat-label">💰 Coins</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-value">{memberProfile.total_tournaments || 0}</span>
                    <span className="stat-label">🏆 Tournois</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-value">{commentStats.total_comments || 0}</span>
                    <span className="stat-label">💬 Commentaires</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-value">
                      {commentStats.average_rating ? commentStats.average_rating.toFixed(1) : '0.0'} ⭐
                    </span>
                    <span className="stat-label">Note moyenne</span>
                  </div>
                </div>
              </div>
              
              <div className="profile-actions">
                <Link to="/communaute" className="btn-outline-pro">
                  ← Retour
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Profile Content */}
        <section className="profile-content">
          <div className="container-pro">
            <div className="profile-sections">
              
              {/* Gaming Info */}
              <div className="profile-section">
                <h3>🎮 Informations Gaming</h3>
                <div className="gaming-info-grid">
                  <div className="info-item">
                    <span className="info-label">Jeux favoris :</span>
                    <span className="info-value">
                      {memberProfile.favorite_games && memberProfile.favorite_games.length > 0
                        ? memberProfile.favorite_games.map(game => getGameDisplay(game)).join(', ')
                        : 'Non renseigné'}
                    </span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Discord :</span>
                    <span className="info-value">
                      {memberProfile.discord_username || 'Non renseigné'}
                    </span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Steam :</span>
                    <span className="info-value">
                      {memberProfile.steam_profile || 'Non renseigné'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Tournament Stats */}
              <div className="profile-section">
                <h3>📊 Statistiques Tournois</h3>
                <div className="stats-grid">
                  <div className="stat-box">
                    <div className="stat-number">{memberProfile.tournaments_won || 0}</div>
                    <div className="stat-label">Victoires</div>
                  </div>
                  <div className="stat-box">
                    <div className="stat-number">{memberProfile.total_tournaments || 0}</div>
                    <div className="stat-label">Participations</div>
                  </div>
                  <div className="stat-box">
                    <div className="stat-number">{memberProfile.trophies_1v1 || 0}</div>
                    <div className="stat-label">Trophées 1v1</div>
                  </div>
                  <div className="stat-box">
                    <div className="stat-number">{memberProfile.trophies_5v5 || 0}</div>
                    <div className="stat-label">Trophées 5v5</div>
                  </div>
                </div>
              </div>

              {/* Comments Section */}
              <div className="profile-section comments-section">
                <div className="comments-header">
                  <h3>💬 Commentaires & Évaluations</h3>
                  {user && user.id !== memberProfile.user_id && (
                    <button 
                      className="btn-primary-pro"
                      onClick={() => setShowCommentForm(!showCommentForm)}
                    >
                      ✏️ Laisser un commentaire
                    </button>
                  )}
                </div>

                {/* Comment Form */}
                {showCommentForm && (
                  <div className="comment-form">
                    <h4>Laisser un commentaire</h4>
                    <div className="rating-selector">
                      <label>Note :</label>
                      <div className="star-selector">
                        {[1, 2, 3, 4, 5].map(star => (
                          <button
                            key={star}
                            type="button"
                            className={`star-btn ${star <= newRating ? 'active' : ''}`}
                            onClick={() => setNewRating(star)}
                          >
                            ⭐
                          </button>
                        ))}
                      </div>
                    </div>
                    <textarea
                      value={newComment}
                      onChange={(e) => setNewComment(e.target.value)}
                      placeholder="Votre commentaire..."
                      className="comment-textarea"
                      rows="4"
                    />
                    <div className="comment-form-actions">
                      <button onClick={submitComment} className="btn-primary-pro">
                        📨 Publier
                      </button>
                      <button 
                        onClick={() => setShowCommentForm(false)}
                        className="btn-outline-pro"
                      >
                        Annuler
                      </button>
                    </div>
                  </div>
                )}

                {/* Comments List */}
                <div className="comments-list">
                  {comments.length === 0 ? (
                    <div className="no-comments">
                      <p>💭 Aucun commentaire pour le moment</p>
                      <p>Soyez le premier à laisser un commentaire sur ce profil !</p>
                    </div>
                  ) : (
                    <>
                      <div className="comments-summary">
                        <p>
                          {commentStats.total_comments} commentaire(s) • 
                          Note moyenne : {commentStats.average_rating ? commentStats.average_rating.toFixed(1) : '0.0'} ⭐
                        </p>
                      </div>
                      
                      {comments.map(comment => (
                        <div key={comment.id} className="comment-card">
                          <div className="comment-header">
                            <div className="comment-author">
                              <strong>{comment.author_name}</strong>
                              <div className="comment-rating">
                                {renderStars(comment.rating)}
                              </div>
                            </div>
                            <div className="comment-meta">
                              <span className="comment-date">
                                {new Date(comment.created_at).toLocaleDateString('fr-FR')}
                              </span>
                              {canDeleteComment(comment) && (
                                <button
                                  onClick={() => deleteComment(comment.id)}
                                  className="delete-comment-btn"
                                  title="Supprimer le commentaire"
                                >
                                  🗑️
                                </button>
                              )}
                            </div>
                          </div>
                          <div className="comment-content">
                            {comment.content}
                          </div>
                        </div>
                      ))}
                    </>
                  )}
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
};

export default ProfilMembre;