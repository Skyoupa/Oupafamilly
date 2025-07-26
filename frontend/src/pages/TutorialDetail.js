import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { getEnhancedContent } from '../data/enhancedTutorialContent';
import COMPLETE_PROFESSIONAL_CONTENT from '../data/completeProfessionalContent';
import MASSIVE_PROFESSIONAL_CONTENT_PART2 from '../data/massiveProfessionalContentPart2';
import { BEGINNER_FRIENDLY_CONTENT } from '../data/beginnerFriendlyContent';
import ResourcesHub from '../components/ResourcesHub';

const TutorialDetail = () => {
  const { gameId, tutorialId } = useParams();
  const navigate = useNavigate();
  const [tutorial, setTutorial] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isFavorite, setIsFavorite] = useState(false);
  const [progress, setProgress] = useState(0);
  const [userNotes, setUserNotes] = useState('');
  const [showNotes, setShowNotes] = useState(false);
  const [completedObjectives, setCompletedObjectives] = useState([]);

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
  const API = `${BACKEND_URL}/api`;

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

  useEffect(() => {
    const fetchTutorial = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Récupérer les tutoriels pour le jeu spécifié
        const response = await axios.get(`${API}/content/tutorials?game=${gameId}&limit=100`);
        const tutorials = response.data;
        console.log('Tutoriels récupérés:', tutorials.length);
        console.log('Recherche pour slug:', tutorialId);
        
        // Trouver le tutoriel qui correspond au slug - essayer plusieurs méthodes
        let matchingTutorial = null;
        
        // Méthode 1: Correspondance exacte du slug
        matchingTutorial = tutorials.find(t => slugify(t.title) === tutorialId);
        
        // Méthode 2: Si pas trouvé, essayer avec les slugs des tutoriels
        if (!matchingTutorial) {
          matchingTutorial = tutorials.find(t => {
            const tutorialSlug = slugify(t.title);
            console.log(`Comparaison: "${tutorialSlug}" vs "${tutorialId}"`);
            return tutorialSlug === tutorialId;
          });
        }
        
        // Méthode 3: Recherche partielle (si le slug contient une partie du titre)
        if (!matchingTutorial) {
          matchingTutorial = tutorials.find(t => {
            const tutorialSlug = slugify(t.title);
            return tutorialSlug.includes(tutorialId) || tutorialId.includes(tutorialSlug);
          });
        }
        
        if (matchingTutorial) {
          console.log('Tutoriel trouvé:', matchingTutorial.title);
          
          // Prioriser le contenu enrichi si disponible
          const enhancedContent = getEnhancedContent(tutorialId);
          const professionalContent = COMPLETE_PROFESSIONAL_CONTENT[tutorialId];
          const massiveContent = MASSIVE_PROFESSIONAL_CONTENT_PART2[tutorialId];
          const beginnerContent = BEGINNER_FRIENDLY_CONTENT[tutorialId];
          
          let enrichedTutorial;
          
          // Priorité : Beginner Content (si niveau débutant) > Massive Content > Professional Content > Enhanced Content > Fallback
          if (matchingTutorial.level === 'beginner' && beginnerContent) {
            enrichedTutorial = {
              ...matchingTutorial,
              ...beginnerContent,
              id: matchingTutorial.id,
              author_id: matchingTutorial.author_id,
              created_at: matchingTutorial.created_at,
              views: matchingTutorial.views,
              likes: matchingTutorial.likes
            };
          } else if (massiveContent) {
            enrichedTutorial = {
              ...matchingTutorial,
              ...massiveContent,
              id: matchingTutorial.id,
              author_id: matchingTutorial.author_id,
              created_at: matchingTutorial.created_at,
              views: matchingTutorial.views,
              likes: matchingTutorial.likes
            };
          } else if (professionalContent) {
            enrichedTutorial = {
              ...matchingTutorial,
              ...professionalContent,
              id: matchingTutorial.id,
              author_id: matchingTutorial.author_id,
              created_at: matchingTutorial.created_at,
              views: matchingTutorial.views,
              likes: matchingTutorial.likes
            };
          } else if (enhancedContent) {
            // Utiliser le contenu enrichi professionnel
            enrichedTutorial = {
              ...matchingTutorial,
              ...enhancedContent,
              // Garder l'ID et les métadonnées de l'API
              id: matchingTutorial.id,
              author_id: matchingTutorial.author_id,
              created_at: matchingTutorial.created_at,
              views: matchingTutorial.views,
              likes: matchingTutorial.likes
            };
          } else {
            // Fallback vers le système existant
            const defaultObjectives = [
              'Comprendre les concepts fondamentaux',
              'Appliquer les techniques enseignées',
              'Développer vos compétences de jeu',
              'Améliorer vos performances',
              'Atteindre le niveau suivant'
            ];
            
            const defaultTips = [
              'Pratiquez régulièrement pour progresser',
              'Regardez des démos de joueurs professionnels',
              'Adaptez les techniques à votre style de jeu',
              'Soyez patient, la progression prend du temps',
              'N\'hésitez pas à demander conseil à la communauté'
            ];
            
            const defaultLinks = [
              { name: '📺 Chaîne YouTube Oupafamilly', url: 'https://youtube.com' },
              { name: '💬 Discord Communauté', url: 'https://discord.gg/oupafamilly' },
              { name: '📖 Guide officiel CS2', url: 'https://blog.counter-strike.net' }
            ];
            
            enrichedTutorial = {
              ...matchingTutorial,
              content: matchingTutorial.content,
              objectives: defaultObjectives,
              tips: defaultTips,
              links: defaultLinks,
              image: 'https://c4.wallpaperflare.com/wallpaper/361/922/362/counter-strike-2-valve-weapon-men-ultrawide-hd-wallpaper-preview.jpg',
              level: matchingTutorial.level === 'beginner' ? 'Débutant' : 
                     matchingTutorial.level === 'intermediate' ? 'Intermédiaire' : 
                     matchingTutorial.level === 'expert' ? 'Expert' : matchingTutorial.level,
              duration: (
                matchingTutorial.level === 'beginner' ? '20 min' :
                matchingTutorial.level === 'intermediate' ? '30 min' :
                matchingTutorial.level === 'expert' ? '45 min' : '25 min'
              ),
              type: 'Guide Pro'
            };
          }
          
          setTutorial(enrichedTutorial);
          
          // Charger les données utilisateur depuis localStorage
          loadUserData(enrichedTutorial.id);
        } else {
          console.log('Aucun tutoriel correspondant trouvé');
          setError('Tutoriel non trouvé');
        }
      } catch (err) {
        console.error('Erreur lors du chargement du tutoriel:', err);
        setError('Erreur de chargement');
      } finally {
        setLoading(false);
      }
    };

    if (gameId && tutorialId) {
      fetchTutorial();
    }
  }, [gameId, tutorialId, API]);

  // Fonctions pour gérer les données utilisateur (localStorage)
  const loadUserData = (tutorialId) => {
    const savedFavorites = JSON.parse(localStorage.getItem('oupafamilly_favorites') || '[]');
    const savedProgress = JSON.parse(localStorage.getItem('oupafamilly_progress') || '{}');
    const savedNotes = JSON.parse(localStorage.getItem('oupafamilly_notes') || '{}');
    const savedObjectives = JSON.parse(localStorage.getItem('oupafamilly_objectives') || '{}');
    
    setIsFavorite(savedFavorites.includes(tutorialId));
    setProgress(savedProgress[tutorialId] || 0);
    setUserNotes(savedNotes[tutorialId] || '');
    setCompletedObjectives(savedObjectives[tutorialId] || []);
  };

  const toggleFavorite = () => {
    const favorites = JSON.parse(localStorage.getItem('oupafamilly_favorites') || '[]');
    let newFavorites;
    
    if (isFavorite) {
      newFavorites = favorites.filter(id => id !== tutorial.id);
    } else {
      newFavorites = [...favorites, tutorial.id];
    }
    
    localStorage.setItem('oupafamilly_favorites', JSON.stringify(newFavorites));
    setIsFavorite(!isFavorite);
  };

  const updateProgress = (newProgress) => {
    const progressData = JSON.parse(localStorage.getItem('oupafamilly_progress') || '{}');
    progressData[tutorial.id] = newProgress;
    localStorage.setItem('oupafamilly_progress', JSON.stringify(progressData));
    setProgress(newProgress);
  };

  const saveNotes = () => {
    const notesData = JSON.parse(localStorage.getItem('oupafamilly_notes') || '{}');
    notesData[tutorial.id] = userNotes;
    localStorage.setItem('oupafamilly_notes', JSON.stringify(notesData));
  };

  const toggleObjective = (index) => {
    const newCompleted = completedObjectives.includes(index)
      ? completedObjectives.filter(i => i !== index)
      : [...completedObjectives, index];
    
    setCompletedObjectives(newCompleted);
    
    const objectivesData = JSON.parse(localStorage.getItem('oupafamilly_objectives') || '{}');
    objectivesData[tutorial.id] = newCompleted;
    localStorage.setItem('oupafamilly_objectives', JSON.stringify(objectivesData));
    
    // Mettre à jour le progrès basé sur les objectifs complétés
    const progressPercent = (newCompleted.length / (tutorial.objectives?.length || 5)) * 100;
    updateProgress(Math.round(progressPercent));
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-white text-lg">Chargement du tutoriel professionnel...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="bg-red-900/20 border border-red-500 rounded-lg p-8 max-w-md">
            <h2 className="text-red-400 text-xl font-bold mb-2">❌ Erreur</h2>
            <p className="text-gray-300">{error}</p>
            <button 
              onClick={() => navigate('/tutoriels')}
              className="mt-4 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              Retour aux tutoriels
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!tutorial) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-white text-xl mb-4">Tutoriel non trouvé</h2>
          <button 
            onClick={() => navigate('/tutoriels')}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Retour aux tutoriels
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Header avec image de fond */}
      <div 
        className="relative h-64 bg-cover bg-center bg-gray-800"
        style={{ 
          backgroundImage: `linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url(${tutorial.image})` 
        }}
      >
        <div className="absolute inset-0 flex items-center">
          <div className="container mx-auto px-6">
            <div className="flex items-center justify-between">
              <button
                onClick={() => navigate('/tutoriels')}
                className="bg-gray-800/80 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition-all duration-200 backdrop-blur-sm flex items-center gap-2"
              >
                <span>←</span> Retour aux tutoriels
              </button>
              
              <div className="flex items-center gap-4">
                {/* Bouton Favori */}
                <button
                  onClick={toggleFavorite}
                  className={`p-3 rounded-full transition-all duration-200 backdrop-blur-sm ${
                    isFavorite 
                      ? 'bg-red-600 hover:bg-red-700 text-white' 
                      : 'bg-gray-800/80 hover:bg-gray-700 text-gray-300'
                  }`}
                >
                  {isFavorite ? '❤️' : '🤍'}
                </button>
                
                {/* Indicateur de progression */}
                <div className="bg-gray-800/80 backdrop-blur-sm rounded-lg px-4 py-2">
                  <div className="flex items-center gap-2">
                    <span className="text-white text-sm font-medium">Progression:</span>
                    <div className="w-24 bg-gray-700 rounded-full h-2">
                      <div 
                        className="bg-green-500 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${progress}%` }}
                      ></div>
                    </div>
                    <span className="text-white text-sm font-bold">{progress}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Contenu principal */}
      <div className="container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Colonne principale - Contenu */}
          <div className="lg:col-span-2">
            
            {/* Header du tutoriel */}
            <div className="bg-gray-800 rounded-xl p-6 mb-6 border border-gray-700">
              <div className="flex flex-wrap items-center gap-3 mb-4">
                <span className={`px-3 py-1 rounded-full text-sm font-bold ${
                  tutorial.level === 'Débutant' ? 'bg-green-900 text-green-300' :
                  tutorial.level === 'Intermédiaire' ? 'bg-orange-900 text-orange-300' :
                  'bg-red-900 text-red-300'
                }`}>
                  {tutorial.level?.toUpperCase()}
                </span>
                <span className="bg-blue-900 text-blue-300 px-3 py-1 rounded-full text-sm font-bold">
                  {tutorial.duration}
                </span>
                <span className="bg-purple-900 text-purple-300 px-3 py-1 rounded-full text-sm font-bold">
                  {tutorial.type}
                </span>
              </div>
              
              <h1 className="text-2xl font-bold text-white mb-3 tutorial-title">
                {tutorial.title}
              </h1>
              
              <p className="text-gray-300 text-base leading-relaxed">
                {tutorial.description}
              </p>
            </div>

            {/* Barre d'outils interactive */}
            <div className="bg-gray-800 rounded-xl p-4 mb-6 border border-gray-700">
              <div className="flex flex-wrap items-center gap-4">
                
                {/* Bouton Notes */}
                <button
                  onClick={() => setShowNotes(!showNotes)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-200 ${
                    showNotes 
                      ? 'bg-blue-600 hover:bg-blue-700 text-white' 
                      : 'bg-gray-700 hover:bg-gray-600 text-gray-300'
                  }`}
                >
                  📝 Notes personnelles
                </button>
                
                {/* Contrôles de progression */}
                <div className="flex items-center gap-2">
                  <span className="text-gray-300 text-sm">Progression manuelle:</span>
                  <button
                    onClick={() => updateProgress(Math.max(0, progress - 10))}
                    className="bg-gray-700 hover:bg-gray-600 text-white px-3 py-1 rounded transition-colors"
                  >
                    -10%
                  </button>
                  <button
                    onClick={() => updateProgress(Math.min(100, progress + 10))}
                    className="bg-green-700 hover:bg-green-600 text-white px-3 py-1 rounded transition-colors"
                  >
                    +10%
                  </button>
                  <button
                    onClick={() => updateProgress(100)}
                    className="bg-blue-700 hover:bg-blue-600 text-white px-3 py-1 rounded transition-colors"
                  >
                    Terminé
                  </button>
                </div>
              </div>
              
              {/* Zone de notes */}
              {showNotes && (
                <div className="mt-4 p-4 bg-gray-900 rounded-lg border border-gray-600">
                  <h3 className="text-white font-bold mb-2">📝 Mes notes sur ce tutoriel</h3>
                  <textarea
                    value={userNotes}
                    onChange={(e) => setUserNotes(e.target.value)}
                    onBlur={saveNotes}
                    placeholder="Ajoutez vos notes personnelles, techniques apprises, points à retenir..."
                    className="w-full h-32 bg-gray-800 text-white p-3 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none resize-none"
                  />
                  <p className="text-gray-400 text-xs mt-1">
                    💾 Sauvegarde automatique lors de la perte de focus
                  </p>
                </div>
              )}
            </div>

            {/* Contenu du tutoriel */}
            <div className="bg-gray-800 rounded-xl p-5 border border-gray-700 shadow-lg">
              <div 
                className="tutorial-content prose prose-sm max-w-none"
                style={{ 
                  color: '#f3f4f6',
                  lineHeight: '1.5',
                  fontSize: '14px',
                  fontFamily: 'system-ui, -apple-system, sans-serif'
                }}
                dangerouslySetInnerHTML={{
                  __html: tutorial.content
                    ?.replace(/\n/g, '<br>')
                    ?.replace(/#{1,6}\s(.+)/g, (match, title) => {
                      const level = match.indexOf(' ') - 1;
                      const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4'];
                      // Tailles plus petites et plus professionnelles
                      const fontSize = level === 0 ? '1.15rem' : // H1 plus compact
                                     level === 1 ? '1.05rem' : // H2 plus compact
                                     level === 2 ? '0.95rem' : // H3 plus compact
                                     '0.9rem'; // H4+ petit
                      return `<h${level + 1} style="color: ${colors[level] || '#3b82f6'}; font-weight: 600; margin: 0.8rem 0 0.5rem 0; font-size: ${fontSize}; background: linear-gradient(135deg, ${colors[level] || '#3b82f6'}15, transparent); padding: 0.4rem 0.6rem; border-left: 2px solid ${colors[level] || '#3b82f6'}; border-radius: 4px; font-family: system-ui, -apple-system, sans-serif;">${title}</h${level + 1}>`;
                    })
                    ?.replace(/\*\*(.+?)\*\*/g, '<strong style="color: #fbbf24; background: #fbbf2415; padding: 1px 3px; border-radius: 2px; font-weight: 500; font-size: 14px;">$1</strong>')
                    ?.replace(/\*(.+?)\*/g, '<em style="color: #a78bfa; font-style: italic; background: #a78bfa10; padding: 1px 2px; border-radius: 2px; font-size: 14px;">$1</em>')
                    ?.replace(/```([\s\S]*?)```/g, '<pre style="background: #111827; padding: 0.6rem; border-radius: 0.4rem; border: 1px solid #374151; overflow-x: auto; margin: 0.6rem 0; box-shadow: 0 1px 4px rgba(0,0,0,0.2);"><code style="color: #10b981; font-size: 13px; font-family: Consolas, Monaco, monospace; line-height: 1.3;">$1</code></pre>')
                    ?.replace(/`(.+?)`/g, '<code style="background: #374151; color: #fbbf24; padding: 1px 3px; border-radius: 2px; font-family: Consolas, Monaco, monospace; font-size: 13px; border: 1px solid #4b5563;">$1</code>')
                    ?.replace(/•/g, '<span style="color: #3b82f6; font-weight: 500; margin-right: 6px;">•</span>')
                    ?.replace(/^(\d+\.\s)/gm, '<span style="color: #10b981; font-weight: 500; margin-right: 4px;">$1</span>')
                    ?.replace(/^-\s/gm, '<span style="color: #3b82f6; font-weight: 500; margin-right: 6px;">•</span>')
                    || tutorial.content
                }}
              />
            </div>
          </div>

          {/* Sidebar - Fonctionnalités avancées */}
          <div className="space-y-6">
            
            {/* Objectifs avec checkboxes */}
            {tutorial.objectives && tutorial.objectives.length > 0 && (
              <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                <h3 className="text-white text-lg font-bold mb-4 flex items-center gap-2">
                  🎯 Objectifs d'apprentissage
                </h3>
                <div className="objectives-list space-y-3">
                  {tutorial.objectives.map((objective, index) => (
                    <div key={index} className="flex items-start gap-3">
                      <button
                        onClick={() => toggleObjective(index)}
                        className={`flex-shrink-0 w-5 h-5 rounded border-2 transition-all duration-200 ${
                          completedObjectives.includes(index)
                            ? 'bg-green-600 border-green-600'
                            : 'border-gray-500 hover:border-green-500'
                        }`}
                      >
                        {completedObjectives.includes(index) && (
                          <span className="text-white text-xs flex items-center justify-center h-full">✓</span>
                        )}
                      </button>
                      <span className={`text-sm leading-relaxed transition-colors ${
                        completedObjectives.includes(index)
                          ? 'text-green-300 line-through'
                          : 'text-gray-300'
                      }`}>
                        {objective}
                      </span>
                    </div>
                  ))}
                </div>
                
                <div className="mt-4 p-3 bg-gray-900 rounded-lg">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-400">Progression objectifs:</span>
                    <span className="text-white font-bold">
                      {completedObjectives.length} / {tutorial.objectives.length}
                    </span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
                    <div 
                      className="bg-gradient-to-r from-green-500 to-green-600 h-2 rounded-full transition-all duration-500"
                      style={{ 
                        width: `${(completedObjectives.length / tutorial.objectives.length) * 100}%` 
                      }}
                    ></div>
                  </div>
                </div>
              </div>
            )}

            {/* Conseils Pro */}
            {tutorial.tips && tutorial.tips.length > 0 && (
              <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                <h3 className="text-white text-lg font-bold mb-4 flex items-center gap-2">
                  💡 Conseils Pro
                </h3>
                <div className="space-y-3">
                  {tutorial.tips.map((tip, index) => (
                    <div key={index} className="bg-yellow-900/20 border border-yellow-700/50 rounded-lg p-3">
                      <p className="text-yellow-200 text-sm leading-relaxed">
                        <span className="font-bold text-yellow-400">Tip #{index + 1}:</span> {tip}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Hub Ressources Utiles - Nouveau système professionnel */}
            <ResourcesHub 
              game={gameId} 
              tutorialTitle={tutorial.title}
            />

            {/* Stats du tutoriel */}
            <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
              <h3 className="text-white text-lg font-bold mb-4">📊 Statistiques</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Vues:</span>
                  <span className="text-white font-bold">{tutorial.views || 0}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Likes:</span>
                  <span className="text-white font-bold">{tutorial.likes || 0}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Difficulté:</span>
                  <span className={`font-bold ${
                    tutorial.level === 'Débutant' ? 'text-green-400' :
                    tutorial.level === 'Intermédiaire' ? 'text-orange-400' :
                    'text-red-400'
                  }`}>
                    {tutorial.level}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400">Temps estimé:</span>
                  <span className="text-blue-400 font-bold">{tutorial.duration}</span>
                </div>
              </div>
            </div>

          </div>
        </div>

        {/* Boutons d'action en bas */}
        <div className="mt-8 flex flex-wrap gap-4 justify-center">
          <button
            onClick={() => navigate('/tutoriels')}
            className="bg-gray-700 hover:bg-gray-600 text-white px-6 py-3 rounded-lg transition-colors font-medium"
          >
            ← Retour aux tutoriels
          </button>
          
          <button
            onClick={() => updateProgress(100)}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg transition-colors font-medium"
          >
            ✅ Marquer comme terminé
          </button>
          
          <button
            onClick={toggleFavorite}
            className={`px-6 py-3 rounded-lg transition-colors font-medium ${
              isFavorite
                ? 'bg-red-600 hover:bg-red-700 text-white'
                : 'bg-gray-700 hover:bg-gray-600 text-white'
            }`}
          >
            {isFavorite ? '❤️ Retirer des favoris' : '🤍 Ajouter aux favoris'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default TutorialDetail;