import pymongo
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['oupafamilly_db']
collection = db['tutorials']

# Get the existing tutorial to keep the same image
existing_tutorial = collection.find_one({'title': 'Mouvement et déplacement optimal'})
if existing_tutorial:
    cs2_image = existing_tutorial.get('image', '')
    print(f'Found existing tutorial with image: {len(cs2_image)} characters')
    
    # Professional content inspired by Vitality's movement techniques
    professional_content = """# 🏃 Mouvement et Déplacement Optimal - Guide Professionnel CS2

## 🌟 Introduction : La Fluidité du Mouvement Style Vitality

Le **mouvement** est l'âme du gameplay CS2. Inspiré par les techniques de **Team Vitality** avec **ZywOo**, **apEX** et **Magisk**, ce guide vous enseignera l'art du **counter-strafe**, **bhop**, et **positionnement pro** pour dominer vos duels.

---

## 🎯 1. Mécaniques de Base du Mouvement CS2

### 🚀 Fondamentaux du Système de Mouvement

#### **Vitesse et Accélération**
- **Vitesse de marche** : 250 unités/seconde
- **Vitesse de course** : 250 unités/seconde (identique à la marche)
- **Accélération** : 5,5 unités/seconde²
- **Décélération** : 10 unités/seconde²

#### **Précision et Mouvement**
- **Mouvement = Imprécision** : Plus vous bougez, moins vous êtes précis
- **Arrêt instantané** : Counter-strafe pour précision maximale
- **Peek timing** : Synchronisation parfaite pour avantage

### 🎪 Mécaniques Avancées

#### **Système de Friction**
- **Friction air** : 0,1 (contrôle en air)
- **Friction sol** : 5,2 (arrêt rapide)
- **Slide distance** : Distance de glissement selon vitesse

#### **Air Strafing**
- **Contrôle aérien** : Mouvement souris + strafe keys
- **Gain de vitesse** : Techniques pour accélérer en air
- **Bhop basics** : Maintenir momentum entre sauts

---

## 🏆 2. Techniques Professionnelles Style Vitality

### 🎯 Maîtrise ZywOo : Précision et Fluidité

#### **Counter-Strafe Perfection**
- **Principe** : Annulation instantanée du momentum
- **Technique** : Appuyer brièvement sur direction opposée
- **Timing** : 0,1 secondes pour arrêt complet
- **Application ZywOo** : Precision parfaite lors des peeks

#### **Jiggle Peek Mastery**
- **Définition** : Mouvement rapide in/out pour information
- **Méthode** : A-D-A rapide pour exposure minimale
- **Avantage** : Collecter intel sans risque
- **Usage pro** : Révéler positions sans engagement

### 🎪 Coordination apEX : Mouvement Tactique

#### **Team Movement Sync**
- **Principe** : Synchronisation des mouvements d'équipe
- **Objectif** : Maximiser trades et support
- **Technique** : Communication timing pour peeks
- **Résultat** : Advantage numérique instantané

#### **Entry Fragger Movement**
- **Aggressive Peeking** : Mouvement rapide pour surprise
- **Wide Peeks** : Angles larges pour désavantager défenseurs
- **Shoulder Peek** : Technique pour bait les shots

### 🎛️ Positionnement Magisk : Intelligence Spatiale

#### **Angle Optimization**
- **Off-Angles** : Positions non-standard pour surprise
- **Crossfire Setup** : Coordination avec teammates
- **Escape Routes** : Toujours planifier la sortie

#### **Map Control Movement**
- **Silent Steps** : Déplacement discret pour flanks
- **Timing Windows** : Exploiter les rotations adverses
- **Zone Control** : Mouvement pour maintenir territory

---

## 🔄 3. Counter-Strafe : La Base de la Précision

### ⚡ Mécaniques du Counter-Strafe

#### **Technique Fondamentale**
- **Mouvement** : Appuyer sur A ou D
- **Arrêt** : Appuyer brièvement sur direction opposée
- **Timing** : Relâcher au bon moment pour arrêt parfait
- **Résultat** : Précision maximale instantanée

#### **Variations Avancées**
- **Quick Peek** : Counter-strafe + peek rapide
- **Delayed Peek** : Pause après counter-strafe pour timing
- **Commit Peek** : Counter-strafe + engagement total

### 🎯 Entraînement Counter-Strafe

#### **Exercice 1 : Arrêt Précis**
1. **Mouvement** : Courir vers la droite (D)
2. **Counter-strafe** : Appuyer A brièvement
3. **Objectif** : Arrêt instantané sans glissement
4. **Répétition** : 50 fois par direction

#### **Exercice 2 : Peek Perfect**
1. **Setup** : Angle pré-défini à dégager
2. **Mouvement** : Peek avec counter-strafe
3. **Tir** : Tirer immédiatement après arrêt
4. **Objectif** : Précision maximale au premier shot

### 📊 Timing et Précision

#### **Timing Optimal**
- **Durée press** : 0,05-0,1 secondes
- **Vitesse réduite** : 0 unités/seconde
- **Précision atteinte** : 100% accuracy
- **Avantage** : Premier shot avantagé

---

## 🐰 4. Bunny Hop : Maintenir le Momentum

### 🚀 Mécaniques du Bhop CS2

#### **Principe de Base**
- **Momentum** : Maintenir vitesse entre sauts
- **Air Strafe** : Contrôle en air avec souris
- **Timing** : Synchronisation parfaite scroll/jump
- **Limitation** : Vitesse cap à 300 unités/seconde

#### **Technique Détaillée**
1. **Pré-vitesse** : Atteindre vitesse maximale
2. **Saut initial** : Jump + strafe simultané
3. **Air control** : Mouvement souris fluide
4. **Atterrissage** : Timing parfait pour enchaîner

### 🎯 Applications Pratiques

#### **Bhop Situationnel**
- **Rotations rapides** : Déplacement entre sites
- **Évasion** : Échapper aux engagements
- **Surprise** : Apparition inattendue
- **Économie** : Moins de bruits de pas

#### **Spots Bhop Utiles**
- **Mirage** : Connector vers A site
- **Inferno** : Apartments vers B site
- **Dust2** : Tunnels vers B site

### 🏋️ Entraînement Bhop

#### **Routine Quotidienne**
1. **Warm-up** : 5 minutes air strafe
2. **Consistency** : 10 bhops consécutifs
3. **Speed** : Maintenir 290+ unités/seconde
4. **Application** : Intégrer en match situations

---

## 🎯 5. Positionnement Professionnel

### 🗺️ Intelligence Spatiale

#### **Angles et Positions**
- **Common Angles** : Positions standard défensives
- **Off-Angles** : Positions non-standard pour surprise
- **Crossfire** : Coordination avec teammates
- **Escape Routes** : Toujours planifier la sortie

#### **Map Awareness**
- **Sound Cues** : Utiliser audio pour positionnement
- **Timing Windows** : Exploiter rotations adverses
- **Utility Usage** : Grenades pour contrôle position

### 🛡️ Positionnement Défensif

#### **Holding Angles**
- **Pré-aim** : Crosshair placement optimal
- **Reaction Time** : Minimiser temps de réaction
- **Surprise Factor** : Positions inattendues
- **Trade Potential** : Faciliter les trades teammates

#### **Rotation Timing**
- **Information** : Quand et comment rotate
- **Speed** : Vitesse de rotation optimale
- **Stealth** : Rotations silencieuses
- **Communication** : Informer teammates

### ⚔️ Positionnement Offensif

#### **Entry Techniques**
- **Wide Peek** : Angles larges pour avantage
- **Shoulder Peek** : Bait shots pour information
- **Jiggle Peek** : Intel gathering sécurisé
- **Commit Peek** : Engagement total calculé

#### **Team Coordination**
- **Sync Peeks** : Peeks simultanés
- **Trade Setup** : Faciliter trades
- **Utility Support** : Grenades pour support

---

## 🎮 6. Techniques Avancées de Peek

### 👁️ Types de Peeks

#### **Wide Peek**
- **Utilisation** : Désavantager défenseur
- **Technique** : Angle large pour voir premier
- **Timing** : Rapide pour surprise
- **Risque** : Exposition prolongée

#### **Shoulder Peek**
- **Utilisation** : Bait shots pour information
- **Technique** : Exposition partielle brève
- **Avantage** : Intel sans risque
- **Timing** : Retrait avant tir adverse

#### **Jiggle Peek**
- **Utilisation** : Information gathering
- **Technique** : A-D-A rapide
- **Avantage** : Difficile à hit
- **Application** : Révéler positions

### 🎯 Peek Timing et Coordination

#### **Solo Peeks**
- **Pré-aim** : Crosshair placement
- **Counter-strafe** : Précision maximale
- **Commit** : Décision engage/disengage
- **Escape** : Plan de sortie

#### **Team Peeks**
- **Synchronisation** : Timing parfait
- **Roles** : Qui peek quoi
- **Communication** : Calls instantanés
- **Trades** : Support immédiat

---

## 🏋️ 7. Entraînement et Développement

### 🎯 Routine d'Entraînement Quotidienne

#### **Échauffement (10 min)**
1. **Counter-strafe** : 5 minutes perfection
2. **Jiggle peek** : 3 minutes répétition
3. **Wide peek** : 2 minutes consistency

#### **Technique Focus (15 min)**
1. **Bhop practice** : 5 minutes air strafe
2. **Angle clearing** : 5 minutes systematic
3. **Peek variety** : 5 minutes different types

#### **Application (10 min)**
1. **1v1 servers** : Mouvement sous pression
2. **Aim maps** : Intégrer mouvement + aim
3. **Scenario practice** : Situations spécifiques

### 📊 Exercices Spécifiques

#### **Exercice 1 : Counter-Strafe Precision**
- **Objectif** : Arrêt parfait à chaque fois
- **Méthode** : Répétition jusqu'à automatisme
- **Métrique** : 95% d'arrêts parfaits
- **Durée** : 10 minutes quotidiennes

#### **Exercice 2 : Peek Consistency**
- **Objectif** : Peeks reproductibles
- **Méthode** : Même angle 50 fois
- **Métrique** : Timing constant
- **Durée** : 15 minutes quotidiennes

#### **Exercice 3 : Movement Under Pressure**
- **Objectif** : Mouvement fluide en combat
- **Méthode** : 1v1 avec focus mouvement
- **Métrique** : Survie increased
- **Durée** : 20 minutes quotidiennes

### 🎯 Progression et Analyse

#### **Métriques de Performance**
- **Accuracy post-movement** : Précision après mouvement
- **Peek success rate** : Réussite des peeks
- **Survival rate** : Survie dans duels
- **Position advantage** : Avantage positionnel

#### **Analyse Vidéo**
- **Demo review** : Analyser mouvement en match
- **Pro comparison** : Comparer avec Vitality
- **Mistake identification** : Identifier erreurs
- **Improvement plan** : Plan d'amélioration

---

## 🔬 8. Mouvement Situationnel

### 🎯 Scenarios de Match

#### **Scenario 1 : Retake Site**
**Situation** : Site pris par adversaires
**Mouvement** : 
- Rotation rapide mais silencieuse
- Peek coordonné avec teammates
- Utilisation cover pour approche

#### **Scenario 2 : Clutch 1v3**
**Situation** : Seul contre plusieurs
**Mouvement** : 
- Repositionnement constant
- Isolation des duels
- Utilisation terrain pour avantage

#### **Scenario 3 : Entry Frag**
**Situation** : Première entrée sur site
**Mouvement** : 
- Wide peek pour surprise
- Commit total après information
- Setup pour trade teammate

### 🏆 Conseils des Pros

#### **ZywOo Philosophy**
- "Mouvement fluide > Mouvement rapide"
- "Chaque peek doit avoir un objectif"
- "Precision avant vitesse"

#### **apEX Wisdom**
- "Synchronisation équipe cruciale"
- "Mouvement agressif mais calculé"
- "Communication pendant mouvement"

#### **Magisk Approach**
- "Positionnement intelligent"
- "Patience dans mouvement"
- "Adaptation constante"

---

## 🔥 Conclusion : Maîtriser l'Art du Mouvement

Le **mouvement** n'est pas juste du déplacement - c'est l'**expression de votre game sense**. En maîtrisant ces techniques inspirées de **Team Vitality**, vous transformez chaque déplacement en avantage tactique.

### 🎯 Points Clés à Retenir
- **Counter-strafe** : Base de toute précision
- **Timing parfait** : Synchronisation avec teammates
- **Positionnement intelligent** : Avantage avant engagement
- **Fluidité constante** : Mouvement naturel et efficace

### 🚀 Prochaines Étapes
1. **Maîtriser** le counter-strafe jusqu'à l'automatisme
2. **Développer** la coordination d'équipe dans les peeks
3. **Analyser** le mouvement des pros en démo
4. **Adapter** votre style selon les situations

---

*Le mouvement parfait n'est pas celui qui impressionne - c'est celui qui vous donne l'avantage au bon moment.* - Philosophy Team Vitality"""

    # Update the tutorial with professional content
    update_result = collection.update_one(
        {'title': 'Mouvement et déplacement optimal'},
        {
            '$set': {
                'title': 'Mouvement et déplacement optimal',
                'description': 'Perfectionnez votre mouvement CS2 avec techniques de counter-strafe, bhop, et positionnement pro pour dominer vos duels.',
                'content': professional_content,
                'level': 'beginner',
                'game': 'cs2',
                'duration': '30 min',
                'type': 'Guide Mouvement',
                'author': 'Oupafamilly Pro Team',
                'objectives': [
                    'Maîtriser parfaitement le counter-strafe pour une précision maximale',
                    'Comprendre les mécaniques du bhop et air strafe pour les rotations',
                    'Développer un positionnement intelligent inspiré des techniques Vitality',
                    'Apprendre les différents types de peeks et leurs applications tactiques',
                    'Intégrer le mouvement fluide dans vos duels et engagements'
                ],
                'tips': [
                    'Entraînez le counter-strafe quotidiennement jusqu\'à l\'automatisme complet',
                    'Étudiez les déplacements de ZywOo, apEX et Magisk dans leurs démos',
                    'Pratiquez chaque type de peek dans des situations réelles de match',
                    'Synchronisez vos mouvements avec vos teammates pour les peeks',
                    'Développez votre game sense pour un positionnement optimal'
                ],
                'image': cs2_image
            }
        }
    )
    
    print(f'Tutorial updated successfully: {update_result.modified_count} document(s) modified')
    print('✅ Professional movement content with Vitality inspiration applied')
    
else:
    print('❌ Could not find existing tutorial')