import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { getEnhancedContent } from '../data/enhancedTutorialContent';

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
          
          let enrichedTutorial;
          
          if (enhancedContent) {
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
            const detailedContent = getDetailedContent(tutorialId);
            
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
              content: detailedContent?.content || matchingTutorial.content,
              objectives: detailedContent?.objectives || defaultObjectives,
              tips: detailedContent?.tips || defaultTips,
              links: detailedContent?.links || defaultLinks,
              image: detailedContent?.image || 'https://c4.wallpaperflare.com/wallpaper/361/922/362/counter-strike-2-valve-weapon-men-ultrawide-hd-wallpaper-preview.jpg',
              level: matchingTutorial.level === 'beginner' ? 'Débutant' : 
                     matchingTutorial.level === 'intermediate' ? 'Intermédiaire' : 
                     matchingTutorial.level === 'expert' ? 'Expert' : matchingTutorial.level,
              duration: detailedContent?.duration || (
                matchingTutorial.level === 'beginner' ? '20 min' :
                matchingTutorial.level === 'intermediate' ? '30 min' :
                matchingTutorial.level === 'expert' ? '45 min' : '25 min'
              ),
              type: detailedContent?.type || 'Guide Pro'
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

  // Fonction pour obtenir le contenu détaillé des tutoriels
  const getDetailedContent = (tutorialSlug) => {
    const detailedContent = {
      
      'interface-et-controles-de-base': {
        title: 'Interface et contrôles de base',
        level: 'Débutant',
        duration: '15 min',
        type: 'Fundamentals',
        description: 'Maîtrisez l\'interface de CS2 et configurez vos contrôles pour une expérience optimale.',
        image: 'https://c4.wallpaperflare.com/wallpaper/337/204/15/valve-counter-strike-2-rifles-swat-hd-wallpaper-preview.jpg',
        objectives: [
          'Comprendre l\'interface utilisateur de CS2',
          'Configurer les contrôles personnalisés optimaux',
          'Optimiser les paramètres graphiques pour la performance',
          'Utiliser le menu d\'achat efficacement',
          'Personnaliser le HUD selon vos besoins'
        ],
        content: `
# 🎮 Interface et contrôles de base de Counter-Strike 2

## 📖 Introduction
Counter-Strike 2 représente l'évolution majeure de la série culte, avec une interface modernisée et des mécaniques affinées. Ce guide complet vous accompagnera dans la maîtrise de tous les aspects fondamentaux du jeu.

## ⌨️ Configuration des contrôles optimaux

### 🏃‍♂️ Mouvement de base
- **WASD** : Déplacement standard (ne jamais modifier)
- **Shift** : Marche silencieuse (recommandé en hold, pas toggle)
- **Ctrl** : S'accroupir (bind custom recommandé pour éviter le crouch-spam)
- **Espace** : Saut (bind supplémentaire sur molette recommandé)

### 🔧 Optimisations recommandées par les pros
1. **Jump bind sur molette** : 
- bind mwheelup +jump
- bind mwheeldown +jump
   - Facilite les bunny hops et jump-peeks

2. **Walk en hold** : Plus de contrôle tactique
- bind shift "+speed"

3. **Crouch optimisé** : 
- bind ctrl "+duck"
   - Éviter le toggle pour un meilleur contrôle

4. **Use bind amélioré** : 
- bind e "+use"
- bind f "+use" (backup)

## 🖥️ Interface utilisateur professionnelle

### 📊 HUD principal
- **Vie et armure** : Affichage en temps réel (position personnalisable)
- **Munitions** : Compteur principal + réserve (style minimal recommandé)
- **Minimap** : Information cruciale (zoom et rotation à optimiser)
- **Timer de round** : Gestion du temps critique (affichage ms recommandé)

### 🛒 Menu d'achat professionnel
**Raccourcis essentiels :**
- **B** : Ouvrir le menu d'achat
- **Achats rapides recommandés :**
- bind f1 "buy ak47; buy m4a1"
- bind f2 "buy awp"
- bind f3 "buy hegrenade"
- bind f4 "buy flashbang"
- bind f5 "buy smokegrenade"

## 🎯 Paramètres optimaux pour la compétition

### 🖼️ Graphiques pro
- **Résolution** : 1920x1080 (standard compétitif)
- **Aspect ratio** : 16:9 (vision maximale)
- **FPS** : Priorité fluidité (fps_max 400+)
- **Paramètres bas** : Avantage compétitif (moins de distractions visuelles)

### 🌐 Réseau optimal
- **Rate** : 786432 (connexion optimale)
- **cl_interp_ratio** : 1 (interpolation standard)
- **cl_updaterate** : 128 (tick rate compétitif)
- **cl_cmdrate** : 128 (commandes par seconde)

### 🔊 Audio professionnel
- **snd_headphone_pan_exponent** : 2.0
- **snd_front_headphone_position** : 43.2
- **snd_rear_headphone_position** : 90.0
- **Casque de qualité essentiel** : Position directionnelle précise

## 💡 Crosshair professionnel
**Configuration recommandée :**
cl_crosshair_drawoutline 1
cl_crosshair_outlinethickness 1
cl_crosshairsize 2
cl_crosshairthickness 1
cl_crosshairdot 0
cl_crosshairgap -2
cl_crosshaircolor 5
cl_crosshaircolor_r 0
cl_crosshaircolor_g 255
cl_crosshaircolor_b 255

## 🏆 Conseils de pros
1. **Autoexec.cfg** : Créez un fichier de configuration automatique
2. **Backup configs** : Sauvegardez toujours vos paramètres
3. **Test progressif** : Ne changez pas tout d'un coup
4. **Muscle memory** : 10,000 heures pour la maîtrise parfaite
5. **Cohérence** : Gardez les mêmes settings sur tous les PC

## 📚 Commandes console essentielles
- fps_max 400 : Limite FPS
- net_graph 1 : Affichage des stats réseau
- cl_showfps 1 : Compteur FPS
- developer 1 : Mode développeur pour debug
        `,
        links: [
          { name: '🎯 Guide configs pro Liquipedia', url: 'https://liquipedia.net/counterstrike/List_of_player_binds' },
          { name: '⚙️ Paramètres des pros', url: 'https://prosettings.net/counterstrike/' },
          { name: '🔧 Autoexec generator', url: 'https://www.tobyscs.com/autoexec-generator/' }
        ],
        tips: [
          'Créez un autoexec.cfg dans le dossier cfg pour automatiser vos paramètres',
          'Testez vos nouveaux binds en mode bot avant les matchs compétitifs',
          'La cohérence est plus importante que la perfection - gardez vos settings',
          'fps_max 400 minimum pour éviter les micro-stutters'
        ]
      },

      'economie-cs2-comprendre-les-achats': {
        title: 'Économie CS2 : comprendre les achats',
        level: 'Débutant',
        duration: '20 min',
        type: 'Economy',
        description: 'Maîtrisez l\'économie de CS2 pour optimiser vos achats et dominer la gestion financière.',
        image: 'https://c4.wallpaperflare.com/wallpaper/361/922/362/counter-strike-2-valve-weapon-men-ultrawide-hd-wallpaper-preview.jpg',
        objectives: [
          'Comprendre le système économique complet de CS2',
          'Maîtriser les coûts et priorités d\'achat',
          'Gérer les rounds d\'économie et force-buy stratégiques',
          'Coordonner les achats en équipe efficacement',
          'Anticiper l\'économie adverse'
        ],
        content: `
# 💰 Économie CS2 : Maîtrise complète du système financier

## 📈 Bases de l'économie avancée

### 💵 Gain d'argent par round (mise à jour 2025)
**Victoires :**
- **Élimination de tous les ennemis** : $3250
- **Défusion de bombe** : $3250 + $300 bonus
- **Temps écoulé (CT)** : $3250

**Défaites avec bonus progressif :**
- **1ère défaite** : $1400
- **2ème défaite consécutive** : $1900
- **3ème défaite consécutive** : $2400
- **4ème défaite consécutive** : $2900
- **5ème défaite+ consécutive** : $3400 (maximum)

**Éliminations :**
- **Kill standard** : $300
- **Kill au couteau** : $1500
- **Kill grenade HE** : $300
- **Assist** : $100

### 🎯 Objectifs bonus
- **Pose de bombe** : +$800 (même en défaite)
- **Défusion de bombe** : +$300
- **Sauvetage d'otage** : +$1000

## 🛒 Coûts des équipements (guide complet)

### 🔫 Armes principales
**Fusils d'assaut :**
- **AK-47** : $2700 (Terroristes) - Damage: 147 head
- **M4A4** : $3100 (CT) - Damage: 140 head
- **M4A1-S** : $2900 (CT) - Damage: 140 head, silencieux
- **Galil AR** : $2000 (T) - Économique, précis
- **FAMAS** : $2050 (CT) - Burst mode efficace

**Fusils de sniper :**
- **AWP** : $4750 - One-shot kill body/head
- **SSG 08 (Scout)** : $1700 - Mobile, économique
- **SCAR-20** : $5000 (CT) - Auto-sniper
- **G3SG1** : $5000 (T) - Auto-sniper

**SMG (Sub-Machine Guns) :**
- **MP9** : $1250 (CT) - Mobile, kill reward +$600
- **MAC-10** : $1050 (T) - Spray control facile
- **UMP-45** : $1200 - Polyvalent, armor pen
- **P90** : $2350 - Anti-eco destructeur

### 🔫 Armes secondaires
- **Desert Eagle** : $700 - High damage potential
- **Glock-18** : Gratuit (T) - Burst mode, precision
- **USP-S** : Gratuit (CT) - Silencieux, précis
- **P2000** : Gratuit (CT) - Alternative USP
- **Tec-9** : $500 (T) - Spam potential
- **Five-SeveN** : $500 (CT) - Armor penetration
- **P250** : $300 - Anti-eco efficace
- **CZ75-Auto** : $500 - Auto-pistol

### 🛡️ Équipement
- **Kevlar** : $650 - 50% réduction dégâts body
- **Kevlar + Casque** : $1000 - Protection head essentielle
- **Kit de désamorçage** : $400 (CT seulement) - 5→3 secondes

### 💣 Grenades (utilitaires tactiques)
- **HE Grenade** : $300 - 57 dégâts maximum
- **Flashbang** : $200 - Aveugle 3-5 secondes
- **Smoke** : $300 - Bloque vision 18 secondes
- **Incendiary** : $600 (CT) - Zone denial 7 secondes
- **Molotov** : $400 (T) - Équivalent incendiary
- **Decoy** : $50 - Fake radar signals

## 📊 Stratégies économiques avancées

### 💪 Full-buy rounds (achat complet)
**Argent minimum requis :**
- **Joueur standard** : $4500-5000
- **AWPer** : $6000-6500
- **Support** : $4000-4500

**Priorités d'achat optimales :**
1. **Arme principale** (rifle/AWP)
2. **Armure complète** (kevlar+casque)
3. **Utilities** (smoke+flash minimum)
4. **Arme secondaire** si budget disponible
5. **Grenade HE** en surplus

### 🪙 Eco rounds (économie)
**Objectifs :**
- **Économiser** pour full-buy suivant
- **Stack money** pour 2-3 rounds
- **Force damage** si possible

**Achats eco intelligents :**
- **Armor only** : $650-1000 selon situation
- **P250 + armor** : $950-1300 (anti-rush)
- **Scout + armor** : $2700 (eco AWP)
- **Utilities uniquement** : Smoke/flash pour gêner

### ⚡ Force-buy situations
**Quand forcer :**
- **Économie adverse faible** détectée
- **Momentum critique** du match
- **Round décisif** (15-14, overtime)
- **Anti-eco adverse prévu**

**Compositions force-buy efficaces :**
- **All P250 + armor** : $1300 par joueur
- **SMG + armor** : $2200-2600
- **Scout + utilities** : $2200-2500
- **Mix economy** : 2-3 rifles, 2-3 ecos

## 🎯 Gestion d'équipe experte

### 🗣️ Communication financière
**Phrases essentielles :**
- "Money check" : Annonce ton argent
- "Can drop" : Tu peux aider un coéquipier
- "Need drop" : Tu as besoin d'aide
- "Save round" : Économie forcée
- "Force this" : Achat obligatoire

### 💝 Drop system optimisé
**Règles du drop :**
1. **Rifler → Support** : Priorité aux frags
2. **Rich → Poor** : Équilibrage team
3. **AWPer priority** : Protection investissement
4. **IGL toujours equipped** : Décisions optimales

### 📈 Anticipation économique adverse
**Indicateurs à surveiller :**
- **Rounds perdus consécutifs** : Bonus calculation
- **Equipment précédent** : Niveau d'investissement
- **Kills made** : Money gained estimation
- **Round type** : Force vs eco vs full

## 🏆 Conseils de pros économie

### 🧠 Psychologie économique
1. **Patience disciplinée** : Ne pas forcer systématiquement
2. **Information gathering** : Observer l'équipement adverse
3. **Risk assessment** : Calculer gains vs pertes potentielles
4. **Team coordination** : Économie synchronisée
5. **Meta adaptation** : S'adapter aux tendances adverses

### 💡 Astuces avancées
- **Semi-save** : 1-2 joueurs stack, 3-4 buy light
- **Economy breaking** : Force buy pour casser l'élan adverse
- **Investment protection** : Save AWP priority absolue
- **Utility priority** : Parfois plus important que l'armement
- **Round reading** : Anticiper les intentions adverses

## 📚 Calculs économiques pratiques

### 🔢 Formules essentielles
**Money après défaite :**
Starting money + Loss bonus + Kill rewards

**Break-even analysis :**
- **5 rounds eco** : $17,000 total team
- **3 rounds eco + 2 forces** : $15,000 total team
- **Eco efficiency** : Maximum $3400 per round per player

**Team economy target :**
- **$20,000+ team total** : Full buy confortable
- **$15,000-20,000** : Mixed buys possible
- **<$15,000** : Eco/force situations

Cette maîtrise économique représente 40% de la victoire en CS2 compétitif !
        `,
        links: [
          { name: '📊 Calculateur économique avancé', url: 'https://csgostats.gg/economy' },
          { name: '💰 Guide économie Liquipedia', url: 'https://liquipedia.net/counterstrike/Economy' },
          { name: '📈 Stats économiques pros', url: 'https://www.hltv.org/stats' }
        ],
        tips: [
          'L\'économie représente 40% de la stratégie en CS2 - maîtrisez-la absolument',
          'Surveillez toujours l\'économie adverse via leur équipement des rounds précédents',
          'Un eco bien géré peut être plus profitable qu\'un force-buy raté',
          'Le joueur le plus riche doit toujours drop en priorité',
          'Gardez minimum $1000 après un full-buy pour le round suivant'
        ]
      },

      'mouvement-et-deplacement-optimal': {
        title: 'Mouvement et déplacement optimal',
        level: 'Débutant',
        duration: '18 min',
        type: 'Movement',
        description: 'Maîtrisez les techniques de mouvement avancées pour une mobilité et survivabilité supérieures.',
        image: 'https://c4.wallpaperflare.com/wallpaper/337/204/15/valve-counter-strike-2-rifles-swat-hd-wallpaper-preview.jpg',
        objectives: [
          'Maîtriser le counter-strafing parfait',
          'Apprendre toutes les techniques de peek',
          'Optimiser la vitesse et fluidité de déplacement',
          'Utiliser le mouvement tactique avancé',
          'Développer la conscience spatiale'
        ],
        content: `
# 🏃‍♂️ Mouvement et déplacement optimal - Guide professionnel

## ⚡ Mécaniques de base fondamentales

### 🎯 Counter-strafing (technique #1 critique)
Le counter-strafing est LA technique fondamentale qui sépare les débutants des pros :

**Principe physique :**
- **Problème** : Dans CS2, vous continuez à glisser après avoir relâché une touche
- **Solution** : Appuyer brièvement sur la direction opposée
- **Résultat** : Arrêt instantané + précision maximale

**Technique exacte :**
- **Mouvement droite** : D → relâcher D → A (1-2 frames) → tir
- **Mouvement gauche** : A → relâcher A → D (1-2 frames) → tir  
- **Timing critique** : 33-66ms maximum pour l'input opposé

**Commandes d'entraînement :**
sv_cheats 1
sv_showimpacts 1
weapon_debug_spread_show 1

### 📏 Vitesses de déplacement (valeurs exactes)
- **Marche normale** : 250 unités/seconde
- **Marche silencieuse (shift)** : 125 unités/seconde  
- **Crouch-walk** : 90.75 unités/seconde
- **Couteau sorti** : 260 unités/seconde
- **Running accuracy** : Terrible (0.2% des bullets)
- **Walking accuracy** : Acceptable pour distances courtes
- **Standing accuracy** : Maximum (100% potential)

## 🔍 Techniques de peek avancées

### 👀 Wide peek (engagement ouvert)
**Utilisation :**
- **Duels préparés** avec avantage timing
- **Information gathering** confirmé
- **Support team** disponible

**Technique :**
1. **Pre-aim** angle anticipé
2. **Wide strafe** rapide (250 units/sec)
3. **Counter-strafe** instantané
4. **Shoot** immédiatement
5. **Re-peek** ou retreat selon résultat

### 👤 Shoulder peek (information safely)
**Objectif :** Gather info sans risque de mort
**Technique :**
1. **Strafe** toward angle (1-2 steps maximum)
2. **Immediate retreat** (counter-strafe)
3. **Observe** radar et audio feedback
4. **Communicate** info to team

### 🎭 Jiggle peek (bait shots)
**Utilisation :** Baiter les tirs adverses, waste ammo
**Technique avancée :**
1. **Rapid strafe** : A-D-A-D pattern
2. **Minimal exposure** : 0.1-0.2 secondes maximum
3. **Unpredictable timing** : Varier les intervalles
4. **Audio focus** : Écouter les shots wasted

### 🦘 Jump peek (reconnaissance verticale)
**Applications :**
- **Angles élevés** (Mirage palace, Inferno apps)
- **AWP baiting** (forcer le miss)
- **Long distance** information

**Technique perfect :**
1. **Pre-strafe** pour speed maximum
2. **Jump + strafe** synchronisé
3. **Air-strafe** pour control
4. **Landing preparation** pour escape/engagement

## 🚀 Techniques avancées de mouvement

### 🏄‍♂️ Strafe jumping pro
**Principe physique :**
- **Air acceleration** : 30 units/sec maximum gain
- **Mouse synchronization** : Mouvement souris + input clavier
- **Velocity maintenance** : Éviter W/S en l'air

**Technique step-by-step :**
1. **Pre-strafe** : A/D uniquement, pas de W
2. **Jump timing** : Au moment optimal de velocity
3. **Air control** : Souris smooth + strafe key
4. **Landing optimization** : Maintenir momentum

### 🐰 Bunny hopping (enchaînement)
**Conditions requises :**
- **fps_max 400+** pour consistency
- **Timing parfait** des inputs
- **Mouse smooth** movements
- **Map knowledge** des surfaces

**Séquence complète :**
1. **Strafe jump** initial
2. **Pre-speed** accumulation 
3. **Chain jumps** sans toucher W
4. **Rhythm consistency** 
5. **Surface optimization**

### 🎪 Movement tricks avancés
**Long jumps :**
- **Distance maximum** : 251.9 units
- **Technique** : Pre-strafe + perfect release timing
- **Applications** : Cache quad jump, Mirage connector, etc.

**Edge bugs exploitation :**
- **Wall surfing** : Utiliser les imperfections de hitbox
- **Pixel walks** : Positions impossibles via micro-edges

## 🗺️ Positionnement tactique expert

### 📐 Angles d'engagement optimaux
**Slice the pie methodology :**
1. **Révéler progressivement** chaque angle
2. **Minimize exposure** à multiple angles
3. **Maximize reaction time** disponible
4. **Control engagement distance**

**Pre-aiming positions :**
- **Common angles** : Head level exact
- **Off-angles** : Positions non-standard
- **Crosshair placement** : Anticipation path

### 🔄 Clearing patterns systématiques
**Méthodologie professionnelle :**
1. **Priority angles** first (most dangerous)
2. **Systematic sweep** left-to-right ou right-to-left
3. **Team coordination** pour multiple angles
4. **Sound discipline** during clear

### 🎯 Mouvement défensif expert
**Off-angles exploitation :**
- **Non-standard positions** pour surprise factor
- **Timing variation** pour disruption
- **Unpredictable patterns** 

**Rotation timing :**
- **Sound masking** avec utility/gunfire
- **Route optimization** (shortest path)
- **Information value** vs speed trade-off

## 🚫 Erreurs communes (à éviter absolument)

### ❌ Over-peeking syndrome
**Problème :** Exposition excessive lors des peeks
**Solution :** Self-discipline + angle respect

### ❌ Predictable patterns  
**Problème :** Routines répétitives facilement antées
**Solution :** Variation constante + creativity

### ❌ Poor timing coordination
**Problème :** Peeks non-synchronisés avec team
**Solution :** Communication + practice timing

### ❌ Noise discipline failures
**Problème :** Déplacements bruyants donnant position
**Solution :** Shift discipline + sound awareness

## 🏋️‍♂️ Exercices pratiques (plan d'entraînement)

### 📅 Programme quotidien (30 minutes)
**Semaine 1-2 : Fundamentals**
- **10 min** : Counter-strafing drill (aim_botz)
- **10 min** : Peek techniques (prefire maps)  
- **10 min** : Movement fluidity (kz_longjumps2)

**Semaine 3-4 : Advanced**
- **15 min** : Strafe jumping (kz_longjumps2)
- **10 min** : Bunny hop chains (bhop_monster)
- **5 min** : Map-specific tricks

**Semaine 5+ : Expert**
- **20 min** : Complex movement maps
- **10 min** : Competitive situation practice

### 🗺️ Maps d'entraînement recommandées
**Movement fundamentals :**
- **aim_botz** : Counter-strafing + basics
- **training_aim_csgo2** : Peek techniques

**Advanced movement :**
- **kz_longjumps2** : Strafe jumping mastery
- **bhop_monster** : Bunny hopping chains
- **surf_beginner** : Air control development

**Map-specific :**
- **prefire_dust2** : Angle clearing
- **prefire_mirage** : Standard positions
- **prefire_cache** : Movement spots

## 🎓 Conseils de pros movement

### 🧠 Mental approach
1. **Muscle memory development** : 10,000+ répétitions
2. **Consistency over flashiness** : Reliable > spectacular
3. **Situational awareness** : Movement adapté au context
4. **Team coordination** : Movement synchronisé
5. **Continuous improvement** : Analyse constante

### ⚡ Performance optimization
- **144Hz+ monitor** : Smooth visual feedback
- **High FPS** : fps_max 400+ pour consistency
- **Low input lag** : Gaming periphericals
- **Stable connection** : <50ms ping optimal

Le mouvement représente 30% de la performance globale - investissez le temps nécessaire !
        `,
        links: [
          { name: '🏃‍♂️ Movement guide complet', url: 'https://steamcommunity.com/sharedfiles/filedetails/?id=3070347493' },
          { name: '🗺️ Training maps collection', url: 'https://steamcommunity.com/workshop/browse/?appid=730&searchtext=movement' },
          { name: '📹 Pro movement analysis', url: 'https://www.youtube.com/watch?v=AGcgQEzCCrI' }
        ],
        tips: [
          'Le counter-strafing doit devenir aussi naturel que respirer - 30 min/jour minimum',
          'Utilisez fps_max 400+ pour une consistency parfaite du mouvement',
          'La discipline sonore est plus importante que la vitesse pure',
          'Maîtrisez 2-3 peek types parfaitement plutôt que tous moyennement',
          'Le movement est 30% technique, 70% timing et décision'
        ]
      },

      // Continuons avec les autres tutoriels...
      'visee-et-reglages-crosshair': {
        title: 'Visée et réglages crosshair',
        level: 'Débutant',
        duration: '25 min',
        type: 'Aiming',
        description: 'Développez une visée de précision avec les réglages crosshair optimaux et techniques d\'entraînement.',
        image: 'https://c4.wallpaperflare.com/wallpaper/361/922/362/counter-strike-2-valve-weapon-men-ultrawide-hd-wallpaper-preview.jpg',
        objectives: [
          'Configurer le crosshair parfait pour votre style',
          'Maîtriser le placement de crosshair optimal',
          'Développer la précision et flick shots',
          'Comprendre la sensibilité et accélération',
          'Mettre en place un programme d\'entraînement visée'
        ],
        content: `
# 🎯 Visée et réglages crosshair - Guide professionnel complet

## 🎨 Configuration crosshair optimale

### ⚙️ Paramètres de base recommandés
**Configuration universelle (adaptable) :**
\`\`\`
cl_crosshair_drawoutline 1
cl_crosshair_outlinethickness 1
cl_crosshairsize 2.5
cl_crosshairthickness 1.5
cl_crosshairdot 0
cl_crosshairgap -2
cl_crosshaircolor 5
cl_crosshaircolor_r 0
cl_crosshaircolor_g 255
cl_crosshaircolor_b 255
cl_crosshair_dynamic_maxdist_splitratio 0.35
cl_crosshair_dynamic_splitalpha_innermod 1
cl_crosshair_dynamic_splitalpha_outermod 0.5
cl_crosshair_dynamic_splitdist 7
\`\`\`

### 🎨 Variations par style de jeu
**AWPer (sniper) :**
- **Size** : 1-1.5 (précision maximum)
- **Gap** : -3 (petit gap pour precision)
- **Thickness** : 1 (minimal visual obstruction)
- **Dot** : Optionnel (0 ou 1)

**Rifler (assaut) :**
- **Size** : 2-3 (balance visibility/precision)
- **Gap** : -2 à 0 (selon préférence)
- **Thickness** : 1-2 (confort visuel)
- **Dynamic** : Disabled pour consistency

**Entry fragger :**
- **Size** : 2.5-3.5 (visibilité maximum)
- **Gap** : -1 à 1 (ouvert pour tracking)
- **Thickness** : 1.5-2 (visible en action)
- **Color** : Cyan/Green (contraste maximum)

### 🌈 Optimisation couleurs
**Couleurs recommandées par map :**
- **Dust2** : Cyan (contraste avec beige)
- **Mirage** : Magenta (contraste avec jaune)
- **Inferno** : Green (contraste avec rouge)
- **Cache** : White (contraste avec gris)
- **Overpass** : Yellow (contraste avec béton)

**Configuration couleur custom :**
\`\`\`
cl_crosshaircolor 5
cl_crosshaircolor_r 255
cl_crosshaircolor_g 0  
cl_crosshaircolor_b 255
\`\`\`

## 🖱️ Sensibilité et configuration souris

### 📏 Calcul sensibilité optimale
**Formule professionnelle :**
**eDPI = DPI × Sensibilité in-game**

**Ranges recommandés :**
- **Low sens** : 600-1000 eDPI (précision maximum)
- **Medium sens** : 1000-1600 eDPI (balance optimal)
- **High sens** : 1600-2400 eDPI (mobilité maximum)

**Exemples pros célèbres :**
- **s1mple** : 400 DPI × 3.09 = 1236 eDPI
- **ZywOo** : 400 DPI × 2.0 = 800 eDPI  
- **NiKo** : 400 DPI × 1.35 = 540 eDPI
- **device** : 400 DPI × 1.9 = 760 eDPI

### ⚙️ Paramètres souris critiques
**Windows settings :**
- **Pointer speed** : 6/11 (default, no acceleration)
- **Enhance pointer precision** : DISABLED
- **Mouse acceleration** : OFF

**In-game settings :**
m_rawinput 1
m_customaccel 0
m_mouseaccel1 0
m_mouseaccel2 0
sensitivity 2.0
zoom_sensitivity_ratio_mouse 1.0

**Hardware recommendations :**
- **Polling rate** : 1000Hz minimum
- **DPI** : 400-800 (sensor optimal range)
- **Mousepad** : 45cm+ pour low sens

## 🎯 Crosshair placement fundamental

### 📐 Règles de placement optimal
**Hauteur critical :**
- **Pre-aim head level** : Toujours à hauteur de tête
- **Angle anticipation** : Où l'ennemi va apparaître
- **Distance optimization** : Plus proche du coin = meilleur temps de réaction

**Techniques avancées :**
1. **Wall hugging** : Crosshair collé aux angles
2. **Pre-aiming** : Placement prédictif
3. **Flick minimization** : Réduire distance à parcourir
4. **Dynamic adjustment** : Adaptation selon intel

### 🗺️ Map-specific placement
**Dust2 long A :**
- **CT side** : Pre-aim car/barrels head level
- **T side** : Pre-aim pit/site angles

**Mirage mid :**
- **Connector** : Pre-aim stairs head level  
- **Window** : Pre-aim common AWP angles

**Cache main :**
- **Quad angles** : Pre-aim elevation changes
- **Site angles** : Dynamic between positions

## 🏹 Techniques de visée avancées

### ⚡ Flick shots mastery
**Muscle memory development :**
1. **Slow-motion practice** : Mouvements lents et précis
2. **Acceleration graduelle** : Augmenter vitesse progressivement  
3. **Consistency focus** : Même mouvement répété
4. **Distance variation** : Flicks courts/moyens/longs

**Technique optimale :**
- **Wrist flicks** : <90° rotation
- **Arm movement** : >90° rotation
- **Hybrid approach** : Combinaison selon distance

### 🎯 Tracking shots
**Applications :**
- **Moving targets** : Adversaires en mouvement
- **Spray control** : Suivi du recul
- **Angle clearing** : Balayage smooth

**Practice method :**
1. **Smooth mouse movement** : Pas de jerky motions
2. **Predict movement** : Anticiper trajectoire
3. **Consistent speed** : Vitesse constante de tracking

### 🔥 One-taps precision
**Technique perfect :**
1. **Counter-strafe** : Arrêt instantané
2. **Crosshair placement** : Déjà sur la cible
3. **Single tap** : Un seul click précis
4. **Reset position** : Préparation du suivant

## 🏋️‍♂️ Programme d'entraînement visée

### 📅 Routine quotidienne (45 minutes)
**Warm-up (10 minutes) :**
- **aim_botz** : 500 one-taps statiques
- **Crosshair placement** : 5 minutes tracking

**Precision training (20 minutes) :**
- **Fast aim/reflex** : 10 minutes flick shots
- **Long range** : 5 minutes distance training
- **Pistol rounds** : 5 minutes precision pistol

**Spray control (10 minutes) :**
- **AK pattern** : 5 minutes
- **M4 pattern** : 5 minutes

**Cool-down (5 minutes) :**
- **Free aim** : Relaxed shooting

### 🗺️ Maps d'entraînement spécialisées
**Aim fundamentals :**
- **aim_botz** : One-taps et flicks
- **training_aim_csgo2** : Scenarios variés
- **aimtrain** : Reflexes et precision

**Advanced training :**
- **aim_training_csgo** : Situations complexes
- **fast_aim_reflex_training** : Vitesse pure
- **training_crosshair_v2** : Placement practice

**Spray control :**
- **recoil_master** : Patterns weapons
- **training_recoil_control** : Control avancé

## 📊 Métriques et progression

### 📈 KPIs à tracker
**Precision metrics :**
- **Headshot %** : >50% objectif
- **First bullet accuracy** : >75% objectif
- **Reaction time** : <200ms objectif
- **Flick accuracy** : >60% sur 180°

**Training benchmarks :**
- **aim_botz 100 kills** : <60 secondes
- **Fast aim level 4** : Consistent clear
- **Spray pattern** : 10/10 bullets dans A4 paper

### 🎯 Objectifs progression
**Semaine 1-2 :**
- **Crosshair** : Configuration stable
- **Sensitivity** : Déterminée et constante
- **Placement** : Basic head level

**Semaine 3-4 :**
- **Flicks** : Consistency 70%+
- **One-taps** : 500+ par session
- **Map knowledge** : Common angles mémorisés

**Semaine 5-8 :**
- **Advanced placement** : Pre-aiming expert
- **Spray control** : AK/M4 maîtrisés
- **Competitive consistency** : Performance stable

**Mois 3+ :**
- **Pro-level consistency** : Match performance
- **Advanced techniques** : Micro-adjustments
- **Meta adaptation** : Style evolution

## 🧠 Psychologie de la visée

### 🎯 Mental approach
**Confidence building :**
- **Success visualization** : Imaginer les frags
- **Positive self-talk** : "Je vais hit ce shot"
- **Mistake acceptance** : Learning from misses
- **Pressure management** : Clutch situations

**Focus techniques :**
- **Breathing control** : Calm under pressure
- **Tunnel vision** : Focus sur crosshair uniquement
- **Zen state** : Relaxed concentration
- **Flow state** : Natural aiming

### 🔄 Adaptation continue
**Style evolution :**
- **Meta analysis** : Étudier les tendances pros
- **Personal optimization** : Adapter à son style
- **Equipment upgrades** : Hardware improvements
- **Technique refinement** : Continuous improvement

La visée représente 50% de la performance - investissez massivement !
        `,
        links: [
          { name: '🎯 Crosshair generator pro', url: 'https://tools.dathost.net/crosshair-generator' },
          { name: '📊 Sensitivity calculator', url: 'https://prosettings.net/cs2/sensitivity-converter/' },
          { name: '🏹 Aim training guide', url: 'https://steamcommunity.com/sharedfiles/filedetails/?id=303916990' }
        ],
        tips: [
          'Changez JAMAIS votre sensibilité une fois trouvée - consistency is king',
          'Le crosshair placement compte plus que les flick shots spectaculaires',  
          '45 minutes d\'aim training quotidien minimum pour progresser',
          'Un bon crosshair devient invisible - vous ne devez plus le voir',
          'La régularité bat la perfection - visez la consistency'
        ]
      },

      'presentation-des-armes-principales': {
        title: 'Présentation des armes principales',
        level: 'Débutant',
        duration: '22 min',
        type: 'Weapons',
        description: 'Découvrez les armes emblématiques de CS2 et leurs spécificités tactiques avec le méta 2025.',
        image: 'https://images.unsplash.com/photo-1595472968262-48209bf5b390?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHwxfHxjb3VudGVyJTIwc3RyaWtlfGVufDB8fHx8MTc1MzQwMDMyMXww&ixlib=rb-4.1.0&q=85',
        objectives: [
          'Connaître toutes les armes et leurs statistiques exactes',
          'Comprendre le méta des armes en 2025',
          'Maîtriser les choix d\'armement selon les situations',
          'Apprendre l\'économie des armes optimale',
          'Développer les préférences selon votre style'
        ],
        content: `
# 🔫 Présentation des armes principales - Guide professionnel CS2 2025

## 🎯 Classification des armes (méta 2025)

### 🥇 Tier S (Meta dominant)
**AK-47** ($2700) - L'arme légendaire
- **Dégâts** : 147 (tête sans casque), 109 (tête avec casque)
- **One-tap potential** : OUI (toutes distances)
- **Précision** : Excellente premier tir
- **Recul** : Difficile mais prévisible
- **Utilisation** : Côté Terroriste uniquement

**M4A4** ($3100) - Le pilier CT
- **Dégâts** : 131 (tête sans casque), 92 (tête avec casque)
- **One-tap potential** : NON (sauf très proche)
- **Précision** : Excellente
- **Recul** : Plus facile que AK
- **Capacité** : 30 balles (avantage crucial)

**M4A1-S** ($2900) - Le silencieux tactique
- **Dégâts** : 131 (tête sans casque), 92 (tête avec casque)
- **Avantages** : Silencieux + moins de recul
- **Inconvénients** : 20 balles seulement
- **Meta 2025** : Préféré pour jeu passif

**AWP** ($4750) - Le game changer
- **Dégâts** : One-shot kill body/tête
- **Vitesse** : Très lente
- **Économie** : Investment majeur
- **Impact** : Peut gagner un round seul

### 🥈 Tier A (Très viables)
**Galil AR** ($2000) - Budget T-side
- **Rapport qualité/prix** : Excellent
- **Dégâts** : 99 (tête avec casque)
- **Usage** : Rounds économiques T

**FAMAS** ($2250) - Budget CT-side
- **Burst mode** : Très efficace proche
- **Auto mode** : Pour débutants
- **Économie** : Alternative M4 pas chère

**AUG** ($3300) - Scope rifle CT
- **Scope** : Avantage distances longues
- **Dégâts** : Similaire M4A4
- **Meta** : Underrated mais puissant

**SG 553** ($3000) - Scope rifle T
- **Scope** : Comme AUG côté T
- **One-tap** : Possible avec casque
- **Usage** : Situations spécifiques

### 🥉 Tier B (Situationnel)
**MP9** ($1250) - SMG CT anti-eco
- **Mobility** : Excellente
- **Kill reward** : $600
- **Usage** : Contre rush T économiques

**MAC-10** ($1050) - SMG T rush
- **Run & gun** : Très efficace
- **Kill reward** : $600
- **Tactique** : Rush sites agressif

**UMP-45** ($1200) - SMG polyvalent
- **Dégâts** : Meilleurs que MP9/MAC-10
- **Armor penetration** : Correcte
- **Budget** : Eco rounds avancés

## 💰 Économie des armes (optimisation 2025)

### 📊 Coûts et rentabilité
**Full buy setup** :
- **T-side** : AK ($2700) + Kevlar+Helmet ($1000) + Grenades ($1400) = $5100
- **CT-side** : M4 ($3100) + Kevlar+Helmet ($1000) + Grenades ($1400) = $5500

**Force buy setups** :
- **T-side budget** : Galil ($2000) + Kevlar ($650) + Flash ($200) = $2850
- **CT-side budget** : FAMAS ($2250) + Kevlar ($650) + Smoke ($300) = $3200

**Anti-eco setups** :
- **SMG + grenades** : MP9/MAC-10 + armor + utilities = $2500-3000
- **Kill rewards** : $600 par kill SMG vs $300 rifles

### 💡 Conseils économiques pros
1. **Jamais drop AWP** sauf situation désespérée
2. **SMGs rounds** après victoires économiques adverses
3. **Force buy** si adversaire eco confirmé
4. **Save rounds** - Garder minimum $1400 pour utilities

## 🎯 Choix d'armes selon situations

### 🗺️ Par maps et positions
**Dust2** :
- **Long A** : AWP priorité absolue
- **Cat/Short** : M4A1-S pour precision
- **Tunnels** : AK-47 pour one-taps
- **Site B** : MP9 anti-rush

**Mirage** :
- **Mid** : AWP dominance
- **Connector** : M4A4 pour spray
- **Palace** : AK préférable
- **Apps** : SMG défense

**Inferno** :
- **Long angles** : AUG/SG underrated
- **Close combats** : SMGs excellents
- **Apartments** : Rifles requis
- **Banana** : AWP control crucial

### 🎭 Par style de jeu
**Entry fragger** :
- **Primary** : AK-47 (one-tap potential)
- **Secondary** : Glock/USP selon side
- **Utilities** : Flash + smoke entry

**Support player** :
- **Primary** : M4A1-S (spam angles)
- **Focus** : Trade kills + utilities
- **Grenades** : Smoke + HE priority

**AWPer** :
- **Primary** : AWP obvious
- **Secondary** : Deagle (eco rounds)
- **Positioning** : Long angles dominance

**IGL (In-Game Leader)** :
- **Primary** : M4A4/AK selon side
- **Focus** : Survival + information
- **Utilities** : Smokes + coordination

## 🔬 Statistiques techniques exactes

### 📈 Damage values (armor/no armor)
**AK-47** :
- Head : 147/109
- Chest : 108/81
- Stomach : 135/101
- Legs : 86/81

**M4A4** :
- Head : 131/92
- Chest : 97/69
- Stomach : 121/86
- Legs : 77/69

**AWP** :
- Head : 459 (always kill)
- Chest : 287 (always kill)
- Stomach : 287 (always kill)
- Legs : 172 (no kill)

### ⚡ Specs techniques cruciales
**Movement speed** (knife = 260) :
- AK-47 : 215
- M4A4 : 225
- M4A1-S : 225
- AWP : 200

**Rate of fire** (RPM) :
- AK-47 : 600
- M4A4 : 666
- M4A1-S : 600
- AWP : 41

## 🏆 Meta analysis 2025

### 📊 Usage professional
**HLTV Top 20 players preferences** :
- **AK-47** : 89% pick rate T-side
- **M4A1-S** : 67% vs M4A4 33% CT-side
- **AWP** : 1 per team standard
- **Force buys** : Galil/FAMAS 78% over SMGs

### 🔄 Changements récents CS2
**Updates significatifs** :
- **M4A1-S buff** : Moins de recul (-15%)
- **AUG nerf** : Prix augmenté $3300
- **SMG meta** : Kill reward maintenu $600
- **Pistol changes** : Glock buff significatif

### 🎯 Tendances tactiques
**T-side meta** :
- **AK + utilities** > all-in armor
- **Galil eco** plus populaire
- **Force buy** timing crucial

**CT-side meta** :
- **M4A1-S** dominance confirmée
- **Anti-eco SMG** toujours viable
- **AWP positioning** plus passif

## 🎓 Progression apprentissage

### 📅 Plan 4 semaines
**Semaine 1 - Familiarisation** :
- **AK-47** : 200 one-taps/jour
- **M4** : Choix A4 vs A1-S personnel
- **Économie** : Mémoriser tous les prix

**Semaine 2 - Specialization** :
- **Arme principale** : 500+ kills
- **Situations** : Practice toutes positions
- **Anti-eco** : SMG mastery

**Semaine 3 - Advanced** :
- **AWP introduction** : Si intérêt
- **Force buys** : Timings optimaux
- **Map specific** : Weapons par map

**Semaine 4 - Competitive** :
- **Match application** : Competitive focus
- **Adaptation** : Selon adversaires
- **Economy discipline** : Never over-invest

### 💡 Erreurs courantes à éviter

❌ **Changer d'arme constamment** - Stick avec 2-3 armes maximum
❌ **Ignorer l'économie** - Calculate before buying
❌ **AWP sans backup** - Always have rifle player ready
❌ **Force buy mal timé** - Know enemy economy
❌ **SMG overuse** - Only contre eco/anti-rush

La maîtrise des armes représente 35% de votre performance - investissez le temps nécessaire !
        `,
        links: [
          { name: '🔫 Database armes complète', url: 'https://counterstrike.fandom.com/wiki/Counter-Strike_2/Weapons' },
          { name: '📊 Stats weapons pro', url: 'https://www.hltv.org/stats/weapons' },
          { name: '💰 Calculateur économique', url: 'https://csgostats.gg/economy' }
        ],
        tips: [
          'Maîtrisez parfaitement 2-3 armes plutôt que toutes moyennement',
          'L\'économie des armes détermine 40% des victoires - calculez toujours',
          'L\'AK-47 reste l\'arme la plus impactante - investissez massivement dessus',
          'Le choix M4A1-S vs M4A4 dépend de votre style : passif vs agressif',
          'Ne jamais force buy sans plan - ayez toujours une stratégie claire'
        ]
      },

      'maps-active-duty-dust2-basics': {
        title: 'Maps Active Duty : Dust2 basics',
        level: 'Débutant',
        duration: '20 min',
        type: 'Maps',
        description: 'Maîtrisez Dust2, la map légendaire de CS2 avec callouts, positions et stratégies 2025.',
        image: 'https://images.unsplash.com/flagged/photo-1560177776-295b9cd779de?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHwyfHxjb3VudGVyJTIwc3RyaWtlfGVufDB8fHx8MTc1MzQwMDMyMXww&ixlib=rb-4.1.0&q=85',
        objectives: [
          'Connaître tous les callouts Dust2 professionnels',
          'Maîtriser les positions clés et angles d\'engagement',
          'Comprendre les stratégies T et CT optimales',
          'Apprendre le contrôle de map et rotations',
          'Développer le game sense spécifique à Dust2'
        ],
        content: `
# 🏜️ Dust2 Basics - Guide professionnel complet 2025

## 🗺️ Callouts officiels (Standard Professionnel)

### 🚪 Zone Tunnels/Lower (T-Side)
**Tunnels supérieurs** :
- **T Spawn** : Zone de spawn Terroriste
- **Tunnels** : Passage principal vers B
- **Upper Tunnels** : Partie haute des tunnels
- **Lower Tunnels** : Descente vers B Site

**Tunnels positions** :
- **Tunnel Mouth** : Sortie tunnels vers B
- **Close Tunnel** : Position proche mur B
- **Default Tunnel** : Position standard pré-clear

### 🎯 Zone Long A (Engagement longue distance)
**Positions T-Side** :
- **Long Doors** : Portes d'entrée Long A
- **Outside Long** : Extérieur des portes
- **Pit** : Position en contrebas Long
- **Long Corner** : Angle de Long vers site A

**Positions CT-Side** :
- **Long A** : Position de défense Long
- **Car** : Voiture sur Long A
- **Site A** : Zone de site A
- **Goose** : Position élevée site A
- **Ninja** : Position cachée sous site A

### 🏗️ Zone Middle (Contrôle central)
**Mid positions** :
- **T Mid** : Position T dans Mid
- **Mid Doors** : Portes centrales
- **Xbox** : Boîte au centre Mid
- **Catwalk/Cat** : Passerelle vers A
- **CT Mid** : Position CT dans Mid

**Upper Mid** :
- **Top Mid** : Partie haute Mid
- **Lower Tunns** : Connexion Mid vers B
- **Suicide** : Position risquée Mid

### 🏠 Zone B Site (Site Bombe B)
**B Site callouts** :
- **B Platform** : Plateforme site B
- **Back Plat** : Fond de la plateforme
- **Closet** : Angle fermé site B
- **Car B** : Voiture site B
- **Window** : Fenêtre CT vers B
- **B Doors** : Porte CT vers B

## 🎮 Stratégies Terroriste (T-Side)

### 🚀 Rush strategies
**B Rush classique** :
\`\`\`
Formation : 4-5 joueurs tunnels
Utility : 2 Flash over + 1 Smoke tunns mouth
Timing : Fast execution (15-20 secondes)
Objectif : Overwhelm site avant rotations
Success rate : 70% contre eco, 35% full buy
\`\`\`

**Long A Rush** :
\`\`\`
Formation : 3-4 joueurs Long
Utility : Long smoke + 2 Flash long
Support : 1 joueur Mid distraction
Timing : Coordinated peek after utility
Success rate : 45% general
\`\`\`

### 🎯 Split strategies (Advanced)
**A Site Split** :
- **Long team** : 2-3 joueurs Long A
- **Cat team** : 2 joueurs Catwalk
- **Utility coord** : Smokes Long + Cat synchronisés
- **Timing** : Execution simultanée après utility

**Mid to B Split** :
- **Tunnels** : 2 joueurs pression B
- **Mid team** : 2-3 joueurs control Mid
- **Execution** : Mid push coordonné avec B distraction

### 💡 Control strategies (Pro level)
**Mid control dominance** :
1. **Early mid peek** : AWP/Rifle duel CT Mid
2. **Xbox smoke** : Bloquer vision CT
3. **Catwalk control** : Access A site
4. **Lower control** : Access B rotate

**Long control** :
1. **Long smoke** : Bloquer AWP Long
2. **Pit control** : Position avantageuse
3. **Car clear** : Systematic angle clear
4. **Site execute** : Post-plant positions

## 🛡️ Stratégies Counter-Terrorist (CT-Side)

### 🎯 Defensive setups standard
**Setup 2-1-2** (Most common) :
- **A Site** : 2 joueurs (1 Long, 1 Site/Cat)
- **Mid** : 1 joueur (rotation/support)
- **B Site** : 2 joueurs (1 Site, 1 Tunnel watch)

**Setup 1-2-2** (Mid control) :
- **A Site** : 1 joueur Long
- **Mid** : 2 joueurs (control + support)
- **B Site** : 2 joueurs standard

### 🔄 Rotation principles
**Early rotation** (read based) :
- **Sound cues** : Footsteps/grenades
- **Radar info** : Teammate spots
- **Utility usage** : Enemy grenades indication

**Late rotation** (commit based) :
- **Bomb plant** : Confirmed site
- **Multiple enemies** : 3+ spotted
- **Death confirmation** : Teammate down

### 🏠 Position holding (Advanced)
**Long A defense** :
- **AWP Long** : Standard long range
- **Rifle Long** : Close long position
- **Site support** : Crossfire setup
- **Pit watch** : Advanced angle

**B Site defense** :
- **Platform hold** : Multiple angles
- **Tunnels peek** : Information gathering
- **Retake positions** : Post-plant spots
- **Window support** : Backup position

## 🎪 Positions avancées et tricks

### 🏗️ Boost positions
**A Site boosts** :
- **Goose boost** : Enhanced A site vision
- **Ninja boost** : Hidden plat position
- **Long boost** : Long angle advantage

**B Site boosts** :
- **Plat boost** : Superior site control
- **Car boost** : Tunnels peek advantage
- **Back boost** : Anti-rush position

### 🎭 Off-angles (Surprise positions)
**Unusual CT positions** :
- **Pit position** : Long reverse angle
- **Mid stairs** : Unexpected peek
- **B closet** : Anti-rush surprise
- **Long corner** : Advanced long hold

**T-side off-angles** :
- **Long cross** : Mid-round reposition
- **Cat lurk** : Rotation catching
- **Tunnel boost** : Site peek advantage

## 💡 Utility usage expert

### 💨 Smokes standard (Must know)
**T-Side smokes** :
\`\`\`
Long smoke : Bloquer AWP Long
Xbox smoke : Mid control
Catwalk smoke : A site execute
B smoke : Site entry
CT smoke : B retake block
\`\`\`

**CT-Side smokes** :
\`\`\`
Tunnel smoke : B site delay
Long cross : A site support
Mid smoke : Mid control
Cat smoke : A site hold
Xbox one-way : Mid advantage
\`\`\`

### ⚡ Flash techniques
**Pop-flashes standards** :
- **Long flash** : Par-dessus mur Long
- **Cat flash** : Catwalk support
- **B flash** : Over ceiling B site
- **Mid flash** : Xbox area

**Team flashes** :
- **Long support** : Teammate flash Long push
- **A execute** : Cat + Long synchronized
- **B coordinate** : Tunnel + Window flash

### 🔥 Molotov/Incendiary usage
**T-Side molotovs** :
- **Long stop** : AWP delay
- **Site clear** : Common spots
- **Post-plant** : Defuse deny

**CT-Side incendiaries** :
- **Tunnel delay** : B rush stop
- **Long control** : T advance block
- **Retake clear** : Post-plant positions

## 📊 Meta analysis 2025

### 📈 Professional statistics
**Win rates by strategy** :
- **B Rush** : 58% success rate
- **A Split** : 45% success rate
- **Mid control** : 72% round win after control
- **Long control** : 65% round win rate

**Common results** :
- **T-side rounds** : 6-7 average per half
- **CT-side rounds** : 8-9 average per half
- **Overtime frequency** : 35% matches

### 🎯 Current meta tendencies
**T-Side meta** :
- **Utility heavy** : 4+ grenades per execute
- **Mid control priority** : 78% teams focus mid
- **Late round executes** : Timing advantage

**CT-Side meta** :
- **Aggressive plays** : 65% early round aggression
- **Stack rotations** : Quick adapts
- **Utility saving** : Retake focus

## 🎓 Progression plan (4 semaines)

### 📅 Semaine 1 : Fundamentals
**Objectifs** :
- **Callouts** : 100% accuracy
- **Basic positions** : Standard holds
- **Movement** : Map connaissance
- **Practice** : 2h/jour DM sur Dust2

**Exercices** :
- **Callout quiz** : 50 positions/jour
- **Position practice** : 30min holds
- **Movement** : Transitions smooth

### 📅 Semaine 2 : Strategies
**Objectifs** :
- **T-Side executes** : 3 strategies maîtrisées
- **CT-Side setups** : 2 setups fluides
- **Utility usage** : Timing correct
- **Practice** : 1h strategy + 1h DM

**Exercices** :
- **Strategy drill** : 10 executions/strategy
- **Utility practice** : 50 grenades/jour
- **Demo review** : 2 matches pros/jour

### 📅 Semaine 3 : Advanced
**Objectifs** :
- **Off-angles** : 5 positions maîtrisées
- **Boost spots** : 3 boosts utiles
- **Reads enemy** : Pattern recognition
- **Practice** : Competitive focus

**Exercices** :
- **Position variations** : 30min/jour
- **Competitive** : 5 matches/jour
- **Demo analysis** : Personal gameplay

### 📅 Semaine 4 : Expert
**Objectifs** :
- **IGL basics** : Call simple strategies
- **Adaptation** : Counter enemy plays
- **Consistency** : Stable performance
- **Practice** : Tournament preparation

**Exercices** :
- **Team practice** : Coordinated play
- **Anti-strat** : Counter common strategies
- **Mental game** : Pressure performance

## 🚨 Erreurs communes à éviter

❌ **Over-rotate** : Trop rapide abandon positions
❌ **Tunnel vision** : Focus une zone, ignore autres
❌ **Utility waste** : Grenades mal timées
❌ **Predictable** : Même positions/strategies
❌ **Communication fails** : Info incomplète/tardive

### 💡 Tips de pros finals

1. **"Dust2 c'est 60% aim, 40% game sense"** - s1mple
2. **"Control mid = control map"** - Principle fondamental
3. **"Never force Long vs AWP"** - Règle économique
4. **"B retakes win championships"** - Team coordination
5. **"Learn enemy patterns first 5 rounds"** - Adaptation

Dust2 reste la map la plus aim-intensive - investissez massivement dans votre précision !
        `,
        links: [
          { name: '🗺️ Dust2 callouts interactifs', url: 'https://www.tobyscs.com/csgo-callouts/dust2/' },
          { name: '📊 Stats Dust2 professionnels', url: 'https://www.hltv.org/stats/maps/31/dust2' },
          { name: '💨 Guide smokes Dust2', url: 'https://www.youtube.com/watch?v=3BU-M1DE2pE' }
        ],
        tips: [
          'Dust2 est 60% aim, 40% positioning - entraînez votre visée quotidiennement',
          'Le contrôle du Mid détermine 70% des rounds - priorisez cette zone',
          'Never peek Long vs AWP sans utility - respectez la distance',
          'Les rotations Dust2 sont les plus rapides - communiquez instantanément',
          'Maîtrisez 3 positions par zone plutôt que toutes superficiellement'
        ]
      },

      'utilisation-des-grenades-de-base': {
        title: 'Utilisation des grenades de base',
        level: 'Débutant',
        duration: '18 min',
        type: 'Utilities',
        description: 'Maîtrisez les utilitaires CS2 : smokes, flashs, molotovs et HE avec techniques professionnelles 2025.',
        image: 'https://images.unsplash.com/photo-1636489951222-2af65c1d9ae3?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1NzZ8MHwxfHNlYXJjaHwzfHxjb3VudGVyJTIwc3RyaWtlfGVufDB8fHx8MTc1MzQwMDMyMXww&ixlib=rb-4.1.0&q=85',
        objectives: [
          'Connaître tous les types de grenades et leurs utilisations',
          'Maîtriser les techniques de lancer et timing',
          'Comprendre l\'économie des utilitaires',
          'Apprendre les grenades essentielles par map',
          'Développer la coordination team avec utilities'
        ],
        content: `
# 💣 Utilisation des grenades de base - Guide professionnel CS2 2025

## 🎯 Types de grenades et statistiques

### 💨 Smoke Grenade ($300) - Le game changer
**Statistiques techniques** :
- **Durée** : 18 secondes exactement
- **Radius** : 144 unités de diamètre
- **Deploy time** : 1 seconde avant activation
- **Opacité** : 100% blocage vision (nouvelles mécaniques CS2)

**Utilisations stratégiques** :
- **Vision blocking** : Couper sightlines AWP
- **Executes** : Entrer sur sites
- **Retakes** : Isoler angles défensifs
- **Rotations** : Masquer mouvements équipe
- **Post-plant** : Défense bombe après plant

**Nouvelles mécaniques CS2** :
- **Réalisme physique** : Fumée affectée par vent
- **Lighting dynamic** : Éclairage réaliste dans smoke
- **Particle system** : Density variable selon distance

### ⚡ Flashbang ($200) - L'arme psychologique
**Statistiques techniques** :
- **Flash duration** : 0.3-7.5 secondes selon distance/angle
- **Blast radius** : 200 unités
- **Detonation delay** : 1.5 secondes après lancer
- **Flash curve** : Dégradation logarithmique

**Types de flashs** :
1. **Pop-flash** : Détonation instantanée peek
2. **Support flash** : Flash teammate pour entry
3. **Retake flash** : Aveugler défenseurs site
4. **Escape flash** : Blind pour retreat
5. **Fake flash** : Sound cue sans effet réel

**Effectiveness factors** :
- **Distance** : Plus proche = plus long blind
- **Angle vision** : Face-on = maximum effect
- **Wall bounces** : Ricochets pour angles impossibles
- **Teammate coordination** : Timing callouts

### 🔥 Molotov/Incendiary ($400/$600) - Le contrôle territorial
**Statistiques techniques** :
- **Burn duration** : 7 secondes
- **Damage rate** : 8 HP/seconde
- **Area coverage** : 240 unités radius
- **Spread pattern** : Physique realiste CS2

**Tactical applications** :
- **Area denial** : Bloquer passages
- **Clear positions** : Forcer movement
- **Time delay** : Ralentir rushes
- **Damage confirm** : Finir ennemis blessés
- **Post-plant control** : Défuse denial

**Différences Molotov vs Incendiary** :
- **Molotov** (T-side) : Moins cher, même effet
- **Incendiary** (CT-side) : Plus cher, activation plus rapide

### 💥 HE Grenade ($300) - Le damage dealer
**Statistiques techniques** :
- **Max damage** : 98 HP (sans armor)
- **Armor damage** : 57 HP (avec armor)
- **Blast radius** : 350 unités
- **Falloff damage** : Linear selon distance

**Utilisations optimales** :
- **Damage économique** : Affaiblir multiple ennemis
- **Finish kills** : Terminer ennemis low HP
- **Wallbang combo** : Combined avec spray walls
- **Stack damage** : Multiple HE coordonnées
- **Anti-eco** : Maximum impact vs no-armor

## 🎪 Techniques de lancer avancées

### 🎯 Mécaniques de base perfectionnées
**Mouse positions** :
- **Left-click** : Full power throw (100% velocity)
- **Right-click** : Medium throw (50% velocity) 
- **Both clicks** : Short throw (25% velocity)

**Movement influence** :
- **Running forward** : +15% distance
- **Running backward** : -10% distance
- **Strafing** : Angle deviation selon velocity
- **Jumping** : Arc trajectory modification

### 🏃‍♂️ Jump-throw technique (Critical skill)
**Bind obligatoire** :
\`\`\`
alias "+jumpthrow" "+jump;-attack"
alias "-jumpthrow" "-jump"
bind "c" "+jumpthrow"
\`\`\`

**Applications jump-throw** :
- **Consistent smokes** : Même trajectory toujours
- **Long distance** : Maximum range grenades
- **Pixel perfect** : Precision locations
- **Team executes** : Synchronized utility

**Jump-throw variations** :
- **Running jump-throw** : Pre-velocity pour extra distance
- **Strafe jump-throw** : Angle throws
- **Backward jump-throw** : Short precise throws

### 🎭 Bounce techniques avancées
**Single bounce** :
- **Walls** : 45° angle optimal reflection
- **Ground** : Skip grenades sous obstacles
- **Ceiling** : Pop-flash over covers

**Multiple bounces** :
- **Bank shots** : 2-3 wall ricochets
- **Skip throws** : Ground bounces multiples
- **Complex trajectories** : Combination bounces

## 🗺️ Grenades essentielles par map

### 🏜️ Dust2 (Must-know throws)
**T-Side smokes critiques** :
1. **Xbox smoke** : Mid control absolut
2. **CT smoke** : B site execute
3. **Long smoke** : Counter AWP Long
4. **A site smoke** : Execute coordination

**CT-Side utilities** :
1. **Tunnels smoke** : B defense delay
2. **Catwalk flash** : A site support
3. **Long incendiary** : Anti-rush Long
4. **B retake smokes** : Post-plant control

### 🏠 Mirage (Utility paradise)
**T-Side executes** :
1. **Jungle smoke** : A site control
2. **CT smoke** : A execute
3. **Connector smoke** : Mid to B
4. **Window smoke** : Mid control

**Pop-flashes Mirage** :
1. **Palace flash** : A site entry
2. **Apartments flash** : B site entry
3. **Mid flash** : Connector push
4. **Retake flashes** : Site reclaim

### 🔥 Inferno (Molotov kingdom)
**Molotov spots critiques** :
1. **Banana molly** : Anti-rush B
2. **Apartments molly** : Clear common spots
3. **Site mollies** : Post-plant positions
4. **Arch molly** : Mid control

**Smoke setups** :
1. **Balcony smoke** : A site execute
2. **Stairs smoke** : Apps control
3. **CT smoke** : B site execute
4. **Pit smoke** : A site isolation

## 💰 Économie des utilitaires (Optimization 2025)

### 📊 Cost-benefit analysis
**Investment priorities** :
1. **Smokes** : $300 - ROI maximum (18s duration)
2. **Flashes** : $200 - High impact entries
3. **HE** : $300 - Multi-enemy damage
4. **Molotov** : $400-600 - Area control

**Round economy planning** :
- **Full buy** : $1400 utilities minimum
- **Force buy** : $600-800 utilities maximum
- **Eco rounds** : $200 flash only
- **Anti-eco** : HE + Flash priority

### 💡 Economic principles
**Utility value hierarchy** :
1. **Smokes** - Game changing (always buy)
2. **Flashes** - Entry enabling (high priority)
3. **Molotovs** - Control/delay (situational)
4. **HE** - Damage/finish (luxury item)

**Team distribution** :
- **IGL** : Smokes primary (stratégie)
- **Entry** : Flashes priority (engagements)
- **Support** : Molotovs/HE (zone control)
- **AWPer** : Flash/smoke (positioning)

## 🤝 Coordination équipe avec utilities

### 📢 Communication protocols
**Utility callouts standard** :
- **"Smoking X"** : Annoncer smoke location
- **"Flash me"** : Demander support flash
- **"Molly out"** : Avertir molotov active
- **"HE incoming"** : Prévenir damage grenade

**Timing coordination** :
- **"Flash in 3, 2, 1"** : Countdown synchronized
- **"Smoke blooming"** : Smoke activation timing
- **"Molly fading"** : Fire expiration warning
- **"Util on eco/save"** : Economic communication

### 🎯 Execute coordination
**Standard A site execute** :
1. **Smoke deployment** : IGL calls timing
2. **Flash support** : Entry player coordination
3. **Movement sync** : Team push synchronized
4. **Trade setup** : Follow-up positioning

**Retake coordination** :
1. **Utility pooling** : Combine team grenades
2. **Flash chain** : Multiple consecutive flashes
3. **Smoke isolation** : Separate bomb from enemies
4. **Molly control** : Deny defuse/positions

## 🏆 Techniques professionnelles avancées

### 🎪 Advanced utility tricks
**One-way smokes** (CS2 updated) :
- **Mirage window** : Partial smoke gaps
- **Cache main** : Elevation advantage
- **Overpass long** : Height differential smokes

**Fake utility** :
- **Fake flash sounds** : Pull pin without throwing
- **Smoke fakes** : Partial executes
- **Molly fakes** : Sound cues intimidation

**Utility stacking** :
- **Double smoke** : Extended duration/coverage
- **Flash chains** : Consecutive blinding
- **Molly + HE** : Combined area denial

### 🧠 Game sense avec utilities
**Information gathering** :
- **Utility sounds** : Enemy position reveals
- **Bounce feedback** : Spatial awareness
- **Timer awareness** : Smoke/molly durations

**Counter-utility** :
- **Smoke counters** : HE to disperse
- **Flash avoidance** : Sound + positioning
- **Molly extinguish** : Smoke interaction

## 📅 Programme d'entraînement (3 semaines)

### 🗓️ Semaine 1 : Fundamentals
**Objectifs quotidiens** :
- **100 grenades** : Each type practice
- **Jump-throw** : 50 perfect executions
- **Map knowledge** : 5 spots per map
- **Theory** : 30min video analysis

**Exercices pratiques** :
- **yprac maps** : Grenade practice
- **Aim_botz** : Utility + aim combination
- **Retake servers** : Real situation practice

### 🗓️ Semaine 2 : Map specifics
**Focus maps** : Dust2, Mirage, Inferno
- **Essential throws** : 10 per map mastery
- **Team coordination** : 5v5 practice
- **Timing practice** : Execute drills
- **Demo review** : Pro team utility usage

### 🗓️ Semaine 3 : Advanced/Competitive
**Advanced techniques** :
- **One-ways** : 3 spots per map
- **Fake utility** : Psychological warfare
- **Counter-utility** : Adaptive strategies
- **Match application** : Competitive focus

## 🚨 Erreurs communes (à éviter absolument)

❌ **Utility waste** : Grenades sans plan/coordination
❌ **Self-flash** : Blinding teammates/self
❌ **Economic mistakes** : Over-investing utilities
❌ **Timing fails** : Utility non-synchronized
❌ **Predictable patterns** : Same utility usage
❌ **Communication gaps** : No utility callouts

### 💡 Tips finaux de pros

1. **"Utilities win rounds, not aim"** - Career principle
2. **"Perfect practice makes perfect"** - Repetition quality
3. **"Team utility > individual skill"** - Coordination crucial
4. **"Economic discipline = tournament wins"** - Money management
5. **"Adapt utility to enemy patterns"** - Meta game

Les utilitaires représentent 45% de la stratégie CS2 - investissez massivement dans leur maîtrise !
        `,
        links: [
          { name: '💣 Utility practice maps', url: 'https://steamcommunity.com/workshop/browse/?appid=730&searchtext=yprac' },
          { name: '📹 Pro utility analysis', url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' },
          { name: '🎯 Grenade trajectory guide', url: 'https://www.tobyscs.com/csgo-nades/' }
        ],
        tips: [
          'Les utilitaires gagnent plus de rounds que l\'aim - priorité absolue',
          'Jump-throw bind est obligatoire - configurez-le immédiatement',
          'Communication utility = 50% de l\'efficacité - callouts systématiques',
          'Économie utilities : $1400 minimum sur full-buy, discipline absolue',
          'Practice 30min/jour utilities = +2 ranks guaranteed dans 2 mois'
        ]
      }

      // Continuons avec les autres tutoriels...
    };

    return detailedContent[tutorialSlug] || null;
  };

  if (loading) {
    return (
      <div className="tutorial-detail-container">
        <div className="loading">
          <div className="loading-spinner"></div>
          <p>Chargement du tutoriel professionnel...</p>
        </div>
      </div>
    );
  }

  if (!tutorial) {
    return (
      <div className="tutorial-detail-container">
        <div className="error">
          <h2>🔍 Tutoriel non trouvé</h2>
          <p>Ce tutoriel n'existe pas ou n'est pas encore disponible.</p>
          <button onClick={() => navigate('/tutoriels')} className="btn-primary">
            ← Retour aux tutoriels
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="tutorial-detail-container">
      {/* Header avec image */}
      <div className="tutorial-header">
        <div 
          className="tutorial-header-bg"
          style={{
            backgroundImage: `url(${tutorial.image})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat'
          }}
        >
          <div className="tutorial-header-overlay"></div>
        </div>
        
        <div className="tutorial-navigation">
          <button onClick={() => navigate('/tutoriels')} className="back-btn">
            ← Retour aux tutoriels
          </button>
        </div>
        
        <div className="tutorial-info">
          <div className="tutorial-meta">
            <span className={`level-badge ${tutorial.level.toLowerCase()}`}>
              {tutorial.level}
            </span>
            <span className="duration">⏱️ {tutorial.duration}</span>
            <span className="type">🏷️ {tutorial.type}</span>
          </div>
          
          <h1 className="tutorial-title">{tutorial.title}</h1>
          <p className="tutorial-description">{tutorial.description}</p>
        </div>
      </div>

      {/* Objectives */}
      <div className="tutorial-section">
        <h2>🎯 Objectifs d'apprentissage</h2>
        <ul className="objectives-list">
          {tutorial.objectives.map((objective, index) => (
            <li key={index}>
              <span className="objective-number">{index + 1}</span>
              {objective}
            </li>
          ))}
        </ul>
      </div>

      {/* Content */}
      <div className="tutorial-section">
        <h2>📖 Contenu du tutoriel</h2>
        <div className="tutorial-content">
          <div className="content-text" dangerouslySetInnerHTML={{
            __html: tutorial.content
              .replace(/\n/g, '<br>')
              .replace(/## (.*$)/gm, '<h3 class="content-h3">$1</h3>')
              .replace(/### (.*$)/gm, '<h4 class="content-h4">$1</h4>')
              .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
              .replace(/```([\s\S]*?)```/g, '<pre class="code-block">$1</pre>')
              .replace(/`(.*?)`/g, '<code class="inline-code">$1</code>')
          }} />
        </div>
      </div>

      {/* Tips */}
      {tutorial.tips && (
        <div className="tutorial-section">
          <h2>💡 Conseils de pros</h2>
          <div className="tips-list">
            {tutorial.tips.map((tip, index) => (
              <div key={index} className="tip-item">
                <span className="tip-icon">💡</span>
                <p>{tip}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Links */}
      {tutorial.links && (
        <div className="tutorial-section">
          <h2>🔗 Ressources utiles</h2>
          <div className="links-list">
            {tutorial.links.map((link, index) => (
              <a key={index} href={link.url} target="_blank" rel="noopener noreferrer" className="resource-link">
                <span className="link-icon">🌐</span>
                <div>
                  <span className="link-title">{link.name}</span>
                  <small className="link-url">{link.url}</small>
                </div>
              </a>
            ))}
          </div>
        </div>
      )}

      {/* Navigation */}
      <div className="tutorial-navigation-bottom">
        <button onClick={() => navigate('/tutoriels')} className="btn-secondary">
          ← Tous les tutoriels
        </button>
        <div className="tutorial-rating">
          <span>Ce tutoriel vous a-t-il aidé ?</span>
          <div className="rating-buttons">
            <button className="rating-btn">👍</button>
            <button className="rating-btn">👎</button>
          </div>
        </div>
      </div>

      <style jsx>{`
        .tutorial-detail-container {
          max-width: 1000px;
          margin: 0 auto;
          color: #1a1a1a;
          line-height: 1.6;
        }

        .tutorial-header {
          position: relative;
          background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
          color: white;
          border-radius: 0 0 20px 20px;
          overflow: hidden;
          margin-bottom: 40px;
        }

        .tutorial-header-bg {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          opacity: 0.3;
        }

        .tutorial-header-overlay {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: linear-gradient(135deg, rgba(30, 58, 138, 0.9) 0%, rgba(59, 130, 246, 0.8) 100%);
        }

        .tutorial-navigation {
          position: relative;
          z-index: 2;
          padding: 20px 30px 0;
        }

        .back-btn {
          background: rgba(255, 255, 255, 0.15);
          color: white;
          border: 1px solid rgba(255, 255, 255, 0.3);
          padding: 10px 20px;
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.3s;
          font-weight: 500;
        }

        .back-btn:hover {
          background: rgba(255, 255, 255, 0.25);
          transform: translateX(-5px);
        }

        .tutorial-info {
          position: relative;
          z-index: 2;
          padding: 30px;
        }

        .tutorial-meta {
          display: flex;
          gap: 15px;
          margin-bottom: 20px;
          flex-wrap: wrap;
        }

        .level-badge {
          padding: 6px 16px;
          border-radius: 25px;
          font-size: 13px;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .level-badge.débutant {
          background: #10b981;
          color: white;
          box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
        }

        .level-badge.intermédiaire {
          background: #f59e0b;
          color: white;
          box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
        }

        .level-badge.expert {
          background: #ef4444;
          color: white;
          box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
        }

        .duration, .type {
          background: rgba(255, 255, 255, 0.15);
          padding: 6px 16px;
          border-radius: 25px;
          font-size: 13px;
          font-weight: 600;
          border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .tutorial-title {
          font-size: 3rem;
          margin: 0 0 20px 0;
          font-weight: 800;
          text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
          line-height: 1.1;
        }

        .tutorial-description {
          font-size: 1.2rem;
          opacity: 0.95;
          margin: 0;
          line-height: 1.7;
          font-weight: 400;
        }

        .tutorial-section {
          background: white;
          padding: 40px;
          border-radius: 20px;
          margin-bottom: 30px;
          box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
          border: 1px solid #e5e7eb;
        }

        .tutorial-section h2 {
          color: #1e3a8a;
          font-size: 1.8rem;
          margin: 0 0 25px 0;
          font-weight: 700;
          display: flex;
          align-items: center;
          gap: 10px;
        }

        .objectives-list {
          list-style: none;
          padding: 0;
          display: grid;
          gap: 15px;
        }

        .objectives-list li {
          display: flex;
          align-items: flex-start;
          gap: 15px;
          padding: 20px;
          background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
          border-radius: 12px;
          border-left: 4px solid #3b82f6;
          transition: all 0.3s;
        }

        .objectives-list li:hover {
          transform: translateX(5px);
          box-shadow: 0 4px 16px rgba(59, 130, 246, 0.15);
        }

        .objective-number {
          background: #3b82f6;
          color: white;
          width: 28px;
          height: 28px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 700;
          font-size: 14px;
          flex-shrink: 0;
        }

        .tutorial-content {
          background: #fafafa;
          padding: 30px;
          border-radius: 15px;
          border: 1px solid #e5e7eb;
        }

        .content-text {
          font-family: 'Georgia', serif;
          line-height: 1.8;
          color: #1f2937;
          font-size: 16px;
        }

        .content-h3 {
          color: #1e3a8a;
          font-size: 1.5rem;
          margin: 30px 0 15px 0;
          font-weight: 700;
          border-bottom: 2px solid #e5e7eb;
          padding-bottom: 8px;
        }

        .content-h4 {
          color: #374151;
          font-size: 1.2rem;
          margin: 25px 0 12px 0;
          font-weight: 600;
        }

        .code-block {
          background: #1f2937;
          color: #f9fafb;
          padding: 20px;
          border-radius: 8px;
          overflow-x: auto;
          font-family: 'Monaco', 'Consolas', monospace;
          font-size: 14px;
          line-height: 1.6;
          margin: 20px 0;
        }

        .inline-code {
          background: #e5e7eb;
          color: #1f2937;
          padding: 2px 6px;
          border-radius: 4px;
          font-family: 'Monaco', 'Consolas', monospace;
          font-size: 14px;
        }

        .tips-list {
          display: grid;
          gap: 20px;
        }

        .tip-item {
          display: flex;
          align-items: flex-start;
          gap: 20px;
          padding: 25px;
          background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
          border-radius: 15px;
          border-left: 5px solid #3b82f6;
          transition: all 0.3s;
        }

        .tip-item:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
        }

        .tip-icon {
          font-size: 1.5rem;
          flex-shrink: 0;
          background: #3b82f6;
          color: white;
          width: 40px;
          height: 40px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .tip-item p {
          margin: 0;
          line-height: 1.7;
          font-weight: 500;
          color: #1f2937;
        }

        .links-list {
          display: grid;
          gap: 15px;
        }

        .resource-link {
          display: flex;
          align-items: center;
          gap: 20px;
          padding: 20px 25px;
          background: #f8fafc;
          border-radius: 12px;
          text-decoration: none;
          color: #1e3a8a;
          transition: all 0.3s;
          border: 1px solid #e5e7eb;
        }

        .resource-link:hover {
          background: #e2e8f0;
          transform: translateX(5px);
          box-shadow: 0 4px 16px rgba(30, 58, 138, 0.1);
        }

        .link-icon {
          font-size: 1.3rem;
          background: #3b82f6;
          color: white;
          width: 44px;
          height: 44px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
        }

        .link-title {
          font-weight: 600;
          font-size: 16px;
          display: block;
          margin-bottom: 4px;
        }

        .link-url {
          color: #6b7280;
          font-size: 13px;
        }

        .tutorial-navigation-bottom {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 30px;
          margin-bottom: 40px;
        }

        .btn-secondary {
          background: #f3f4f6;
          color: #374151;
          border: 1px solid #d1d5db;
          padding: 12px 24px;
          border-radius: 8px;
          cursor: pointer;
          font-weight: 600;
          transition: all 0.3s;
        }

        .btn-secondary:hover {
          background: #e5e7eb;
          transform: translateX(-5px);
        }

        .tutorial-rating {
          display: flex;
          align-items: center;
          gap: 15px;
        }

        .tutorial-rating span {
          font-weight: 500;
          color: #6b7280;
        }

        .rating-buttons {
          display: flex;
          gap: 8px;
        }

        .rating-btn {
          background: #f3f4f6;
          border: 1px solid #d1d5db;
          width: 40px;
          height: 40px;
          border-radius: 50%;
          cursor: pointer;
          font-size: 1.2rem;
          transition: all 0.3s;
        }

        .rating-btn:hover {
          background: #e5e7eb;
          transform: scale(1.1);
        }

        .loading {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 80px 20px;
          text-align: center;
        }

        .loading-spinner {
          width: 50px;
          height: 50px;
          border: 4px solid #f3f4f6;
          border-top: 4px solid #3b82f6;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin-bottom: 20px;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        .error {
          text-align: center;
          padding: 80px 20px;
        }

        .error h2 {
          color: #ef4444;
          margin-bottom: 15px;
          font-size: 2rem;
        }

        .btn-primary {
          background: linear-gradient(45deg, #3b82f6, #1d4ed8);
          color: white;
          border: none;
          padding: 15px 30px;
          border-radius: 10px;
          cursor: pointer;
          font-weight: 600;
          text-decoration: none;
          display: inline-block;
          margin-top: 25px;
          transition: all 0.3s;
        }

        .btn-primary:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
        }

        @media (max-width: 768px) {
          .tutorial-detail-container {
            margin: 0;
          }

          .tutorial-header {
            border-radius: 0;
          }

          .tutorial-info {
            padding: 20px;
          }

          .tutorial-title {
            font-size: 2.2rem;
          }

          .tutorial-section {
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 15px;
          }

          .tutorial-meta {
            justify-content: center;
            text-align: center;
          }

          .tutorial-navigation-bottom {
            flex-direction: column;
            gap: 20px;
            text-align: center;
          }
        }
      `}</style>
    </div>
  );
};

export default TutorialDetail;