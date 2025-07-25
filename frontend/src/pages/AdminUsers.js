import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

const AdminUsers = () => {
  const { user, token, API_BASE_URL } = useAuth();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterRole, setFilterRole] = useState('all');

  useEffect(() => {
    if (user?.role === 'admin') {
      fetchUsers();
    }
  }, [user, filterStatus, filterRole]);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      let url = `${API_BASE_URL}/admin/users?limit=100`;
      if (filterStatus !== 'all') {
        url += `&status=${filterStatus}`;
      }
      if (filterRole !== 'all') {
        url += `&role=${filterRole}`;
      }

      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setUsers(data);
      } else {
        setError('Erreur lors du chargement des utilisateurs');
      }
    } catch (error) {
      console.error('Erreur fetch users:', error);
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  const updateUserStatus = async (userId, newStatus) => {
    try {
      const response = await fetch(`${API_BASE_URL}/admin/users/${userId}/status?new_status=${newStatus}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        setSuccess(`Statut utilisateur mis à jour : ${newStatus}`);
        fetchUsers();
        setTimeout(() => setSuccess(''), 3000);
      } else {
        setError('Erreur lors de la mise à jour du statut');
      }
    } catch (error) {
      setError('Erreur de connexion au serveur');
    }
  };

  const updateUserRole = async (userId, newRole) => {
    try {
      const response = await fetch(`${API_BASE_URL}/admin/users/${userId}/role?new_role=${newRole}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        setSuccess(`Rôle utilisateur mis à jour : ${newRole}`);
        fetchUsers();
        setTimeout(() => setSuccess(''), 3000);
      } else {
        setError('Erreur lors de la mise à jour du rôle');
      }
    } catch (error) {
      setError('Erreur de connexion au serveur');
    }
  };

  const deleteUser = async (userId, username) => {
    if (window.confirm(`Êtes-vous sûr de vouloir supprimer l'utilisateur "${username}" ? Cette action est irréversible.`)) {
      try {
        const response = await fetch(`${API_BASE_URL}/admin/users/${userId}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.ok) {
          setSuccess(`Utilisateur "${username}" supprimé avec succès`);
          fetchUsers();
          setTimeout(() => setSuccess(''), 3000);
        } else {
          setError('Erreur lors de la suppression');
        }
      } catch (error) {
        setError('Erreur de connexion au serveur');
      }
    }
  };

  if (user?.role !== 'admin') {
    return (
      <div className="admin-container">
        <div className="access-denied">
          <h1>⛔ Accès refusé</h1>
          <p>Seuls les administrateurs peuvent gérer les utilisateurs.</p>
        </div>
      </div>
    );
  }

  const getRoleColor = (role) => {
    switch(role) {
      case 'admin': return '#ef4444';
      case 'moderator': return '#f59e0b';
      case 'member': return '#10b981';
      default: return '#6b7280';
    }
  };

  const getStatusColor = (status) => {
    switch(status) {
      case 'active': return '#10b981';
      case 'inactive': return '#6b7280';
      case 'pending': return '#f59e0b';
      default: return '#6b7280';
    }
  };

  return (
    <div className="admin-container">
      <div className="admin-header">
        <h1>👥 Gestion des Utilisateurs</h1>
        <p>Gérez les membres de votre communauté</p>
      </div>

      <div className="admin-section">
        <div className="section-header">
          <h2>🔍 Filtres</h2>
          <div className="user-stats">
            <span>Total: {users.length} utilisateurs</span>
          </div>
        </div>

        {/* Messages */}
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        {/* Filtres */}
        <div className="filters">
          <div className="filter-group">
            <label htmlFor="status-filter">Statut :</label>
            <select 
              id="status-filter"
              value={filterStatus} 
              onChange={(e) => setFilterStatus(e.target.value)}
            >
              <option value="all">Tous les statuts</option>
              <option value="active">Actif</option>
              <option value="inactive">Inactif</option>
              <option value="pending">En attente</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="role-filter">Rôle :</label>
            <select 
              id="role-filter"
              value={filterRole} 
              onChange={(e) => setFilterRole(e.target.value)}
            >
              <option value="all">Tous les rôles</option>
              <option value="admin">Administrateur</option>
              <option value="moderator">Modérateur</option>
              <option value="member">Membre</option>
            </select>
          </div>

          <button className="btn-refresh" onClick={fetchUsers}>
            🔄 Actualiser
          </button>
        </div>
      </div>

      {/* Liste des utilisateurs */}
      <div className="admin-section">
        <h2>📋 Liste des utilisateurs</h2>
        
        {loading ? (
          <div className="loading">Chargement des utilisateurs...</div>
        ) : users.length === 0 ? (
          <div className="empty-state">
            <p>Aucun utilisateur trouvé avec ces critères.</p>
          </div>
        ) : (
          <div className="users-table">
            <div className="table-header">
              <div className="col-user">Utilisateur</div>
              <div className="col-role">Rôle</div>
              <div className="col-status">Statut</div>
              <div className="col-date">Inscription</div>
              <div className="col-actions">Actions</div>
            </div>

            {users.map(userItem => (
              <div key={userItem.id} className="table-row">
                <div className="col-user">
                  <div className="user-info">
                    <strong>{userItem.username}</strong>
                    <span className="user-email">{userItem.email}</span>
                  </div>
                </div>

                <div className="col-role">
                  <select
                    value={userItem.role}
                    onChange={(e) => updateUserRole(userItem.id, e.target.value)}
                    className="role-select"
                    style={{ borderColor: getRoleColor(userItem.role) }}
                    disabled={userItem.id === user.id} // Empêcher l'admin de changer son propre rôle
                  >
                    <option value="member">Membre</option>
                    <option value="moderator">Modérateur</option>
                    <option value="admin">Administrateur</option>
                  </select>
                </div>

                <div className="col-status">
                  <select
                    value={userItem.status}
                    onChange={(e) => updateUserStatus(userItem.id, e.target.value)}
                    className="status-select"
                    style={{ borderColor: getStatusColor(userItem.status) }}
                  >
                    <option value="active">Actif</option>
                    <option value="inactive">Inactif</option>
                    <option value="pending">En attente</option>
                  </select>
                </div>

                <div className="col-date">
                  {new Date(userItem.created_at).toLocaleDateString('fr-FR')}
                </div>

                <div className="col-actions">
                  <div className="action-buttons">
                    {userItem.status === 'pending' && (
                      <button 
                        className="btn-action approve"
                        onClick={() => updateUserStatus(userItem.id, 'active')}
                      >
                        ✅ Approuver
                      </button>
                    )}
                    {userItem.id !== user.id && ( // Empêcher l'admin de se supprimer
                      <button 
                        className="btn-action delete"
                        onClick={() => deleteUser(userItem.id, userItem.username)}
                      >
                        🗑️ Supprimer
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Statistiques rapides */}
      <div className="admin-section">
        <h2>📊 Statistiques rapides</h2>
        <div className="quick-stats">
          <div className="stat-item">
            <span className="stat-number">
              {users.filter(u => u.status === 'active').length}
            </span>
            <span className="stat-label">Utilisateurs actifs</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">
              {users.filter(u => u.status === 'pending').length}
            </span>
            <span className="stat-label">En attente d'approbation</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">
              {users.filter(u => u.role === 'admin').length}
            </span>
            <span className="stat-label">Administrateurs</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">
              {users.filter(u => u.role === 'moderator').length}
            </span>
            <span className="stat-label">Modérateurs</span>
          </div>
        </div>
      </div>

      <style jsx>{`
        .admin-container {
          max-width: 1200px;
          margin: 40px auto;
          padding: 0 20px;
        }

        .admin-header {
          text-align: center;
          margin-bottom: 40px;
          padding: 30px;
          background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
          border-radius: 15px;
          color: white;
        }

        .admin-header h1 {
          margin: 0 0 10px 0;
          font-size: 32px;
          font-weight: 700;
        }

        .admin-section {
          background: white;
          border-radius: 15px;
          padding: 30px;
          margin-bottom: 30px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }

        .section-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 25px;
        }

        .section-header h2 {
          margin: 0;
          color: #1e3a8a;
          font-size: 24px;
          font-weight: 600;
        }

        .user-stats {
          color: #333333;
          font-weight: 600;
        }

        .filters {
          display: flex;
          gap: 20px;
          align-items: end;
          flex-wrap: wrap;
        }

        .filter-group {
          display: flex;
          flex-direction: column;
          gap: 5px;
        }

        .filter-group label {
          font-weight: 600;
          color: #1a1a1a;
          font-size: 14px;
        }

        .filter-group select {
          padding: 10px;
          border: 2px solid #e5e7eb;
          border-radius: 8px;
          background: white;
          min-width: 150px;
          color: #1a1a1a;
        }

        .btn-refresh {
          background: #3b82f6;
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 8px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
        }

        .btn-refresh:hover {
          background: #2563eb;
          transform: translateY(-1px);
        }

        .users-table {
          border: 2px solid #e5e7eb;
          border-radius: 12px;
          overflow: hidden;
        }

        .table-header {
          display: grid;
          grid-template-columns: 2fr 1fr 1fr 1fr 2fr;
          gap: 20px;
          padding: 20px;
          background: #f8fafc;
          font-weight: 700;
          color: #1e3a8a;
          border-bottom: 2px solid #e5e7eb;
        }

        .table-row {
          display: grid;
          grid-template-columns: 2fr 1fr 1fr 1fr 2fr;
          gap: 20px;
          padding: 20px;
          border-bottom: 1px solid #f1f5f9;
          align-items: center;
          transition: background 0.3s;
        }

        .table-row:hover {
          background: #f8fafc;
        }

        .table-row:last-child {
          border-bottom: none;
        }

        .user-info {
          display: flex;
          flex-direction: column;
        }

        .user-info strong {
          color: #1e3a8a;
          font-weight: 600;
        }

        .user-email {
          color: #333333 !important;
          font-size: 14px;
        }

        .role-select,
        .status-select {
          padding: 8px 12px;
          border: 2px solid;
          border-radius: 6px;
          background: white;
          font-weight: 600;
          font-size: 14px;
          cursor: pointer;
          transition: all 0.3s;
          color: #1a1a1a;
        }

        .role-select:focus,
        .status-select:focus {
          outline: none;
          box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        .action-buttons {
          display: flex;
          gap: 8px;
          flex-wrap: wrap;
        }

        .btn-action {
          padding: 6px 12px;
          border: none;
          border-radius: 6px;
          font-size: 12px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
        }

        .btn-action.approve {
          background: #dcfce7;
          color: #166534;
        }

        .btn-action.approve:hover {
          background: #bbf7d0;
          transform: translateY(-1px);
        }

        .btn-action.delete {
          background: #fee2e2;
          color: #dc2626;
        }

        .btn-action.delete:hover {
          background: #fecaca;
          transform: translateY(-1px);
        }

        .quick-stats {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 20px;
        }

        .stat-item {
          text-align: center;
          padding: 20px;
          background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
          border-radius: 12px;
          border: 2px solid #bae6fd;
        }

        .stat-number {
          display: block;
          font-size: 32px;
          font-weight: 700;
          color: #1e3a8a;
          margin-bottom: 5px;
        }

        .stat-label {
          color: #333333;
          font-weight: 600;
        }

        .error-message {
          background: #fee2e2;
          color: #dc2626;
          padding: 12px;
          border-radius: 8px;
          margin-bottom: 20px;
          border: 1px solid #fecaca;
        }

        .success-message {
          background: #dcfce7;
          color: #166534;
          padding: 12px;
          border-radius: 8px;
          margin-bottom: 20px;
          border: 1px solid #bbf7d0;
        }

        .loading, .empty-state {
          text-align: center;
          padding: 40px;
          color: #333333;
        }

        .access-denied {
          text-align: center;
          padding: 60px 20px;
          background: white;
          border-radius: 15px;
          margin: 40px 0;
        }

        .access-denied h1 {
          color: #dc2626;
          margin-bottom: 15px;
        }

        @media (max-width: 768px) {
          .admin-container {
            margin: 20px auto;
            padding: 0 15px;
          }

          .admin-section {
            padding: 20px;
          }

          .filters {
            flex-direction: column;
            align-items: stretch;
          }

          .filter-group select {
            min-width: auto;
          }

          .table-header,
          .table-row {
            grid-template-columns: 1fr;
            gap: 10px;
          }

          .table-header {
            display: none;
          }

          .table-row {
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            margin-bottom: 15px;
          }

          .col-user,
          .col-role,
          .col-status,
          .col-date,
          .col-actions {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 5px 0;
          }

          .col-user::before { content: "Utilisateur: "; font-weight: 600; }
          .col-role::before { content: "Rôle: "; font-weight: 600; }
          .col-status::before { content: "Statut: "; font-weight: 600; }
          .col-date::before { content: "Inscription: "; font-weight: 600; }
          .col-actions::before { content: "Actions: "; font-weight: 600; }

          .quick-stats {
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          }
        }
      `}</style>
    </div>
  );
};

export default AdminUsers;