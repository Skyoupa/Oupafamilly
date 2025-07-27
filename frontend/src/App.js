import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
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
import UltimateDashboard from './pages/UltimateDashboard';
import AdminTournaments from './pages/AdminTournaments';
import AdminUsers from './pages/AdminUsers';
import AdminContent from './pages/AdminContent';
import ProfilMembre from './pages/ProfilMembre';
import './App.css';

function App() {
  useEffect(() => {
    // Remove Emergent badge with optimized approach
    const removeEmergentBadge = () => {
      // More targeted selectors to avoid scanning all elements
      const targetSelectors = [
        '[data-testid*="emergent"]',
        '[class*="emergent"]', 
        '[id*="emergent"]',
        '*[title*="Made with Emergent"]',
        '*[alt*="Made with Emergent"]'
      ];
      
      let removed = false;
      targetSelectors.forEach(selector => {
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
              removed = true;
            }
          });
        } catch (e) {
          // Ignore selector errors
        }
      });
      
      // Only scan all elements if targeted approach didn't work
      if (!removed) {
        const textWalker = document.createTreeWalker(
          document.body,
          NodeFilter.SHOW_TEXT,
          {
            acceptNode: function(node) {
              const text = node.textContent.trim();
              return (text === 'Made with Emergent' || 
                     (text.includes('Made with Emergent') && text.length < 50)) 
                     ? NodeFilter.FILTER_ACCEPT 
                     : NodeFilter.FILTER_REJECT;
            }
          }
        );
        
        const nodesToRemove = [];
        let node;
        while ((node = textWalker.nextNode())) {
          nodesToRemove.push(node.parentElement);
        }
        
        nodesToRemove.forEach(element => {
          if (element) {
            element.remove();
            console.log('Removed Emergent badge by text content');
          }
        });
      }
    };
    
    // Use MutationObserver for dynamic content instead of interval
    const observer = new MutationObserver((mutations) => {
      let shouldCheck = false;
      mutations.forEach((mutation) => {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
          shouldCheck = true;
        }
      });
      if (shouldCheck) {
        removeEmergentBadge();
      }
    });
    
    // Start observing
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
    
    // Run once immediately
    removeEmergentBadge();
    
    // Also run when page visibility changes
    const handleVisibilityChange = () => {
      if (!document.hidden) {
        setTimeout(removeEmergentBadge, 100);
      }
    };
    
    document.addEventListener('visibilitychange', handleVisibilityChange);
    
    return () => {
      observer.disconnect();
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, []);

  return (
    <ThemeProvider>
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
                <Route path="/admin/ultimate" element={<UltimateDashboard />} />
                <Route path="/admin/tournaments" element={<AdminTournaments />} />
                <Route path="/admin/users" element={<AdminUsers />} />
                <Route path="/admin/content" element={<AdminContent />} />
              </Routes>
            </main>
            <Footer />
          </div>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;