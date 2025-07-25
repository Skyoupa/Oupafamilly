import React, { useState, useEffect } from 'react';
import { tutorialAI } from '../utils/tutorialAI';

const GamificationPanel = ({ tutorial, progress, onTutorialComplete }) => {
  const [achievements, setAchievements] = useState([]);
  const [skillTree, setSkillTree] = useState({});
  const [userLevel, setUserLevel] = useState(1);
  const [totalPoints, setTotalPoints] = useState(0);
  const [showAchievement, setShowAchievement] = useState(null);
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    loadGamificationData();
  }, []);

  const loadGamificationData = () => {
    const savedAchievements = tutorialAI.achievements;
    const savedSkillTree = tutorialAI.skillTree;
    
    setAchievements(savedAchievements.unlockedAchievements || []);
    setSkillTree(savedSkillTree);
    setUserLevel(savedAchievements.level || 1);
    setTotalPoints(savedAchievements.totalPoints || 0);
    
    // Charger les recommandations IA
    const allTutorials = JSON.parse(localStorage.getItem('cached_tutorials') || '[]');
    const recs = tutorialAI.getPersonalizedRecommendations(tutorial, allTutorials);
    setRecommendations(recs);
  };

  const handleTutorialCompletion = (score = 85) => {
    const timeSpent = 1800; // 30 minutes par défaut
    const newAchievements = tutorialAI.checkAchievements(tutorial, timeSpent, score);
    
    // Mise à jour de l'arbre de compétences
    tutorialAI.updateSkillTree(tutorial);
    
    // Afficher les nouveaux achievements
    newAchievements.forEach((achievement, index) => {
      setTimeout(() => {
        setShowAchievement(achievement);
        setTimeout(() => setShowAchievement(null), 3000);
      }, index * 4000);
    });
    
    // Mise à jour du profil
    tutorialAI.userProfile.completedTutorials.push(tutorial.id);
    tutorialAI.achievements.unlockedAchievements.push(...newAchievements);
    tutorialAI.achievements.totalPoints += newAchievements.reduce((sum, a) => sum + a.points, 0);
    tutorialAI.saveUserProfile();
    
    // Rafraîchir les données
    loadGamificationData();
    
    if (onTutorialComplete) {
      onTutorialComplete(newAchievements);
    }
  };

  const getSkillLevelColor = (level, maxLevel) => {
    const percentage = (level / maxLevel) * 100;
    if (percentage >= 80) return 'text-yellow-400';
    if (percentage >= 60) return 'text-blue-400';
    if (percentage >= 40) return 'text-green-400';
    return 'text-gray-400';
  };

  const getSkillBarColor = (level, maxLevel) => {
    const percentage = (level / maxLevel) * 100;
    if (percentage >= 80) return 'bg-gradient-to-r from-yellow-500 to-yellow-600';
    if (percentage >= 60) return 'bg-gradient-to-r from-blue-500 to-blue-600';
    if (percentage >= 40) return 'bg-gradient-to-r from-green-500 to-green-600';
    return 'bg-gradient-to-r from-gray-500 to-gray-600';
  };

  return (
    <div className="space-y-6">
      
      {/* Achievement Popup */}
      {showAchievement && (
        <div className="fixed top-4 right-4 z-50 bg-gradient-to-r from-yellow-400 to-yellow-600 text-black p-4 rounded-lg shadow-2xl animate-bounce">
          <div className="flex items-center gap-3">
            <span className="text-2xl">{showAchievement.icon}</span>
            <div>
              <h3 className="font-bold text-lg">🎉 Achievement Unlocked!</h3>
              <p className="font-medium">{showAchievement.name}</p>
              <p className="text-sm opacity-90">{showAchievement.description}</p>
              <p className="text-xs font-bold">+{showAchievement.points} points</p>
            </div>
          </div>
        </div>
      )}

      {/* Profil Joueur */}
      <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-600 shadow-xl">
        <h3 className="text-white text-xl font-bold mb-4 flex items-center gap-2">
          🎮 Profil Joueur
        </h3>
        
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gradient-to-br from-blue-900/50 to-blue-800/30 rounded-lg p-4 text-center border border-blue-700/50">
            <div className="text-3xl font-bold text-blue-300">{userLevel}</div>
            <div className="text-sm text-blue-200">Niveau</div>
          </div>
          
          <div className="bg-gradient-to-br from-yellow-900/50 to-yellow-800/30 rounded-lg p-4 text-center border border-yellow-700/50">
            <div className="text-3xl font-bold text-yellow-300">{totalPoints}</div>
            <div className="text-sm text-yellow-200">Points XP</div>
          </div>
        </div>

        {/* Barre de progression du niveau */}
        <div className="mt-4">
          <div className="flex justify-between text-sm text-gray-300 mb-2">
            <span className="font-medium">Niveau {userLevel}</span>
            <span className="font-medium">Niveau {userLevel + 1}</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-4 border border-gray-600">
            <div 
              className="bg-gradient-to-r from-blue-500 to-purple-600 h-4 rounded-full transition-all duration-500 relative overflow-hidden"
              style={{ width: `${(totalPoints % 1000) / 10}%` }}
            >
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse"></div>
            </div>
          </div>
          <p className="text-sm text-gray-300 mt-2 font-medium">
            {1000 - (totalPoints % 1000)} XP jusqu'au niveau suivant
          </p>
        </div>
      </div>

      {/* Arbre de Compétences */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-white text-xl font-bold mb-4 flex items-center gap-2">
          🌟 Arbre de Compétences
        </h3>
        
        <div className="space-y-4">
          {Object.entries(skillTree).map(([categoryKey, category]) => (
            <div key={categoryKey} className="bg-gray-900 rounded-lg p-4">
              <h4 className="text-white font-bold mb-3 flex items-center gap-2">
                <span className="text-xl">{category.icon}</span>
                {category.name}
              </h4>
              
              <div className="space-y-2">
                {Object.entries(category.skills).map(([skillKey, skill]) => (
                  <div key={skillKey} className={`p-2 rounded transition-opacity ${
                    skill.unlocked ? 'bg-gray-800' : 'bg-gray-700 opacity-50'
                  }`}>
                    <div className="flex justify-between items-center mb-1">
                      <span className={`text-sm font-medium ${
                        skill.unlocked ? 'text-white' : 'text-gray-500'
                      }`}>
                        {skillKey.charAt(0).toUpperCase() + skillKey.slice(1)}
                      </span>
                      <span className={`text-xs font-bold ${getSkillLevelColor(skill.level, skill.maxLevel)}`}>
                        {skill.level}/{skill.maxLevel}
                      </span>
                    </div>
                    
                    {skill.unlocked && (
                      <div className="w-full bg-gray-600 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full transition-all duration-500 ${getSkillBarColor(skill.level, skill.maxLevel)}`}
                          style={{ width: `${(skill.level / skill.maxLevel) * 100}%` }}
                        ></div>
                      </div>
                    )}
                    
                    {!skill.unlocked && (
                      <div className="text-xs text-gray-500">🔒 Verrouillé</div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Achievements Récents */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-white text-xl font-bold mb-4 flex items-center gap-2">
          🏆 Achievements Récents
        </h3>
        
        {achievements.length > 0 ? (
          <div className="space-y-2">
            {achievements.slice(-3).reverse().map((achievement, index) => (
              <div key={index} className="bg-gray-900 rounded-lg p-3 flex items-center gap-3">
                <span className="text-2xl">{achievement.icon}</span>
                <div className="flex-1">
                  <div className="text-white font-medium">{achievement.name}</div>
                  <div className="text-gray-400 text-sm">{achievement.description}</div>
                </div>
                <div className={`text-xs px-2 py-1 rounded-full ${
                  achievement.rarity === 'rare' ? 'bg-purple-900 text-purple-300' :
                  achievement.rarity === 'uncommon' ? 'bg-blue-900 text-blue-300' :
                  'bg-gray-700 text-gray-300'
                }`}>
                  +{achievement.points} XP
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-gray-400 text-center py-4">
            Complétez votre premier tutoriel pour débloquer des achievements !
          </div>
        )}
      </div>

      {/* Recommandations IA */}
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <h3 className="text-white text-xl font-bold mb-4 flex items-center gap-2">
          🤖 Recommandations IA
        </h3>
        
        {recommendations.length > 0 ? (
          <div className="space-y-3">
            <p className="text-gray-400 text-sm mb-3">
              Basé sur votre progression et style d'apprentissage :
            </p>
            {recommendations.map((rec, index) => (
              <div key={index} className="bg-gray-900 rounded-lg p-3 hover:bg-gray-750 transition-colors cursor-pointer">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-white font-medium">{rec.title}</div>
                    <div className="text-gray-400 text-sm">{rec.level} • {rec.duration || '25 min'}</div>
                  </div>
                  <div className="text-blue-400 text-sm font-bold">
                    Recommandé ✨
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-gray-400 text-center py-4">
            L'IA analyse votre progression pour personnaliser les recommandations...
          </div>
        )}
      </div>

      {/* Bouton de completion pour test */}
      <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
        <button
          onClick={() => handleTutorialCompletion(Math.floor(Math.random() * 20) + 80)}
          className="w-full bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white px-4 py-3 rounded-lg transition-all duration-200 font-medium"
        >
          🎯 Simuler Completion Tutoriel (TEST)
        </button>
      </div>
    </div>
  );
};

export default GamificationPanel;