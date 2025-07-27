import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Tournois = () => {
  const [activeTab, setActiveTab] = useState('a-venir');
  const [tournaments, setTournaments] = useState({
    'en-cours': [],
    'a-venir': [],
    'termines': []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { API_BASE_URL, user, token } = useAuth();
  
  // États pour l'inscription améliorée
  const [showRegistrationModal, setShowRegistrationModal] = useState(false);
  const [selectedTournament, setSelectedTournament] = useState(null);
  const [userTeams, setUserTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState('');
  const [registrationLoading, setRegistrationLoading] = useState(false);

  useEffect(() => {
    fetchTournaments();
    if (user) {
      fetchUserTeams();
    }
  }, [user]);

  const fetchUserTeams = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/teams/my-teams`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setUserTeams(data.teams || []);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des équipes:', error);
    }
  };

  const fetchTournaments = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/tournaments/`);
      
      if (response.ok) {
        const data = await response.json();
        
        // Organiser les tournois par statut
        const organized = {
          'en-cours': data.filter(t => t.status === 'in_progress'),
          'a-venir': data.filter(t => t.status === 'open' || t.status === 'draft'),
          'termines': data.filter(t => t.status === 'completed')
        };
        
        setTournaments(organized);
      } else {
        setError('Erreur lors du chargement des tournois');
      }
    } catch (error) {
      console.error('Erreur fetch tournaments:', error);
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  const registerForTournament = async (tournamentId) => {
    if (!user) {
      alert('Vous devez être connecté pour vous inscrire à un tournoi');
      return;
    }

    // Trouver le tournoi sélectionné
    const tournament = [...tournaments['a-venir'], ...tournaments['en-cours'], ...tournaments['termines']]
      .find(t => t.id === tournamentId);
    
    if (!tournament) {
      alert('Tournoi non trouvé');
      return;
    }

    setSelectedTournament(tournament);
    setShowRegistrationModal(true);
  };

  const handleRegistrationSubmit = async () => {
    if (!selectedTournament) return;

    setRegistrationLoading(true);
    try {
      const registrationData = {
        tournament_id: selectedTournament.id
      };

      if (selectedTeam) {
        registrationData.team_id = selectedTeam;
      }

      const response = await fetch(`${API_BASE_URL}/tournaments/${selectedTournament.id}/register`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(registrationData)
      });

      if (response.ok) {
        alert('Inscription réussie !');
        setShowRegistrationModal(false);
        setSelectedTournament(null);
        setSelectedTeam('');
        fetchTournaments(); // Actualiser la liste
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'Erreur lors de l\'inscription');
      }
    } catch (error) {
      alert('Erreur de connexion au serveur');
    } finally {
      setRegistrationLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  const formatDateTime = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusBadge = (status) => {
    switch(status) {
      case 'draft':
        return <span className="status-badge draft">📝 Brouillon</span>;
      case 'open':
        return <span className="status-badge open">🟢 Inscriptions ouvertes</span>;
      case 'in_progress':
        return <span className="status-badge progress">⏳ En cours</span>;
      case 'completed':
        return <span className="status-badge completed">✅ Terminé</span>;
      default:
        return <span className="status-badge">❓ Inconnu</span>;
    }
  };

  const getTournamentTypeName = (type) => {
    switch(type) {
      case 'elimination':
        return 'Élimination Directe';
      case 'bracket':
        return 'Bracket';
      case 'round_robin':
        return 'Round Robin';
      default:
        return type;
    }
  };

  const getGameName = (gameId) => {
    // Support uniquement CS2 pour Oupafamilly
    return gameId === 'cs2' ? 'Counter-Strike 2' : 'CS2';
  };

  const renderTournamentCard = (tournament) => (
    <div key={tournament.id} className="tournament-card-pro">
      <div className="tournament-header-pro">
        <div className="tournament-title-pro">
          <h3>{tournament.title}</h3>
          <div className="tournament-badges">
            {getStatusBadge(tournament.status)}
            <span className="game-badge">{getGameName(tournament.game)}</span>
          </div>
        </div>
        <div className="tournament-prize">
          {tournament.prize_pool > 0 ? `${tournament.prize_pool}€` : 'Gratuit'}
        </div>
      </div>

      <div className="tournament-details-pro">
        <div className="detail-row">
          <span className="detail-label">Type:</span>
          <span className="detail-value">{getTournamentTypeName(tournament.tournament_type)}</span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Participants:</span>
          <span className="detail-value">{tournament.participants.length}/{tournament.max_participants}</span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Début:</span>
          <span className="detail-value">{formatDateTime(tournament.tournament_start)}</span>
        </div>
        <div className="detail-row">
          <span className="detail-label">Inscriptions:</span>
          <span className="detail-value">
            Jusqu'au {formatDate(tournament.registration_end)}
          </span>
        </div>
      </div>

      <div className="tournament-description">
        <p>{tournament.description}</p>
      </div>

      <div className="tournament-actions-pro">
        {tournament.status === 'open' && user && (
          <button 
            className="btn-register-pro"
            onClick={() => registerForTournament(tournament.id)}
            disabled={tournament.participants.length >= tournament.max_participants}
          >
            {tournament.participants.includes(user.id) ? '✅ Inscrit' : '🚀 Rejoindre'}
          </button>
        )}
        <Link to={`/tournois/${tournament.id}`} className="btn-details-pro">
          📋 Détails
        </Link>
      </div>
    </div>
  );

  return (
    <div className="tournaments-container-pro">
      <div className="tournaments-header-pro">
        <h1>🏆 Tournois CS2</h1>
        <p>Rejoignez l'élite compétitive d'Oupafamilly</p>
        {user && user.role === 'admin' && (
          <Link to="/admin/tournaments" className="admin-link-pro">
            ⚙️ Gérer les tournois
          </Link>
        )}
      </div>

      {error && (
        <div className="error-banner">
          ❌ {error}
          <button onClick={fetchTournaments}>🔄 Réessayer</button>
        </div>
      )}

      <div className="tournaments-tabs-pro">
        <button 
          className={`tab-pro ${activeTab === 'a-venir' ? 'active' : ''}`}
          onClick={() => setActiveTab('a-venir')}
        >
          🚀 À venir ({tournaments['a-venir'].length})
        </button>
        <button 
          className={`tab-pro ${activeTab === 'en-cours' ? 'active' : ''}`}
          onClick={() => setActiveTab('en-cours')}
        >
          ⏳ En cours ({tournaments['en-cours'].length})
        </button>
        <button 
          className={`tab-pro ${activeTab === 'termines' ? 'active' : ''}`}
          onClick={() => setActiveTab('termines')}
        >
          ✅ Terminés ({tournaments['termines'].length})
        </button>
      </div>

      <div className="tournaments-grid-pro">
        {loading ? (
          <div className="loading-tournaments">
            <div className="spinner"></div>
            <p>Chargement des tournois...</p>
          </div>
        ) : tournaments[activeTab].length === 0 ? (
          <div className="empty-tournaments">
            <div className="empty-icon">🏆</div>
            <h3>Aucun tournoi {activeTab.replace('-', ' ')}</h3>
            <p>
              {activeTab === 'a-venir' && 'Les prochains tournois apparaîtront ici bientôt !'}
              {activeTab === 'en-cours' && 'Aucun tournoi en cours actuellement.'}
              {activeTab === 'termines' && 'L\'historique des tournois apparaîtra ici.'}
            </p>
            {user && user.role === 'admin' && (
              <Link to="/admin/tournaments" className="btn-create-tournament">
                ➕ Créer un tournoi
              </Link>
            )}
          </div>
        ) : (
          tournaments[activeTab].map(tournament => renderTournamentCard(tournament))
        )}
      </div>

      {/* Section information participation */}
      <div className="participation-info-section">
        <div className="participation-header">
          <h2>🎮 Comment participer aux tournois ?</h2>
          <div className="discord-logo">💬</div>
        </div>
        <div className="participation-content">
          <p>
            Tous les tournois d'Oupafamilly sont organisés et coordonnés sur notre serveur Discord officiel. 
            C'est là que vous trouverez toutes les informations importantes, les annonces de matches, 
            les règlements détaillés et où vous pourrez échanger avec les autres participants.
          </p>
          <div className="participation-features">
            <div className="feature-item">
              <span className="feature-icon">📢</span>
              <div className="feature-text">
                <strong>Annonces officielles</strong>
                <p>Notifications en temps réel des matches et événements</p>
              </div>
            </div>
            <div className="feature-item">
              <span className="feature-icon">🗣️</span>
              <div className="feature-text">
                <strong>Communication d'équipe</strong>
                <p>Salons vocaux dédiés pour coordonner vos stratégies</p>
              </div>
            </div>
            <div className="feature-item">
              <span className="feature-icon">🎯</span>
              <div className="feature-text">
                <strong>Support direct</strong>
                <p>Assistance immédiate de nos administrateurs</p>
              </div>
            </div>
          </div>
          <div className="discord-cta">
            <a 
              href="https://discord.gg/PY3WtKJu" 
              target="_blank" 
              rel="noopener noreferrer"
              className="discord-btn"
            >
              <div className="discord-btn-content">
                <span className="discord-icon">🎮</span>
                <div>
                  <strong>Rejoindre le Discord Oupafamilly</strong>
                  <small>Cliquez ici pour accéder à notre communauté</small>
                </div>
              </div>
            </a>
          </div>
        </div>
      </div>

      {/* Modal d'inscription amélioré */}
      {showRegistrationModal && selectedTournament && (
        <div className="modal-overlay" onClick={() => setShowRegistrationModal(false)}>
          <div className="registration-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>🚀 Inscription au Tournoi</h3>
              <button 
                className="modal-close"
                onClick={() => setShowRegistrationModal(false)}
              >
                ✕
              </button>
            </div>
            
            <div className="modal-content">
              <div className="tournament-info">
                <h4>{selectedTournament.title}</h4>
                <div className="tournament-details">
                  <div className="detail-item">
                    <span className="detail-label">🎮 Jeu:</span>
                    <span>{getGameName(selectedTournament.game)}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">🏆 Type:</span>
                    <span>{getTournamentTypeName(selectedTournament.tournament_type)}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">👥 Participants:</span>
                    <span>{selectedTournament.participants.length}/{selectedTournament.max_participants}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">💰 Prix:</span>
                    <span>{selectedTournament.prize_pool > 0 ? `${selectedTournament.prize_pool}€` : 'Gratuit'}</span>
                  </div>
                </div>
              </div>
              
              <div className="team-selection">
                <h4>⚡ Sélection d'équipe</h4>
                <p>Choisissez avec quelle équipe vous souhaitez participer au tournoi:</p>
                
                <div className="team-options">
                  <div className="team-option">
                    <input
                      type="radio"
                      id="solo"
                      name="team"
                      value=""
                      checked={selectedTeam === ''}
                      onChange={(e) => setSelectedTeam(e.target.value)}
                    />
                    <label htmlFor="solo" className="team-option-label">
                      <div className="team-icon">👤</div>
                      <div className="team-info">
                        <strong>Participation Solo</strong>
                        <small>Je participe individuellement</small>
                      </div>
                    </label>
                  </div>
                  
                  {userTeams.length > 0 && userTeams.map(team => (
                    <div key={team.id} className="team-option">
                      <input
                        type="radio"
                        id={`team-${team.id}`}
                        name="team"
                        value={team.id}
                        checked={selectedTeam === team.id}
                        onChange={(e) => setSelectedTeam(e.target.value)}
                      />
                      <label htmlFor={`team-${team.id}`} className="team-option-label">
                        <div className="team-icon">🛡️</div>
                        <div className="team-info">
                          <strong>{team.name}</strong>
                          <small>{team.members?.length || 0} membres - Capitaine: {team.captain_name}</small>
                        </div>
                      </label>
                    </div>
                  ))}
                </div>
                
                {userTeams.length === 0 && (
                  <div className="no-teams-message">
                    <div className="no-teams-icon">🤝</div>
                    <p>Vous n'avez pas encore d'équipe. Vous pouvez participer en solo ou créer une équipe dans la section Communauté.</p>
                    <Link to="/communaute" className="create-team-link">
                      ➕ Créer une équipe
                    </Link>
                  </div>
                )}
              </div>
            </div>
            
            <div className="modal-actions">
              <button 
                className="btn-cancel"
                onClick={() => setShowRegistrationModal(false)}
                disabled={registrationLoading}
              >
                Annuler
              </button>
              <button 
                className="btn-confirm"
                onClick={handleRegistrationSubmit}
                disabled={registrationLoading}
              >
                {registrationLoading ? '⏳ Inscription...' : '🚀 Confirmer l\'inscription'}
              </button>
            </div>
          </div>
        </div>
      )}

      <style jsx>{`
        .tournaments-container-pro {
          max-width: 1200px;
          margin: 40px auto;
          padding: 0 20px;
        }

        .tournaments-header-pro {
          text-align: center;
          margin-bottom: 40px;
          position: relative;
        }

        .tournaments-header-pro h1 {
          color: #1e3a8a;
          font-size: 48px;
          font-weight: 800;
          margin: 0 0 15px 0;
          text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }

        .tournaments-header-pro p {
          color: #64748b;
          font-size: 18px;
          margin: 0;
        }

        .admin-link-pro {
          position: absolute;
          top: 0;
          right: 0;
          background: linear-gradient(45deg, #3b82f6, #1d4ed8);
          color: white;
          padding: 10px 20px;
          border-radius: 10px;
          text-decoration: none;
          font-weight: 600;
          transition: all 0.3s;
        }

        .admin-link-pro:hover {
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(59, 130, 246, 0.3);
        }

        .error-banner {
          background: #fee2e2;
          color: #dc2626;
          padding: 15px;
          border-radius: 10px;
          margin-bottom: 30px;
          text-align: center;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .error-banner button {
          background: #dc2626;
          color: white;
          border: none;
          padding: 8px 16px;
          border-radius: 6px;
          cursor: pointer;
        }

        .tournaments-tabs-pro {
          display: flex;
          gap: 10px;
          margin-bottom: 30px;
          justify-content: center;
        }

        .tab-pro {
          background: #f1f5f9;
          color: #1a1a1a;
          border: 2px solid #e2e8f0;
          padding: 15px 25px;
          border-radius: 12px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
          font-size: 16px;
        }

        .tab-pro.active {
          background: linear-gradient(45deg, #3b82f6, #1d4ed8);
          color: white;
          border-color: #3b82f6;
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(59, 130, 246, 0.3);
        }

        .tab-pro:hover:not(.active) {
          background: #e2e8f0;
          transform: translateY(-1px);
        }

        .tournaments-grid-pro {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
          gap: 25px;
        }

        .tournament-card-pro {
          background: white;
          border-radius: 20px;
          padding: 25px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
          border: 2px solid #e5e7eb;
          transition: all 0.3s;
          position: relative;
          overflow: hidden;
        }

        .tournament-card-pro:hover {
          transform: translateY(-5px);
          box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
          border-color: #3b82f6;
        }

        .tournament-header-pro {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 20px;
        }

        .tournament-title-pro h3 {
          color: #1e3a8a;
          font-size: 22px;
          font-weight: 700;
          margin: 0 0 10px 0;
        }

        .tournament-badges {
          display: flex;
          gap: 8px;
          flex-wrap: wrap;
        }

        .status-badge {
          padding: 4px 10px;
          border-radius: 15px;
          font-size: 12px;
          font-weight: 600;
        }

        .status-badge.draft {
          background: #fef3c7;
          color: #92400e;
        }

        .status-badge.open {
          background: #dcfce7;
          color: #166534;
        }

        .status-badge.progress {
          background: #dbeafe;
          color: #1e40af;
        }

        .status-badge.completed {
          background: #f3e8ff;
          color: #7c3aed;
        }

        .game-badge {
          background: #3b82f6;
          color: white;
          padding: 4px 10px;
          border-radius: 15px;
          font-size: 12px;
          font-weight: 600;
        }

        .tournament-prize {
          background: linear-gradient(45deg, #f59e0b, #d97706);
          color: white;
          padding: 8px 15px;
          border-radius: 20px;
          font-weight: 700;
          font-size: 16px;
        }

        .tournament-details-pro {
          margin-bottom: 20px;
        }

        .detail-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 8px;
        }

        .detail-label {
          color: #1a1a1a;
          font-weight: 600;
        }

        .detail-value {
          color: #333333;
          font-weight: 500;
        }

        .tournament-description {
          background: #f8fafc;
          padding: 15px;
          border-radius: 10px;
          margin-bottom: 20px;
          border-left: 4px solid #3b82f6;
        }

        .tournament-description p {
          color: #1a1a1a;
          margin: 0;
          line-height: 1.5;
        }

        .tournament-actions-pro {
          display: flex;
          gap: 10px;
        }

        .btn-register-pro {
          flex: 1;
          background: linear-gradient(45deg, #10b981, #059669);
          color: white;
          border: none;
          padding: 12px 20px;
          border-radius: 10px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
        }

        .btn-register-pro:hover:not(:disabled) {
          background: linear-gradient(45deg, #059669, #047857);
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(16, 185, 129, 0.3);
        }

        .btn-register-pro:disabled {
          opacity: 0.6;
          cursor: not-allowed;
          transform: none;
        }

        .btn-details-pro {
          background: #f1f5f9;
          color: #1e3a8a;
          border: 2px solid #e2e8f0;
          padding: 12px 20px;
          border-radius: 10px;
          font-weight: 600;
          text-decoration: none;
          transition: all 0.3s;
          text-align: center;
        }

        .btn-details-pro:hover {
          background: #e2e8f0;
          transform: translateY(-2px);
        }

        .loading-tournaments {
          grid-column: 1 / -1;
          text-align: center;
          padding: 60px 20px;
        }

        .spinner {
          width: 50px;
          height: 50px;
          border: 4px solid #e5e7eb;
          border-top: 4px solid #3b82f6;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin: 0 auto 20px;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        .loading-tournaments p {
          color: #333333;
          font-size: 18px;
          font-weight: 600;
        }

        .empty-tournaments {
          grid-column: 1 / -1;
          text-align: center;
          padding: 60px 20px;
        }

        .empty-icon {
          font-size: 80px;
          margin-bottom: 20px;
        }

        .empty-tournaments h3 {
          color: #1e3a8a;
          font-size: 24px;
          margin-bottom: 10px;
        }

        .empty-tournaments p {
          color: #333333;
          font-size: 16px;
          margin-bottom: 30px;
        }

        .btn-create-tournament {
          background: linear-gradient(45deg, #3b82f6, #1d4ed8);
          color: white;
          padding: 15px 30px;
          border-radius: 15px;
          text-decoration: none;
          font-weight: 600;
          transition: all 0.3s;
          display: inline-block;
        }

        .btn-create-tournament:hover {
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(59, 130, 246, 0.3);
        }

        @media (max-width: 768px) {
          .tournaments-container-pro {
            padding: 0 15px;
          }

          .tournaments-header-pro h1 {
            font-size: 32px;
          }

          .admin-link-pro {
            position: static;
            display: block;
            margin-top: 15px;
          }

          .tournaments-tabs-pro {
            flex-direction: column;
          }

          .tournament-header-pro {
            flex-direction: column;
            gap: 15px;
          }

          .tournament-actions-pro {
            flex-direction: column;
          }

          .tournaments-grid-pro {
            grid-template-columns: 1fr;
          }

          .participation-features {
            flex-direction: column;
          }

          .feature-item {
            text-align: center;
          }

          .discord-btn-content {
            text-align: center;
          }
        }

        /* Styles pour la section participation */
        .participation-info-section {
          background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
          color: white;
          border-radius: 20px;
          padding: 40px;
          margin-top: 50px;
          text-align: center;
        }

        .participation-header {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 15px;
          margin-bottom: 30px;
        }

        .participation-header h2 {
          margin: 0;
          font-size: 28px;
          font-weight: 700;
        }

        .discord-logo {
          font-size: 32px;
          background: rgba(255, 255, 255, 0.1);
          padding: 10px;
          border-radius: 50%;
        }

        .participation-content p {
          font-size: 18px;
          line-height: 1.6;
          margin-bottom: 30px;
          opacity: 0.9;
          max-width: 800px;
          margin-left: auto;
          margin-right: auto;
        }

        .participation-features {
          display: flex;
          gap: 30px;
          margin-bottom: 40px;
          justify-content: center;
          flex-wrap: wrap;
        }

        .feature-item {
          display: flex;
          align-items: flex-start;
          gap: 15px;
          max-width: 250px;
        }

        .feature-icon {
          font-size: 24px;
          background: rgba(255, 255, 255, 0.1);
          padding: 10px;
          border-radius: 10px;
          flex-shrink: 0;
        }

        .feature-text strong {
          display: block;
          font-size: 16px;
          margin-bottom: 5px;
        }

        .feature-text p {
          margin: 0;
          font-size: 14px;
          opacity: 0.8;
          line-height: 1.4;
        }

        .discord-cta {
          display: flex;
          justify-content: center;
        }

        .discord-btn {
          background: linear-gradient(45deg, #5865f2, #404eed);
          color: white;
          text-decoration: none;
          padding: 20px 30px;
          border-radius: 15px;
          transition: all 0.3s;
          box-shadow: 0 5px 20px rgba(88, 101, 242, 0.3);
        }

        .discord-btn:hover {
          transform: translateY(-3px);
          box-shadow: 0 8px 25px rgba(88, 101, 242, 0.4);
          background: linear-gradient(45deg, #404eed, #3c44e9);
        }

        .discord-btn-content {
          display: flex;
          align-items: center;
          gap: 15px;
        }

        .discord-icon {
          font-size: 24px;
        }

        .discord-btn-content strong {
          display: block;
          font-size: 18px;
          margin-bottom: 2px;
        }

        .discord-btn-content small {
          font-size: 14px;
          opacity: 0.9;
        }

        /* Styles pour le modal d'inscription */
        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.7);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 1000;
          padding: 20px;
        }

        .registration-modal {
          background: white;
          border-radius: 20px;
          max-width: 600px;
          width: 100%;
          max-height: 90vh;
          overflow-y: auto;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }

        .modal-header {
          padding: 30px 30px 20px;
          border-bottom: 1px solid #e5e7eb;
          display: flex;
          align-items: center;
          justify-content: space-between;
        }

        .modal-header h3 {
          margin: 0;
          color: #1f2937;
          font-size: 24px;
          font-weight: 700;
        }

        .modal-close {
          background: none;
          border: none;
          font-size: 24px;
          color: #6b7280;
          cursor: pointer;
          padding: 5px;
          border-radius: 50%;
          transition: all 0.2s;
        }

        .modal-close:hover {
          background: #f3f4f6;
          color: #374151;
        }

        .modal-content {
          padding: 30px;
        }

        .tournament-info {
          margin-bottom: 30px;
          padding: 20px;
          background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
          border-radius: 15px;
        }

        .tournament-info h4 {
          margin: 0 0 15px 0;
          color: #1e40af;
          font-size: 20px;
          font-weight: 600;
        }

        .tournament-details {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 10px;
        }

        .detail-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 8px 0;
        }

        .detail-label {
          font-weight: 500;
          color: #6b7280;
        }

        .team-selection h4 {
          margin: 0 0 10px 0;
          color: #1f2937;
          font-size: 18px;
          font-weight: 600;
        }

        .team-selection p {
          margin: 0 0 20px 0;
          color: #6b7280;
          line-height: 1.5;
        }

        .team-options {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .team-option {
          position: relative;
        }

        .team-option input[type="radio"] {
          position: absolute;
          opacity: 0;
          width: 0;
          height: 0;
        }

        .team-option-label {
          display: flex;
          align-items: center;
          gap: 15px;
          padding: 15px;
          border: 2px solid #e5e7eb;
          border-radius: 12px;
          cursor: pointer;
          transition: all 0.2s;
          background: white;
        }

        .team-option input[type="radio"]:checked + .team-option-label {
          border-color: #3b82f6;
          background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        }

        .team-option-label:hover {
          border-color: #60a5fa;
          background: #f8fafc;
        }

        .team-icon {
          font-size: 24px;
          width: 40px;
          height: 40px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: #f1f5f9;
          border-radius: 50%;
          flex-shrink: 0;
        }

        .team-option input[type="radio"]:checked + .team-option-label .team-icon {
          background: #3b82f6;
          color: white;
        }

        .team-info strong {
          display: block;
          color: #1f2937;
          font-size: 16px;
          margin-bottom: 2px;
        }

        .team-info small {
          color: #6b7280;
          font-size: 14px;
        }

        .no-teams-message {
          text-align: center;
          padding: 30px 20px;
          background: #fef3c7;
          border: 1px solid #f59e0b;
          border-radius: 12px;
          margin-top: 15px;
        }

        .no-teams-icon {
          font-size: 48px;
          margin-bottom: 15px;
        }

        .no-teams-message p {
          margin: 0 0 15px 0;
          color: #92400e;
          line-height: 1.5;
        }

        .create-team-link {
          display: inline-flex;
          align-items: center;
          gap: 8px;
          background: #f59e0b;
          color: white;
          text-decoration: none;
          padding: 10px 20px;
          border-radius: 8px;
          font-weight: 500;
          transition: all 0.2s;
        }

        .create-team-link:hover {
          background: #d97706;
          transform: translateY(-1px);
        }

        .modal-actions {
          padding: 20px 30px 30px;
          border-top: 1px solid #e5e7eb;
          display: flex;
          gap: 15px;
          justify-content: flex-end;
        }

        .btn-cancel {
          background: #f8fafc;
          color: #6b7280;
          border: 1px solid #d1d5db;
          padding: 12px 24px;
          border-radius: 8px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
        }

        .btn-cancel:hover {
          background: #f1f5f9;
          border-color: #9ca3af;
        }

        .btn-cancel:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .btn-confirm {
          background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
          color: white;
          border: none;
          padding: 12px 24px;
          border-radius: 8px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
          box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }

        .btn-confirm:hover {
          background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
          transform: translateY(-1px);
          box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
        }

        .btn-confirm:disabled {
          opacity: 0.6;
          cursor: not-allowed;
          transform: none;
        }

        @media (max-width: 768px) {
          .modal-overlay {
            padding: 10px;
          }
          
          .registration-modal {
            max-height: 95vh;
          }
          
          .modal-header, .modal-content, .modal-actions {
            padding: 20px;
          }
          
          .tournament-details {
            grid-template-columns: 1fr;
          }
          
          .modal-actions {
            flex-direction: column-reverse;
          }
          
          .btn-cancel, .btn-confirm {
            width: 100%;
          }
        }
      `}</style>
    </div>
  );
};

export default Tournois;