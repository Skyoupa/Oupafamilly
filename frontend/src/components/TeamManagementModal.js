import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

const TeamManagementModal = ({ isOpen, onClose, team, onTeamUpdated }) => {
  const { API_BASE_URL, token } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [availableUsers, setAvailableUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState('');

  useEffect(() => {
    if (isOpen && team) {
      fetchAvailableUsers();
    }
  }, [isOpen, team]);

  const fetchAvailableUsers = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/teams/${team.id}/available-users`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setAvailableUsers(data.available_users || []);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des utilisateurs disponibles:', error);
    }
  };

  const handleAddMember = async () => {
    if (!selectedUser) return;

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch(`${API_BASE_URL}/teams/${team.id}/add-member?user_id=${selectedUser}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setSuccess(data.message);
        setSelectedUser('');
        fetchAvailableUsers(); // Refresh available users
        if (onTeamUpdated) onTeamUpdated();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Erreur lors de l\'ajout du membre');
      }
    } catch (error) {
      setError('Erreur lors de l\'ajout du membre');
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveMember = async (userId, username) => {
    if (!window.confirm(`Êtes-vous sûr de vouloir retirer ${username} de l'équipe ?`)) {
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch(`${API_BASE_URL}/teams/${team.id}/remove-member/${userId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setSuccess(data.message);
        fetchAvailableUsers(); // Refresh available users
        if (onTeamUpdated) onTeamUpdated();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Erreur lors de la suppression du membre');
      }
    } catch (error) {
      setError('Erreur lors de la suppression du membre');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTeam = async () => {
    const confirmDelete = window.confirm(
      `⚠️ ATTENTION ⚠️\n\nVoulez-vous vraiment supprimer définitivement l'équipe "${team.name}" ?\n\n` +
      `Cette action est IRRÉVERSIBLE et supprimera :\n` +
      `• L'équipe et tous ses membres\n` +
      `• L'historique de l'équipe\n` +
      `• Les statistiques de l'équipe\n\n` +
      `Tapez "SUPPRIMER" dans la prochaine boîte de dialogue pour confirmer.`
    );

    if (!confirmDelete) return;

    const confirmText = window.prompt(
      `Pour confirmer la suppression de l'équipe "${team.name}", tapez exactement : SUPPRIMER`
    );

    if (confirmText !== 'SUPPRIMER') {
      if (confirmText !== null) { // User didn't cancel
        alert('Confirmation incorrecte. Suppression annulée.');
      }
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch(`${API_BASE_URL}/teams/${team.id}/delete`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        alert(data.message || 'Équipe supprimée avec succès !');
        onClose(); // Close modal
        if (onTeamUpdated) onTeamUpdated(); // Refresh parent component
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Erreur lors de la suppression de l\'équipe');
      }
    } catch (error) {
      setError('Erreur lors de la suppression de l\'équipe');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content team-management-modal">
        <div className="modal-header">
          <h2>Gérer l'équipe : {team?.name}</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          {error && <div className="error-message">{error}</div>}
          {success && <div className="success-message">{success}</div>}

          {/* Current Team Members */}
          <div className="team-members-section">
            <h3>Membres actuels ({team?.member_count || 0}/{team?.max_members || 6})</h3>
            <div className="members-list">
              {team?.members?.map(member => (
                <div key={member.id || member} className="member-item">
                  <div className="member-info">
                    <span className="member-name">
                      {member.username || member}
                      {team.captain === member.username && <span className="captain-icon"> 👑</span>}
                    </span>
                  </div>
                  {team.captain !== (member.username || member) && (
                    <button
                      className="btn-danger-sm"
                      onClick={() => handleRemoveMember(member.id || member, member.username || member)}
                      disabled={loading}
                    >
                      Retirer
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Add New Member */}
          {availableUsers.length > 0 && team?.member_count < team?.max_members && (
            <div className="add-member-section">
              <h3>Ajouter un membre</h3>
              <div className="add-member-form">
                <select
                  value={selectedUser}
                  onChange={(e) => setSelectedUser(e.target.value)}
                  disabled={loading}
                >
                  <option value="">Sélectionner un utilisateur</option>
                  {availableUsers.map(user => (
                    <option key={user.id} value={user.id}>
                      {user.username} ({user.role})
                    </option>
                  ))}
                </select>
                <button
                  className="btn-primary"
                  onClick={handleAddMember}
                  disabled={loading || !selectedUser}
                >
                  {loading ? 'Ajout...' : 'Ajouter'}
                </button>
              </div>
            </div>
          )}

          {availableUsers.length === 0 && team?.member_count < team?.max_members && (
            <div className="no-users-message">
              <p>Aucun utilisateur disponible pour rejoindre cette équipe.</p>
            </div>
          )}

          {team?.member_count >= team?.max_members && (
            <div className="team-full-message">
              <p>L'équipe est complète ({team.max_members} membres maximum).</p>
            </div>
          )}
        </div>

        <div className="modal-footer">
          <div className="footer-left">
            <button 
              className="btn-danger-team" 
              onClick={handleDeleteTeam}
              disabled={loading}
              title="Supprimer définitivement cette équipe"
            >
              🗑️ Supprimer l'équipe
            </button>
          </div>
          <div className="footer-right">
            <button className="btn-secondary" onClick={onClose}>
              Fermer
            </button>
          </div>
        </div>

        <style jsx>{`
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

          .team-management-modal {
            background: white;
            border-radius: 15px;
            width: 90%;
            max-width: 600px;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
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

          .team-members-section,
          .add-member-section {
            margin-bottom: 2rem;
          }

          .team-members-section h3,
          .add-member-section h3 {
            color: #1e3a8a;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #e5e7eb;
          }

          .members-list {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
          }

          .member-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem;
            background: #f8fafc;
            border-radius: 8px;
            border: 1px solid #e5e7eb;
          }

          .member-info {
            display: flex;
            align-items: center;
            gap: 0.5rem;
          }

          .member-name {
            font-weight: 500;
            color: #1a1a1a;
          }

          .captain-icon {
            font-size: 1.2rem;
          }

          .btn-danger-sm {
            background: #ef4444;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-size: 0.875rem;
            font-weight: 500;
            cursor: pointer;
            transition: background-color 0.3s;
          }

          .btn-danger-sm:hover:not(:disabled) {
            background: #dc2626;
          }

          .btn-danger-sm:disabled {
            opacity: 0.6;
            cursor: not-allowed;
          }

          .add-member-form {
            display: flex;
            gap: 1rem;
            align-items: center;
          }

          .add-member-form select {
            flex: 1;
            padding: 0.75rem;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            font-size: 1rem;
            color: #1a1a1a;
            background: white;
          }

          .add-member-form select:focus {
            outline: none;
            border-color: #3b82f6;
          }

          .btn-primary {
            background: linear-gradient(45deg, #3b82f6, #1d4ed8);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s;
            white-space: nowrap;
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

          .no-users-message,
          .team-full-message {
            padding: 1rem;
            background: #f3f4f6;
            border-radius: 8px;
            color: #6b7280;
            text-align: center;
            font-style: italic;
          }

          .team-full-message {
            background: #fef3c7;
            color: #92400e;
          }

          .modal-footer {
            padding: 1rem 1.5rem;
            border-top: 1px solid #e5e7eb;
            display: flex;
            justify-content: space-between;
            align-items: center;
          }

          .footer-left {
            display: flex;
          }

          .footer-right {
            display: flex;
          }

          .btn-danger-team {
            background: #ef4444;
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
          }

          .btn-danger-team:hover:not(:disabled) {
            background: #dc2626;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
          }

          .btn-danger-team:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
          }

          .btn-secondary {
            background: #6b7280;
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: background-color 0.3s;
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

          .success-message {
            background-color: rgba(34, 197, 94, 0.1);
            color: #16a34a;
            padding: 0.75rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            border: 1px solid rgba(34, 197, 94, 0.2);
          }

          @media (max-width: 768px) {
            .team-management-modal {
              width: 95%;
              margin: 1rem;
            }

            .add-member-form {
              flex-direction: column;
              align-items: stretch;
            }

            .member-item {
              flex-direction: column;
              align-items: flex-start;
              gap: 0.5rem;
            }
          }
        `}</style>
      </div>
    </div>
  );
};

export default TeamManagementModal;