import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './ProfilMembre.css';

const ProfilMembre = () => {
  const { memberId } = useParams();
  const { API_BASE_URL, user: currentUser } = useAuth();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [memberProfile, setMemberProfile] = useState(null);
  const [comments, setComments] = useState([]);
  const [commentStats, setCommentStats] = useState({ total_comments: 0, average_rating: 0 });
  const [newComment, setNewComment] = useState('');
  const [newRating, setNewRating] = useState(5);
  const [showCommentForm, setShowCommentForm] = useState(false);

  useEffect(() => {
    // Scroll vers le haut quand le composant se monte
    window.scrollTo(0, 0);
    
    if (memberId) {
      fetchMemberProfile();
      fetchMemberComments();
    }
    
    // Debug pour voir l'état de currentUser
    console.log('Current user in ProfilMembre:', currentUser);
    console.log('Member ID:', memberId);
  }, [memberId, currentUser]);

  const fetchMemberProfile = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/profiles/${memberId}`);
      
      if (response.ok) {
        const profileData = await response.json();
        setMemberProfile(profileData);
      } else {
        setError('Profil non trouvé');
      }
    } catch (error) {
      console.error('Erreur lors du chargement du profil:', error);
      setError('Erreur lors du chargement du profil');
    } finally {
      setLoading(false);
    }
  };

  const fetchMemberComments = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/comments/user/${memberId}`);
      
      if (response.ok) {
        const commentsData = await response.json();
        setComments(commentsData.comments || []);
        
        // Fetch comment stats
        const statsResponse = await fetch(`${API_BASE_URL}/comments/stats/user/${memberId}`);
        if (statsResponse.ok) {
          const statsData = await statsResponse.json();
          setCommentStats(statsData);
        }
      }
    } catch (error) {
      console.error('Erreur lors du chargement des commentaires:', error);
    }
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

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, i) => (
      <span key={i} className={`star ${i < rating ? 'filled' : 'empty'}`}>
        ⭐
      </span>
    ));
  };

  const submitComment = async () => {
    if (newComment.trim() && currentUser) {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          alert('Vous devez être connecté pour laisser un commentaire');
          return;
        }

        const response = await fetch(`${API_BASE_URL}/comments/user`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            target_id: memberId,
            content: newComment,
            rating: newRating
          })
        });

        if (response.ok) {
          alert('Commentaire ajouté avec succès !');
          setShowCommentForm(false);
          setNewComment('');
          setNewRating(5);
          fetchMemberComments(); // Refresh comments
        } else {
          const data = await response.json();
          alert(data.detail || 'Erreur lors de l\'ajout du commentaire');
        }
      } catch (error) {
        console.error('Erreur lors de l\'ajout du commentaire:', error);
        alert('Erreur lors de l\'ajout du commentaire');
      }
    }
  };

  const deleteComment = async (commentId) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch(`${API_BASE_URL}/comments/user/${commentId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        alert('Commentaire supprimé');
        fetchMemberComments(); // Refresh comments
      } else {
        const data = await response.json();
        alert(data.detail || 'Erreur lors de la suppression');
      }
    } catch (error) {
      console.error('Erreur lors de la suppression:', error);
    }
  };

  const canDeleteComment = (comment) => {
    return currentUser && (
      currentUser.role === 'admin' ||
      currentUser.role === 'moderator'
    );
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Chargement du profil...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <h2>Erreur</h2>
        <p>{error}</p>
        <Link to="/communaute" className="btn-primary-pro">
          ← Retour à la communauté
        </Link>
      </div>
    );
  }

  if (!memberProfile) {
    return (
      <div className="error-container">
        <h2>Profil non trouvé</h2>
        <p>Le profil demandé n'existe pas ou n'est plus disponible.</p>
        <Link to="/communaute" className="btn-primary-pro">
          ← Retour à la communauté
        </Link>
      </div>
    );
  }

  return (
    <div className="profil-membre-container">
      {/* Profile Header */}
      <section className="profile-header">
        <div className="profile-header-bg">
          <div className="profile-overlay"></div>
          {/* Bannière équipée */}
          {memberProfile.profile?.equipped_banner && (
            <div className="equipped-banner">
              <img 
                src={memberProfile.profile.equipped_banner.image_url || '/images/default-banner.jpg'} 
                alt="Bannière de profil"
                className="banner-image"
              />
            </div>
          )}
        </div>
          
          <div className="container-pro">
            <div className="profile-info-main">
              <div className="profile-avatar-large">
                {memberProfile.profile?.avatar_url ? (
                  <img 
                    src={memberProfile.profile.avatar_url} 
                    alt={memberProfile.profile.display_name || memberProfile.user.username}
                    className="avatar-image"
                  />
                ) : (
                  (memberProfile.profile?.display_name || memberProfile.user?.username || 'U').charAt(0).toUpperCase()
                )}
              </div>
              
              <div className="profile-details">
                <h1 className="profile-name">
                  {memberProfile.profile?.display_name || memberProfile.user?.username || 'Utilisateur'}
                </h1>
                <p className="profile-bio">
                  {memberProfile.profile?.bio || 'Aucune biographie disponible'}
                </p>
                
                <div className="profile-stats-bar">
                  <div className="stat-item">
                    <span className="stat-value">
                      {memberProfile.statistics?.ranking?.level || 'Novice'}
                    </span>
                    <span className="stat-label">Niveau</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-value">
                      {memberProfile.statistics?.ranking?.total_points || 0}
                    </span>
                    <span className="stat-label">🏆 Points</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-value">
                      {memberProfile.statistics?.tournaments?.total || 0}
                    </span>
                    <span className="stat-label">🎯 Tournois</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-value">{commentStats.total_comments}</span>
                    <span className="stat-label">💬 Commentaires</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-value">
                      {commentStats.average_rating > 0 ? commentStats.average_rating.toFixed(1) : '0.0'} ⭐
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
                <div className="simple-info">
                  <p><strong>Nom d'utilisateur :</strong> {memberProfile.user?.username || 'Non spécifié'}</p>
                  <p><strong>Steam :</strong> {memberProfile.profile?.steam_profile || 'Non spécifié'}</p>
                  <p><strong>Membre depuis :</strong> {new Date(memberProfile.user?.created_at).toLocaleDateString('fr-FR', { year: 'numeric', month: 'long' })}</p>
                </div>
              </div>

              {/* Tournament Stats */}
              <div className="profile-section">
                <h3>📊 Statistiques Tournois</h3>
                <div className="stats-grid">
                  <div className="stat-box">
                    <div className="stat-number">
                      {memberProfile.statistics?.tournaments?.victories || 0}
                    </div>
                    <div className="stat-label">Victoires</div>
                  </div>
                  <div className="stat-box">
                    <div className="stat-number">
                      {memberProfile.statistics?.tournaments?.total || 0}
                    </div>
                    <div className="stat-label">Participations</div>
                  </div>
                  <div className="stat-box">
                    <div className="stat-number">
                      {memberProfile.statistics?.trophies?.['1v1'] || 0}
                    </div>
                    <div className="stat-label">Trophées 1v1</div>
                  </div>
                  <div className="stat-box">
                    <div className="stat-number">
                      {memberProfile.statistics?.trophies?.['5v5'] || 0}
                    </div>
                    <div className="stat-label">Trophées 5v5</div>
                  </div>
                </div>
                
                {memberProfile.statistics?.matches && (
                  <div className="additional-stats">
                    <h4>Statistiques Matches</h4>
                    <div className="match-stats">
                      <span>
                        Matches joués: {memberProfile.statistics.matches.total}
                      </span>
                      <span>
                        Taux de victoire: {memberProfile.statistics.matches.win_rate}%
                      </span>
                    </div>
                  </div>
                )}
              </div>

              {/* Teams Information */}
              {memberProfile.teams && memberProfile.teams.length > 0 && (
                <div className="profile-section">
                  <h3>👥 Équipes</h3>
                  <div className="teams-list">
                    {memberProfile.teams.map(team => (
                      <div key={team.id} className="team-item">
                        <div className="team-info">
                          <span className="team-name">{team.name}</span>
                          <span className="team-game">({getGameDisplay(team.game)})</span>
                          {team.is_captain && <span className="captain-badge">👑 Capitaine</span>}
                        </div>
                        <div className="team-id">ID: {team.id}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Comments Section */}
              <div className="profile-section comments-section">
                <div className="comments-header">
                  <h3>💬 Commentaires & Évaluations</h3>
                  {currentUser && currentUser.id !== memberProfile?.user?.id && (
                    <button 
                      className="btn-primary-pro"
                      onClick={() => setShowCommentForm(!showCommentForm)}
                    >
                      ✏️ Laisser un commentaire
                    </button>
                  )}
                  {!currentUser && (
                    <p className="login-required">Connectez-vous pour laisser un commentaire</p>
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
                  <div className="comments-summary">
                    <p>
                      {commentStats.total_comments} commentaire(s) • 
                      Note moyenne : {commentStats.average_rating > 0 ? commentStats.average_rating.toFixed(1) : '0.0'} ⭐
                    </p>
                  </div>
                  
                  {comments.length === 0 ? (
                    <div className="no-comments">
                      <p>Aucun commentaire pour le moment.</p>
                      {currentUser && currentUser.id !== memberProfile?.user?.id && (
                        <p>Soyez le premier à laisser un commentaire !</p>
                      )}
                    </div>
                  ) : (
                    comments.map(comment => (
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
                                onClick={() => {
                                  if (window.confirm('Êtes-vous sûr de vouloir supprimer ce commentaire ?')) {
                                    deleteComment(comment.id);
                                  }
                                }}
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
                    ))
                  )}
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
  );
};

export default ProfilMembre;