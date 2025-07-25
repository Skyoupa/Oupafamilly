import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import AuthModal from './AuthModal';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [authModalMode, setAuthModalMode] = useState('login');
  const location = useLocation();
  const { user, isAuthenticated, logout } = useAuth();

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
          </nav>

          {/* Auth Section Desktop */}
          <div className="auth-section-desktop">
            {isAuthenticated ? (
              <div className="user-menu">
                <Link to="/profil" className="profile-link">
                  <span className="welcome-text">Salut, {user?.username}!</span>
                </Link>
                {user?.role === 'admin' && (
                  <>
                    <Link to="/admin" className="admin-link">
                      <span className="admin-badge">ADMIN</span>
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