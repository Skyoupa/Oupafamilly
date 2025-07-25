import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Tutoriels = () => {
  const [selectedGame, setSelectedGame] = useState('cs2');

  // Fonction pour convertir le titre en slug URL (améliorée pour gérer les accents français)
  const slugify = (text) => {
    return text
      .toLowerCase()
      .normalize('NFD') // Décomposer les caractères accentués
      .replace(/[\u0300-\u036f]/g, '') // Supprimer les marques diacritiques
      .replace(/[^a-z0-9\s-]/g, '') // Supprimer les caractères spéciaux
      .replace(/\s+/g, '-') // Remplacer les espaces par des tirets
      .replace(/-+/g, '-') // Supprimer les tirets multiples
      .trim();
  };

  const games = [
    {
      id: 'cs2',
      name: 'Counter-Strike 2',
      description: 'FPS Tactique Compétitif',
      color: '#FF6B35',
      backgroundImage: 'https://c4.wallpaperflare.com/wallpaper/361/922/362/counter-strike-2-valve-weapon-men-ultrawide-hd-wallpaper-preview.jpg',
      tutorials: [
        // === NIVEAU DÉBUTANT (15 tutoriels) ===
        { title: 'Interface et contrôles de base', level: 'Débutant', duration: '15 min', type: 'Fundamentals' },
        { title: 'Économie CS2 : comprendre les achats', level: 'Débutant', duration: '20 min', type: 'Economy' },
        { title: 'Mouvement et déplacement optimal', level: 'Débutant', duration: '18 min', type: 'Movement' },
        { title: 'Visée et réglages crosshair', level: 'Débutant', duration: '25 min', type: 'Aiming' },
        { title: 'Présentation des armes principales', level: 'Débutant', duration: '22 min', type: 'Weapons' },
        { title: 'Maps Active Duty : Dust2 basics', level: 'Débutant', duration: '20 min', type: 'Maps' },
        { title: 'Maps Active Duty : Mirage basics', level: 'Débutant', duration: '20 min', type: 'Maps' },
        { title: 'Maps Active Duty : Inferno basics', level: 'Débutant', duration: '20 min', type: 'Maps' },
        { title: 'Utilisation des grenades de base', level: 'Débutant', duration: '18 min', type: 'Utilities' },
        { title: 'Positionnement et angles communs', level: 'Débutant', duration: '17 min', type: 'Positioning' },
        { title: 'Communication team efficace', level: 'Débutant', duration: '15 min', type: 'Communication' },
        { title: 'Rounds d\'échauffement et warm-up', level: 'Débutant', duration: '12 min', type: 'Training' },
        { title: 'Paramètres audio et son directionnel', level: 'Débutant', duration: '14 min', type: 'Settings' },
        { title: 'Gestion du stress et mental game', level: 'Débutant', duration: '16 min', type: 'Mental' },
        { title: 'Routine pré-match et préparation', level: 'Débutant', duration: '13 min', type: 'Preparation' },

        // === NIVEAU INTERMÉDIAIRE (15 tutoriels) ===
        { title: 'Contrôle de recul avancé (AK-47)', level: 'Intermédiaire', duration: '30 min', type: 'Advanced Weapons' },
        { title: 'Contrôle de recul avancé (M4A4/A1-S)', level: 'Intermédiaire', duration: '28 min', type: 'Advanced Weapons' },
        { title: 'Smokes dynamiques et nouvelles mécaniques', level: 'Intermédiaire', duration: '35 min', type: 'Advanced Utilities' },
        { title: 'Flashbangs : timing et coordination', level: 'Intermédiaire', duration: '25 min', type: 'Advanced Utilities' },
        { title: 'Molotovs/HE : contrôle territorial', level: 'Intermédiaire', duration: '22 min', type: 'Advanced Utilities' },
        { title: 'Maps Active Duty : Ancient stratégies', level: 'Intermédiaire', duration: '32 min', type: 'Advanced Maps' },
        { title: 'Maps Active Duty : Nuke verticality', level: 'Intermédiaire', duration: '35 min', type: 'Advanced Maps' },
        { title: 'Maps Active Duty : Overpass contrôle', level: 'Intermédiaire', duration: '30 min', type: 'Advanced Maps' },
        { title: 'Maps Active Duty : Train positioning', level: 'Intermédiaire', duration: '28 min', type: 'Advanced Maps' },
        { title: 'Peek techniques et angle advantage', level: 'Intermédiaire', duration: '27 min', type: 'Advanced Positioning' },
        { title: 'Retakes et post-plant situations', level: 'Intermédiaire', duration: '33 min', type: 'Advanced Tactics' },
        { title: 'Économie avancée et force-buy', level: 'Intermédiaire', duration: '24 min', type: 'Advanced Economy' },
        { title: 'Counter-strafing et movement tech', level: 'Intermédiaire', duration: '26 min', type: 'Advanced Movement' },
        { title: 'Analyse de démos et replay review', level: 'Intermédiaire', duration: '29 min', type: 'Analysis' },
        { title: 'Jeu en équipe et synchronisation', level: 'Intermédiaire', duration: '31 min', type: 'Teamplay' },

        // === NIVEAU EXPERT (15 tutoriels) ===
        { title: 'Meta gaming et adaptation stratégique', level: 'Expert', duration: '45 min', type: 'Professional' },
        { title: 'IGL : In-Game Leadership avancé', level: 'Expert', duration: '50 min', type: 'Leadership' },
        { title: 'Anti-strats et counter-tactical play', level: 'Expert', duration: '42 min', type: 'Counter-Strategy' },
        { title: 'Setups utilitaires complexes (5-stack)', level: 'Expert', duration: '40 min', type: 'Pro Utilities' },
        { title: 'Timing perfection et map control', level: 'Expert', duration: '38 min', type: 'Pro Timing' },
        { title: 'Clutch situations et 1vX scenarios', level: 'Expert', duration: '43 min', type: 'Clutch' },
        { title: 'Psychology warfare et mind games', level: 'Expert', duration: '35 min', type: 'Psychology' },
        { title: 'AWP mastery : sniping pro level', level: 'Expert', duration: '48 min', type: 'AWP Pro' },
        { title: 'Entry fragging et aggressive play', level: 'Expert', duration: '41 min', type: 'Entry' },
        { title: 'Support role et utility distribution', level: 'Expert', duration: '39 min', type: 'Support' },
        { title: 'Lurking et information gathering', level: 'Expert', duration: '37 min', type: 'Lurking' },
        { title: 'Tournament prep et match analysis', level: 'Expert', duration: '52 min', type: 'Tournament' },
        { title: 'Advanced crosshair placement pro', level: 'Expert', duration: '44 min', type: 'Pro Aiming' },
        { title: 'Team chemistry et role specialization', level: 'Expert', duration: '46 min', type: 'Team Dynamics' },
        { title: 'Professional mindset et career path', level: 'Expert', duration: '47 min', type: 'Professional' }
      ]
    },
    {
      id: 'wow',
      name: 'World of Warcraft',
      description: 'MMORPG Stratégique',
      color: '#F4D03F',
      backgroundImage: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHxnYW1pbmd8ZW58MHx8fHwxNzUzMzE0OTQ4fDA&ixlib=rb-4.1.0&q=85',
      tutorials: [
        { title: 'Création et classes', level: 'Débutant', duration: '20 min', type: 'Character' },
        { title: 'Combat et quêtes', level: 'Débutant', duration: '25 min', type: 'Combat' },
        { title: 'Interface et macros', level: 'Débutant', duration: '30 min', type: 'UI' },
        { title: 'Donjons et mécaniques', level: 'Intermédiaire', duration: '35 min', type: 'Dungeons' },
        { title: 'Talents et builds', level: 'Intermédiaire', duration: '30 min', type: 'Builds' },
        { title: 'Professions et craft', level: 'Intermédiaire', duration: '40 min', type: 'Crafting' },
        { title: 'Raids mythiques', level: 'Expert', duration: '60 min', type: 'Raids' },
        { title: 'PvP Arena et RBG', level: 'Expert', duration: '50 min', type: 'PvP' },
        { title: 'Optimisation DPS/HPS', level: 'Expert', duration: '45 min', type: 'Optimization' }
      ]
    },
    {
      id: 'lol',
      name: 'League of Legends',
      description: 'MOBA Esports',
      color: '#3498DB',
      backgroundImage: 'https://images.unsplash.com/photo-1593280359364-5242f1958068?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHw0fHxnYW1pbmd8ZW58MHx8fGJsdWV8MTc1MzM0MTQxMXww&ixlib=rb-4.1.0&q=85',
      tutorials: [
        { title: 'Interface et contrôles', level: 'Débutant', duration: '15 min', type: 'Basics' },
        { title: 'Champions et rôles', level: 'Débutant', duration: '25 min', type: 'Champions' },
        { title: 'Last hit et farming', level: 'Débutant', duration: '20 min', type: 'Farming' },
        { title: 'Vision et warding', level: 'Intermédiaire', duration: '30 min', type: 'Vision' },
        { title: 'Jungle et objectives', level: 'Intermédiaire', duration: '35 min', type: 'Jungle' },
        { title: 'Teamfights positioning', level: 'Intermédiaire', duration: '40 min', type: 'Teamfight' },
        { title: 'Macro game avancé', level: 'Expert', duration: '50 min', type: 'Macro' },
        { title: 'Draft et meta analysis', level: 'Expert', duration: '45 min', type: 'Draft' },
        { title: 'Solo queue climbing', level: 'Expert', duration: '55 min', type: 'Climbing' }
      ]
    },
    {
      id: 'sc2',
      name: 'StarCraft II',
      description: 'RTS Stratégique',
      color: '#9B59B6',
      backgroundImage: 'https://images.unsplash.com/photo-1504370164829-8c6ef0c41d06?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwyfHxnYW1pbmd8ZW58MHx8fGJsdWV8MTc1MzM0MTQxMXww&ixlib=rb-4.1.0&q=85',
      tutorials: [
        { title: 'Les trois races', level: 'Débutant', duration: '25 min', type: 'Races' },
        { title: 'Économie et ressources', level: 'Débutant', duration: '20 min', type: 'Economy' },
        { title: 'Build orders de base', level: 'Débutant', duration: '30 min', type: 'Builds' },
        { title: 'Micro et macro', level: 'Intermédiaire', duration: '40 min', type: 'Control' },
        { title: 'Timings d\'attaque', level: 'Intermédiaire', duration: '35 min', type: 'Timing' },
        { title: 'Scouting efficace', level: 'Intermédiaire', duration: '30 min', type: 'Scouting' },
        { title: 'Builds pro meta', level: 'Expert', duration: '60 min', type: 'Professional' },
        { title: 'APM et vitesse', level: 'Expert', duration: '45 min', type: 'Speed' },
        { title: 'Analyse de replays', level: 'Expert', duration: '50 min', type: 'Analysis' }
      ]
    },
    {
      id: 'minecraft',
      name: 'Minecraft',
      description: 'Créatif & Compétitif',
      color: '#27AE60',
      backgroundImage: 'https://images.unsplash.com/photo-1524685794168-52985e79c1f8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwxfHxNaW5lY3JhZnR8ZW58MHx8fHwxNzUzMzk3Mjg4fDA&ixlib=rb-4.1.0&q=85',
      tutorials: [
        { title: 'Survie première nuit', level: 'Débutant', duration: '20 min', type: 'Survival' },
        { title: 'Crafting et outils', level: 'Débutant', duration: '25 min', type: 'Crafting' },
        { title: 'Construction basics', level: 'Débutant', duration: '30 min', type: 'Building' },
        { title: 'Redstone fundamentals', level: 'Intermédiaire', duration: '45 min', type: 'Redstone' },
        { title: 'Fermes automatiques', level: 'Intermédiaire', duration: '35 min', type: 'Farming' },
        { title: 'Exploration avancée', level: 'Intermédiaire', duration: '40 min', type: 'Exploration' },
        { title: 'Redstone complexe', level: 'Expert', duration: '60 min', type: 'Advanced' },
        { title: 'Architectures monumentales', level: 'Expert', duration: '90 min', type: 'Architecture' },
        { title: 'Mods et customisation', level: 'Expert', duration: '70 min', type: 'Modding' }
      ]
    }
  ];

  const levels = ['Débutant', 'Intermédiaire', 'Expert'];

  const getDifficultyColor = (level) => {
    switch (level) {
      case 'Débutant': return 'difficulty-beginner';
      case 'Intermédiaire': return 'difficulty-intermediate';
      case 'Expert': return 'difficulty-expert';
      default: return 'difficulty-default';
    }
  };

  const filteredTutorials = () => {
    if (selectedGame === 'all') {
      return games.flatMap(game => 
        game.tutorials.map(tutorial => ({
          ...tutorial,
          game: game.name,
          gameId: game.id,
          gameColor: game.color
        }))
      );
    }
    
    const selectedGameData = games.find(g => g.id === selectedGame);
    return selectedGameData ? selectedGameData.tutorials.map(tutorial => ({
      ...tutorial,
      game: selectedGameData.name,
      gameId: selectedGameData.id,
      gameColor: selectedGameData.color
    })) : [];
  };

  return (
    <div className="page-pro">
      {/* Header */}
      <section className="page-header-pro tutorials-header">
        <div className="tutorials-bg">
          <div className="tutorials-overlay"></div>
          <div className="tutorials-pattern"></div>
        </div>
        <div className="container-pro">
          <div className="tutorials-badge">
            <svg className="tutorials-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2L15.09 8.26L22 9L16 14.74L17.18 21.02L12 18.77L6.82 21.02L8 14.74L2 9L8.91 8.26L12 2Z"/>
            </svg>
            <span>GUIDES D'ÉLITE</span>
          </div>
          <h1 className="page-title-pro">TUTORIELS GAMING</h1>
          <p className="page-subtitle-pro">
            Formations professionnelles • Techniques avancées • Progression garantie
          </p>
        </div>
      </section>

      {/* Games Selection */}
      <section className="section-pro">
        <div className="container-pro">
          <div className="section-header-pro">
            <div className="section-badge">
              <span>NOS SPÉCIALITÉS</span>
            </div>
            <h2 className="section-title-pro">Choisissez votre domaine</h2>
            <p className="section-subtitle-pro">5 jeux, expertise garantie à tous les niveaux</p>
          </div>
          
          <div className="games-selection">
            <button 
              className={`game-selector ${selectedGame === 'all' ? 'active' : ''}`}
              onClick={() => setSelectedGame('all')}
            >
              <div className="selector-content">
                <div className="selector-icon all-games">
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M4 6H20V18H4V6M20 4H4C2.89 4 2 4.89 2 6V18C2 19.11 2.89 20 4 20H20C21.11 20 22 19.11 22 18V6C22 4.89 21.11 4 20 4Z"/>
                  </svg>
                </div>
                <div className="selector-text">
                  <h3>TOUS LES JEUX</h3>
                  <p>Vue d'ensemble complète</p>
                </div>
              </div>
            </button>

            {games.map(game => (
              <button 
                key={game.id}
                className={`game-selector ${selectedGame === game.id ? 'active' : ''}`}
                onClick={() => setSelectedGame(game.id)}
              >
                <div 
                  className="selector-gradient"
                  style={{
                    backgroundImage: `url(${game.backgroundImage})`,
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    backgroundRepeat: 'no-repeat'
                  }}
                ></div>
                <div className="selector-content">
                  <div className="selector-info">
                    <h3>{game.name}</h3>
                    <p>{game.description}</p>
                    <span className="tutorial-count">{game.tutorials.length} guides</span>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Game Banner */}
      {selectedGame !== 'all' && (
        <section className="game-banner-section">
          <div className="container-pro">
            {games.filter(game => game.id === selectedGame).map(game => (
              <div key={game.id} className="game-banner">
                <div 
                  className="banner-bg"
                  style={{
                    backgroundImage: `url(${game.backgroundImage})`,
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    backgroundRepeat: 'no-repeat'
                  }}
                >
                  <div className="banner-pattern"></div>
                </div>
                <div className="banner-content">
                  <div className="banner-info">
                    <h2 className="banner-title">{game.name}</h2>
                    <p className="banner-description">{game.description}</p>
                    <div className="banner-stats">
                      <div className="banner-stat">
                        <span className="stat-number">{game.tutorials.length}</span>
                        <span className="stat-label">Tutoriels</span>
                      </div>
                      <div className="banner-stat">
                        <span className="stat-number">{levels.length}</span>
                        <span className="stat-label">Niveaux</span>
                      </div>
                      <div className="banner-stat">
                        <span className="stat-number">PRO</span>
                        <span className="stat-label">Qualité</span>
                      </div>
                    </div>
                  </div>
                  <div className="banner-levels">
                    {levels.map(level => (
                      <div key={level} className="level-indicator">
                        <div className={`level-dot ${getDifficultyColor(level)}`}></div>
                        <span className="level-label">{level}</span>
                        <span className="level-count">
                          ({game.tutorials.filter(t => t.level === level).length})
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Tutorials List */}
      <section className="section-pro section-alt-pro">
        <div className="container-pro">
          <div className="section-header-pro">
            <h2 className="section-title-pro">
              {selectedGame === 'all' 
                ? `Tous les tutoriels (${filteredTutorials().length})`
                : `${games.find(g => g.id === selectedGame)?.name} - ${filteredTutorials().length} guides`
              }
            </h2>
          </div>
          
          <div className="tutorials-grid-pro">
            {filteredTutorials().map((tutorial, index) => (
              <div key={index} className="tutorial-card-pro">
                <div className="tutorial-header-pro">
                  <div className="tutorial-game-info">
                    <span className="game-name-small">{tutorial.game}</span>
                    <span className="tutorial-type">{tutorial.type}</span>
                  </div>
                  <span className={`difficulty-badge-pro ${getDifficultyColor(tutorial.level)}`}>
                    {tutorial.level}
                  </span>
                </div>
                
                <h3 className="tutorial-title-pro">{tutorial.title}</h3>
                
                <div className="tutorial-meta-pro">
                  <div className="meta-item">
                    <svg className="meta-icon" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 2C6.48 2 2 6.48 2 12S6.48 22 12 22 22 17.52 22 12 17.52 2 12 2M15.5 11H13V7H11V13H15.5V11Z"/>
                    </svg>
                    <span>{tutorial.duration}</span>
                  </div>
                  <div className="meta-item">
                    <svg className="meta-icon" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 2L15.09 8.26L22 9L16 14.74L17.18 21.02L12 18.77L6.82 21.02L8 14.74L2 9L8.91 8.26L12 2Z"/>
                    </svg>
                    <span>Guide Pro</span>
                  </div>
                </div>
                
                <div className="tutorial-actions-pro">
                  <Link 
                    to={`/tutoriels/${tutorial.gameId}/${slugify(tutorial.title)}`}
                    className="btn-primary-pro btn-tutorial"
                  >
                    <span>COMMENCER</span>
                    <svg className="btn-icon" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                    </svg>
                  </Link>
                </div>
              </div>
            ))}
          </div>
          
          {filteredTutorials().length === 0 && (
            <div className="no-tutorials-pro">
              <div className="no-tutorials-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2L15.09 8.26L22 9L16 14.74L17.18 21.02L12 18.77L6.82 21.02L8 14.74L2 9L8.91 8.26L12 2Z"/>
                </svg>
              </div>
              <h3>Aucun tutoriel disponible</h3>
              <p>Les guides pour ce jeu arrivent bientôt !</p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default Tutoriels;