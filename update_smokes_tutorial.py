import pymongo
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['oupafamilly_db']
collection = db['tutorials']

# Get the existing tutorial to keep the same image
existing_tutorial = collection.find_one({'title': 'Smokes avancées et lineups'})
if existing_tutorial:
    cs2_image = existing_tutorial.get('image', '')
    print(f'Found existing tutorial with image: {len(cs2_image)} characters')
    
    # Professional content inspired by Vitality's smoke mastery
    professional_content = """# 🌫️ Smokes Avancées et Lineups - Guide Professionnel CS2

## 🌟 Introduction : La Maîtrise des Smokes Style Vitality

Les **smokes** sont l'épine dorsale de la stratégie CS2. Inspiré par les techniques de **Team Vitality** avec **ZywOo**, **apEX** et **Magisk**, ce guide vous enseignera la maîtrise des **lineups professionnels** avec les **nouvelles mécaniques volumétriques** CS2 2025.

---

## 🌫️ 1. Mécaniques Smokes CS2 2025

### 🎯 Nouvelle Physique Volumétrique

#### **Système 3D Révolutionnaire**
- **Volumétrie Réaliste** : Fumée avec profondeur et densité
- **Interaction Environnementale** : Adaptation aux surfaces et obstacles
- **Dissipation Naturelle** : Évaporation progressive et réaliste
- **Hauteur Variable** : Différentes densités selon altitude

#### **Mécaniques Avancées**
- **Durée** : 18 secondes de fumée complète
- **Déploiement** : 2 secondes pour expansion totale
- **Rayon** : 144 unités de diamètre
- **Transparence** : Différents niveaux de vision selon position

### 🔬 Nouvelles Propriétés Techniques

#### **One-Way Opportunities**
- **Angles d'Élévation** : Créer avantages visuels
- **Positionnement Précis** : Exploitation des reliefs
- **Timing Critique** : Utilisation des phases d'expansion
- **Contre-Mesures** : Techniques anti-one-way

#### **Interaction Bullets**
- **Pénétration** : Balles traversent fumée sans perte
- **Tracers** : Révélation partielle des trajectoires
- **Spray Patterns** : Maintien précision dans fumée
- **Sound Masking** : Atténuation partielle du son

---

## 🏆 2. Philosophie Smokes Style Vitality

### 🎯 Approche ZywOo : Précision et Timing

#### **Smokes Défensives**
- **Principe** : Contrôler engagements et angles
- **Technique** : Lineups précis pour isolation
- **Timing** : Synchronisation avec rotations
- **Impact** : Forcer adversaire sur angles choisis

#### **Smokes Offensives**
- **Principe** : Créer opportunités d'entry
- **Technique** : Coordination avec flashs
- **Timing** : Exploitation des fenêtres temporelles
- **Impact** : Faciliter prises de sites

### 🎪 Coordination apEX : Leadership et Synchronisation

#### **Smokes d'Équipe**
- **Principe** : Coordination multiple smokes
- **Technique** : Timing parfait entre teammates
- **Timing** : Simultanéité pour impact maximum
- **Impact** : Contrôle total des sightlines

#### **Smokes Tactiques**
- **Principe** : Utilisation stratégique selon plan
- **Technique** : Adaptation mid-round
- **Timing** : Réaction aux informations
- **Impact** : Flexibility tactique

### 🎛️ Utilité Magisk : Support et Facilitation

#### **Smokes de Support**
- **Principe** : Faciliter actions des stars
- **Technique** : Lineups pour teammates
- **Timing** : Anticipation des besoins
- **Impact** : Maximiser potentiel d'équipe

---

## 🗺️ 3. Lineups Professionnels par Cartes

### 🏜️ Dust2 : Contrôle des Longs

#### **Lineups Terroristes**
- **Long Smoke** : Desde spawn, viser croix blanche mur
- **Catwalk Smoke** : Position Xbox, throw par-dessus
- **CT Smoke** : Depuis upper tunnels, bounce mur
- **Car Smoke** : Position long, viser antenne

#### **Lineups Anti-Terroristes**
- **Long Cross** : Depuis pit, bloquer cross
- **Catwalk Block** : Depuis site, couper rotation
- **Tunnels Smoke** : Depuis B, bloquer sortie
- **Mid Control** : Depuis CT, contrôler doors

#### **Smokes Spéciales Dust2**
- **One-Way Long** : Exploitation relief pour avantage
- **Fake A Smoke** : Misdirection pour split B
- **Retake Smokes** : Isolation post-plant
- **Save Smokes** : Faciliter saves économiques

### 🏛️ Mirage : Domination du Mid

#### **Lineups Terroristes**
- **CT Smoke** : Depuis ramp, viser angle bâtiment
- **Jungle Smoke** : Position connector, throw diagonal
- **Stairs Smoke** : Depuis palace, bounce mur
- **Connector Smoke** : Depuis T spawn, arc parfait

#### **Lineups Anti-Terroristes**
- **Top Mid** : Depuis connector, bloquer vision
- **Ramp Smoke** : Depuis jungle, ralentir push
- **Palace Smoke** : Depuis A site, couper flanks
- **Market Smoke** : Depuis B, faciliter rotations

#### **Smokes Avancées Mirage**
- **Triple Smoke A** : CT + Jungle + Stairs simultané
- **Mid Control** : Coordination pour domination
- **Retake Sequences** : Smokes échelonnés
- **Eco Denial** : Bloquer rushes économiques

### 🔥 Inferno : Maîtrise des Appartements

#### **Lineups Terroristes**
- **Spools Smoke** : Depuis apartments, viser coin
- **CT Smoke** : Position balcon, throw précis
- **Coffins Smoke** : Depuis banana, arc optimal
- **Quad Smoke** : Position pit, viser angle

#### **Lineups Anti-Terroristes**
- **Banana Smoke** : Depuis site, bloquer advance
- **Apartments** : Depuis quad, ralentir rush
- **Arch Smoke** : Depuis library, contrôler mid
- **Balcony** : Depuis site, couper flanks

#### **Smokes Complexes Inferno**
- **Apartments Execute** : Séquence 3 smokes
- **Banana Control** : Smokes échelonnés
- **Site Retakes** : Coordination post-plant
- **Anti-Rush** : Smokes défensifs rapides

---

## 🎯 4. Techniques Avancées de Lancement

### 🎮 Types de Throws

#### **Lineups Statiques**
- **Avantage** : Précision maximale garantie
- **Inconvénient** : Vulnérabilité pendant setup
- **Usage** : Préparation pré-round
- **Exemple** : Smokes depuis spawn positions

#### **Lineups Dynamiques**
- **Avantage** : Flexibilité et adaptation
- **Inconvénient** : Précision variable
- **Usage** : Réaction mid-round
- **Exemple** : Smokes depuis positions variables

#### **Lineups de Mouvement**
- **Avantage** : Unpredictability et vitesse
- **Inconvénient** : Difficulté technique
- **Usage** : Situations pressées
- **Exemple** : Running throws coordonnés

### 🎯 Mécaniques de Précision

#### **Alignement Visuel**
- **Crosshair Placement** : Positionnement précis
- **Reference Points** : Utilisation landmarks
- **Angle Compensation** : Ajustement selon position
- **Consistency** : Reproduction fidèle

#### **Timing et Séquences**
- **Wind-Up Time** : Temps préparation throw
- **Release Timing** : Moment optimal lancement
- **Coordination** : Synchronisation avec team
- **Adaptation** : Ajustement selon situation

---

## 🧠 5. Stratégies et Coordination

### 🎯 Smokes d'Exécution

#### **Standard Executes**
- **Préparation** : Positioning préalable
- **Timing** : Lancement coordonné
- **Suivi** : Exploitation immediate
- **Backup** : Plans alternatifs

#### **Fast Executes**
- **Préparation** : Minimal setup
- **Timing** : Lancement rapide
- **Suivi** : Entry agressive
- **Backup** : Adaptation instantanée

#### **Slow Executes**
- **Préparation** : Setup méticuleux
- **Timing** : Timing patient
- **Suivi** : Progression contrôlée
- **Backup** : Multiple options

### 🛡️ Smokes Défensives

#### **Retake Smokes**
- **Isolation** : Séparer adversaires
- **Confusion** : Désorienter ennemis
- **Positioning** : Faciliter positionnement
- **Timing** : Coordination avec team

#### **Rotation Smokes**
- **Cover** : Protection déplacements
- **Misdirection** : Tromper adversaire
- **Speed** : Accélérer rotations
- **Safety** : Réduire risques

---

## 🎮 6. Entraînement et Perfectionnement

### 🏋️ Routine d'Entraînement

#### **Échauffement Lineups (10 min)**
1. **Mirage CT** : 5 répétitions parfaites
2. **Dust2 Long** : 5 répétitions précises
3. **Inferno Spools** : 5 répétitions fluides

#### **Consistency Training (15 min)**
1. **Même Lineup** : 10 répétitions identiques
2. **Chrono Challenge** : Vitesse vs précision
3. **Pressure Test** : Sous stress temporel

#### **Application Pratique (20 min)**
1. **Deathmatch** : Intégrer smokes en combat
2. **Retake Servers** : Smokes en situation
3. **Team Practice** : Coordination avec équipe

### 📊 Exercices Spécifiques

#### **Exercice 1 : Pixel Perfect**
- **Objectif** : Précision absolue lineups
- **Méthode** : Référence visuelle constante
- **Mesure** : Emplacement fumée parfait
- **Progression** : 95% de réussite

#### **Exercice 2 : Speed Smokes**
- **Objectif** : Vitesse d'exécution
- **Méthode** : Chronométrer chaque throw
- **Mesure** : Temps setup + lancement
- **Progression** : Sub-3 secondes

#### **Exercice 3 : Coordination**
- **Objectif** : Synchronisation d'équipe
- **Méthode** : Smokes simultanés
- **Mesure** : Timing parfait
- **Progression** : 0,5 secondes écart max

---

## 🔬 7. Techniques Avancées et Innovations

### 🎯 One-Way Mastery

#### **Mécaniques One-Way**
- **Principe** : Exploitation différences hauteur
- **Technique** : Positionnement précis
- **Timing** : Utilisation phases fumée
- **Counter** : Reconnaissance et adaptation

#### **Spots One-Way Populaires**
- **Mirage Connector** : Depuis jungle
- **Dust2 Xbox** : Depuis catwalk
- **Inferno Banana** : Depuis car
- **Cache Quad** : Depuis site

### 🌪️ Smokes Créatives

#### **Fake Smokes**
- **Principe** : Misdirection tactique
- **Technique** : Smoke visible sans engagement
- **Timing** : Coordination avec vraie attaque
- **Impact** : Force rotations adverses

#### **Delayed Smokes**
- **Principe** : Timing décalé pour surprise
- **Technique** : Lancement après initial
- **Timing** : Exploitation confusion
- **Impact** : Désorientation défense

### 🎪 Anti-Smokes Strategies

#### **Spam Spots**
- **Principe** : Tirer dans fumées communes
- **Technique** : Pré-aim positions standards
- **Timing** : Après déploiement fumée
- **Impact** : Punir positioning prévisible

#### **Utility Clearing**
- **Principe** : HE/Molotov pour clear fumées
- **Technique** : Coordination explosifs
- **Timing** : Avant expiration fumée
- **Impact** : Révéler positions cachées

---

## 🏆 8. Conseils des Professionnels

### 🎯 Philosophie ZywOo

#### **Precision First**
- "Lineup parfait > Timing parfait"
- "Pratique quotidienne = muscle memory"
- "Adaptation selon adversaire crucial"

#### **Game Integration**
- "Smokes = extension de votre aim"
- "Coordination avec team prioritaire"
- "Patience dans l'exécution"

### 🎪 Leadership apEX

#### **Team Coordination**
- "Communication avant action"
- "Timing collectif > skill individuel"
- "Backup plans toujours prêts"

#### **Tactical Usage**
- "Chaque smoke doit servir stratégie"
- "Adaptation mid-round essentielle"
- "Information guide utilisation"

### 🎛️ Support Magisk

#### **Utility Mastery**
- "Faciliter teammates avant soi"
- "Anticipation des besoins"
- "Consistency dans l'exécution"

#### **Continuous Learning**
- "Analyser échecs pour amélioration"
- "Innover sur lineups existants"
- "Partager knowledge avec team"

---

## 🔥 Conclusion : Maîtriser l'Art des Smokes

Les **smokes** ne sont pas de simples outils de blocage - elles sont l'**expression de votre vision tactique**. En maîtrisant ces techniques inspirées de **Team Vitality**, vous transformez chaque fumée en avantage stratégique.

### 🎯 Points Clés à Retenir
- **Precision Absolue** : Lineups parfaits par répétition
- **Timing Coordination** : Synchronisation avec teammates
- **Adaptation Tactique** : Ajustement selon situation
- **Innovation Continue** : Développement nouveaux lineups

### 🚀 Prochaines Étapes
1. **Maîtriser** 20 lineups essentiels parfaitement
2. **Développer** la coordination d'équipe
3. **Innover** avec nouvelles mécaniques CS2
4. **Analyser** l'usage des pros constamment

---

*Une smoke parfaitement placée ne cache pas seulement la vision - elle révèle l'intelligence tactique de celui qui l'a lancée.* - Philosophy Team Vitality"""

    # Update the tutorial with professional content
    update_result = collection.update_one(
        {'title': 'Smokes avancées et lineups'},
        {
            '$set': {
                'title': 'Smokes avancées et lineups',
                'description': 'Maîtrisez les smokes CS2 2025 avec 50+ lineups professionnels, nouvelles mécaniques volumétriques et coordination d\'équipe.',
                'content': professional_content,
                'level': 'intermediate',
                'game': 'cs2',
                'duration': '40 min',
                'type': 'Guide Utilities',
                'author': 'Oupafamilly Pro Team',
                'objectives': [
                    'Maîtriser 50+ lineups professionnels sur Dust2, Mirage et Inferno',
                    'Comprendre les nouvelles mécaniques volumétriques CS2 2025',
                    'Développer la coordination d\'équipe pour smokes synchronisés',
                    'Apprendre les techniques avancées : one-ways, fakes, et anti-smokes',
                    'Intégrer les philosophies de smokes de ZywOo, apEX et Magisk'
                ],
                'tips': [
                    'Entraînez-vous quotidiennement avec 10 lineups jusqu\'à la perfection',
                    'Étudiez les smokes de Team Vitality dans leurs matchs officiels',
                    'Maîtrisez les nouvelles mécaniques volumétriques pour one-ways',
                    'Coordonnez vos smokes avec teammates pour impact maximum',
                    'Innovez constamment avec de nouveaux lineups selon les updates'
                ],
                'image': cs2_image
            }
        }
    )
    
    print(f'Tutorial updated successfully: {update_result.modified_count} document(s) modified')
    print('✅ Professional smokes content with Vitality inspiration applied')
    
else:
    print('❌ Could not find existing tutorial')