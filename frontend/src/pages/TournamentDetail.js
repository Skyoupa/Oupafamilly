import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import TeamManagementModal from '../components/TeamManagementModal';

const TournamentDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [tournament, setTournament] = useState(null);
  const [participantsInfo, setParticipantsInfo] = useState([]);
  const [userTeamsForTournament, setUserTeamsForTournament] = useState(null);
  const [showRegistrationModal, setShowRegistrationModal] = useState(false);
  const [showTeamManagementModal, setShowTeamManagementModal] = useState(false);
  const [selectedTeamForManagement, setSelectedTeamForManagement] = useState(null);
  const [selectedTeamForRegistration, setSelectedTeamForRegistration] = useState('');
  const [newTeamName, setNewTeamName] = useState('');
  const [registrationType, setRegistrationType] = useState('existing');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [registrationLoading, setRegistrationLoading] = useState(false);
  const [registrationError, setRegistrationError] = useState('');
  const { API_BASE_URL, user, token } = useAuth();

  useEffect(() => {
    fetchTournamentDetails();
    fetchParticipantsInfo();
    if (user) {
      fetchUserTeamsForTournament();
    }
  }, [id, user]);

  const fetchTournamentDetails = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/tournaments/${id}`);
      
      if (response.ok) {
        const data = await response.json();
        setTournament(data);
      } else if (response.status === 404) {
        setError('Tournoi non trouvé');
        setTimeout(() => navigate('/tournois'), 3000);
      } else {
        setError('Erreur lors du chargement du tournoi');
      }
    } catch (error) {
      console.error('Erreur fetch tournament:', error);
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  const fetchParticipantsInfo = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/tournaments/${id}/participants-info`);
      if (response.ok) {
        const data = await response.json();
        setParticipantsInfo(data.participants || []);
      }
    } catch (error) {
      console.error('Error fetching participants info:', error);
    }
  };

  const fetchUserTeamsForTournament = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/tournaments/${id}/user-teams`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setUserTeamsForTournament(data);
        // Set default team selection if only one team available
        if (data.eligible_teams && data.eligible_teams.length === 1) {
          setSelectedTeamForRegistration(data.eligible_teams[0].id);
        }
      }
    } catch (error) {
      console.error('Erreur fetch user teams for tournament:', error);
    }
  };

  const handleOpenRegistrationModal = () => {
    setShowRegistrationModal(true);
    setRegistrationError('');
    if (userTeamsForTournament?.eligible_teams?.length === 1) {
      setSelectedTeamForRegistration(userTeamsForTournament.eligible_teams[0].id);
    }
  };

  const handleCloseRegistrationModal = () => {
    setShowRegistrationModal(false);
    setSelectedTeamForRegistration('');
    setNewTeamName('');
    setRegistrationType('existing');
    setRegistrationError('');
  };

  const handleRegistration = async () => {
    if (!user) {
      alert('Vous devez être connecté pour vous inscrire');
      return;
    }

    // Check if tournament requires team and user has no eligible teams
    if (userTeamsForTournament?.requires_team && (!userTeamsForTournament.eligible_teams || userTeamsForTournament.eligible_teams.length === 0)) {
      setRegistrationError(`Ce tournoi ${userTeamsForTournament.tournament_name.includes('2v2') ? '2v2' : '5v5'} nécessite une équipe. Vous devez d'abord créer ou rejoindre une équipe pour le jeu ${userTeamsForTournament.tournament_game}.`);
      return;
    }

    // For team tournaments, ensure a team is selected
    if (userTeamsForTournament?.requires_team && !selectedTeamForRegistration && registrationType === 'existing') {
      setRegistrationError('Veuillez sélectionner une équipe pour ce tournoi.');
      return;
    }

    setRegistrationLoading(true);
    setRegistrationError('');

    try {
      let teamIdToUse = null;

      if (registrationType === 'new' && newTeamName.trim()) {
        // Create new team first
        const teamResponse = await fetch(`${API_BASE_URL}/teams/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: newTeamName.trim(),
            game: tournament.game,
            max_members: 6
          })
        });

        if (teamResponse.ok) {
          const teamData = await teamResponse.json();
          teamIdToUse = teamData.id;
        } else {
          const errorData = await teamResponse.json();
          setRegistrationError(errorData.detail || 'Erreur lors de la création de l\'équipe');
          return;
        }
      } else if (registrationType === 'existing' && selectedTeamForRegistration) {
        teamIdToUse = selectedTeamForRegistration;
      }

      // Register for tournament
      const registrationPayload = {};
      if (teamIdToUse) {
        registrationPayload.team_id = teamIdToUse;
      }

      const response = await fetch(`${API_BASE_URL}/tournaments/${id}/register`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(registrationPayload)
      });

      if (response.ok) {
        const data = await response.json();
        alert(data.message || 'Inscription réussie !');
        handleCloseRegistrationModal();
        fetchTournamentDetails(); // Refresh tournament data
        fetchParticipantsInfo(); // Refresh participants
      } else {
        const errorData = await response.json();
        setRegistrationError(errorData.detail || 'Erreur lors de l\'inscription');
      }
    } catch (error) {
      console.error('Erreur registration:', error);
      setRegistrationError('Erreur de connexion lors de l\'inscription');
    } finally {
      setRegistrationLoading(false);
    }
  };

  const handleTeamManagement = (team) => {
    setSelectedTeamForManagement(team);
    setShowTeamManagementModal(true);
  };

  const handleTeamUpdated = () => {
    fetchUserTeamsForTournament(); // Refresh teams data
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatGameName = (game) => {
    const gameNames = {
      'cs2': 'Counter-Strike 2',
      'lol': 'League of Legends',
      'wow': 'World of Warcraft',
      'sc2': 'StarCraft II',
      'minecraft': 'Minecraft'
    };
    return gameNames[game] || game;
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      'open': { text: 'Inscriptions ouvertes', class: 'status-open' },
      'in_progress': { text: 'En cours', class: 'status-progress' },
      'completed': { text: 'Terminé', class: 'status-completed' },
      'cancelled': { text: 'Annulé', class: 'status-cancelled' }
    };
    
    const config = statusConfig[status] || { text: status, class: 'status-default' };
    return (
      <span className={`status-badge ${config.class}`}>
        {config.text}
      </span>
    );
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Chargement du tournoi...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-container">
        <div className="error-container">
          <h2>Erreur</h2>
          <p>{error}</p>
          <Link to="/tournois" className="btn-primary">
            Retour aux tournois
          </Link>
        </div>
      </div>
    );
  }

  if (!tournament) {
    return (
      <div className="page-container">
        <div className="error-container">
          <h2>Tournoi non trouvé</h2>
          <Link to="/tournois" className="btn-primary">
            Retour aux tournois
          </Link>
        </div>
      </div>
    );
  }

  const userIsRegistered = user && tournament.participants.includes(user.id);
  const isRegistrationOpen = tournament.status === 'open' && new Date() < new Date(tournament.registration_end);

  return (
    <div className="page-container">
      {/* Header */}
      <div className="tournament-header">
        <div className="header-content">
          <div className="tournament-info">
            <h1 className="tournament-title">{tournament.title}</h1>
            <div className="tournament-meta">
              <span className="game-badge">
                🎮 {formatGameName(tournament.game)}
              </span>
              {getStatusBadge(tournament.status)}
              <span className="participants-count">
                👥 {tournament.participants.length}/{tournament.max_participants}
              </span>
            </div>
            <p className="tournament-description">{tournament.description}</p>
          </div>
          
          <div className="tournament-actions">
            {user && !userIsRegistered && isRegistrationOpen && (
              <button 
                className="btn-primary btn-register"
                onClick={handleOpenRegistrationModal}
              >
                🎯 S'inscrire
              </button>
            )}
            {userIsRegistered && (
              <div className="registered-badge">
                ✅ Inscrit
              </div>
            )}
            {tournament.status === 'in_progress' && (
              <Link 
                to={`/tournois/${id}/bracket`} 
                className="btn-secondary"
              >
                🏆 Voir le bracket
              </Link>
            )}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="tournament-content">
        <div className="content-grid">
          {/* Left Column - Details */}
          <div className="tournament-details">
            <div className="details-card">
              <h3>📋 Informations</h3>
              <div className="detail-item">
                <strong>Type :</strong> {tournament.tournament_type}
              </div>
              <div className="detail-item">
                <strong>Participants max :</strong> {tournament.max_participants}
              </div>
              <div className="detail-item">
                <strong>Prix :</strong> {tournament.entry_fee === 0 ? 'Gratuit' : `${tournament.entry_fee}€`}
              </div>
              <div className="detail-item">
                <strong>Organisateur :</strong> {tournament.organizer_name}
              </div>
            </div>

            <div className="details-card">
              <h3>📅 Planning</h3>
              <div className="detail-item">
                <strong>Inscriptions :</strong>
                <br />
                Du {formatDate(tournament.registration_start)}
                <br />
                Au {formatDate(tournament.registration_end)}
              </div>
              <div className="detail-item">
                <strong>Début du tournoi :</strong>
                <br />
                {formatDate(tournament.tournament_start)}
              </div>
            </div>

            {tournament.rules && (
              <div className="details-card">
                <h3>📜 Règles</h3>
                <div 
                  className="rules-content"
                  dangerouslySetInnerHTML={{ __html: tournament.rules.replace(/\n/g, '<br>') }}
                />
              </div>
            )}
          </div>

          {/* Right Column - Participants */}
          <div className="tournament-sidebar">
            <div className="participants-card">
              <h3>👥 Participants ({participantsInfo.length}/{tournament.max_participants})</h3>
              
              {participantsInfo.length === 0 ? (
                <p className="no-participants">Aucun participant pour le moment</p>
              ) : (
                <div className="participants-list">
                  {participantsInfo.map((participant, index) => (
                    <div key={participant.id} className="participant-item">
                      <div className="participant-info">
                        <span className="participant-rank">#{index + 1}</span>
                        <span className="participant-name">
                          {participant.is_team ? (
                            <>
                              <span className="team-icon">👥</span>
                              {participant.name}
                              <span className="member-count">({participant.member_count})</span>
                            </>
                          ) : (
                            <>
                              <span className="user-icon">👤</span>
                              {participant.name}
                            </>
                          )}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* User's Teams for Management (if any) */}
            {user && userTeamsForTournament?.eligible_teams && userTeamsForTournament.eligible_teams.length > 0 && (
              <div className="user-teams-card">
                <h3>⚡ Mes équipes pour ce tournoi</h3>
                <div className="teams-list">
                  {userTeamsForTournament.eligible_teams.map(team => (
                    <div key={team.id} className="team-item">
                      <div className="team-info">
                        <span className="team-name">{team.name}</span>
                        {team.is_captain && <span className="captain-badge">👑 Capitaine</span>}
                        <span className="team-members">({team.member_count}/{team.max_members})</span>
                      </div>
                      {team.is_captain && (
                        <button 
                          className="btn-manage-team"
                          onClick={() => handleTeamManagement(team)}
                        >
                          ⚙️ Gérer
                        </button>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Registration Modal */}
      {showRegistrationModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h2>🎯 Inscription au tournoi</h2>
              <button className="modal-close" onClick={handleCloseRegistrationModal}>×</button>
            </div>
            
            <div className="modal-body">
              {registrationError && (
                <div className="error-message">{registrationError}</div>
              )}

              <div className="tournament-info-summary">
                <h3>{tournament.title}</h3>
                <p><strong>Jeu :</strong> {formatGameName(tournament.game)}</p>
                {userTeamsForTournament?.requires_team ? (
                  <p className="team-required">⚠️ Ce tournoi nécessite une équipe</p>
                ) : (
                  <p className="individual-allowed">✅ Inscription individuelle autorisée</p>
                )}
              </div>

              {/* Team Selection for Team Tournaments */}
              {userTeamsForTournament?.requires_team && (
                <div className="registration-options">
                  {userTeamsForTournament.eligible_teams && userTeamsForTournament.eligible_teams.length > 0 ? (
                    <>
                      <div className="option-group">
                        <label>
                          <input
                            type="radio"
                            name="registrationType"
                            value="existing"
                            checked={registrationType === 'existing'}
                            onChange={(e) => setRegistrationType(e.target.value)}
                          />
                          Utiliser une équipe existante
                        </label>
                        
                        {registrationType === 'existing' && (
                          <select
                            value={selectedTeamForRegistration}
                            onChange={(e) => setSelectedTeamForRegistration(e.target.value)}
                            className="team-select"
                          >
                            <option value="">Sélectionner une équipe</option>
                            {userTeamsForTournament.eligible_teams.map(team => (
                              <option key={team.id} value={team.id}>
                                {team.name} ({team.member_count}/{team.max_members}) 
                                {team.is_captain ? ' - Capitaine' : ' - Membre'}
                              </option>
                            ))}
                          </select>
                        )}
                      </div>

                      <div className="option-group">
                        <label>
                          <input
                            type="radio"
                            name="registrationType"
                            value="new"
                            checked={registrationType === 'new'}
                            onChange={(e) => setRegistrationType(e.target.value)}
                          />
                          Créer une nouvelle équipe
                        </label>
                        
                        {registrationType === 'new' && (
                          <input
                            type="text"
                            placeholder="Nom de la nouvelle équipe"
                            value={newTeamName}
                            onChange={(e) => setNewTeamName(e.target.value)}
                            className="team-name-input"
                          />
                        )}
                      </div>
                    </>
                  ) : (
                    <div className="no-teams-message">
                      <p>❌ Vous n'avez aucune équipe éligible pour ce tournoi.</p>
                      <p>Vous devez créer ou rejoindre une équipe pour le jeu <strong>{formatGameName(tournament.game)}</strong>.</p>
                      
                      <div className="option-group">
                        <label>
                          <input
                            type="radio"
                            name="registrationType"
                            value="new"
                            checked={registrationType === 'new'}
                            onChange={(e) => setRegistrationType(e.target.value)}
                          />
                          Créer une nouvelle équipe maintenant
                        </label>
                        
                        {registrationType === 'new' && (
                          <input
                            type="text"
                            placeholder="Nom de la nouvelle équipe"
                            value={newTeamName}
                            onChange={(e) => setNewTeamName(e.target.value)}
                            className="team-name-input"
                          />
                        )}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Individual Registration Info */}
              {!userTeamsForTournament?.requires_team && (
                <div className="individual-registration-info">
                  <p>✅ Vous vous inscrivez en tant qu'individu à ce tournoi 1v1.</p>
                </div>
              )}
            </div>

            <div className="modal-footer">
              <button className="btn-secondary" onClick={handleCloseRegistrationModal}>
                Annuler
              </button>
              <button
                className="btn-primary"
                onClick={handleRegistration}
                disabled={registrationLoading || (
                  userTeamsForTournament?.requires_team &&
                  registrationType === 'existing' &&
                  !selectedTeamForRegistration
                ) || (
                  registrationType === 'new' &&
                  !newTeamName.trim()
                )}
              >
                {registrationLoading ? 'Inscription...' : 'S\'inscrire'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Team Management Modal */}
      <TeamManagementModal
        isOpen={showTeamManagementModal}
        onClose={() => setShowTeamManagementModal(false)}
        team={selectedTeamForManagement}
        onTeamUpdated={handleTeamUpdated}
      />

      <style jsx>{`
        .page-container {
          min-height: 100vh;
          background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
          color: white;
        }

        .tournament-header {
          background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
          padding: 2rem 0;
        }

        .header-content {
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 1rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 2rem;
        }

        .tournament-info {
          flex: 1;
        }

        .tournament-title {
          font-size: 2.5rem;
          font-weight: 700;
          margin: 0 0 1rem 0;
          text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }

        .tournament-meta {
          display: flex;
          gap: 1rem;
          margin-bottom: 1rem;
          flex-wrap: wrap;
        }

        .game-badge,
        .status-badge,
        .participants-count {
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-size: 0.9rem;
          font-weight: 500;
        }

        .game-badge {
          background: rgba(255, 255, 255, 0.2);
        }

        .status-open { 
          background: #10b981; 
          color: white;
          font-weight: 600;
          box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
        }
        .status-progress { background: #f59e0b; }
        .status-completed { background: #6b7280; }
        .status-cancelled { background: #ef4444; }

        .participants-count {
          background: rgba(255, 255, 255, 0.15);
        }

        .tournament-description {
          font-size: 1.1rem;
          opacity: 0.9;
          line-height: 1.6;
          margin: 0;
        }

        .tournament-actions {
          display: flex;
          flex-direction: column;
          gap: 1rem;
          align-items: center;
        }

        .btn-register {
          font-size: 1.1rem;
          padding: 1rem 2rem;
          white-space: nowrap;
        }

        .registered-badge {
          background: #10b981;
          color: white;
          padding: 1rem 2rem;
          border-radius: 8px;
          font-weight: 600;
          font-size: 1.1rem;
        }

        .tournament-content {
          max-width: 1200px;
          margin: 0 auto;
          padding: 2rem 1rem;
        }

        .content-grid {
          display: grid;
          grid-template-columns: 2fr 1fr;
          gap: 2rem;
        }

        .details-card,
        .participants-card,
        .user-teams-card {
          background: white;
          border-radius: 12px;
          padding: 1.5rem;
          margin-bottom: 1.5rem;
          border: 1px solid #e5e7eb;
          color: #1a1a1a;
        }

        .details-card h3,
        .participants-card h3,
        .user-teams-card h3 {
          margin: 0 0 1rem 0;
          color: #1e3a8a;
          font-size: 1.2rem;
          font-weight: 600;
        }

        .detail-item {
          margin-bottom: 1rem;
          line-height: 1.6;
          color: #1a1a1a;
        }

        .detail-item strong {
          color: #1e3a8a;
        }

        .rules-content {
          line-height: 1.7;
          color: #4b5563;
        }

        .participants-list {
          max-height: 400px;
          overflow-y: auto;
        }

        .participant-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0.75rem;
          margin-bottom: 0.5rem;
          background: #f8fafc;
          border-radius: 8px;
          border: 1px solid #e5e7eb;
        }

        .participant-info {
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .participant-rank {
          color: #1e3a8a;
          font-weight: 600;
          font-size: 0.9rem;
        }

        .participant-name {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-weight: 500;
          color: #1a1a1a;
        }

        .team-icon,
        .user-icon {
          font-size: 1.1rem;
        }

        .member-count {
          color: #6b7280;
          font-size: 0.9rem;
        }

        .no-participants {
          text-align: center;
          color: #6b7280;
          font-style: italic;
          padding: 2rem;
        }

        .teams-list {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .team-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 1rem;
          background: #f8fafc;
          border-radius: 8px;
          border: 1px solid #e5e7eb;
        }

        .team-info {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
        }

        .team-name {
          font-weight: 600;
          color: #1a1a1a;
        }

        .captain-badge {
          font-size: 0.8rem;
          color: #fbbf24;
          font-weight: 500;
        }

        .team-members {
          font-size: 0.9rem;
          color: #6b7280;
        }

        .btn-manage-team {
          background: #3b82f6;
          color: white;
          border: none;
          padding: 0.5rem 1rem;
          border-radius: 6px;
          font-size: 0.9rem;
          font-weight: 500;
          cursor: pointer;
          transition: background-color 0.3s;
        }

        .btn-manage-team:hover {
          background: #2563eb;
        }

        /* Modal Styles */
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
        }

        .modal-content {
          background: white;
          border-radius: 15px;
          width: 90%;
          max-width: 600px;
          max-height: 90vh;
          overflow-y: auto;
          color: #1a1a1a;
        }

        .modal-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 1.5rem;
          border-bottom: 1px solid #e5e7eb;
          background: linear-gradient(135deg, #1e3a8a, #3b82f6);
          color: white;
          border-radius: 15px 15px 0 0;
        }

        .modal-header h2 {
          margin: 0;
          font-size: 1.25rem;
          font-weight: 600;
        }

        .modal-close {
          background: none;
          border: none;
          font-size: 2rem;
          color: white;
          cursor: pointer;
          padding: 0;
          width: 40px;
          height: 40px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 50%;
          transition: background-color 0.3s;
        }

        .modal-close:hover {
          background: rgba(255, 255, 255, 0.2);
        }

        .modal-body {
          padding: 1.5rem;
        }

        .tournament-info-summary {
          margin-bottom: 1.5rem;
          padding: 1rem;
          background: #f8fafc;
          border-radius: 8px;
          border: 1px solid #e5e7eb;
        }

        .tournament-info-summary h3 {
          margin: 0 0 0.5rem 0;
          color: #1e3a8a;
        }

        .team-required {
          color: #dc2626;
          font-weight: 600;
          margin: 0.5rem 0 0 0;
        }

        .individual-allowed {
          color: #16a34a;
          font-weight: 600;
          margin: 0.5rem 0 0 0;
        }

        .registration-options {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }

        .option-group {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .option-group label {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-weight: 500;
          cursor: pointer;
        }

        .team-select,
        .team-name-input {
          padding: 0.75rem;
          border: 2px solid #e5e7eb;
          border-radius: 8px;
          font-size: 1rem;
          margin-left: 1.5rem;
        }

        .team-select:focus,
        .team-name-input:focus {
          outline: none;
          border-color: #3b82f6;
        }

        .no-teams-message {
          padding: 1rem;
          background: #fee2e2;
          border: 1px solid #fecaca;
          border-radius: 8px;
          color: #991b1b;
          margin-bottom: 1rem;
        }

        .individual-registration-info {
          padding: 1rem;
          background: #d1fae5;
          border: 1px solid #a7f3d0;
          border-radius: 8px;
          color: #065f46;
        }

        .modal-footer {
          padding: 1rem 1.5rem;
          border-top: 1px solid #e5e7eb;
          display: flex;
          justify-content: flex-end;
          gap: 1rem;
        }

        .btn-primary,
        .btn-secondary {
          padding: 0.75rem 1.5rem;
          border-radius: 8px;
          font-size: 1rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.3s;
          border: none;
        }

        .btn-primary {
          background: linear-gradient(45deg, #3b82f6, #1d4ed8);
          color: white;
        }

        .btn-primary:hover:not(:disabled) {
          background: linear-gradient(45deg, #2563eb, #1e40af);
          transform: translateY(-1px);
        }

        .btn-primary:disabled {
          opacity: 0.6;
          cursor: not-allowed;
          transform: none;
        }

        .btn-secondary {
          background: #6b7280;
          color: white;
        }

        .btn-secondary:hover {
          background: #4b5563;
        }

        .error-message {
          background-color: rgba(239, 68, 68, 0.1);
          color: #dc2626;
          padding: 0.75rem;
          border-radius: 8px;
          margin-bottom: 1rem;
          border: 1px solid rgba(239, 68, 68, 0.2);
        }

        .loading-container,
        .error-container {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          min-height: 50vh;
          padding: 2rem;
          text-align: center;
        }

        .loading-spinner {
          width: 40px;
          height: 40px;
          border: 4px solid rgba(255, 255, 255, 0.3);
          border-left: 4px solid #3b82f6;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin-bottom: 1rem;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        /* Responsive Design */
        @media (max-width: 768px) {
          .header-content {
            flex-direction: column;
            text-align: center;
          }

          .tournament-title {
            font-size: 2rem;
          }

          .content-grid {
            grid-template-columns: 1fr;
          }

          .tournament-meta {
            justify-content: center;
          }

          .modal-content {
            width: 95%;
            margin: 1rem;
          }

          .option-group {
            gap: 0.5rem;
          }

          .team-select,
          .team-name-input {
            margin-left: 0;
            margin-top: 0.5rem;
          }
        }
      `}</style>
    </div>
  );
};

export default TournamentDetail;