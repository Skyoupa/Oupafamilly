import React from 'react';
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
import './App.css';

function App() {
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
              <Route path="/communaute" element={<Communaute />} />
              <Route path="/a-propos" element={<APropos />} />
              <Route path="/news" element={<News />} />
              <Route path="/profil" element={<Profil />} />
            <Route path="/profil/:userId" element={<Profil />} />
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