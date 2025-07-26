import React, { useState, useEffect, useRef } from 'react';

const NotificationCenter = ({ user }) => {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const dropdownRef = useRef(null);

  // Simuler des notifications (en attendant l'intégration backend)
  const mockNotifications = [
    {
      id: '1',
      type: 'achievement',
      title: '🏆 Nouveau badge obtenu !',
      message: 'Vous avez débloqué le badge "Première Victoire"',
      timestamp: new Date(Date.now() - 5 * 60 * 1000), // Il y a 5 minutes
      read: false,
      icon: '🏆',
      color: '#f59e0b'
    },
    {
      id: '2',
      type: 'tournament',
      title: '🎮 Nouveau tournoi disponible',
      message: 'Tournoi CS2 Elite - Inscriptions ouvertes',
      timestamp: new Date(Date.now() - 30 * 60 * 1000), // Il y a 30 minutes
      read: false,
      icon: '⚡',
      color: '#3b82f6'
    },
    {
      id: '3',
      type: 'social',
      title: '👥 Nouveau membre dans votre équipe',
      message: 'ProGamer2024 a rejoint votre équipe',
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // Il y a 2 heures
      read: true,
      icon: '👤',
      color: '#10b981'
    },
    {
      id: '4',
      type: 'quest',
      title: '⭐ Quête quotidienne terminée',
      message: 'Vous avez gagné 150 coins pour "Guerrier du Week-end"',
      timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000), // Il y a 4 heures
      read: true,
      icon: '⭐',
      color: '#8b5cf6'
    },
    {
      id: '5',
      type: 'system',
      title: '🔄 Mise à jour disponible',
      message: 'Nouvelles fonctionnalités disponibles ! Actualisez la page.',
      timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000), // Il y a 1 jour
      read: true,
      icon: '🚀',
      color: '#6b7280'
    }
  ];

  useEffect(() => {
    // Charger les notifications (pour l'instant, on utilise les mock)
    setNotifications(mockNotifications);
    const unread = mockNotifications.filter(n => !n.read).length;
    setUnreadCount(unread);
  }, []);

  // Fermer le dropdown si on clique à l'extérieur
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const formatTimeAgo = (timestamp) => {
    const now = new Date();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'À l\'instant';
    if (minutes < 60) return `Il y a ${minutes}m`;
    if (hours < 24) return `Il y a ${hours}h`;
    return `Il y a ${days}j`;
  };

  const markAsRead = async (notificationId) => {
    setNotifications(prev => 
      prev.map(n => 
        n.id === notificationId ? { ...n, read: true } : n
      )
    );
    setUnreadCount(prev => Math.max(0, prev - 1));
  };

  const markAllAsRead = async () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })));
    setUnreadCount(0);
  };

  const clearNotification = (notificationId) => {
    setNotifications(prev => prev.filter(n => n.id !== notificationId));
    const notification = notifications.find(n => n.id === notificationId);
    if (notification && !notification.read) {
      setUnreadCount(prev => Math.max(0, prev - 1));
    }
  };

  // Demander permission pour les notifications push
  const requestNotificationPermission = async () => {
    if ('Notification' in window && 'serviceWorker' in navigator) {
      const permission = await Notification.requestPermission();
      if (permission === 'granted') {
        console.log('🔔 Notifications push autorisées');
      }
    }
  };

  useEffect(() => {
    // Demander automatiquement la permission au premier chargement
    if (user && unreadCount > 0) {
      requestNotificationPermission();
    }
  }, [user, unreadCount]);

  const getNotificationTypeColor = (type) => {
    const colors = {
      achievement: '#f59e0b',
      tournament: '#3b82f6', 
      social: '#10b981',
      quest: '#8b5cf6',
      system: '#6b7280',
      default: '#3b82f6'
    };
    return colors[type] || colors.default;
  };

  return (
    <div className="notification-center" ref={dropdownRef}>
      {/* Bell Icon avec badge */}
      <button 
        className="notification-bell"
        onClick={() => setIsOpen(!isOpen)}
        title="Notifications"
        style={{
          position: 'relative',
          background: 'transparent',
          border: 'none',
          cursor: 'pointer',
          padding: '8px',
          borderRadius: '50%',
          color: '#e2e8f0',
          fontSize: '20px',
          transition: 'all 0.3s ease'
        }}
        onMouseEnter={(e) => {
          e.target.style.background = 'rgba(59, 130, 246, 0.2)';
          e.target.style.color = '#3b82f6';
        }}
        onMouseLeave={(e) => {
          e.target.style.background = 'transparent';
          e.target.style.color = '#e2e8f0';
        }}
      >
        🔔
        
        {/* Badge de notifications non lues */}
        {unreadCount > 0 && (
          <span 
            className="notification-badge"
            style={{
              position: 'absolute',
              top: '-2px',
              right: '-2px',
              background: '#ef4444',
              color: 'white',
              borderRadius: '10px',
              padding: '2px 6px',
              fontSize: '11px',
              fontWeight: 'bold',
              minWidth: '18px',
              height: '18px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              animation: unreadCount > 3 ? 'pulse 2s infinite' : 'none'
            }}
          >
            {unreadCount > 99 ? '99+' : unreadCount}
          </span>
        )}
      </button>

      {/* Dropdown des notifications */}
      {isOpen && (
        <div 
          className="notification-dropdown"
          style={{
            position: 'absolute',
            top: '100%',
            right: '0',
            width: '380px',
            maxWidth: '95vw',
            background: 'rgba(30, 35, 50, 0.95)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(71, 85, 105, 0.3)',
            borderRadius: '12px',
            boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
            zIndex: 1000,
            maxHeight: '500px',
            overflow: 'hidden',
            marginTop: '8px'
          }}
        >
          {/* Header */}
          <div 
            className="notification-header"
            style={{
              padding: '16px 20px',
              borderBottom: '1px solid rgba(71, 85, 105, 0.3)',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              background: 'rgba(59, 130, 246, 0.1)'
            }}
          >
            <h3 style={{ 
              margin: 0, 
              color: '#f8fafc', 
              fontSize: '16px',
              fontWeight: '600'
            }}>
              🔔 Notifications {unreadCount > 0 && `(${unreadCount})`}
            </h3>
            
            {unreadCount > 0 && (
              <button
                onClick={markAllAsRead}
                style={{
                  background: 'transparent',
                  border: '1px solid #3b82f6',
                  color: '#3b82f6',
                  padding: '4px 8px',
                  borderRadius: '6px',
                  fontSize: '12px',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease'
                }}
                onMouseEnter={(e) => {
                  e.target.style.background = '#3b82f6';
                  e.target.style.color = 'white';
                }}
                onMouseLeave={(e) => {
                  e.target.style.background = 'transparent';
                  e.target.style.color = '#3b82f6';
                }}
              >
                Tout marquer lu
              </button>
            )}
          </div>

          {/* Liste des notifications */}
          <div 
            className="notification-list"
            style={{
              maxHeight: '400px',
              overflowY: 'auto'
            }}
          >
            {notifications.length === 0 ? (
              <div 
                className="no-notifications"
                style={{
                  padding: '40px 20px',
                  textAlign: 'center',
                  color: '#94a3b8'
                }}
              >
                <div style={{ fontSize: '48px', marginBottom: '16px' }}>📭</div>
                <p>Aucune notification pour le moment</p>
              </div>
            ) : (
              notifications.map((notification) => (
                <div
                  key={notification.id}
                  className="notification-item"
                  style={{
                    padding: '16px 20px',
                    borderBottom: '1px solid rgba(71, 85, 105, 0.2)',
                    background: notification.read ? 'transparent' : 'rgba(59, 130, 246, 0.05)',
                    borderLeft: notification.read ? 'none' : '3px solid #3b82f6',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease',
                    position: 'relative'
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.background = 'rgba(59, 130, 246, 0.1)';
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.background = notification.read ? 'transparent' : 'rgba(59, 130, 246, 0.05)';
                  }}
                  onClick={() => {
                    if (!notification.read) {
                      markAsRead(notification.id);
                    }
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
                    {/* Icône de notification */}
                    <div 
                      style={{
                        width: '40px',
                        height: '40px',
                        borderRadius: '50%',
                        background: `${getNotificationTypeColor(notification.type)}20`,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '20px',
                        flexShrink: 0
                      }}
                    >
                      {notification.icon}
                    </div>

                    <div style={{ flex: 1, minWidth: 0 }}>
                      <h4 style={{
                        margin: '0 0 4px 0',
                        color: '#f8fafc',
                        fontSize: '14px',
                        fontWeight: notification.read ? '500' : '600',
                        lineHeight: '1.4'
                      }}>
                        {notification.title}
                      </h4>
                      
                      <p style={{
                        margin: '0 0 8px 0',
                        color: '#94a3b8',
                        fontSize: '13px',
                        lineHeight: '1.4'
                      }}>
                        {notification.message}
                      </p>
                      
                      <span style={{
                        color: '#64748b',
                        fontSize: '12px'
                      }}>
                        {formatTimeAgo(notification.timestamp)}
                      </span>
                    </div>

                    {/* Bouton supprimer */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        clearNotification(notification.id);
                      }}
                      style={{
                        background: 'transparent',
                        border: 'none',
                        color: '#64748b',
                        cursor: 'pointer',
                        padding: '4px',
                        borderRadius: '4px',
                        fontSize: '14px',
                        opacity: '0.7',
                        transition: 'all 0.3s ease'
                      }}
                      onMouseEnter={(e) => {
                        e.target.style.background = 'rgba(239, 68, 68, 0.2)';
                        e.target.style.color = '#ef4444';
                        e.target.style.opacity = '1';
                      }}
                      onMouseLeave={(e) => {
                        e.target.style.background = 'transparent';
                        e.target.style.color = '#64748b';
                        e.target.style.opacity = '0.7';
                      }}
                      title="Supprimer"
                    >
                      ×
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Footer */}
          {notifications.length > 0 && (
            <div 
              className="notification-footer"
              style={{
                padding: '12px 20px',
                borderTop: '1px solid rgba(71, 85, 105, 0.3)',
                background: 'rgba(59, 130, 246, 0.05)',
                textAlign: 'center'
              }}
            >
              <button
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: '#3b82f6',
                  cursor: 'pointer',
                  fontSize: '13px',
                  fontWeight: '500'
                }}
                onClick={() => {
                  // Naviguer vers une page complète de notifications
                  setIsOpen(false);
                }}
              >
                Voir toutes les notifications
              </button>
            </div>
          )}
        </div>
      )}

      <style jsx>{`
        @keyframes pulse {
          0% {
            transform: scale(1);
          }
          50% {
            transform: scale(1.1);
          }
          100% {
            transform: scale(1);
          }
        }
        
        .notification-list::-webkit-scrollbar {
          width: 6px;
        }
        
        .notification-list::-webkit-scrollbar-track {
          background: rgba(71, 85, 105, 0.1);
          border-radius: 3px;
        }
        
        .notification-list::-webkit-scrollbar-thumb {
          background: rgba(59, 130, 246, 0.5);
          border-radius: 3px;
        }
        
        .notification-list::-webkit-scrollbar-thumb:hover {
          background: rgba(59, 130, 246, 0.7);
        }
      `}</style>
    </div>
  );
};

export default NotificationCenter;