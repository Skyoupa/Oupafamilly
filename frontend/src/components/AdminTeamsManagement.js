import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

const AdminTeamsManagement = () => {
  const { token, API_BASE_URL } = useAuth();
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchTeams();
  }, []);

  const fetchTeams = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/teams/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setTeams(data);
      } else {
        setError('Erreur lors du chargement des équipes');
      }
    } catch (error) {
      console.error('Erreur fetch teams:', error);
      setError('Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTeam = async (teamId, teamName) => {
    const confirmDelete = window.confirm(
      `⚠️ ATTENTION - SUPPRESSION ADMIN ⚠️\n\n` +
      `Voulez-vous vraiment supprimer définitivement l'équipe "${teamName}" ?\n\n` +
      `Cette action d'admin FORCE la suppression même si l'équipe est inscrite dans des tournois actifs.\n\n` +
      `Tapez "ADMIN-DELETE" pour confirmer cette action administrative.`
    );

    if (!confirmDelete) return;

    const confirmText = window.prompt(
      `Pour confirmer la suppression administrative de l'équipe "${teamName}", tapez exactement : ADMIN-DELETE`
    );

    if (confirmText !== 'ADMIN-DELETE') {
      if (confirmText !== null) {
        alert('Confirmation incorrecte. Suppression annulée.');
      }
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/teams/${teamId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        setSuccess(`Équipe "${teamName}" supprimée avec succès`);
        setError('');
        fetchTeams(); // Refresh teams list
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Erreur lors de la suppression de l\'équipe');
      }
    } catch (error) {
      console.error('Erreur suppression équipe:', error);
      setError('Erreur de connexion lors de la suppression');
    }
  };

  const getGameDisplay = (game) => {
    const gameNames = {
      'cs2': 'Counter-Strike 2',
      'lol': 'League of Legends',
      'wow': 'World of Warcraft',
      'sc2': 'StarCraft II',
      'minecraft': 'Minecraft'
    };
    return gameNames[game] || game;
  };

  if (loading) {
    return (
      <div className="admin-section">
        <h2>🛡️ Gestion des Équipes</h2>
        <div className="loading">Chargement des équipes...</div>
      </div>
    );
  }

  return (
    <div className="admin-section">
      <div className="section-header">
        <h2>🛡️ Gestion des Équipes</h2>
        <p className="section-description">
          Gestion administrative des équipes - Suppression forcée disponible même pour équipes dans tournois actifs
        </p>
      </div>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <div className="teams-admin-grid">
        {teams.length === 0 ? (
          <div className="no-teams">
            <p>Aucune équipe créée pour le moment</p>
          </div>
        ) : (
          teams.map(team => (
            <div key={team.id} className="team-admin-card">
              <div className="team-header">
                <h3 className="team-name">{team.name}</h3>
                <span className="team-game-badge">{getGameDisplay(team.game)}</span>
              </div>

              <div className="team-info">
                <div className="info-row">
                  <span className="label">Capitaine:</span>
                  <span className="value">{team.captain}</span>
                </div>
                <div className="info-row">
                  <span className="label">Membres:</span>
                  <span className="value">{team.member_count}/{team.max_members}</span>
                </div>
                <div className="info-row">
                  <span className="label">Statut:</span>
                  <span className={`status ${team.is_open ? 'open' : 'closed'}`}>
                    {team.is_open ? 'Recrute' : 'Fermée'}
                  </span>
                </div>
                {team.description && (
                  <div className="info-row">
                    <span className="label">Description:</span>
                    <span className="value description">{team.description}</span>
                  </div>
                )}
              </div>

              <div className="team-members">
                <h4>Membres:</h4>
                <div className="members-list">
                  {team.members && team.members.length > 0 ? (
                    team.members.map((member, index) => (
                      <span key={index} className="member-tag">
                        {member === team.captain && <span className="captain-icon">👑</span>}
                        {member}
                      </span>
                    ))
                  ) : (
                    <span className="no-members">Aucun membre</span>
                  )}
                </div>
              </div>

              <div className="team-actions">
                <button
                  className="btn-danger-admin"
                  onClick={() => handleDeleteTeam(team.id, team.name)}
                  title="Suppression administrative forcée"
                >
                  🗑️ Supprimer (Admin)
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      <style jsx>{`
        .admin-section {
          margin-bottom: 3rem;
        }

        .section-header {
          margin-bottom: 2rem;
        }

        .section-header h2 {
          color: #1e3a8a;
          font-size: 1.5rem;
          font-weight: 600;
          margin: 0 0 0.5rem 0;
        }

        .section-description {
          color: #6b7280;
          font-size: 0.9rem;
          margin: 0;
          font-style: italic;
        }

        .teams-admin-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
          gap: 1.5rem;
        }

        .team-admin-card {
          background: white;
          border-radius: 12px;
          padding: 1.5rem;
          border: 1px solid #e5e7eb;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          transition: all 0.3s;
        }

        .team-admin-card:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .team-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
          padding-bottom: 0.75rem;
          border-bottom: 1px solid #e5e7eb;
        }

        .team-name {
          color: #1e3a8a;
          font-size: 1.1rem;
          font-weight: 600;
          margin: 0;
        }

        .team-game-badge {
          background: #3b82f6;
          color: white;
          padding: 0.25rem 0.75rem;
          border-radius: 12px;
          font-size: 0.8rem;
          font-weight: 500;
        }

        .team-info {
          margin-bottom: 1rem;
        }

        .info-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.5rem;
        }

        .info-row .label {
          font-weight: 500;
          color: #374151;
          font-size: 0.9rem;
        }

        .info-row .value {
          color: #6b7280;
          font-size: 0.9rem;
        }

        .info-row .value.description {
          font-style: italic;
          max-width: 60%;
          text-align: right;
        }

        .status.open {
          color: #16a34a;
          font-weight: 500;
        }

        .status.closed {
          color: #dc2626;
          font-weight: 500;
        }

        .team-members {
          margin-bottom: 1.5rem;
        }

        .team-members h4 {
          color: #374151;
          font-size: 0.9rem;
          font-weight: 600;
          margin: 0 0 0.5rem 0;
        }

        .members-list {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }

        .member-tag {
          background: #f3f4f6;
          color: #374151;
          padding: 0.25rem 0.5rem;
          border-radius: 6px;
          font-size: 0.8rem;
          font-weight: 500;
          display: flex;
          align-items: center;
          gap: 0.25rem;
        }

        .captain-icon {
          font-size: 0.9rem;
        }

        .no-members {
          color: #9ca3af;
          font-style: italic;
          font-size: 0.8rem;
        }

        .team-actions {
          display: flex;
          justify-content: flex-end;
        }

        .btn-danger-admin {
          background: #dc2626;
          color: white;
          border: none;
          padding: 0.5rem 1rem;
          border-radius: 8px;
          font-size: 0.9rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.3s;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .btn-danger-admin:hover {
          background: #b91c1c;
          transform: translateY(-1px);
          box-shadow: 0 4px 8px rgba(220, 38, 38, 0.3);
        }

        .no-teams {
          grid-column: 1 / -1;
          text-align: center;
          padding: 3rem;
          color: #6b7280;
          font-style: italic;
        }

        .loading {
          text-align: center;
          padding: 2rem;
          color: #6b7280;
        }

        .error-message {
          background-color: rgba(239, 68, 68, 0.1);
          color: #dc2626;
          padding: 0.75rem;
          border-radius: 8px;
          margin-bottom: 1rem;
          border: 1px solid rgba(239, 68, 68, 0.2);
        }

        .success-message {
          background-color: rgba(34, 197, 94, 0.1);
          color: #16a34a;
          padding: 0.75rem;
          border-radius: 8px;
          margin-bottom: 1rem;
          border: 1px solid rgba(34, 197, 94, 0.2);
        }

        @media (max-width: 768px) {
          .teams-admin-grid {
            grid-template-columns: 1fr;
          }

          .info-row {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.25rem;
          }

          .info-row .value.description {
            max-width: 100%;
            text-align: left;
          }

          .team-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.5rem;
          }
        }
      `}</style>
    </div>
  );
};

export default AdminTeamsManagement;