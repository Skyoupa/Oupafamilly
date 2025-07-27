import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import AdminTeamsManagement from '../components/AdminTeamsManagement';

const AdminDashboard = () => {
  const { user, token, API_BASE_URL } = useAuth();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showTeamsManagement, setShowTeamsManagement] = useState(false);

  useEffect(() => {
    if (user?.role === 'admin') {
      fetchDashboardData();
    }
  }, [user]);

  const fetchDashboardData = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/admin/dashboard`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setDashboardData(data);
      } else {
        setError('Erreur lors du chargement du dashboard');
      }
    } catch (error) {
      console.error('Erreur dashboard:', error);
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  if (user?.role !== 'admin') {
    return (
      <div className="admin-container">
        <div className="access-denied">
          <h1>⛔ Accès refusé</h1>
          <p>Seuls les administrateurs peuvent accéder à cette page.</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="admin-container">
        <div className="loading">Chargement du dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="admin-container">
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div className="admin-container">
      <div className="admin-header">
        <h1>🛡️ Dashboard Administrateur</h1>
        <p>Gestion de la communauté Oupafamilly</p>
      </div>

      {dashboardData && (
        <>
          {/* Statistiques principales */}
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon">👥</div>
              <div className="stat-content">
                <h3>{dashboardData.community_overview.total_members}</h3>
                <p>Membres total</p>
                <span className="stat-detail">
                  {dashboardData.community_overview.active_members} actifs
                </span>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">🏆</div>
              <div className="stat-content">
                <h3>{dashboardData.tournaments.total}</h3>
                <p>Tournois</p>
                <span className="stat-detail">
                  {dashboardData.tournaments.active} en cours
                </span>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">📰</div>
              <div className="stat-content">
                <h3>{dashboardData.content.news_articles}</h3>
                <p>Articles</p>
                <span className="stat-detail">
                  {dashboardData.content.tutorials} tutoriels
                </span>
              </div>
            </div>

            <div className="stat-card growth">
              <div className="stat-icon">📈</div>
              <div className="stat-content">
                <h3>{dashboardData.community_overview.growth_this_week}</h3>
                <p>Nouveaux cette semaine</p>
                <span className="stat-detail">
                  {dashboardData.community_overview.activity_rate}% actifs
                </span>
              </div>
            </div>
          </div>

          {/* Nouveaux membres */}
          <div className="admin-section">
            <h2>👋 Nouveaux membres</h2>
            <div className="members-list">
              {dashboardData.recent_members.map(member => (
                <div key={member.id} className="member-card">
                  <div className="member-info">
                    <strong>{member.username}</strong>
                    <span className="member-email">{member.email}</span>
                  </div>
                  <div className="member-status">
                    <span className={`status ${member.status}`}>
                      {member.status === 'active' ? '✅ Actif' : '⏳ En attente'}
                    </span>
                    <span className="member-date">
                      {new Date(member.created_at).toLocaleDateString('fr-FR')}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Actions rapides */}
          <div className="admin-section">
            <h2>⚡ Actions rapides</h2>
            <div className="quick-actions">
              <a 
                href="/admin/ultimate"
                className="action-btn premium"
                style={{
                  background: 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
                  border: '2px solid #60a5fa',
                  boxShadow: '0 8px 25px rgba(59, 130, 246, 0.4)',
                  transform: 'scale(1.05)',
                  position: 'relative'
                }}
              >
                🚀 COMMAND CENTER ULTIME
                <span style={{
                  position: 'absolute',
                  top: '-8px',
                  right: '-8px',
                  background: '#ef4444',
                  color: 'white',
                  borderRadius: '50%',
                  width: '20px',
                  height: '20px',
                  fontSize: '10px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  animation: 'pulse 2s infinite'
                }}>
                  NEW
                </span>
              </a>
              <a 
                href="/admin/tournaments"
                className="action-btn primary"
              >
                🏆 Gérer les tournois
              </a>
              <a 
                href="/admin/users"
                className="action-btn secondary"
              >
                👥 Gérer les utilisateurs
              </a>
              <a 
                href="/admin/content"
                className="action-btn secondary"
              >
                📝 Gérer le contenu
              </a>
              <button 
                className="action-btn secondary"
                onClick={() => setShowTeamsManagement(!showTeamsManagement)}
              >
                🛡️ Gérer les équipes
              </button>
              <button 
                className="action-btn tertiary"
                onClick={fetchDashboardData}
              >
                🔄 Actualiser
              </button>
            </div>
          </div>

          {/* Gestion des équipes */}
          {showTeamsManagement && (
            <div className="admin-section">
              <div className="section-header">
                <h2>🛡️ Gestion des équipes</h2>
                <button 
                  className="close-section-btn"
                  onClick={() => setShowTeamsManagement(false)}
                >
                  ✕ Fermer
                </button>
              </div>
              <AdminTeamsManagement />
            </div>
          )}

          {/* Santé de la communauté */}
          <div className="admin-section">
            <h2>💚 Santé de la communauté</h2>
            <div className="health-card">
              <div className="health-score">
                <div className="score-circle">
                  <span>{dashboardData.community_health.engagement_score}</span>
                </div>
                <p>Score d'engagement</p>
              </div>
              <div className="health-details">
                <div className="health-item">
                  <span className="health-label">État général:</span>
                  <span className={`health-value ${dashboardData.community_health.needs_attention ? 'warning' : 'good'}`}>
                    {dashboardData.community_health.needs_attention ? '⚠️ Attention requise' : '✅ Excellent'}
                  </span>
                </div>
                <div className="health-item">
                  <span className="health-label">Croissance:</span>
                  <span className="health-value good">📈 Positive</span>
                </div>
              </div>
            </div>
          </div>
        </>
      )}

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

        .admin-header p {
          margin: 0;
          opacity: 0.9;
          font-size: 18px;
        }

        .stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 20px;
          margin-bottom: 40px;
        }

        .stat-card {
          background: white;
          border-radius: 15px;
          padding: 25px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
          display: flex;
          align-items: center;
          gap: 20px;
          transition: transform 0.3s;
        }

        .stat-card:hover {
          transform: translateY(-5px);
        }

        .stat-card.growth {
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
          color: white;
        }

        .stat-icon {
          font-size: 40px;
          width: 60px;
          height: 60px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: rgba(59, 130, 246, 0.1);
          border-radius: 50%;
        }

        .growth .stat-icon {
          background: rgba(255, 255, 255, 0.2);
        }

        .stat-content h3 {
          margin: 0 0 5px 0;
          font-size: 32px;
          font-weight: 700;
          color: #1e3a8a;
        }

        .growth .stat-content h3 {
          color: white;
        }

        .stat-content p {
          margin: 0 0 5px 0;
          font-size: 16px;
          font-weight: 600;
          color: #1a1a1a;
        }

        .growth .stat-content p {
          color: rgba(255, 255, 255, 0.9);
        }

        .stat-detail {
          font-size: 14px;
          color: #333333;
        }

        .growth .stat-detail {
          color: rgba(255, 255, 255, 0.8);
        }

        .admin-section {
          background: white;
          border-radius: 15px;
          padding: 30px;
          margin-bottom: 30px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }

        .admin-section h2 {
          margin: 0 0 25px 0;
          color: #1e3a8a;
          font-size: 24px;
          font-weight: 600;
        }

        .members-list {
          display: flex;
          flex-direction: column;
          gap: 15px;
        }

        .member-card {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 15px;
          background: #f8fafc;
          border-radius: 10px;
          border: 1px solid #e5e7eb;
        }

        .member-info strong {
          display: block;
          color: #1e3a8a;
          font-weight: 600;
        }

        .member-email {
          color: #333333 !important;
          font-size: 14px;
        }

        .member-status {
          display: flex;
          flex-direction: column;
          align-items: flex-end;
          gap: 5px;
        }

        .status {
          padding: 4px 8px;
          border-radius: 6px;
          font-size: 12px;
          font-weight: 600;
        }

        .status.active {
          background: #dcfce7;
          color: #166534;
        }

        .status.pending {
          background: #fef3c7;
          color: #92400e;
        }

        .member-date {
          font-size: 12px;
          color: #333333 !important;
        }

        .quick-actions {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 15px;
        }

        .action-btn {
          padding: 15px 20px;
          border: none;
          border-radius: 10px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s;
          text-decoration: none;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
        }

        .action-btn.primary {
          background: linear-gradient(45deg, #3b82f6, #1d4ed8);
          color: white;
        }

        .action-btn.primary:hover {
          background: linear-gradient(45deg, #2563eb, #1e40af);
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(59, 130, 246, 0.3);
        }

        .action-btn.secondary {
          background: linear-gradient(45deg, #3b82f6, #1d4ed8);
          color: white;
          border: none;
        }

        .action-btn.secondary:hover {
          background: linear-gradient(45deg, #2563eb, #1e40af);
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(59, 130, 246, 0.3);
        }

        .action-btn.tertiary {
          background: transparent;
          color: #6b7280;
          border: 2px dashed #d1d5db;
        }

        .action-btn.tertiary:hover {
          background: #f9fafb;
          color: #374151;
        }

        .health-card {
          display: flex;
          align-items: center;
          gap: 30px;
          padding: 20px;
          background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
          border-radius: 15px;
          border: 1px solid #bae6fd;
        }

        .health-score {
          text-align: center;
        }

        .score-circle {
          width: 80px;
          height: 80px;
          border-radius: 50%;
          background: linear-gradient(135deg, #10b981 0%, #059669 100%);
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-size: 24px;
          font-weight: 700;
          margin-bottom: 10px;
        }

        .health-details {
          flex: 1;
        }

        .health-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 10px;
        }

        .health-label {
          font-weight: 600;
          color: #374151;
        }

        .health-value {
          font-weight: 600;
        }

        .health-value.good {
          color: #059669;
        }

        .health-value.warning {
          color: #d97706;
        }

        .section-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
        }

        .close-section-btn {
          background: #ef4444;
          color: white;
          border: none;
          padding: 8px 16px;
          border-radius: 6px;
          font-size: 14px;
          font-weight: 500;
          cursor: pointer;
          transition: background-color 0.3s;
        }

        .close-section-btn:hover {
          background: #dc2626;
        }

        .loading, .error, .access-denied {
          text-align: center;
          padding: 60px 20px;
          background: white;
          border-radius: 15px;
          margin: 40px 0;
        }

        .error {
          color: #dc2626;
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

          .stats-grid {
            grid-template-columns: 1fr;
          }

          .stat-card {
            padding: 20px;
          }

          .admin-section {
            padding: 20px;
          }

          .health-card {
            flex-direction: column;
            text-align: center;
          }

          .quick-actions {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
};

export default AdminDashboard;