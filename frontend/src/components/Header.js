import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import AuthModal from './AuthModal';
import NotificationCenter from './NotificationCenter';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [authModalMode, setAuthModalMode] = useState('login');
  const [userBalance, setUserBalance] = useState(0);
  const location = useLocation();
  const { user, isAuthenticated, logout, API_BASE_URL } = useAuth();
  const { isDarkMode, toggleTheme } = useTheme();

  useEffect(() => {
    const handleOpenAuthModal = (event) => {
      setIsAuthModalOpen(true);
      if (event.detail?.mode === 'register') {
        // If there's a way to set the modal to register mode, do it here
        // For now, just open the modal
      }
    };

    window.addEventListener('openAuthModal', handleOpenAuthModal);
    
    return () => {
      window.removeEventListener('openAuthModal', handleOpenAuthModal);
    };
  }, []);

  useEffect(() => {
    if (isAuthenticated) {
      fetchUserBalance();
    }
  }, [isAuthenticated]);

  const fetchUserBalance = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) return;

      const response = await fetch(`${API_BASE_URL}/currency/balance`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setUserBalance(data.balance || 0);
      }
    } catch (error) {
      console.error('Erreur lors du chargement du solde:', error);
    }
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  const navItems = [
    { path: '/', label: 'ACCUEIL' },
    { path: '/tournois', label: 'TOURNOIS CS2' },
    { path: '/communaute', label: 'COMMUNAUTÉ' },
    { path: '/news', label: 'NEWS' },
    { path: '/tutoriels', label: 'TUTORIELS' },
    { path: '/a-propos', label: 'À PROPOS' }
  ];

  // Economic navigation items for authenticated users
  const economicNavItems = isAuthenticated ? [
    { path: '/communaute?tab=marketplace', label: '🛒 MARKETPLACE' },
    { path: '/communaute?tab=paris', label: '🎲 PARIS' }
  ] : [];

  const handleAuthClick = (mode) => {
    setAuthModalMode(mode);
    setIsAuthModalOpen(true);
    setIsMenuOpen(false);
  };

  const handleLogout = () => {
    logout();
    setIsMenuOpen(false);
  };

  return (
    <>
      <header className="header-pro">
        <div className="header-container-pro">
          <Link to="/" className="logo-pro">
            <div className="logo-shield">
              <img 
                src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath d='M50 10 L85 25 L85 65 Q85 80 50 90 Q15 80 15 65 L15 25 Z' fill='%23213547'/%3E%3Ctext x='50' y='55' text-anchor='middle' fill='%23ffffff' font-family='Arial Black' font-size='12' font-weight='bold'%3EOUPA%3C/text%3E%3C/svg%3E" 
                alt="Oupafamilly Logo" 
                className="logo-img"
              />
              <span className="logo-text-pro">OUPAFAMILLY</span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="nav-desktop-pro">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`nav-link-pro ${isActive(item.path) ? 'active' : ''}`}
              >
                <span className="nav-text">{item.label}</span>
                <span className="nav-underline"></span>
              </Link>
            ))}
            {/* Economic Navigation */}
            {economicNavItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`nav-link-pro economic-nav ${isActive(item.path) ? 'active' : ''}`}
              >
                <span className="nav-text">{item.label}</span>
                <span className="nav-underline"></span>
              </Link>
            ))}
          </nav>

          {/* Auth Section Desktop */}
          <div className="auth-section-desktop">
            {/* Dark Mode Toggle */}
            <button 
              className="theme-toggle-btn" 
              onClick={toggleTheme}
              title={isDarkMode ? 'Passer en mode clair' : 'Passer en mode sombre'}
              aria-label={isDarkMode ? 'Activer le mode clair' : 'Activer le mode sombre'}
            >
              <span className="theme-icon">
                {isDarkMode ? (
                  // Icône soleil pour mode clair
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="5"/>
                    <line x1="12" y1="1" x2="12" y2="3"/>
                    <line x1="12" y1="21" x2="12" y2="23"/>
                    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
                    <line x1="1" y1="12" x2="3" y2="12"/>
                    <line x1="21" y1="12" x2="23" y2="12"/>
                    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
                    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
                  </svg>
                ) : (
                  // Icône lune pour mode sombre
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
                  </svg>
                )}
              </span>
            </button>

            {/* Notification Center - Desktop */}
            {isAuthenticated && (
              <div style={{ position: 'relative' }}>
                <NotificationCenter user={user} />
              </div>
            )}

            {isAuthenticated ? (
              <div className="user-menu">
                {/* Economic Status */}
                <div className="user-economy">
                  <Link to="/communaute" className="balance-link" title="Voir le marketplace">
                    <span className="coin-icon">💰</span>
                    <span className="balance-amount">{userBalance}</span>
                    <span className="balance-label">coins</span>
                  </Link>
                </div>
                
                <Link to="/profil" className="profile-link">
                  <span className="welcome-text">Salut, {user?.username}!</span>
                </Link>
                {user?.role === 'admin' && (
                  <>
                    <Link to="/admin" className="admin-link">
                      <span className="admin-badge">ADMIN</span>
                    </Link>
                    <Link to="/admin/ultimate" className="admin-link">
                      <span className="ultimate-badge">DASHBOARD</span>
                    </Link>
                  </>
                )}
                <button className="logout-btn" onClick={handleLogout}>
                  Déconnexion
                </button>
              </div>
            ) : (
              <div className="auth-buttons">
                <button 
                  className="auth-btn login-btn"
                  onClick={() => handleAuthClick('login')}
                >
                  Connexion
                </button>
                <button 
                  className="auth-btn register-btn"
                  onClick={() => handleAuthClick('register')}
                >
                  Inscription
                </button>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            className="mobile-menu-btn-pro"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            aria-label="Toggle menu"
          >
            <span className={`hamburger-pro ${isMenuOpen ? 'open' : ''}`}>
              <span></span>
              <span></span>
              <span></span>
            </span>
          </button>

          {/* Mobile Navigation */}
          <nav className={`nav-mobile-pro ${isMenuOpen ? 'open' : ''}`}>
            <div className="mobile-nav-content">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`nav-link-mobile-pro ${isActive(item.path) ? 'active' : ''}`}
                  onClick={() => setIsMenuOpen(false)}
                >
                  {item.label}
                </Link>
              ))}
              
              {/* Auth Section Mobile */}
              <div className="auth-section-mobile">
                {/* Dark Mode Toggle Mobile */}
                <div className="theme-toggle-mobile">
                  <button 
                    className="theme-toggle-btn-mobile" 
                    onClick={toggleTheme}
                    title={isDarkMode ? 'Passer en mode clair' : 'Passer en mode sombre'}
                  >
                    <span className="theme-icon-mobile">
                      {isDarkMode ? (
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <circle cx="12" cy="12" r="5"/>
                          <line x1="12" y1="1" x2="12" y2="3"/>
                          <line x1="12" y1="21" x2="12" y2="23"/>
                          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
                          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
                          <line x1="1" y1="12" x2="3" y2="12"/>
                          <line x1="21" y1="12" x2="23" y2="12"/>
                          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
                          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
                        </svg>
                      ) : (
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
                        </svg>
                      )}
                    </span>
                    <span className="theme-text-mobile">
                      {isDarkMode ? 'Mode Clair' : 'Mode Sombre'}
                    </span>
                  </button>
                </div>

                {isAuthenticated ? (
                  <div className="user-menu-mobile">
                    <div className="user-info-mobile">
                      <Link to="/profil" className="profile-link-mobile" onClick={() => setIsMenuOpen(false)}>
                        <span className="welcome-text-mobile">Connecté : {user?.username}</span>
                      </Link>
                      {user?.role === 'admin' && (
                        <Link to="/admin" className="admin-link-mobile" onClick={() => setIsMenuOpen(false)}>
                          <span className="admin-badge-mobile">ADMIN</span>
                        </Link>
                      )}
                    </div>
                    <button className="logout-btn-mobile" onClick={handleLogout}>
                      Déconnexion
                    </button>
                  </div>
                ) : (
                  <div className="auth-buttons-mobile">
                    <button 
                      className="auth-btn-mobile login-btn-mobile"
                      onClick={() => handleAuthClick('login')}
                    >
                      Connexion
                    </button>
                    <button 
                      className="auth-btn-mobile register-btn-mobile"
                      onClick={() => handleAuthClick('register')}
                    >
                      Inscription
                    </button>
                  </div>
                )}
              </div>
            </div>
          </nav>
        </div>
      </header>

      <AuthModal 
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        initialMode={authModalMode}
      />

      <style jsx>{`
        /* Theme Toggle Styles */
        .theme-toggle-btn {
          background: rgba(255, 255, 255, 0.1);
          border: 1px solid rgba(255, 255, 255, 0.2);
          border-radius: 8px;
          padding: 8px;
          cursor: pointer;
          transition: all 0.3s ease;
          display: flex;
          align-items: center;
          justify-content: center;
          min-width: 36px;
          height: 36px;
        }

        .theme-toggle-btn:hover {
          background: rgba(255, 255, 255, 0.2);
          border-color: rgba(255, 255, 255, 0.4);
          transform: translateY(-1px);
        }

        .theme-icon {
          color: #fbbf24;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.3s ease;
        }

        .theme-toggle-btn:hover .theme-icon {
          transform: rotate(15deg);
        }

        .theme-toggle-mobile {
          display: flex;
          justify-content: center;
          margin-bottom: 15px;
          padding-bottom: 15px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .theme-toggle-btn-mobile {
          background: rgba(255, 255, 255, 0.1);
          border: 1px solid rgba(255, 255, 255, 0.2);
          border-radius: 8px;
          padding: 12px 16px;
          cursor: pointer;
          transition: all 0.3s ease;
          display: flex;
          align-items: center;
          gap: 10px;
          color: white;
          font-size: 14px;
          font-weight: 500;
        }

        .theme-toggle-btn-mobile:hover {
          background: rgba(255, 255, 255, 0.2);
          transform: translateY(-1px);
        }

        .theme-icon-mobile {
          color: #fbbf24;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .theme-text-mobile {
          color: white;
        }

        .auth-section-desktop {
          display: flex;
          align-items: center;
          gap: 15px;
        }

        .user-menu {
          display: flex;
          align-items: center;
          gap: 10px;
        }

        .welcome-text {
          color: white;
          font-size: 14px;
          font-weight: 500;
        }

        .profile-link {
          text-decoration: none;
          color: inherit;
          transition: color 0.3s;
        }

        .profile-link:hover {
          color: #93c5fd;
        }

        .profile-link-mobile {
          text-decoration: none;
          color: inherit;
        }

        .admin-badge {
          background: linear-gradient(45deg, #ef4444, #dc2626);
          color: white;
          padding: 2px 8px;
          border-radius: 12px;
          font-size: 10px;
          font-weight: bold;
          text-transform: uppercase;
          text-decoration: none;
          transition: all 0.3s;
        }

        .admin-link {
          text-decoration: none;
        }

        .admin-link:hover .admin-badge {
          background: linear-gradient(45deg, #dc2626, #b91c1c);
          transform: translateY(-1px);
          box-shadow: 0 3px 8px rgba(239, 68, 68, 0.3);
        }

        .logout-btn {
          background: rgba(255, 255, 255, 0.1);
          color: white;
          border: 1px solid rgba(255, 255, 255, 0.3);
          padding: 8px 16px;
          border-radius: 6px;
          cursor: pointer;
          font-size: 14px;
          transition: all 0.3s;
        }

        .logout-btn:hover {
          background: rgba(255, 255, 255, 0.2);
          transform: translateY(-1px);
        }

        .auth-buttons {
          display: flex;
          gap: 10px;
        }

        .auth-btn {
          padding: 8px 16px;
          border-radius: 6px;
          font-size: 14px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.3s;
          border: none;
        }

        .login-btn {
          background: rgba(255, 255, 255, 0.1);
          color: white;
          border: 1px solid rgba(255, 255, 255, 0.3);
        }

        .login-btn:hover {
          background: rgba(255, 255, 255, 0.2);
          transform: translateY(-1px);
        }

        .register-btn {
          background: linear-gradient(45deg, #3b82f6, #1d4ed8);
          color: white;
        }

        .register-btn:hover {
          background: linear-gradient(45deg, #2563eb, #1e40af);
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }

        .auth-section-mobile {
          border-top: 1px solid rgba(255, 255, 255, 0.1);
          padding-top: 20px;
          margin-top: 20px;
        }

        .user-menu-mobile {
          text-align: center;
        }

        .user-info-mobile {
          margin-bottom: 15px;
        }

        .welcome-text-mobile {
          color: white;
          font-size: 14px;
          display: block;
          margin-bottom: 5px;
        }

        .admin-badge-mobile {
          background: linear-gradient(45deg, #ef4444, #dc2626);
          color: white;
          padding: 2px 8px;
          border-radius: 12px;
          font-size: 10px;
          font-weight: bold;
          text-transform: uppercase;
          text-decoration: none;
        }

        .admin-link-mobile {
          text-decoration: none;
        }

        .logout-btn-mobile {
          width: 100%;
          background: rgba(255, 255, 255, 0.1);
          color: white;
          border: 1px solid rgba(255, 255, 255, 0.3);
          padding: 12px;
          border-radius: 6px;
          cursor: pointer;
          font-size: 14px;
        }

        .auth-buttons-mobile {
          display: flex;
          flex-direction: column;
          gap: 10px;
        }

        .auth-btn-mobile {
          width: 100%;
          padding: 12px;
          border-radius: 6px;
          font-size: 14px;
          font-weight: 500;
          cursor: pointer;
          border: none;
        }

        .login-btn-mobile {
          background: rgba(255, 255, 255, 0.1);
          color: white;
          border: 1px solid rgba(255, 255, 255, 0.3);
        }

        .register-btn-mobile {
          background: linear-gradient(45deg, #3b82f6, #1d4ed8);
          color: white;
        }

        @media (max-width: 768px) {
          .auth-section-desktop {
            display: none;
          }
        }

        @media (min-width: 769px) {
          .auth-section-mobile {
            display: none;
          }
        }
      `}</style>
    </>
  );
};

export default Header;