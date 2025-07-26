import pymongo
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['oupafamilly_db']
collection = db['tutorials']

# Get the existing tutorial to keep the same image
existing_tutorial = collection.find_one({'title': 'Utilisation des grenades de base'})
if existing_tutorial:
    cs2_image = existing_tutorial.get('image', '')
    print(f'Found existing tutorial with image: {len(cs2_image)} characters')
    
    # Professional content inspired by Vitality's utility usage
    professional_content = """# 💣 Utilisation des Grenades de Base - Guide Professionnel CS2

## 🌟 Introduction : La Maîtrise des Utilities Style Vitality

L'utilisation des **grenades** sépare les joueurs amateurs des professionnels. Inspiré par les techniques de **Team Vitality** avec **ZywOo**, **apEX** et **Magisk**, ce guide vous enseignera l'art des **4 types de grenades** CS2 avec les **timings** et **techniques** des équipes Tier 1.

---

## 💥 1. Les 4 Types de Grenades CS2

### 🎯 Arsenal Complet des Utilities

#### **HE Grenade (Explosive)**
- **Coût** : 300$ (T et CT)
- **Dégâts** : 98 maximum (diminue avec distance)
- **Utilisation** : Dégâts de zone et finitions
- **Timing** : 1,6 secondes avant explosion

#### **Smoke Grenade (Fumigène)**
- **Coût** : 300$ (T et CT)
- **Durée** : 18 secondes
- **Utilisation** : Blocage de vision et contrôle de zone
- **Timing** : 2 secondes avant déploiement

#### **Flashbang (Aveuglante)**
- **Coût** : 200$ (T et CT)
- **Durée** : 2-5 secondes selon distance
- **Utilisation** : Aveuglement et création d'opportunities
- **Timing** : 1,5 secondes avant explosion

#### **Molotov/Incendiary (Incendiaire)**
- **Coût** : 400$ (T) / 600$ (CT)
- **Durée** : 7 secondes
- **Utilisation** : Contrôle de zone et denial
- **Timing** : Impact immédiat

---

## 🏆 2. Techniques Professionnelles Style Vitality

### 🎯 Philosophie ZywOo : Précision et Timing

#### **Pop Flash Mastery**
- **Définition** : Flash qui explose immédiatement après le corner
- **Technique** : Lancé à 45° vers le mur pour rebond optimal
- **Timing** : 0,5 secondes avant peek pour synchronisation parfaite
- **Usage ZywOo** : Création d'opportunities sur angles difficiles

#### **Utility Combo Precision**
- **Smoke + Flash** : Flash par-dessus smoke pour désorienter
- **HE + Flash** : Explosion suivie de flash pour maximiser dégâts
- **Molotov + Smoke** : Contrôle multi-layer pour déni de zone

### 🎪 Coordination apEX : Leadership et Timing d'Équipe

#### **Utility Stacking**
- **Principe** : Concentrer plusieurs utilities sur un objectif
- **Exemple** : 2 flashs + 1 smoke pour execute A site
- **Timing** : Synchronisation parfaite entre teammates
- **Résultat** : Overwhelm de la défense adverse

#### **Delayed Utility Usage**
- **Stratégie** : Utiliser les grenades avec délai calculé
- **Objectif** : Contrôler le pace et forcer les rotations
- **Application** : Smoke delayed pour fake puis rotate

### 🎛️ Adaptabilité Magisk : Réaction et Flexibilité

#### **Situational Awareness**
- **Mid-Round Adjustments** : Adapter l'usage selon situation
- **Information-Based Usage** : Utiliser selon intel gathéré
- **Defensive Utility** : Maximiser impact en situation défensive

---

## 🎯 3. Techniques Avancées par Grenade

### 💥 HE Grenade : Dégâts Maximisés

#### **Mécaniques de Dégâts**
- **Dégâts par Distance** :
  - 0-50 unités : 98 dégâts
  - 51-100 unités : 85 dégâts
  - 101-150 unités : 65 dégâts
  - 151-200 unités : 45 dégâts

#### **Techniques Professionnelles**
- **Bounce Timing** : Utiliser les rebonds pour timing parfait
- **Prediction Throws** : Anticiper les mouvements adverses
- **Combo Finisher** : Terminer les ennemis low HP

#### **Spots Clés par Carte**
- **Mirage** : Connector, Ramp, Jungle
- **Inferno** : Banana, Apartments, Pit
- **Dust2** : Long corner, Tunnels, Catwalk

### 🌫️ Smoke Grenade : Contrôle Territorial

#### **Mécaniques Avancées**
- **One-Way Smokes** : Créer des avantages visuels
- **Smoke Lineups** : Positions précises pour spots clés
- **Timing Perfect** : Lancer au bon moment pour maximiser impact

#### **Techniques Style Vitality**
- **Map Control Smokes** : Bloquer les rotations adverses
- **Execute Smokes** : Faciliter les prises de sites
- **Defensive Smokes** : Ralentir les rushes adverses

#### **Lineups Essentiels**
- **Mirage A** : Smoke CT, Jungle, Stairs
- **Inferno B** : Smoke Spools, New Box, Coffins
- **Dust2 A** : Smoke Long, Catwalk, CT

### ⚡ Flashbang : Création d'Opportunities

#### **Types de Flashs**
- **Pop Flash** : Explosion immédiate après corner
- **Shoulder Flash** : Flash par-dessus épaule teammate
- **Bank Flash** : Rebond sur mur pour angle parfait
- **Deep Flash** : Flash profond pour clear zone

#### **Timing et Coordination**
- **Self Flash** : 0,5 secondes avant peek
- **Team Flash** : Communication précise pour timing
- **Counter Flash** : Réponse aux flashs adverses

#### **Anti-Flash Techniques**
- **Turn Away** : Rotation 180° pour réduire effet
- **Wall Facing** : Regarder mur pour minimiser impact
- **Prefire Common** : Tirer sur angles communs même flashé

### 🔥 Molotov/Incendiary : Contrôle de Zone

#### **Mécaniques de Dégâts**
- **Dégâts par Seconde** : 8 HP/seconde
- **Dégâts Totaux** : 56 HP maximum
- **Zone d'Effect** : Rayon de 144 unités

#### **Utilisations Tactiques**
- **Site Denial** : Empêcher plant/defuse
- **Slow Push** : Ralentir advance adverse
- **Force Rotation** : Forcer mouvements adverses

#### **Spots Stratégiques**
- **Mirage** : Default plant, Jungle, Connector
- **Inferno** : Banana, New Box, Balcony
- **Dust2** : Long corner, Tunnels exit, Default plant

---

## 🧠 4. Stratégies d'Équipe et Coordination

### 🎯 Execute Protocols Style Vitality

#### **Standard Execute Pattern**
1. **Setup Phase** : Positionnement et préparation utilities
2. **Utility Deploy** : Lancement coordonné des grenades
3. **Entry Phase** : Entrée synchronisée après utilities
4. **Trade Phase** : Support et trades après entry

#### **Exemples d'Executes**
- **Mirage A Execute** : Smoke CT + Flash Ramp + Molotov Jungle
- **Inferno B Execute** : Smoke Spools + Flash Apps + HE Site
- **Dust2 A Execute** : Smoke Long + Flash Catwalk + Molotov Site

### 🛡️ Defensive Utility Usage

#### **Retake Strategies**
- **Isolation** : Séparer les adversaires avec smokes
- **Disable** : Flasher pour désavantager ennemis
- **Damage** : HE pour affaiblir avant engagement
- **Deny** : Molotov pour empêcher positions

#### **Hold Strategies**
- **Delay** : Smokes pour ralentir advance
- **Information** : HE pour révéler positions
- **Punishment** : Molotov pour punir aggressive plays

---

## 🎮 5. Entraînement et Développement

### 🏋️ Routine d'Entraînement Quotidienne

#### **Warm-up Utility (15 min)**
1. **Lineups Practice** : 5 smokes essentiels par carte
2. **Flash Timing** : 10 pop flashs parfaits
3. **HE Bounces** : 5 rebonds techniques
4. **Molotov Spreads** : 3 zones de contrôle

#### **Coordination Drills (20 min)**
1. **Team Executes** : 3 executes par site
2. **Retake Scenarios** : 5 retakes coordonnés
3. **Utility Trades** : Échanges d'utilities optimaux
4. **Communication** : Calls précis pour utilities

### 🎯 Exercices Spécifiques

#### **Exercice 1 : Lineups Mastery**
- **Objectif** : Mémoriser 20 lineups essentiels
- **Méthode** : Répétition quotidienne jusqu'à automatisme
- **Test** : Exécution sous pression en 3 secondes max

#### **Exercice 2 : Timing Perfect**
- **Objectif** : Synchroniser utilities avec peek
- **Méthode** : Metronome mental pour timing
- **Test** : 90% de réussite sur 10 tentatives

#### **Exercice 3 : Utility Economy**
- **Objectif** : Maximiser impact avec budget limité
- **Méthode** : Scenarios avec contraintes financières
- **Test** : Efficacité mesurée en impact/dollar

### 📊 Analyse et Amélioration

#### **Metrics de Performance**
- **Utility Success Rate** : % d'utilities ayant impact
- **Timing Accuracy** : Précision des timings
- **Damage per Utility** : Dégâts moyens par grenade
- **Team Coordination** : Synchronisation d'équipe

#### **Demo Analysis Focus**
- **Utility Usage** : Quand et comment utiliser
- **Timing Mistakes** : Erreurs de synchronisation
- **Missed Opportunities** : Occasions ratées
- **Professional Comparison** : Comparaison avec pros

---

## 🔬 6. Mécaniques CS2 Avancées

### 🎯 Nouvelles Mécaniques 2025

#### **Smoke Volumétrique**
- **Nouveauté** : Système de fumée 3D réaliste
- **Impact** : One-ways plus complexes
- **Adaptation** : Nouveaux lineups requis

#### **Physics Améliorées**
- **Rebonds** : Physique plus réaliste
- **Bounces** : Calculs précis requis
- **Timing** : Ajustements nécessaires

### 🧪 Techniques Expérimentales

#### **Utility Combos Avancés**
- **Triple Flash** : 3 flashs coordonnés
- **Smoke Wall** : Mur de fumée complet
- **HE Cascade** : Explosions en chaîne

#### **Anti-Utility Tactics**
- **Smoke Disruption** : Perturber les smokes adverses
- **Flash Counters** : Répondre aux flashs
- **Molotov Denial** : Empêcher les molotovs

---

## 📚 7. Situations Spécifiques et Solutions

### 🎯 Scenarios Courants

#### **Scenario 1 : Retake Site**
**Situation** : Site pris par adversaires
**Solution** : 
- Smoke pour isoler
- Flash pour aveugler
- HE pour damage
- Molotov pour deny

#### **Scenario 2 : Slow Push**
**Situation** : Advance méthodique
**Solution** : 
- Smokes pour vision
- Flash pour clear angles
- HE pour damage chip
- Molotov pour contrôle

#### **Scenario 3 : Fast Rush**
**Situation** : Rush rapide adverse
**Solution** : 
- Molotov pour ralentir
- HE pour damage groupe
- Flash pour désorienter
- Smoke pour repositionner

### 🏆 Conseils de Pros

#### **ZywOo Tips**
- "Timing parfait > Lineups parfaits"
- "Adapter utilities selon situation"
- "Garder grenades pour moments clés"

#### **apEX Wisdom**
- "Coordination équipe > Skill individuel"
- "Communication avant action"
- "Utility = Extension de votre aim"

---

## 🔥 Conclusion : Maîtriser l'Art des Grenades

Les **grenades** ne sont pas de simples outils - elles sont l'**extension tactique** de votre gameplay. En maîtrisant ces techniques inspirées de **Team Vitality**, vous transformez chaque utility en avantage stratégique.

### 🎯 Points Clés à Retenir
- **Precision avant Power** : Timing parfait plus important que damage
- **Coordination d'Équipe** : Utilities synchronisées = Impact maximum
- **Adaptation Constante** : Ajuster selon situation et adversaire
- **Practice Quotidienne** : Muscle memory pour utilities

### 🚀 Prochaines Étapes
1. **Maîtriser** les 20 lineups essentiels
2. **Pratiquer** le timing parfait quotidiennement
3. **Développer** la coordination d'équipe
4. **Analyser** l'usage des pros en démo

---

*Les grenades ne font pas de vous un meilleur joueur - c'est leur maîtrise qui fait la différence entre amateur et professionnel.* - Philosophy Team Vitality"""

    # Update the tutorial with professional content
    update_result = collection.update_one(
        {'title': 'Utilisation des grenades de base'},
        {
            '$set': {
                'title': 'Utilisation des grenades de base',
                'description': 'Maîtrisez les 4 types de grenades CS2 avec techniques professionnelles et timings utilisés par les équipes tier 1.',
                'content': professional_content,
                'level': 'beginner',
                'game': 'cs2',
                'duration': '25 min',
                'type': 'Guide Utilities',
                'author': 'Oupafamilly Pro Team',
                'objectives': [
                    'Comprendre les 4 types de grenades CS2 et leurs mécaniques',
                    'Maîtriser les techniques de timing et coordination style Vitality',
                    'Développer les lineups essentiels et pop flashs professionnels',
                    'Apprendre l\'usage tactique des utilities en situation de match',
                    'Perfectionner la coordination d\'équipe avec les grenades'
                ],
                'tips': [
                    'Entraînez-vous aux lineups quotidiennement jusqu\'à l\'automatisme',
                    'Étudiez les timings de ZywOo et apEX dans leurs démos',
                    'Priorisez la coordination d\'équipe sur les skills individuels',
                    'Adaptez votre usage des utilities selon la situation du match',
                    'Gardez toujours vos grenades pour les moments clés'
                ],
                'image': cs2_image
            }
        }
    )
    
    print(f'Tutorial updated successfully: {update_result.modified_count} document(s) modified')
    print('✅ Professional grenades content with Vitality inspiration applied')
    
else:
    print('❌ Could not find existing tutorial')