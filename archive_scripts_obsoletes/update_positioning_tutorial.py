import pymongo
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['oupafamilly_db']
collection = db['tutorials']

# Get the existing tutorial to keep the same image
existing_tutorial = collection.find_one({'title': 'Positionnement et angles avancés'})
if existing_tutorial:
    cs2_image = existing_tutorial.get('image', '')
    print(f'Found existing tutorial with image: {len(cs2_image)} characters')
    
    # Professional content inspired by Vitality's positioning mastery
    professional_content = """# 🎯 Positionnement et Angles sur Cartes - Guide Professionnel CS2

## 🌟 Introduction : L'Art du Positionnement Style Vitality

Le **positionnement** est l'essence même du CS2 tactique. Inspiré par les techniques de **Team Vitality** avec **ZywOo**, **apEX** et **Magisk**, ce guide vous enseignera l'art du **game sense avancé** et du **contrôle de carte** pour dominer vos adversaires.

---

## 🗺️ 1. Fondamentaux du Positionnement Professionnel

### 🎯 Philosophie du Positionnement

#### **Principes de Base**
- **Information First** : Chaque position doit apporter de l'information
- **Trade Potential** : Faciliter les trades de teammates
- **Escape Routes** : Toujours avoir une sortie planifiée
- **Angle Advantage** : Maximiser votre avantage visuel

#### **Types de Positions**
- **Positions Défensives** : Tenir angles et zones
- **Positions Offensives** : Prendre contrôle et space
- **Positions Rotatives** : Mobilité et adaptation
- **Positions Utilitaires** : Support et information

### 🧠 Game Sense et Lecture de Carte

#### **Information Gathering**
- **Sound Cues** : Interpréter les bruits de pas
- **Utility Usage** : Analyser l'usage des grenades
- **Timing Windows** : Exploiter les fenêtres temporelles
- **Pattern Recognition** : Identifier les habitudes adverses

#### **Anticipation Tactique**
- **Rotation Prediction** : Anticiper les mouvements
- **Economy Reading** : Adapter selon l'économie
- **Round State** : Ajuster selon la situation
- **Team Coordination** : Synchroniser avec équipe

---

## 🏆 2. Techniques Professionnelles Style Vitality

### 🎯 Maîtrise ZywOo : Positionnement AWP Elite

#### **Contrôle des Angles Longs**
- **Principe** : Dominer les sightlines importantes
- **Technique** : Pré-aim et timing parfait
- **Mobilité** : Rotation rapide entre positions
- **Impact** : Créer pression constante sur adversaire

#### **Positionnement Adaptatif**
- **Lecture Anti-Strat** : Changer positions selon adversaire
- **Utility Coordination** : Synchroniser avec supports
- **Information Trading** : Équilibrer risk/reward
- **Technique ZywOo** : Positions non-standard pour surprise

### 🎪 Leadership apEX : Positionnement IGL

#### **Contrôle de Carte Tactique**
- **Map Control** : Prendre zones clés méthodiquement
- **Information Flow** : Centraliser intel pour décisions
- **Team Positioning** : Coordonner positions d'équipe
- **Timing Mastery** : Orchestrer les mouvements

#### **Positionnement Agressif**
- **Entry Angles** : Positions pour premiers frags
- **Risk Management** : Calculer risques vs rewards
- **Team Setup** : Faciliter trades et support
- **Adaptation** : Ajuster selon feedback

### 🎛️ Intelligence Magisk : Positionnement Utilitaire

#### **Support Positioning**
- **Utility Spots** : Positions optimales pour grenades
- **Crossfire Setup** : Coordination avec teammates
- **Rotation Support** : Faciliter mouvements d'équipe
- **Information Relay** : Transmettre intel efficacement

---

## 🗺️ 3. Positionnement par Cartes

### 🏜️ Dust2 : Contrôle des Longs

#### **Positions Clés T-Side**
- **Long Control** : Pit, Car, Barrels
- **Catwalk Control** : Xbox, Elevator, Cat
- **Tunnels Control** : Lower, Upper, B Platform
- **Mid Control** : Doors, Suicide, Window

#### **Positions Clés CT-Side**
- **Long Defense** : Pit, Car, Site
- **Catwalk Defense** : Goose, Site, Ramp
- **B Defense** : Platform, Closet, Window
- **Mid Defense** : Doors, Catwalk, Connector

#### **Rotations Optimales**
- **A vers B** : Connector, Catwalk, Tunnels
- **B vers A** : Tunnels, Mid, Long
- **Timing** : 15-20 secondes selon route
- **Utility Usage** : Smoke support pour rotations

### 🏛️ Mirage : Contrôle du Mid

#### **Positions Clés T-Side**
- **Mid Control** : Top Mid, Connector, Jungle
- **A Execute** : Ramp, Palace, Tetris
- **B Execute** : Apps, Market, Bench
- **Lurk Spots** : Connector, Palace, Kitchen

#### **Positions Clés CT-Side**
- **Mid Defense** : Connector, Jungle, Ticket
- **A Defense** : Site, Quad, Stairs
- **B Defense** : Site, Apps, Market
- **Rotation** : Connector, Jungle, CT

#### **Crossfires Efficaces**
- **A Site** : Quad + Stairs, Site + Tetris
- **B Site** : Apps + Site, Market + Bench
- **Mid** : Connector + Jungle, Ticket + Top Mid

### 🔥 Inferno : Contrôle des Apps

#### **Positions Clés T-Side**
- **Banana Control** : Car, Logs, Sandbags
- **Apps Control** : Boiler, Stairs, Balcony
- **Mid Control** : Arch, Moto, Second Mid
- **A Execute** : Quad, Pit, Graveyard

#### **Positions Clés CT-Side**
- **Banana Defense** : Site, Spools, Coffins
- **Apps Defense** : Site, Quad, Boiler
- **Mid Defense** : Arch, Library, Apartments
- **A Defense** : Site, Quad, Balcony

---

## 🎯 4. Angles et Sightlines Avancés

### 👁️ Types d'Angles

#### **Angles Communs**
- **Définition** : Positions standard et prévisibles
- **Avantage** : Familiarité et facilité
- **Inconvénient** : Pré-aim adverse facile
- **Usage** : Situations standard et holds

#### **Off-Angles**
- **Définition** : Positions non-standard et inattendues
- **Avantage** : Surprise et désorientation
- **Inconvénient** : Escape difficile
- **Usage** : Rounds anti-éco et surprise

#### **Angles Serrés**
- **Définition** : Exposition minimale du corps
- **Avantage** : Réduction des dégâts potentiels
- **Inconvénient** : Champ de vision réduit
- **Usage** : Défense passive et information

#### **Angles Larges**
- **Définition** : Exposition maximale pour vision
- **Avantage** : Information complète et trades
- **Inconvénient** : Vulnérabilité accrue
- **Usage** : Clears agressifs et entries

### 🔄 Peek Techniques Avancées

#### **Shoulder Peek**
- **Technique** : Exposition partielle pour information
- **Timing** : Rapide in/out pour éviter dégâts
- **Objectif** : Révéler positions sans risque
- **Application** : Scouting et bait shots

#### **Wide Peek**
- **Technique** : Angle large pour avantage
- **Timing** : Rapide pour surprise
- **Objectif** : Désavantager défenseur
- **Application** : Duels agressifs et entries

#### **Jiggle Peek**
- **Technique** : Mouvement A-D-A rapide
- **Timing** : Timing parfait pour éviter hits
- **Objectif** : Information sans exposition
- **Application** : Angles dangereux et scouting

---

## 🛡️ 5. Positionnement Défensif Avancé

### 🏰 Holding Angles

#### **Passive Holding**
- **Principe** : Attendre patiemment l'adversaire
- **Avantage** : Surprise et premier shot
- **Inconvénient** : Prévisibilité long terme
- **Application** : Éco rounds et positions fixes

#### **Active Holding**
- **Principe** : Varier positions et timings
- **Avantage** : Imprévisibilité et adaptation
- **Inconvénient** : Complexité et coordination
- **Application** : Rounds buy et anti-strat

### 🔄 Rotation Défensive

#### **Rotation Complète**
- **Trigger** : Information confirmée d'attaque
- **Timing** : Immédiat après confirmation
- **Route** : Chemin le plus rapide
- **Communication** : Annoncer départ et arrivée

#### **Rotation Partielle**
- **Trigger** : Suspicion d'attaque
- **Timing** : Delayed pour confirmation
- **Route** : Position intermédiaire
- **Communication** : Statut et intentions

#### **Fake Rotation**
- **Trigger** : Bruit intentionnel
- **Timing** : Coordonné avec team
- **Route** : Retour rapide position
- **Communication** : Silence radio

---

## ⚔️ 6. Positionnement Offensif Avancé

### 🗡️ Entry Positioning

#### **Primary Entry**
- **Rôle** : Premier contact avec défense
- **Position** : Angle principal d'attaque
- **Support** : Utility et trade fragging
- **Objective** : Créer ouverture pour team

#### **Secondary Entry**
- **Rôle** : Support et trade du primary
- **Position** : Angle complémentaire
- **Support** : Utility et cleanup
- **Objective** : Exploiter ouverture créée

#### **Lurker Position**
- **Rôle** : Information et flanking
- **Position** : Isolé du groupe principal
- **Support** : Autonomie et timing
- **Objective** : Disruption et picks

### 🎯 Execute Positioning

#### **Standard Execute**
- **Formation** : Groupe coordonné
- **Timing** : Simultané et synchronisé
- **Utility** : Smoke/flash support
- **Objective** : Overwhelm défense

#### **Split Execute**
- **Formation** : Deux groupes séparés
- **Timing** : Coordonné mais angles différents
- **Utility** : Distribution entre groupes
- **Objective** : Diviser attention défensive

#### **Slow Execute**
- **Formation** : Progression méthodique
- **Timing** : Contrôlé et patient
- **Utility** : Usage économique
- **Objective** : Contrôle et information

---

## 🧠 7. Game Sense et Lecture de Jeu

### 📊 Information Processing

#### **Sound Analysis**
- **Footsteps** : Nombre et direction des ennemis
- **Reloads** : Timing et vulnérabilité
- **Utility** : Type et origine des grenades
- **Defuse** : Timing et interruption

#### **Visual Cues**
- **Tracers** : Direction et origine des tirs
- **Utility Effects** : Smokes, flashes, molotovs
- **Player Models** : Positions et équipement
- **Damage Indicators** : Santé et armure

### 🎯 Prediction et Anticipation

#### **Pattern Recognition**
- **Tendances Individuelles** : Habitudes des joueurs
- **Tendances d'Équipe** : Stratégies récurrentes
- **Tendances Situationnelles** : Réactions typiques
- **Tendances Temporelles** : Évolution du match

#### **Timing Windows**
- **Rotation Timing** : Temps de déplacement
- **Utility Timing** : Durée et cooldown
- **Economic Timing** : Cycles d'achat
- **Psychological Timing** : Momentum et pression

---

## 🎮 8. Entraînement et Développement

### 🏋️ Exercices de Positionnement

#### **Exercice 1 : Angle Clearing**
- **Objectif** : Systematic clearing of positions
- **Méthode** : Solo practice sur cartes vides
- **Progression** : Vitesse et précision
- **Durée** : 15 minutes par carte

#### **Exercice 2 : Crossfire Setup**
- **Objectif** : Coordination avec teammate
- **Méthode** : Practice avec partner
- **Progression** : Timing et communication
- **Durée** : 20 minutes par session

#### **Exercice 3 : Rotation Drills**
- **Objectif** : Vitesse et efficacité rotation
- **Méthode** : Chronométrer rotations
- **Progression** : Temps et routes
- **Durée** : 10 minutes par carte

### 📊 Analyse et Amélioration

#### **Demo Analysis**
- **Positionnement** : Analyser choix positions
- **Timing** : Évaluer timing décisions
- **Information** : Utilisation intel disponible
- **Adaptation** : Ajustements mid-round

#### **Pro Study**
- **Vitality VODs** : Étudier positionnement équipe
- **Player POV** : Analyser perspectives individuelles
- **Adaptation** : Intégrer techniques observées
- **Practice** : Reproduire situations

---

## 🏆 9. Conseils des Professionnels

### 🎯 Sagesse ZywOo

#### **Positionnement AWP**
- "Position > Skill dans 70% des situations"
- "Chaque position doit servir l'équipe"
- "Adaptation constante selon adversaire"

#### **Game Sense**
- "Écouter plus que regarder"
- "Anticipation basée sur expérience"
- "Patience dans les décisions"

### 🎪 Leadership apEX

#### **Coordination Équipe**
- "Positionnement collectif > individuel"
- "Communication continue essentielle"
- "Adaptation temps réel crucial"

#### **Contrôle de Carte**
- "Information = pouvoir tactique"
- "Chaque zone a sa valeur"
- "Timing > force brute"

### 🎛️ Intelligence Magisk

#### **Support Positioning**
- "Faciliter teammates avant soi"
- "Utility positioning critique"
- "Consistency > spectaculaire"

#### **Adaptation**
- "Lire adversaire en temps réel"
- "Ajuster sans compromettre team"
- "Patience dans exécution"

---

## 🔥 Conclusion : Maîtriser l'Art du Positionnement

Le **positionnement** n'est pas une position - c'est une **philosophie tactique**. En maîtrisant ces techniques inspirées de **Team Vitality**, vous transformez chaque position en avantage stratégique.

### 🎯 Points Clés à Retenir
- **Information First** : Chaque position doit apporter de l'intel
- **Team Coordination** : Synchroniser avec teammates
- **Adaptation Continue** : Ajuster selon situation
- **Game Sense** : Anticiper et réagir intelligemment

### 🚀 Prochaines Étapes
1. **Maîtriser** les positions clés de vos cartes favorites
2. **Développer** votre game sense par l'observation
3. **Pratiquer** la coordination avec votre équipe
4. **Analyser** les démos des professionnels

---

*Le meilleur positionnement n'est pas celui qui vous met en sécurité - c'est celui qui donne l'avantage à votre équipe.* - Philosophy Team Vitality"""

    # Update the tutorial with professional content
    update_result = collection.update_one(
        {'title': 'Positionnement et angles avancés'},
        {
            '$set': {
                'title': 'Positionnement et angles avancés',
                'description': 'Développez votre game sense et positionnement avec techniques tier 1 inspirées de Vitality pour dominer cartes et angles.',
                'content': professional_content,
                'level': 'intermediate',
                'game': 'cs2',
                'duration': '35 min',
                'type': 'Guide Tactique',
                'author': 'Oupafamilly Pro Team',
                'objectives': [
                    'Maîtriser les positions clés et angles sur Dust2, Mirage et Inferno',
                    'Développer un game sense avancé pour la lecture de carte et anticipation',
                    'Comprendre les techniques de peek et contrôle d\'angles professionnels',
                    'Apprendre la coordination positionnelle et rotations d\'équipe',
                    'Intégrer les philosophies de positionnement de ZywOo, apEX et Magisk'
                ],
                'tips': [
                    'Étudiez les positions de Team Vitality dans leurs matchs officiels',
                    'Pratiquez le clearing systematique des angles sur cartes vides',
                    'Développez votre écoute pour l\'information audio cruciale',
                    'Coordonnez vos positions avec teammates pour crossfires efficaces',
                    'Adaptez constamment votre positionnement selon l\'adversaire'
                ],
                'image': cs2_image
            }
        }
    )
    
    print(f'Tutorial updated successfully: {update_result.modified_count} document(s) modified')
    print('✅ Professional positioning content with Vitality inspiration applied')
    
else:
    print('❌ Could not find existing tutorial')