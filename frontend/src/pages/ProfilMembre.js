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
    if (memberId) {
      fetchMemberProfile();
      fetchMemberComments();
    }
  }, [memberId]);

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

  const submitComment = () => {
    if (newComment.trim()) {
      alert('Fonctionnalité de commentaire en cours de développement !');
      setShowCommentForm(false);
      setNewComment('');
      setNewRating(5);
    }
  };

  const canDeleteComment = () => {
    return true; // Simplified for demo
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
                <p className="profile-bio">{memberProfile.bio}</p>
                
                <div className="profile-stats-bar">
                  <div className="stat-item">
                    <span className="stat-value">Niv. {memberProfile.level}</span>
                    <span className="stat-label">Niveau</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-value">{memberProfile.coins}</span>
                    <span className="stat-label">💰 Coins</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-value">{memberProfile.total_tournaments}</span>
                    <span className="stat-label">🏆 Tournois</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-value">{commentStats.total_comments}</span>
                    <span className="stat-label">💬 Commentaires</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-value">
                      {commentStats.average_rating.toFixed(1)} ⭐
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
                      {memberProfile.favorite_games.map(game => getGameDisplay(game)).join(', ')}
                    </span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Discord :</span>
                    <span className="info-value">{memberProfile.discord_username}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Steam :</span>
                    <span className="info-value">{memberProfile.steam_profile}</span>
                  </div>
                </div>
              </div>

              {/* Tournament Stats */}
              <div className="profile-section">
                <h3>📊 Statistiques Tournois</h3>
                <div className="stats-grid">
                  <div className="stat-box">
                    <div className="stat-number">{memberProfile.tournaments_won}</div>
                    <div className="stat-label">Victoires</div>
                  </div>
                  <div className="stat-box">
                    <div className="stat-number">{memberProfile.total_tournaments}</div>
                    <div className="stat-label">Participations</div>
                  </div>
                  <div className="stat-box">
                    <div className="stat-number">{memberProfile.trophies_1v1}</div>
                    <div className="stat-label">Trophées 1v1</div>
                  </div>
                  <div className="stat-box">
                    <div className="stat-number">{memberProfile.trophies_5v5}</div>
                    <div className="stat-label">Trophées 5v5</div>
                  </div>
                </div>
              </div>

              {/* Comments Section */}
              <div className="profile-section comments-section">
                <div className="comments-header">
                  <h3>💬 Commentaires & Évaluations</h3>
                  {currentUser && currentUser.id !== memberProfile?.user_id && (
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
                  <div className="comments-summary">
                    <p>
                      {commentStats.total_comments} commentaire(s) • 
                      Note moyenne : {commentStats.average_rating.toFixed(1)} ⭐
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
                              onClick={() => alert('Fonction de suppression en développement')}
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