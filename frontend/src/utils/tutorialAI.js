// Système d'Intelligence Artificielle pour recommandations et gamification
// Innovation révolutionnaire pour Oupafamilly

export class TutorialAI {
  constructor() {
    this.userProfile = this.loadUserProfile();
    this.achievements = this.loadAchievements();
    this.skillTree = this.initializeSkillTree();
  }

  // Profil utilisateur basé sur l'IA
  loadUserProfile() {
    const saved = localStorage.getItem('oupafamilly_ai_profile');
    return saved ? JSON.parse(saved) : {
      skillLevel: 'beginner',
      preferredPlayStyle: 'balanced',
      completedTutorials: [],
      timeSpent: 0,
      favoriteMaps: [],
      weakPoints: [],
      strengths: [],
      learningPace: 'normal',
      lastActive: Date.now()
    };
  }

  // Système d'achievements gamifiés
  loadAchievements() {
    const saved = localStorage.getItem('oupafamilly_achievements');
    return saved ? JSON.parse(saved) : {
      unlockedAchievements: [],
      totalPoints: 0,
      level: 1,
      badges: [],
      streaks: {
        dailyPractice: 0,
        perfectScores: 0,
        tutorialCompletion: 0
      }
    };
  }

  // Arbre de compétences révolutionnaire
  initializeSkillTree() {
    return {
      fundamentals: {
        name: 'Fondamentaux',
        icon: '🎯',
        skills: {
          aim: { level: 0, maxLevel: 10, unlocked: true },
          movement: { level: 0, maxLevel: 10, unlocked: true },
          crosshair: { level: 0, maxLevel: 10, unlocked: true }
        }
      },
      weapons: {
        name: 'Maîtrise des Armes',
        icon: '🔫',
        skills: {
          rifles: { level: 0, maxLevel: 10, unlocked: false },
          awp: { level: 0, maxLevel: 10, unlocked: false },
          pistols: { level: 0, maxLevel: 10, unlocked: false }
        }
      },
      tactics: {
        name: 'Tactiques Avancées',
        icon: '🧠',
        skills: {
          positioning: { level: 0, maxLevel: 10, unlocked: false },
          teamwork: { level: 0, maxLevel: 10, unlocked: false },
          igl: { level: 0, maxLevel: 10, unlocked: false }
        }
      },
      professional: {
        name: 'Niveau Professionnel',
        icon: '🏆',
        skills: {
          meta: { level: 0, maxLevel: 10, unlocked: false },
          psychology: { level: 0, maxLevel: 10, unlocked: false },
          championship: { level: 0, maxLevel: 10, unlocked: false }
        }
      }
    };
  }

  // IA de recommandation de tutoriels
  getPersonalizedRecommendations(currentTutorial, allTutorials) {
    const recommendations = [];
    
    // Analyser le profil utilisateur
    const skillLevel = this.userProfile.skillLevel;
    const completed = this.userProfile.completedTutorials;
    const weakPoints = this.userProfile.weakPoints;
    
    // Recommandations basées sur la progression
    if (skillLevel === 'beginner') {
      recommendations.push(...this.getBeginnerPath(allTutorials, completed));
    } else if (skillLevel === 'intermediate') {
      recommendations.push(...this.getIntermediatePath(allTutorials, completed));
    } else {
      recommendations.push(...this.getExpertPath(allTutorials, completed));
    }
    
    // Recommandations pour améliorer les faiblesses
    if (weakPoints.length > 0) {
      recommendations.push(...this.getWeaknessImprovementTutorials(allTutorials, weakPoints));
    }
    
    // Recommandations de suivi logique
    recommendations.push(...this.getLogicalNextSteps(currentTutorial, allTutorials));
    
    return this.rankRecommendations(recommendations).slice(0, 3);
  }

  getLogicalNextSteps(currentTutorial, allTutorials) {
    // Logique simplifiée pour les prochaines étapes
    const currentLevel = currentTutorial?.level?.toLowerCase() || 'beginner';
    
    if (currentLevel === 'beginner') {
      return allTutorials.filter(t => t.level?.toLowerCase() === 'intermediate').slice(0, 2);
    } else if (currentLevel === 'intermediate') {
      return allTutorials.filter(t => t.level?.toLowerCase() === 'expert').slice(0, 2);  
    }
    
    return allTutorials.filter(t => t.level?.toLowerCase() === 'expert').slice(0, 2);
  }

  getWeaknessImprovementTutorials(allTutorials, weakPoints) {
    // Recommandations basées sur les faiblesses identifiées
    return allTutorials.filter(tutorial => {
      const title = tutorial.title?.toLowerCase() || '';
      return weakPoints.some(weakness => title.includes(weakness.toLowerCase()));
    }).slice(0, 2);
  }

  getBeginnerPath(tutorials, completed) {
    const beginnerSequence = [
      'interface-et-controles-de-base',
      'visee-et-reglages-crosshair',
      'mouvement-et-deplacement-optimal',
      'utilisation-des-grenades-de-base',
      'economie-cs2-comprendre-les-achats'
    ];
    
    return tutorials.filter(t => 
      beginnerSequence.includes(this.slugify(t.title)) && 
      !completed.includes(t.id)
    );
  }

  getIntermediatePath(tutorials, completed) {
    const intermediateSequence = [
      'controle-de-recul-avance-ak-47',
      'controle-de-recul-avance-m4a4-a1-s',
      'smokes-dynamiques-et-nouvelles-mecaniques',
      'flashbangs-timing-et-coordination',
      'peek-techniques-et-angle-advantage'
    ];
    
    return tutorials.filter(t => 
      intermediateSequence.includes(this.slugify(t.title)) && 
      !completed.includes(t.id)
    );
  }

  getExpertPath(tutorials, completed) {
    const expertSequence = [
      'meta-gaming-et-adaptation-strategique',
      'igl-in-game-leadership-avance',
      'awp-mastery-sniping-pro-level',
      'psychology-warfare-et-mind-games',
      'professional-mindset-et-career-path'
    ];
    
    return tutorials.filter(t => 
      expertSequence.includes(this.slugify(t.title)) && 
      !completed.includes(t.id)
    );
  }

  // Système d'achievements automatique
  checkAchievements(tutorialCompleted, timeSpent, score) {
    const newAchievements = [];
    
    // Achievement: Premier tutoriel
    if (this.userProfile.completedTutorials.length === 0) {
      newAchievements.push({
        id: 'first_tutorial',
        name: 'Premier Pas',
        description: 'Complétez votre premier tutoriel',
        icon: '🥇',
        points: 100,
        rarity: 'common'
      });
    }
    
    // Achievement: Série de 5 tutoriels
    if (this.userProfile.completedTutorials.length === 4) {
      newAchievements.push({
        id: 'tutorial_streak_5',
        name: 'Apprenant Dédié',
        description: 'Complétez 5 tutoriels',
        icon: '🔥',
        points: 250,
        rarity: 'uncommon'
      });
    }
    
    // Achievement: Score parfait
    if (score >= 95) {
      newAchievements.push({
        id: 'perfect_score',
        name: 'Perfection',
        description: 'Obtenez un score de 95% ou plus',
        icon: '⭐',
        points: 500,
        rarity: 'rare'
      });
    }
    
    // Achievement: Session longue
    if (timeSpent > 3600) { // 1 heure
      newAchievements.push({
        id: 'marathon_session',
        name: 'Marathon',
        description: 'Étudiez pendant plus d\'une heure',
        icon: '🏃‍♂️',
        points: 300,
        rarity: 'uncommon'
      });
    }
    
    // Achievement: Maître AK-47
    if (tutorialCompleted.title.includes('AK-47')) {
      newAchievements.push({
        id: 'ak47_master',
        name: 'Maître AK-47',
        description: 'Maîtrisez le contrôle de recul AK-47',
        icon: '🎯',
        points: 400,
        rarity: 'rare'
      });
    }
    
    return newAchievements;
  }

  // Progression de l'arbre de compétences
  updateSkillTree(tutorialCompleted) {
    const title = tutorialCompleted.title.toLowerCase();
    
    // Mise à jour automatique basée sur le contenu
    if (title.includes('visée') || title.includes('crosshair')) {
      this.skillTree.fundamentals.skills.aim.level += 1;
    }
    
    if (title.includes('mouvement') || title.includes('déplacement')) {
      this.skillTree.fundamentals.skills.movement.level += 1;
    }
    
    if (title.includes('ak-47') || title.includes('m4')) {
      this.skillTree.weapons.skills.rifles.level += 1;
    }
    
    if (title.includes('awp') || title.includes('sniping')) {
      this.skillTree.weapons.skills.awp.level += 1;
    }
    
    if (title.includes('meta') || title.includes('stratégie')) {
      this.skillTree.tactics.skills.positioning.level += 1;
    }
    
    if (title.includes('igl') || title.includes('leadership')) {
      this.skillTree.professional.skills.meta.level += 1;
    }
    
    // Débloquer nouvelles compétences
    this.unlockNewSkills();
    
    // Sauvegarder
    localStorage.setItem('oupafamilly_skill_tree', JSON.stringify(this.skillTree));
  }

  unlockNewSkills() {
    const fundamentalsComplete = Object.values(this.skillTree.fundamentals.skills)
      .every(skill => skill.level >= 3);
    
    if (fundamentalsComplete) {
      Object.values(this.skillTree.weapons.skills).forEach(skill => {
        skill.unlocked = true;
      });
    }
    
    const weaponsComplete = Object.values(this.skillTree.weapons.skills)
      .every(skill => skill.level >= 5);
    
    if (weaponsComplete) {
      Object.values(this.skillTree.tactics.skills).forEach(skill => {
        skill.unlocked = true;
      });
    }
    
    const tacticsComplete = Object.values(this.skillTree.tactics.skills)
      .every(skill => skill.level >= 7);
    
    if (tacticsComplete) {
      Object.values(this.skillTree.professional.skills).forEach(skill => {
        skill.unlocked = true;
      });
    }
  }

  // Analyse intelligente des habitudes d'apprentissage
  analyzeUserBehavior() {
    const sessions = JSON.parse(localStorage.getItem('oupafamilly_sessions') || '[]');
    const now = Date.now();
    const weekAgo = now - (7 * 24 * 60 * 60 * 1000);
    
    const recentSessions = sessions.filter(s => s.timestamp > weekAgo);
    
    return {
      averageSessionLength: this.calculateAverageSessionLength(recentSessions),
      mostActiveTime: this.findMostActiveTime(recentSessions),
      learningPace: this.calculateLearningPace(recentSessions),
      consistency: this.calculateConsistency(recentSessions),
      preferredDifficulty: this.analyzeDifficultyPreference(recentSessions)
    };
  }

  // Prédictions IA avancées
  predictNextBestTutorial(userBehavior, availableTutorials) {
    const weights = {
      difficulty: 0.3,
      duration: 0.2,
      topic: 0.25,
      userProgress: 0.25
    };
    
    return availableTutorials.map(tutorial => ({
      tutorial,
      score: this.calculateTutorialScore(tutorial, userBehavior, weights)
    })).sort((a, b) => b.score - a.score)[0];
  }

  // Utilitaires
  slugify(text) {
    return text
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .trim();
  }

  rankRecommendations(recommendations) {
    return recommendations.sort((a, b) => {
      // Priorité aux tutoriels non complétés
      const aCompleted = this.userProfile.completedTutorials.includes(a.id);
      const bCompleted = this.userProfile.completedTutorials.includes(b.id);
      
      if (aCompleted !== bCompleted) {
        return aCompleted ? 1 : -1;
      }
      
      // Ensuite par niveau approprié
      const userLevel = this.userProfile.skillLevel;
      const aAppropriate = this.isAppropriateLevel(a.level, userLevel);
      const bAppropriate = this.isAppropriateLevel(b.level, userLevel);
      
      if (aAppropriate !== bAppropriate) {
        return aAppropriate ? -1 : 1;
      }
      
      // Enfin par nombre de vues (popularité)
      return (b.views || 0) - (a.views || 0);
    });
  }

  isAppropriateLevel(tutorialLevel, userLevel) {
    const levelMap = { 'beginner': 0, 'intermediate': 1, 'expert': 2 };
    const userLevelNum = levelMap[userLevel] || 0;
    const tutorialLevelNum = levelMap[tutorialLevel?.toLowerCase()] || 0;
    
    // Approprié si c'est le même niveau ou un niveau au-dessus
    return tutorialLevelNum <= userLevelNum + 1;
  }

  // Sauvegarde du profil utilisateur
  saveUserProfile() {
    localStorage.setItem('oupafamilly_ai_profile', JSON.stringify(this.userProfile));
    localStorage.setItem('oupafamilly_achievements', JSON.stringify(this.achievements));
  }
}

// Instance globale de l'IA
export const tutorialAI = new TutorialAI();