import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import axios from 'axios';

const Tutoriels = () => {
  const [selectedGame, setSelectedGame] = useState('cs2');
  const [tutorials, setTutorials] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const location = useLocation();

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
  const API = `${BACKEND_URL}/api`;

  // Gérer les paramètres de query pour sélectionner le jeu
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const gameParam = params.get('game');
    if (gameParam && ['cs2', 'lol', 'wow', 'sc2', 'minecraft'].includes(gameParam)) {
      setSelectedGame(gameParam);
    }
  }, [location.search]);

  // Fonction pour convertir le titre en slug URL (améliorée pour gérer les accents français)
  const slugify = (text) => {
    return text
      .toLowerCase()
      .normalize('NFD') // Décomposer les caractères accentués
      .replace(/[\u0300-\u036f]/g, '') // Supprimer les marques diacritiques
      .replace(/'/g, ' ') // Remplacer les apostrophes par des espaces
      .replace(/[^a-z0-9\s-]/g, '') // Supprimer les caractères spéciaux
      .replace(/\s+/g, '-') // Remplacer les espaces par des tirets
      .replace(/-+/g, '-') // Supprimer les tirets multiples
      .trim();
  };

  // Load tutorials from API
  useEffect(() => {
    const fetchTutorials = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`${API}/content/tutorials?limit=100`);
        console.log('Tutorials loaded:', response.data.length);
        console.log('First tutorial image:', response.data[0]?.image);
        console.log('First tutorial level:', response.data[0]?.level);
        setTutorials(response.data);
        setError(null);
      } catch (err) {
        console.error('Error loading tutorials:', err);
        setError('Erreur de chargement des tutoriels');
      } finally {
        setLoading(false);
      }
    };

    fetchTutorials();
  }, [API]);

  const games = [
    {
      id: 'cs2',
      name: 'Counter-Strike 2',
      description: 'FPS Tactique Compétitif',
      color: '#FF6B35',
      backgroundImage: 'https://c4.wallpaperflare.com/wallpaper/361/922/362/counter-strike-2-valve-weapon-men-ultrawide-hd-wallpaper-preview.jpg',
    },
    {
      id: 'wow',
      name: 'World of Warcraft',
      description: 'MMORPG Stratégique',
      color: '#F4D03F',
      backgroundImage: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHxnYW1pbmd8ZW58MHx8fHwxNzUzMzE0OTQ4fDA&ixlib=rb-4.1.0&q=85',
    },
    {
      id: 'lol',
      name: 'League of Legends',
      description: 'MOBA Esports',
      color: '#3498DB',
      backgroundImage: 'https://images.unsplash.com/photo-1593280359364-5242f1958068?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHw0fHxnYW1pbmd8ZW58MHx8fGJsdWV8MTc1MzM0MTQxMXww&ixlib=rb-4.1.0&q=85',
    },
    {
      id: 'sc2',
      name: 'StarCraft II',
      description: 'RTS Stratégique',
      color: '#9B59B6',
      backgroundImage: 'https://images.unsplash.com/photo-1504370164829-8c6ef0c41d06?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2Mzl8MHwxfHNlYXJjaHwyfHxnYW1pbmd8ZW58MHx8fGJsdWV8MTc1MzM0MTQxMXww&ixlib=rb-4.1.0&q=85',
    },
    {
      id: 'minecraft',
      name: 'Minecraft',
      description: 'Créatif & Compétitif',
      color: '#27AE60',
      backgroundImage: 'https://images.unsplash.com/photo-1524685794168-52985e79c1f8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwxfHxNaW5lY3JhZnR8ZW58MHx8fHwxNzUzMzk3Mjg4fDA&ixlib=rb-4.1.0&q=85',
    }
  ];

  const levels = ['beginner', 'intermediate', 'expert'];
  const levelDisplayNames = {
    'beginner': 'Débutant',
    'intermediate': 'Intermédiaire', 
    'expert': 'Expert'
  };

  const getDifficultyColor = (level) => {
    switch (level) {
      case 'beginner': return 'difficulty-beginner';
      case 'intermediate': return 'difficulty-intermediate';
      case 'expert': return 'difficulty-expert';
      default: return 'difficulty-default';
    }
  };

  const filteredTutorials = () => {
    if (selectedGame === 'all') {
      return tutorials.map(tutorial => {
        const game = games.find(g => g.id === tutorial.game);
        return {
          ...tutorial,
          gameName: game ? game.name : tutorial.game,
          gameId: tutorial.game,
          gameColor: game ? game.color : '#666',
          levelDisplay: levelDisplayNames[tutorial.level] || tutorial.level,
          // Garder le level original pour les classes CSS
          levelOriginal: tutorial.level
        };
      });
    }
    
    const gameTutorials = tutorials.filter(t => t.game === selectedGame);
    const selectedGameData = games.find(g => g.id === selectedGame);
    
    return gameTutorials.map(tutorial => ({
      ...tutorial,
      gameName: selectedGameData ? selectedGameData.name : tutorial.game,
      gameId: selectedGame,
      gameColor: selectedGameData ? selectedGameData.color : '#666',
      levelDisplay: levelDisplayNames[tutorial.level] || tutorial.level,
      // Garder le level original pour les classes CSS
      levelOriginal: tutorial.level
    }));
  };

  // Get tutorial count per game
  const getGameTutorialCount = (gameId) => {
    return tutorials.filter(t => t.game === gameId).length;
  };

  if (loading) {
    return (
      <div className="page-pro">
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-white text-lg">Chargement des tutoriels professionnels...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-pro">
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="bg-red-900/20 border border-red-500 rounded-lg p-8 max-w-md">
              <h2 className="text-red-400 text-xl font-bold mb-2">❌ Erreur</h2>
              <p className="text-gray-300">{error}</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page-pro">
      {/* Hero Section avec fond dynamique */}
      <div 
        className="relative min-h-screen bg-cover bg-center"
        style={{
          backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.8)), url('${games.find(game => game.id === selectedGame)?.backgroundImage}')`
        }}
      >
        {/* Header Navigation */}
        <div className="absolute top-0 left-0 right-0 z-50">
          <div className="container mx-auto px-6 py-8">
            <div className="flex justify-between items-center">
              <div>
                <h1 className="text-5xl font-bold text-white mb-2 glow-text">
                  🎯 Tutoriels Pro
                </h1>
                <p className="text-xl text-gray-300">
                  Maîtrisez votre jeu avec nos guides professionnels
                </p>
              </div>
              
              <div className="text-right">
                <div className="bg-black/40 backdrop-blur-sm rounded-lg px-6 py-3 border border-orange-500/30">
                  <p className="text-orange-400 font-semibold">
                    📚 {tutorials.length} Tutoriels Professionnels
                  </p>
                  <p className="text-gray-300 text-sm">
                    Contenu enrichi et vérifié
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Sélecteur de jeux */}
        <div className="absolute top-32 left-0 right-0 z-40">
          <div className="container mx-auto px-6">
            <div className="flex justify-center space-x-4 flex-wrap">
              {games.map((game) => (
                <button
                  key={game.id}
                  onClick={() => setSelectedGame(game.id)}
                  className={`px-8 py-4 rounded-lg font-semibold transition-all duration-300 flex items-center space-x-3 mb-4 ${
                    selectedGame === game.id
                      ? 'bg-gradient-to-r from-orange-500 to-orange-600 text-white shadow-lg shadow-orange-500/30 scale-105'
                      : 'bg-black/50 backdrop-blur-sm text-gray-300 hover:bg-black/70 border border-gray-600'
                  }`}
                >
                  <span className="text-2xl">
                    {game.id === 'cs2' ? '🎯' : 
                     game.id === 'wow' ? '🏰' :
                     game.id === 'lol' ? '🏆' :
                     game.id === 'sc2' ? '🚀' :
                     game.id === 'minecraft' ? '🧱' : '🎮'}
                  </span>
                  <div className="text-left">
                    <div>{game.name}</div>
                    <div className="text-xs opacity-75">
                      {getGameTutorialCount(game.id)} tutoriels
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Section principale avec tutoriels */}
        <div className="absolute bottom-0 left-0 right-0 h-2/3 overflow-y-auto">
          <div className="container mx-auto px-6 pb-12">
            
            {/* Header de section avec statistiques */}
            <div className="bg-black/60 backdrop-blur-lg rounded-t-2xl p-8 border-t border-orange-500/30">
              <div className="flex justify-between items-center mb-6">
                <div>
                  <h2 className="text-3xl font-bold text-white mb-2">
                    {games.find(g => g.id === selectedGame)?.name} - Tutoriels Pro
                  </h2>
                  <p className="text-gray-300">
                    {games.find(g => g.id === selectedGame)?.description}
                  </p>
                </div>
                
                <div className="text-right">
                  <div className="bg-orange-500/20 rounded-lg px-4 py-2 border border-orange-500/40">
                    <p className="text-orange-400 font-bold text-lg">
                      {getGameTutorialCount(selectedGame)} tutoriels
                    </p>
                    <p className="text-gray-300 text-sm">disponibles</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Grille des tutoriels */}
            <div className="bg-black/40 backdrop-blur-lg rounded-b-2xl p-8 border border-orange-500/20">
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredTutorials().map((tutorial) => (
                  <div
                    key={tutorial.id}
                    className="group relative bg-gray-900/80 rounded-xl overflow-hidden border border-gray-700 
                               hover:border-orange-500/50 hover:shadow-xl hover:shadow-orange-500/20 
                               hover:scale-105 transition-all duration-300"
                  >
                    {/* Image de tutoriel */}
                    <div className="relative h-48 overflow-hidden">
                      <img
                        src={tutorial.image || '/images/tutorials/gaming_setup.jpg'}
                        alt={tutorial.title}
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                        onError={(e) => {
                          console.log('Image loading error for tutorial:', tutorial.title, 'Image path:', tutorial.image);
                          e.target.src = '/images/tutorials/gaming_setup.jpg';
                        }}
                        onLoad={() => {
                          console.log('Image loaded successfully for tutorial:', tutorial.title);
                        }}
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-transparent to-transparent"></div>
                      
                      {/* Badge niveau */}
                      <div className="absolute top-4 left-4">
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getDifficultyColor(tutorial.levelOriginal || tutorial.level)}`}>
                          {tutorial.levelDisplay || tutorial.level}
                        </span>
                      </div>
                      
                      {/* Badge Pro */}
                      <div className="absolute top-4 right-4">
                        <span className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-2 py-1 rounded-full text-xs font-bold">
                          GUIDE PRO
                        </span>
                      </div>
                    </div>

                    {/* Contenu de la carte */}
                    <div className="p-6">
                      <h3 className="text-xl font-bold text-white mb-3 line-clamp-2 group-hover:text-orange-400 transition-colors">
                        {tutorial.title}
                      </h3>
                      
                      <p className="text-gray-400 mb-4 line-clamp-3 text-sm">
                        {tutorial.description}
                      </p>

                      <div className="flex justify-between items-center">
                        <div className="flex items-center space-x-2 text-gray-400 text-sm">
                          <span>📖</span>
                          <span>Guide professionnel</span>
                        </div>
                        
                        <Link
                          to={`/tutoriels/${tutorial.gameId}/${slugify(tutorial.title)}`}
                          className="bg-gradient-to-r from-orange-500 to-orange-600 text-white px-4 py-2 rounded-lg 
                                   hover:from-orange-600 hover:to-orange-700 transition-all duration-300 
                                   font-semibold text-sm hover:scale-105"
                        >
                          COMMENCER
                        </Link>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Message si aucun tutoriel */}
              {filteredTutorials().length === 0 && (
                <div className="text-center py-12">
                  <div className="text-6xl mb-4">🚧</div>
                  <h3 className="text-2xl font-bold text-gray-300 mb-2">
                    Aucun tutoriel disponible
                  </h3>
                  <p className="text-gray-500">
                    Les tutoriels pour ce jeu arrivent bientôt !
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Tutoriels;