import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
const API = `${BACKEND_URL}/api`;

const Accueil = () => {
  const { isAuthenticated, user } = useAuth();

  // Test API connection
  useEffect(() => {
    const testApi = async () => {
      try {
        const response = await axios.get(`${API}/`);
        console.log('API Connected:', response.data.message);
      } catch (error) {
        console.error('API Error:', error);
      }
    };
    testApi();
  }, []);

  const values = [
    {
      icon: (
        <svg className="value-icon-svg" viewBox="0 0 64 64" fill="none">
          <circle cx="32" cy="32" r="28" stroke="currentColor" strokeWidth="3" fill="rgba(59, 130, 246, 0.1)"/>
          <path d="M20 32L28 40L44 24" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      ),
      title: 'Excellence Compétitive',
      description: 'Nous visons l\'excellence dans chaque match, avec un esprit de compétition saine et une progression constante.'
    },
    {
      icon: (
        <svg className="value-icon-svg" viewBox="0 0 64 64" fill="none">
          <rect x="12" y="20" width="40" height="28" rx="4" stroke="currentColor" strokeWidth="3" fill="rgba(59, 130, 246, 0.1)"/>
          <path d="M18 32h28M18 38h20" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          <circle cx="42" cy="35" r="3" fill="currentColor"/>
        </svg>
      ),
      title: 'Stratégie Professionnelle',
      description: 'Chaque membre bénéficie d\'un coaching personnalisé et d\'analyses tactiques approfondies.'
    },
    {
      icon: (
        <svg className="value-icon-svg" viewBox="0 0 64 64" fill="none">
          <circle cx="32" cy="25" r="8" stroke="currentColor" strokeWidth="3" fill="rgba(59, 130, 246, 0.1)"/>
          <path d="M20 45c0-8 5-12 12-12s12 4 12 12" stroke="currentColor" strokeWidth="3"/>
          <path d="M15 52h34" stroke="currentColor" strokeWidth="3" strokeLinecap="round"/>
        </svg>
      ),
      title: 'Esprit Familial',
      description: 'Une communauté soudée où chaque membre compte et contribue au succès collectif.'
    },
    {
      icon: (
        <svg className="value-icon-svg" viewBox="0 0 64 64" fill="none">
          <path d="M32 8L42 22H22L32 8z" stroke="currentColor" strokeWidth="3" fill="rgba(59, 130, 246, 0.1)"/>
          <rect x="22" y="22" width="20" height="20" stroke="currentColor" strokeWidth="3" fill="rgba(59, 130, 246, 0.1)"/>
          <path d="M27 47h10v8h-10z" stroke="currentColor" strokeWidth="3" fill="currentColor"/>
        </svg>
      ),
      title: 'Innovation Gaming',
      description: 'Toujours à la pointe des méta et techniques, nous adaptons constamment nos stratégies.'
    }
  ];

  const games = [
    { 
      name: 'Counter-Strike 2', 
      description: 'FPS Tactique Compétitif',
      status: 'FOCUS PRINCIPAL',
      backgroundImage: 'https://c4.wallpaperflare.com/wallpaper/337/204/15/valve-counter-strike-2-rifles-swat-hd-wallpaper-preview.jpg'
    },
    { 
      name: 'World of Warcraft', 
      description: 'MMORPG Stratégique',
      status: 'ÉQUIPE ACTIVE',
      backgroundImage: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHxnYW1pbmd8ZW58MHx8fHwxNzUzMzE0OTQ4fDA&ixlib=rb-4.1.0&q=85'
    },
    { 
      name: 'League of Legends', 
      description: 'MOBA Esports',
      status: 'ÉQUIPE PRO',
      backgroundImage: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHxnYW1pbmd8ZW58MHx8fHwxNzUzMzE0OTQ4fDA&ixlib=rb-4.1.0&q=85'
    },
    { 
      name: 'StarCraft II', 
      description: 'RTS Compétitif',
      status: 'ÉLITE',
      backgroundImage: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHxnYW1pbmd8ZW58MHx8fHwxNzUzMzE0OTQ4fDA&ixlib=rb-4.1.0&q=85'
    },
    { 
      name: 'Minecraft', 
      description: 'Créatif & Compétitif',
      status: 'COMMUNAUTÉ',
      backgroundImage: 'https://images.unsplash.com/photo-1524685794168-52985e79c1f8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwxfHxNaW5lY3JhZnR8ZW58MHx8fHwxNzUzMzk3Mjg4fDA&ixlib=rb-4.1.0&q=85'
    }
  ];

  return (
    <div className="page-pro">
      {/* Hero Section */}
      <section className="hero-pro">
        <div className="hero-bg-pro">
          <div className="hero-overlay-pro"></div>
          <div className="hero-grid-pattern"></div>
        </div>
        <div className="hero-content-pro">
          <div className="hero-badge">
            <span className="hero-badge-text">ESPORTS COMMUNITY</span>
          </div>
          <h1 className="hero-title-pro">
            <span className="hero-title-line1">BIENVENUE DANS LA</span>
            <span className="hero-title-line2">OUPAFAMILLY</span>
          </h1>
          <p className="hero-subtitle-pro">
            Communauté gaming d'élite où <strong>l'excellence compétitive</strong> rencontre <strong>l'esprit familial</strong>
          </p>
          {isAuthenticated && (
            <div className="welcome-message">
              <p>🎮 Bienvenue, <strong>{user?.username}</strong>!</p>
              {user?.role === 'admin' && (
                <p className="admin-notice">⚡ Vous êtes connecté en tant qu'administrateur</p>
              )}
            </div>
          )}
          <div className="hero-stats">
            <div className="hero-stat">
              <span className="stat-number">150+</span>
              <span className="stat-label">Membres</span>
            </div>
            <div className="hero-stat">
              <span className="stat-number">50+</span>
              <span className="stat-label">Tournois</span>
            </div>
            <div className="hero-stat">
              <span className="stat-number">5</span>
              <span className="stat-label">Jeux Pro</span>
            </div>
          </div>
          <div className="hero-buttons-pro">
            {isAuthenticated ? (
              <Link to="/profil" className="btn-primary-pro">
                <span>MON PROFIL</span>
                <svg className="btn-icon" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                </svg>
              </Link>
            ) : (
              <button 
                className="btn-primary-pro" 
                onClick={() => document.querySelector('.auth-btn.register-btn')?.click()}
              >
                <span>REJOINDRE L'ÉLITE</span>
                <svg className="btn-icon" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            )}
            <Link to="/tournois" className="btn-secondary-pro">
              <span>TOURNOIS CS2</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="section-pro">
        <div className="container-pro">
          <div className="section-header-pro">
            <div className="section-badge">
              <span>NOS VALEURS</span>
            </div>
            <h2 className="section-title-pro">L'ADN Oupafamilly</h2>
            <p className="section-subtitle-pro">Les piliers qui font notre force depuis 2023</p>
          </div>
          <div className="values-grid-pro">
            {values.map((value, index) => (
              <div key={index} className="value-card-pro">
                <div className="value-icon-container">
                  {value.icon}
                </div>
                <h3 className="value-title-pro">{value.title}</h3>
                <p className="value-description-pro">{value.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Games Section */}
      <section className="section-pro section-alt-pro">
        <div className="container-pro">
          <div className="section-header-pro">
            <div className="section-badge">
              <span>NOS DOMAINES</span>
            </div>
            <h2 className="section-title-pro">Excellence Multi-Gaming</h2>
            <p className="section-subtitle-pro">5 jeux, 5 communautés d'élite</p>
          </div>
          <div className="games-grid-pro">
            {games.map((game, index) => (
              <div key={index} className="game-card-pro">
                <div 
                  className="game-background"
                  style={{
                    backgroundImage: `url(${game.backgroundImage})`,
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    backgroundRepeat: 'no-repeat'
                  }}
                ></div>
                <div className="game-content">
                  <div className="game-status">
                    <span className="status-badge">{game.status}</span>
                  </div>
                  <h3 className="game-name-pro">{game.name}</h3>
                  <p className="game-description-pro">{game.description}</p>
                  <div className="game-actions">
                    <button className="game-btn">
                      <span>DÉCOUVRIR</span>
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <div className="section-cta-pro">
            <Link to="/tutoriels" className="btn-primary-pro">
              <span>VOIR TOUS LES TUTORIELS</span>
              <svg className="btn-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section-pro">
        <div className="cta-bg">
          <div className="cta-pattern"></div>
        </div>
        <div className="container-pro">
          <div className="cta-content-pro">
            <div className="cta-badge">
              <span>REJOIGNEZ-NOUS</span>
            </div>
            <h2 className="cta-title-pro">Prêt à faire partie de l'élite ?</h2>
            <p className="cta-subtitle-pro">
              Intégrez une communauté d'exception où talent et passion se rencontrent
            </p>
            <div className="cta-buttons-pro">
              <button 
                className="btn-primary-pro btn-large" 
                onClick={() => {
                  // Emit custom event to open auth modal
                  window.dispatchEvent(new CustomEvent('openAuthModal', { detail: { mode: 'register' } }));
                }}
              >
                <span>NOUS REJOINDRE</span>
                <svg className="btn-icon" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
              <Link to="/a-propos" className="btn-outline-pro">
                <span>NOTRE HISTOIRE</span>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Accueil;