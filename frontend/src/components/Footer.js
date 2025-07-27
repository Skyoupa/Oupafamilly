import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="footer-pro">
      <div className="footer-container-pro">
        <div className="footer-grid-pro">
          {/* Brand Section */}
          <div className="footer-section-pro">
            <div className="footer-brand">
              <div className="footer-logo">
                <div className="logo-shield-footer">
                  <img 
                    src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath d='M50 10 L85 25 L85 65 Q85 80 50 90 Q15 80 15 65 L15 25 Z' fill='%23213547'/%3E%3Ctext x='50' y='55' text-anchor='middle' fill='%23ffffff' font-family='Arial Black' font-size='12' font-weight='bold'%3EOUPA%3C/text%3E%3C/svg%3E" 
                    alt="Oupafamilly Logo" 
                    className="footer-logo-img"
                  />
                  <span className="footer-logo-text">OUPAFAMILLY</span>
                </div>
              </div>
              <p className="footer-description-pro">
                Communauté gaming d'élite depuis 2023. Excellence compétitive, esprit familial, innovation constante.
              </p>
              <div className="social-links-pro">
                <a href="#" className="social-link-pro discord" aria-label="Discord">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03z"/>
                  </svg>
                </a>
                <a href="#" className="social-link-pro twitch" aria-label="Twitch">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M11.571 4.714h1.715v5.143H11.57zm4.715 0H18v5.143h-1.714zM6 0L1.714 4.286v15.428h5.143V24l4.286-4.286h3.428L22.286 12V0zm14.571 11.143l-3.428 3.428h-3.429l-3 3v-3H6.857V1.714h13.714Z"/>
                  </svg>
                </a>
                <a href="#" className="social-link-pro youtube" aria-label="YouTube">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                  </svg>
                </a>
                <a href="#" className="social-link-pro twitter" aria-label="Twitter">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                  </svg>
                </a>
              </div>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="footer-section-pro">
            <h4 className="footer-subtitle-pro">NAVIGATION</h4>
            <ul className="footer-links-pro">
              <li><Link to="/">Accueil</Link></li>
              <li><Link to="/tutoriels">Tutoriels</Link></li>
              <li><Link to="/tournois">Tournois CS2</Link></li>
              <li><Link to="/communaute">Communauté</Link></li>
              <li><Link to="/a-propos">À propos</Link></li>
            </ul>
          </div>

          {/* Games */}
          <div className="footer-section-pro">
            <h4 className="footer-subtitle-pro">NOS JEUX</h4>
            <ul className="footer-links-pro">
              <li><Link to="/tutoriels?game=cs2">Counter-Strike 2</Link></li>
              <li><Link to="/tutoriels?game=wow">World of Warcraft</Link></li>
              <li><Link to="/tutoriels?game=lol">League of Legends</Link></li>
              <li><Link to="/tutoriels?game=sc2">StarCraft II</Link></li>
              <li><Link to="/tutoriels?game=minecraft">Minecraft</Link></li>
            </ul>
          </div>

          {/* Contact & Community */}
          <div className="footer-section-pro">
            <h4 className="footer-subtitle-pro">COMMUNAUTÉ</h4>
            <ul className="footer-links-pro">
              <li><a href="mailto:contact@oupafamilly.com">contact@oupafamilly.com</a></li>
              <li><Link to="/communaute">Serveur Discord</Link></li>
              <li><Link to="/communaute">Chaîne Twitch</Link></li>
              <li><Link to="/communaute">Rejoindre l'élite</Link></li>
            </ul>
          </div>
        </div>

        <div className="footer-bottom-pro">
          <div className="footer-bottom-content">
            <p className="copyright">&copy; 2025 Oupafamilly. Tous droits réservés.</p>
            <div className="footer-bottom-links-pro">
              <a href="#">Conditions d'utilisation</a>
              <a href="#">Politique de confidentialité</a>
              <a href="#">Code de conduite</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;