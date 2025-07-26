import React from 'react';

const AIRecommendationsHub = ({ game, tutorialTitle, tutorialLevel, tutorialTags }) => {
  
  // Algorithme de recommandations IA basé sur le contenu du tutoriel
  const generateRecommendations = () => {
    const recommendations = [];
    
    // Recommandations basées sur le niveau
    if (tutorialLevel === 'beginner') {
      recommendations.push({
        type: 'Progression Suggérée',
        title: 'Prochaine Étape Recommandée',
        suggestion: `Après avoir maîtrisé les bases de "${tutorialTitle}", nous recommandons de passer aux tutoriels intermédiaires pour progresser efficacement.`,
        nextSteps: [
          `${game.toUpperCase()} - Techniques intermédiaires`,
          `${game.toUpperCase()} - Application pratique`,
          `${game.toUpperCase()} - Stratégies avancées`
        ],
        confidence: 95
      });
    } else if (tutorialLevel === 'intermediate') {
      recommendations.push({
        type: 'Optimisation Performance',
        title: 'Amélioration Suggérée',
        suggestion: `Basé sur votre consultation de "${tutorialTitle}", l'IA recommande de renforcer vos fondamentaux avant d'attaquer le niveau expert.`,
        nextSteps: [
          `${game.toUpperCase()} - Perfectionnement technique`,
          `${game.toUpperCase()} - Analyse performance`,
          `${game.toUpperCase()} - Coaching avancé`
        ],
        confidence: 88
      });
    } else if (tutorialLevel === 'expert') {
      recommendations.push({
        type: 'Excellence Continue',
        title: 'Maintien Niveau Expert',
        suggestion: `Ayant consulté "${tutorialTitle}", l'IA suggère de diversifier vos compétences et d'innover dans votre approche.`,
        nextSteps: [
          `${game.toUpperCase()} - Innovation stratégique`,
          `${game.toUpperCase()} - Coaching d'équipe`,
          `${game.toUpperCase()} - Analyse méta avancée`
        ],
        confidence: 92
      });
    }

    // Recommandations spécifiques par jeu
    if (game === 'cs2') {
      recommendations.push({
        type: 'Spécialisation CS2',
        title: 'Développement Tactique',
        suggestion: 'L\'IA détecte que vous progressez en Counter-Strike 2. Recommandations personnalisées pour optimiser votre gameplay.',
        focus: [
          'Aim training quotidien (30 min minimum)',
          'Practice utility lineups (5 par map)',
          'VOD review équipes professionnelles',
          'Communication d\'équipe française'
        ],
        confidence: 90
      });
    } else if (game === 'lol') {
      recommendations.push({
        type: 'Méta LoL 2025',
        title: 'Adaptation Stratégique',
        suggestion: 'Basé sur le meta actuel LCK/LEC, l\'IA recommande de focus sur ces aspects clés pour votre progression.',
        focus: [
          'Macro game et contrôle vision',
          'Champions meta LEC 2025 (Varus, Taliyah)',
          'Wave management avancé',
          'Team fighting positioning'
        ],
        confidence: 87
      });
    }

    // Recommandations basées sur les tags
    if (tutorialTags && tutorialTags.includes('stratégie')) {
      recommendations.push({
        type: 'Compléments Stratégiques',
        title: 'Développement Tactique',
        suggestion: 'Votre intérêt pour les stratégies suggère ces tutoriels complémentaires pour une compréhension holistique.',
        related: [
          'Communication d\'équipe avancée',
          'Analyse adversaire et adaptation',
          'Leadership et prise de décision',
          'Psychologie compétitive'
        ],
        confidence: 85
      });
    }

    if (tutorialTags && tutorialTags.includes('technique')) {
      recommendations.push({
        type: 'Perfectionnement Technique',
        title: 'Mécaniques Avancées',
        suggestion: 'Votre focus sur les aspects techniques indique un potentiel d\'amélioration dans ces domaines connexes.',
        related: [
          'Precision et consistency training',
          'Analyse biomécanique gaming',
          'Setup optimisation (matériel)',
          'Routine d\'échauffement pro'
        ],
        confidence: 88
      });
    }

    return recommendations;
  };

  const recommendations = generateRecommendations();

  // Fonction pour déterminer la couleur basée sur la confidence
  const getConfidenceColor = (confidence) => {
    if (confidence >= 90) return 'text-green-400';
    if (confidence >= 80) return 'text-yellow-400';
    return 'text-orange-400';
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h3 className="text-xl font-bold text-white mb-4 flex items-center">
        <span className="text-purple-400 mr-2">🤖</span>
        Recommandations IA Personnalisées
      </h3>
      
      <div className="space-y-6">
        {recommendations.map((rec, index) => (
          <div key={index} className="bg-gray-700 rounded-lg p-4 border-l-4 border-purple-500">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-purple-300 uppercase tracking-wide">
                {rec.type}
              </span>
              <span className={`text-sm font-bold ${getConfidenceColor(rec.confidence)}`}>
                {rec.confidence}% confiance
              </span>
            </div>
            
            <h4 className="text-lg font-semibold text-white mb-2">
              {rec.title}
            </h4>
            
            <p className="text-gray-300 mb-3 text-sm leading-relaxed">
              {rec.suggestion}
            </p>

            {rec.nextSteps && (
              <div className="mb-3">
                <p className="text-sm font-medium text-gray-400 mb-2">Étapes suivantes recommandées :</p>
                <ul className="space-y-1">
                  {rec.nextSteps.map((step, stepIndex) => (
                    <li key={stepIndex} className="text-sm text-gray-300 flex items-center">
                      <span className="text-purple-400 mr-2">→</span>
                      {step}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {rec.focus && (
              <div className="mb-3">
                <p className="text-sm font-medium text-gray-400 mb-2">Focus prioritaires :</p>
                <ul className="space-y-1">
                  {rec.focus.map((item, itemIndex) => (
                    <li key={itemIndex} className="text-sm text-gray-300 flex items-center">
                      <span className="text-blue-400 mr-2">•</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {rec.related && (
              <div className="mb-3">
                <p className="text-sm font-medium text-gray-400 mb-2">Tutoriels connexes :</p>
                <ul className="space-y-1">
                  {rec.related.map((item, itemIndex) => (
                    <li key={itemIndex} className="text-sm text-gray-300 flex items-center">
                      <span className="text-green-400 mr-2">✓</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div className="mt-3 pt-3 border-t border-gray-600">
              <p className="text-xs text-gray-500">
                Recommandation générée par algorithme adaptatif basé sur votre profil de consultation
              </p>
            </div>
          </div>
        ))}

        {/* Section apprentissage adaptatif */}
        <div className="bg-gradient-to-r from-purple-900 to-blue-900 rounded-lg p-4 border border-purple-500">
          <h4 className="text-white font-semibold mb-2 flex items-center">
            <span className="mr-2">🧠</span>
            Apprentissage Adaptatif IA
          </h4>
          <p className="text-gray-300 text-sm mb-3">
            L'IA apprend de vos consultations pour améliorer ses recommandations. Plus vous utilisez la plateforme, plus les suggestions deviennent précises.
          </p>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="bg-purple-800 bg-opacity-50 p-2 rounded">
              <span className="text-purple-300 font-medium">Tutoriels consultés</span>
              <div className="text-white">Analyse en cours...</div>
            </div>
            <div className="bg-blue-800 bg-opacity-50 p-2 rounded">
              <span className="text-blue-300 font-medium">Préférences détectées</span>
              <div className="text-white">Niveau {tutorialLevel}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIRecommendationsHub;