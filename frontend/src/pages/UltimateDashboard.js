import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';

/**
 * 🚀 OUPAFAMILLY COMMAND CENTER - DASHBOARD ULTIME
 * La dashboard de gestion la plus avancée jamais créée
 */

const UltimateDashboard = () => {
  const { user, token, API_BASE_URL } = useAuth();
  
  // États globaux
  const [activeSection, setActiveSection] = useState('overview');
  const [realTimeData, setRealTimeData] = useState(null);
  const [isRealTimeEnabled, setIsRealTimeEnabled] = useState(true);
  const [loading, setLoading] = useState(true);
  const [alerts, setAlerts] = useState([]);
  const [dashboardConfig, setDashboardConfig] = useState({
    theme: 'dark',
    refreshInterval: 5000,
    autoRefresh: true,
    showNotifications: true
  });
  
  // Données par section
  const [overviewData, setOverviewData] = useState(null);
  const [usersData, setUsersData] = useState(null);
  const [contentData, setContentData] = useState(null);
  const [tournamentsData, setTournamentsData] = useState(null);
  const [analyticsData, setAnalyticsData] = useState(null);
  const [economyData, setEconomyData] = useState(null);
  const [systemData, setSystemData] = useState(null);
  const [moderationData, setModerationData] = useState(null);
  
  // Refs pour auto-refresh
  const intervalRef = useRef(null);
  const wsRef = useRef(null);

  // ===================================
  // SECTIONS DE LA DASHBOARD
  // ===================================
  
  const dashboardSections = [
    {
      id: 'overview',
      name: '📊 Vue d\'ensemble',
      icon: '🎯',
      color: '#3b82f6',
      description: 'Métriques principales et alertes'
    },
    {
      id: 'analytics',
      name: '📈 Analytics Avancées',
      icon: '📊',
      color: '#10b981',
      description: 'Analyses poussées et insights'
    },
    {
      id: 'users',
      name: '👥 Gestion Utilisateurs',
      icon: '👤',
      color: '#8b5cf6',
      description: 'Membres, rôles, sanctions'
    },
    {
      id: 'content',
      name: '📝 Gestion Contenu',
      icon: '📄',
      color: '#f59e0b',
      description: 'Tutoriels, news, média'
    },
    {
      id: 'tournaments',
      name: '🏆 Tournois & Compétitions',
      icon: '⚡',
      color: '#ef4444',
      description: 'Événements, matchs, résultats'
    },
    {
      id: 'economy',
      name: '💰 Économie Virtuelle',
      icon: '💎',
      color: '#06b6d4',
      description: 'Coins, marketplace, premium'
    },
    {
      id: 'moderation',
      name: '🛡️ Modération & Sécurité',
      icon: '🔒',
      color: '#dc2626',
      description: 'Reports, bans, surveillance'
    },
    {
      id: 'system',
      name: '⚙️ Système & Performance',
      icon: '🖥️',
      color: '#6b7280',
      description: 'Serveurs, logs, monitoring'
    },
    {
      id: 'integrations',
      name: '🔗 Intégrations',
      icon: '🌐',
      color: '#7c3aed',
      description: 'Discord, Steam, APIs'
    },
    {
      id: 'settings',
      name: '⚙️ Configuration',
      icon: '🛠️',
      color: '#059669',
      description: 'Paramètres globaux'
    }
  ];

  // ===================================
  // FONCTIONS DE CHARGEMENT DES DONNÉES
  // ===================================

  const fetchOverviewData = useCallback(async () => {
    try {
      const [overview, realtime, alerts] = await Promise.all([
        fetch(`${API_BASE_URL}/analytics/overview`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()),
        
        fetch(`${API_BASE_URL}/analytics/realtime`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()),
        
        fetch(`${API_BASE_URL}/admin/alerts`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()).catch(() => ({ alerts: [] }))
      ]);

      setOverviewData(overview);
      setRealTimeData(realtime);
      setAlerts(alerts.alerts || []);
      
    } catch (error) {
      console.error('Erreur chargement vue d\'ensemble:', error);
    }
  }, [API_BASE_URL, token]);

  const fetchAnalyticsData = useCallback(async () => {
    try {
      const [engagement, gaming, economy, achievements] = await Promise.all([
        fetch(`${API_BASE_URL}/analytics/users/engagement?days=30`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()),
        
        fetch(`${API_BASE_URL}/analytics/gaming/performance?days=30`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()),
        
        fetch(`${API_BASE_URL}/analytics/economy/insights?days=30`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()),
        
        fetch(`${API_BASE_URL}/analytics/achievements/progress?days=30`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json())
      ]);

      setAnalyticsData({
        engagement,
        gaming,
        economy,
        achievements
      });
      
    } catch (error) {
      console.error('Erreur chargement analytics:', error);
    }
  }, [API_BASE_URL, token]);

  const fetchUsersData = useCallback(async () => {
    try {
      const [users, stats, actions] = await Promise.all([
        fetch(`${API_BASE_URL}/admin/users?page=1&limit=50`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()),
        
        fetch(`${API_BASE_URL}/admin/users/stats`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()).catch(() => ({})),
        
        fetch(`${API_BASE_URL}/admin/recent-actions?limit=20`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()).catch(() => ({ actions: [] }))
      ]);

      setUsersData({
        users: users.users || users,
        stats,
        recentActions: actions.actions || []
      });
      
    } catch (error) {
      console.error('Erreur chargement utilisateurs:', error);
    }
  }, [API_BASE_URL, token]);

  const fetchContentData = useCallback(async () => {
    try {
      const [tutorials, news, stats] = await Promise.all([
        fetch(`${API_BASE_URL}/content/tutorials`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()),
        
        fetch(`${API_BASE_URL}/content/news`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()).catch(() => ({ articles: [] })),
        
        fetch(`${API_BASE_URL}/admin/content/stats`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()).catch(() => ({}))
      ]);

      setContentData({
        tutorials: tutorials.tutorials || tutorials,
        news: news.articles || [],
        stats
      });
      
    } catch (error) {
      console.error('Erreur chargement contenu:', error);
    }
  }, [API_BASE_URL, token]);

  const fetchTournamentsData = useCallback(async () => {
    try {
      const [tournaments, matches, stats] = await Promise.all([
        fetch(`${API_BASE_URL}/tournaments/`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()),
        
        fetch(`${API_BASE_URL}/matches?limit=20`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()).catch(() => []),
        
        fetch(`${API_BASE_URL}/admin/tournaments/stats`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()).catch(() => ({}))
      ]);
      
      setTournamentsData({
        tournaments,
        matches,
        stats
      });
      
    } catch (error) {
      console.error('Erreur chargement tournois:', error);
    }
  }, [API_BASE_URL, token]);

  const fetchEconomyData = useCallback(async () => {
    try {
      const [premium, transactions, stats] = await Promise.all([
        fetch(`${API_BASE_URL}/premium/admin/subscriptions?limit=20`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()).catch(() => ({ subscriptions: [] })),
        
        fetch(`${API_BASE_URL}/admin/economy/transactions?limit=50`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()).catch(() => ({ transactions: [] })),
        
        fetch(`${API_BASE_URL}/admin/economy/stats`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()).catch(() => ({}))
      ]);

      setEconomyData({
        premium: premium.subscriptions || [],
        transactions: transactions.transactions || [],
        stats
      });
      
    } catch (error) {
      console.error('Erreur chargement économie:', error);
    }
  }, [API_BASE_URL, token]);

  const fetchSystemData = useCallback(async () => {
    try {
      const [performance, monitoring, logs] = await Promise.all([
        fetch(`${API_BASE_URL}/analytics/performance/system`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()),
        
        fetch(`${API_BASE_URL}/monitoring/health`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()).catch(() => ({})),
        
        fetch(`${API_BASE_URL}/admin/logs?limit=50`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).then(r => r.json()).catch(() => ({ logs: [] }))
      ]);

      setSystemData({
        performance,
        monitoring,
        logs: logs.logs || []
      });
      
    } catch (error) {
      console.error('Erreur chargement système:', error);
    }
  }, [API_BASE_URL, token]);

  // ===================================
  // FONCTION PRINCIPALE DE CHARGEMENT
  // ===================================

  const loadSectionData = useCallback(async (section) => {
    setLoading(true);
    
    try {
      switch (section) {
        case 'overview':
          await fetchOverviewData();
          break;
        case 'analytics':
          await fetchAnalyticsData();
          break;
        case 'users':
          await fetchUsersData();
          break;
        case 'content':
          await fetchContentData();
          break;
        case 'tournaments':
          await fetchTournamentsData();
          break;
        case 'economy':
          await fetchEconomyData();
          break;
        case 'system':
          await fetchSystemData();
          break;
        default:
          await fetchOverviewData();
      }
    } catch (error) {
      console.error('Erreur chargement section:', error);
    } finally {
      setLoading(false);
    }
  }, [fetchOverviewData, fetchAnalyticsData, fetchUsersData, fetchContentData, fetchTournamentsData, fetchEconomyData, fetchSystemData]);

  // ===================================
  // EFFECTS ET AUTO-REFRESH
  // ===================================

  useEffect(() => {
    if (user?.role === 'admin') {
      loadSectionData(activeSection);
    }
  }, [user, activeSection, loadSectionData]);

  useEffect(() => {
    if (dashboardConfig.autoRefresh && isRealTimeEnabled) {
      intervalRef.current = setInterval(() => {
        loadSectionData(activeSection);
      }, dashboardConfig.refreshInterval);
      
      return () => {
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
        }
      };
    }
  }, [activeSection, dashboardConfig, isRealTimeEnabled, loadSectionData]);

  // ===================================
  // FONCTIONS UTILITAIRES
  // ===================================

  const formatNumber = (num) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num?.toString() || '0';
  };

  const getAlertColor = (level) => {
    const colors = {
      'critical': '#ef4444',
      'warning': '#f59e0b',
      'info': '#3b82f6',
      'success': '#10b981'
    };
    return colors[level] || colors.info;
  };

  // Vérification des droits d'accès
  if (user?.role !== 'admin') {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 100%)',
        color: '#f8fafc'
      }}>
        <div style={{
          textAlign: 'center',
          padding: '40px',
          background: 'rgba(239, 68, 68, 0.1)',
          border: '2px solid #ef4444',
          borderRadius: '16px'
        }}>
          <div style={{ fontSize: '64px', marginBottom: '16px' }}>🚫</div>
          <h1 style={{ margin: '0 0 16px 0', color: '#ef4444' }}>Accès Refusé</h1>
          <p style={{ margin: 0, opacity: 0.8 }}>
            Seuls les administrateurs peuvent accéder au Command Center.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="ultimate-dashboard" style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 100%)',
      color: '#f8fafc',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    }}>
      {/* Header Principal */}
      <div style={{
        background: 'rgba(26, 31, 46, 0.95)',
        backdropFilter: 'blur(20px)',
        borderBottom: '2px solid rgba(59, 130, 246, 0.3)',
        padding: '16px 24px',
        position: 'sticky',
        top: 0,
        zIndex: 100
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          maxWidth: '1600px',
          margin: '0 auto'
        }}>
          {/* Logo et titre */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{
              width: '48px',
              height: '48px',
              background: 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
              borderRadius: '12px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '24px'
            }}>
              🚀
            </div>
            <div>
              <h1 style={{ 
                margin: 0, 
                fontSize: '24px', 
                fontWeight: '700',
                background: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent'
              }}>
                OUPAFAMILLY COMMAND CENTER
              </h1>
              <p style={{ margin: 0, fontSize: '14px', opacity: 0.7 }}>
                Dashboard Ultime v2.0 • Admin: {user?.username}
              </p>
            </div>
          </div>

          {/* Controls */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            {/* Real-time indicator */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '8px 12px',
              background: isRealTimeEnabled ? 'rgba(16, 185, 129, 0.2)' : 'rgba(107, 114, 128, 0.2)',
              borderRadius: '8px',
              fontSize: '14px'
            }}>
              <div style={{
                width: '8px',
                height: '8px',
                borderRadius: '50%',
                background: isRealTimeEnabled ? '#10b981' : '#6b7280',
                animation: isRealTimeEnabled ? 'pulse 2s infinite' : 'none'
              }} />
              {isRealTimeEnabled ? 'LIVE' : 'PAUSED'}
            </div>

            {/* Alerts counter */}
            {alerts?.length > 0 && (
              <div style={{
                position: 'relative',
                padding: '8px 12px',
                background: 'rgba(239, 68, 68, 0.2)',
                borderRadius: '8px',
                fontSize: '14px',
                cursor: 'pointer'
              }}>
                🚨 {alerts.length} alerte{alerts.length > 1 ? 's' : ''}
              </div>
            )}

            {/* Refresh button */}
            <button
              onClick={() => loadSectionData(activeSection)}
              disabled={loading}
              style={{
                padding: '8px 16px',
                background: loading ? 'rgba(107, 114, 128, 0.3)' : 'rgba(59, 130, 246, 0.2)',
                border: '1px solid rgba(59, 130, 246, 0.5)',
                borderRadius: '8px',
                color: '#f8fafc',
                cursor: loading ? 'not-allowed' : 'pointer',
                fontSize: '14px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}
            >
              <span style={{ 
                animation: loading ? 'spin 1s linear infinite' : 'none',
                display: 'inline-block'
              }}>
                🔄
              </span>
              {loading ? 'Chargement...' : 'Actualiser'}
            </button>
          </div>
        </div>
      </div>

      <div style={{ display: 'flex', maxWidth: '1600px', margin: '0 auto' }}>
        {/* Sidebar Navigation */}
        <div style={{
          width: '280px',
          background: 'rgba(30, 35, 50, 0.8)',
          backdropFilter: 'blur(15px)',
          padding: '24px 0',
          borderRight: '1px solid rgba(71, 85, 105, 0.3)',
          minHeight: 'calc(100vh - 84px)',
          position: 'sticky',
          top: '84px'
        }}>
          {dashboardSections.map((section) => (
            <div
              key={section.id}
              onClick={() => setActiveSection(section.id)}
              style={{
                padding: '16px 24px',
                margin: '4px 12px',
                borderRadius: '12px',
                cursor: 'pointer',
                background: activeSection === section.id 
                  ? `linear-gradient(135deg, ${section.color}20, ${section.color}10)`
                  : 'transparent',
                border: activeSection === section.id 
                  ? `1px solid ${section.color}50`
                  : '1px solid transparent',
                transition: 'all 0.3s ease',
                position: 'relative'
              }}
              onMouseEnter={(e) => {
                if (activeSection !== section.id) {
                  e.target.style.background = 'rgba(59, 130, 246, 0.1)';
                }
              }}
              onMouseLeave={(e) => {
                if (activeSection !== section.id) {
                  e.target.style.background = 'transparent';
                }
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <span style={{ fontSize: '20px' }}>{section.icon}</span>
                <div style={{ flex: 1 }}>
                  <div style={{ 
                    fontWeight: '600', 
                    fontSize: '14px',
                    color: activeSection === section.id ? section.color : '#f8fafc'
                  }}>
                    {section.name}
                  </div>
                  <div style={{ 
                    fontSize: '12px', 
                    opacity: 0.7,
                    marginTop: '4px'
                  }}>
                    {section.description}
                  </div>
                </div>
              </div>

              {activeSection === section.id && (
                <div style={{
                  position: 'absolute',
                  left: 0,
                  top: '50%',
                  transform: 'translateY(-50%)',
                  width: '4px',
                  height: '70%',
                  background: section.color,
                  borderRadius: '0 4px 4px 0'
                }} />
              )}
            </div>
          ))}
        </div>

        {/* Main Content */}
        <div style={{ flex: 1, padding: '24px' }}>
          {loading ? (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: '400px',
              flexDirection: 'column',
              gap: '16px'
            }}>
              <div style={{
                width: '48px',
                height: '48px',
                border: '4px solid rgba(59, 130, 246, 0.3)',
                borderTop: '4px solid #3b82f6',
                borderRadius: '50%',
                animation: 'spin 1s linear infinite'
              }} />
              <p style={{ opacity: 0.7 }}>Chargement des données...</p>
            </div>
          ) : (
            <div>
              {/* Section Content sera rendue ici */}
              {activeSection === 'overview' && <OverviewSection data={overviewData} realTime={realTimeData} />}
              {activeSection === 'analytics' && <AnalyticsSection data={analyticsData} />}
              {activeSection === 'users' && <UsersSection data={usersData} />}
              {activeSection === 'content' && <ContentSection data={contentData} />}
              {activeSection === 'tournaments' && <TournamentsSection data={tournamentsData} />}
              {activeSection === 'economy' && <EconomySection data={economyData} />}
              {activeSection === 'system' && <SystemSection data={systemData} />}
              {activeSection === 'moderation' && <ModerationSection />}
              {activeSection === 'integrations' && <IntegrationsSection />}
              {activeSection === 'settings' && <SettingsSection />}
            </div>
          )}
        </div>
      </div>

      {/* Styles globaux */}
      <style jsx>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
        
        .ultimate-dashboard {
          --primary-blue: #3b82f6;
          --primary-blue-dark: #1d4ed8;
          --success-green: #10b981;
          --warning-orange: #f59e0b;
          --error-red: #ef4444;
          --gray-600: #6b7280;
        }
      `}</style>
    </div>
  );
};

// ===================================
// COMPOSANTS DES SECTIONS
// ===================================

// Section Vue d'ensemble
const OverviewSection = ({ data, realTime }) => (
  <div>
    <div style={{ marginBottom: '24px' }}>
      <h2 style={{ 
        margin: '0 0 8px 0', 
        fontSize: '28px', 
        fontWeight: '700',
        background: 'linear-gradient(135deg, #3b82f6, #60a5fa)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent'
      }}>
        📊 Vue d'ensemble globale
      </h2>
      <p style={{ margin: 0, opacity: 0.7 }}>
        Tableau de bord principal avec les métriques clés en temps réel
      </p>
    </div>

    {/* Métriques principales */}
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
      gap: '20px',
      marginBottom: '32px'
    }}>
      {[
        {
          title: 'Utilisateurs en ligne',
          value: realTime?.users_online || 0,
          change: '+5.2%',
          icon: '👥',
          color: '#10b981'
        },
        {
          title: 'Tournois actifs',
          value: realTime?.active_tournaments || 0,
          change: '+12%',
          icon: '🏆',
          color: '#3b82f6'
        },
        {
          title: 'Revenus Premium',
          value: '€2,847',
          change: '+28.5%',
          icon: '💰',
          color: '#f59e0b'
        },
        {
          title: 'Performance système',
          value: '98.2%',
          change: '+0.8%',
          icon: '⚡',
          color: '#06b6d4'
        }
      ].map((metric, index) => (
        <div key={index} style={{
          background: 'rgba(30, 35, 50, 0.6)',
          backdropFilter: 'blur(15px)',
          border: '1px solid rgba(71, 85, 105, 0.3)',
          borderRadius: '16px',
          padding: '24px',
          position: 'relative',
          overflow: 'hidden'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
            <span style={{ fontSize: '24px' }}>{metric.icon}</span>
            <span style={{
              padding: '4px 8px',
              background: `${metric.color}20`,
              color: metric.color,
              borderRadius: '6px',
              fontSize: '12px',
              fontWeight: '600'
            }}>
              {metric.change}
            </span>
          </div>
          <div style={{ fontSize: '32px', fontWeight: '700', marginBottom: '8px' }}>
            {metric.value}
          </div>
          <div style={{ fontSize: '14px', opacity: 0.7 }}>
            {metric.title}
          </div>
          <div style={{
            position: 'absolute',
            bottom: 0,
            left: 0,
            right: 0,
            height: '4px',
            background: `linear-gradient(90deg, ${metric.color}, ${metric.color}80)`
          }} />
        </div>
      ))}
    </div>

    {/* Graphiques et données en temps réel */}
    <div style={{
      display: 'grid',
      gridTemplateColumns: '2fr 1fr',
      gap: '20px'
    }}>
      <div style={{
        background: 'rgba(30, 35, 50, 0.6)',
        border: '1px solid rgba(71, 85, 105, 0.3)',
        borderRadius: '16px',
        padding: '24px'
      }}>
        <h3 style={{ margin: '0 0 16px 0' }}>📈 Activité en temps réel</h3>
        <div style={{ 
          height: '200px', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          background: 'rgba(0,0,0,0.2)',
          borderRadius: '8px'
        }}>
          <p>Graphique d'activité temps réel (à implémenter avec Chart.js)</p>
        </div>
      </div>

      <div style={{
        background: 'rgba(30, 35, 50, 0.6)',
        border: '1px solid rgba(71, 85, 105, 0.3)',
        borderRadius: '16px',
        padding: '24px'
      }}>
        <h3 style={{ margin: '0 0 16px 0' }}>🚨 Alertes récentes</h3>
        <div style={{ maxHeight: '200px', overflowY: 'auto' }}>
          {[
            { type: 'warning', message: 'Pic d\'activité détecté', time: '2 min' },
            { type: 'info', message: 'Nouveau tournoi créé', time: '5 min' },
            { type: 'success', message: 'Sauvegarde réussie', time: '10 min' }
          ].map((alert, index) => (
            <div key={index} style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '12px',
              marginBottom: '8px',
              background: 'rgba(0,0,0,0.2)',
              borderRadius: '8px'
            }}>
              <span>{alert.type === 'warning' ? '⚠️' : alert.type === 'info' ? 'ℹ️' : '✅'}</span>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: '14px' }}>{alert.message}</div>
                <div style={{ fontSize: '12px', opacity: 0.7 }}>Il y a {alert.time}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
);

// Placeholder pour les autres sections
const AnalyticsSection = ({ data }) => (
  <div>
    <h2>📈 Analytics Avancées</h2>
    <p>Section analytics avec graphiques détaillés (à implémenter)</p>
  </div>
);

const UsersSection = ({ data }) => (
  <div>
    <h2>👥 Gestion Utilisateurs</h2>
    <p>Gestion complète des utilisateurs (à implémenter)</p>
  </div>
);

const ContentSection = ({ data }) => (
  <div>
    <h2>📝 Gestion Contenu</h2>
    <p>Gestion des tutoriels et contenus (à implémenter)</p>
  </div>
);

const TournamentsSection = ({ data }) => (
  <div>
    <h2>🏆 Tournois & Compétitions</h2>
    <p>Gestion complète des tournois (à implémenter)</p>
  </div>
);

const EconomySection = ({ data }) => (
  <div>
    <h2>💰 Économie Virtuelle</h2>
    <p>Gestion de l'économie et des abonnements premium (à implémenter)</p>
  </div>
);

const SystemSection = ({ data }) => (
  <div>
    <h2>⚙️ Système & Performance</h2>
    <p>Monitoring système et logs (à implémenter)</p>
  </div>
);

const ModerationSection = () => (
  <div>
    <h2>🛡️ Modération & Sécurité</h2>
    <p>Outils de modération avancés (à implémenter)</p>
  </div>
);

const IntegrationsSection = () => (
  <div>
    <h2>🔗 Intégrations</h2>
    <p>Gestion Discord, Steam et autres APIs (à implémenter)</p>
  </div>
);

const SettingsSection = () => (
  <div>
    <h2>⚙️ Configuration</h2>
    <p>Paramètres globaux de la plateforme (à implémenter)</p>
  </div>
);

export default UltimateDashboard;