import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Header from './components/Header';
import Footer from './components/Footer';
import Accueil from './pages/Accueil';
import Tutoriels from './pages/Tutoriels';
import TutorialDetail from './pages/TutorialDetail';
import Tournois from './pages/Tournois';
import TournamentDetail from './pages/TournamentDetail';
import TournamentBracket from './pages/TournamentBracket';
import Communaute from './pages/Communaute';

import APropos from './pages/APropos';
import News from './pages/News';
import Profil from './pages/Profil';
import AdminDashboard from './pages/AdminDashboard';
import AdminTournaments from './pages/AdminTournaments';
import AdminUsers from './pages/AdminUsers';
import AdminContent from './pages/AdminContent';
import ProfilMembre from './pages/ProfilMembre';
import './App.css';

function App() {
  useEffect(() => {
    // Remove Emergent badge dynamically
    const removeEmergentBadge = () => {
      // Wait a bit for the badge to load
      setTimeout(() => {
        // Find and remove all potential Emergent badges
        const selectors = [
          '[data-testid*="emergent"]',
          '[class*="emergent"]', 
          '[id*="emergent"]',
          'div[style*="position: fixed"][style*="bottom"][style*="right"]',
          'div[style*="position: absolute"][style*="bottom"][style*="right"]',
          'button[style*="position: fixed"]',
          '*[title*="Made with Emergent"]',
          '*[alt*="Made with Emergent"]'
        ];
        
        selectors.forEach(selector => {
          try {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
              const text = element.textContent || element.innerText || '';
              const title = element.title || '';
              const alt = element.alt || '';
              
              if (text.includes('Made with Emergent') || 
                  text.includes('Emergent') || 
                  title.includes('Made with Emergent') ||
                  alt.includes('Made with Emergent') ||
                  element.classList.toString().includes('emergent') ||
                  element.id.includes('emergent')) {
                element.remove();
                console.log('Removed Emergent badge element');
              }
            });
          } catch (e) {
            // Ignore selector errors
          }
        });
        
        // Also try to find elements by text content
        const allElements = document.querySelectorAll('*');
        allElements.forEach(element => {
          const text = element.textContent || '';
          if (text.trim() === 'Made with Emergent' || 
              (text.includes('Made with Emergent') && text.length < 50)) {
            element.remove();
            console.log('Removed Emergent badge by text content');
          }
        });
      }, 500);
    };
    
    // Run immediately and also set up interval to catch dynamically added badges
    removeEmergentBadge();
    const interval = setInterval(removeEmergentBadge, 2000);
    
    // Also run when page visibility changes
    const handleVisibilityChange = () => {
      if (!document.hidden) {
        setTimeout(removeEmergentBadge, 100);
      }
    };
    
    document.addEventListener('visibilitychange', handleVisibilityChange);
    
    return () => {
      clearInterval(interval);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, []);

  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Header />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Accueil />} />
              <Route path="/tutoriels" element={<Tutoriels />} />
              <Route path="/tutoriels/:gameId/:tutorialId" element={<TutorialDetail />} />
              <Route path="/tournois" element={<Tournois />} />
              <Route path="/tournois/:id" element={<TournamentDetail />} />
              <Route path="/tournois/:id/bracket" element={<TournamentBracket />} />
              <Route path="/profil/:memberId" element={<ProfilMembre />} />
              <Route path="/communaute" element={<Communaute />} />
              <Route path="/a-propos" element={<APropos />} />
              <Route path="/news" element={<News />} />
              <Route path="/profil" element={<Profil />} />
              <Route path="/admin" element={<AdminDashboard />} />
              <Route path="/admin/tournaments" element={<AdminTournaments />} />
              <Route path="/admin/users" element={<AdminUsers />} />
              <Route path="/admin/content" element={<AdminContent />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;