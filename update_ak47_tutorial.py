import pymongo
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['oupafamilly_db']
collection = db['tutorials']

# Get the existing tutorial to keep the same image
existing_tutorial = collection.find_one({'title': 'Contrôle de recul avancé (AK-47)'})
if existing_tutorial:
    cs2_image = existing_tutorial.get('image', '')
    print(f'Found existing tutorial with image: {len(cs2_image)} characters')
    
    # Professional content inspired by Vitality's AK-47 mastery
    professional_content = """# 🔥 Contrôle de Recul Avancé (AK-47) - Guide Professionnel CS2

## 🌟 Introduction : La Maîtrise de l'AK-47 Style Vitality

L'**AK-47** est l'arme signature des terroristes CS2. Inspiré par les techniques de **Team Vitality** avec **ZywOo**, ce guide vous enseignera la maîtrise parfaite du **spray pattern** avec les **mécaniques CS2 2025** et **méthodes d'entraînement professionnelles**.

---

## 🎯 1. Mécaniques AK-47 CS2 2025

### 📊 Statistiques Complètes

#### **Caractéristiques de Base**
- **Coût** : 2 700$ (Terroristes uniquement)
- **Dégâts** : 36 dégâts corps, 144 dégâts tête (sans casque)
- **Cadence de tir** : 600 coups/minute
- **Capacité** : 30 balles par chargeur

#### **Mécaniques de Précision**
- **Précision debout** : 73% (stationnaire)
- **Précision en mouvement** : 25% (pénalité sévère)
- **Temps de récupération** : 0,35 secondes
- **Pénétration** : 77,5% (excellente contre armure)

### 🎯 Physique du Recul CS2

#### **Pattern de Recul**
- **Balles 1-3** : Recul vertical pur (compensation vers le bas)
- **Balles 4-8** : Recul diagonal gauche (compensation bas-droite)
- **Balles 9-15** : Recul diagonal droite (compensation bas-gauche)
- **Balles 16-30** : Pattern horizontal alternant

#### **Mécaniques Avancées**
- **Reset Time** : 0,4 secondes pour reset complet
- **Spray Decay** : Réduction progressive du recul
- **Movement Penalty** : Multiplication x4 du recul en mouvement

---

## 🏆 2. Techniques Professionnelles Style Vitality

### 🎯 Maîtrise ZywOo : Contrôle Absolu

#### **Spray Control Perfection**
- **Principe** : Mouvement souris opposé au pattern
- **Technique** : Compensation fluide et progressive
- **Timing** : Synchronisation parfaite avec cadence
- **Résultat** : Grouping serré même à longue distance

#### **Burst Fire Mastery**
- **Définition** : Tirs par salves de 3-5 balles
- **Avantage** : Précision maintenue, reset rapide
- **Application** : Distances moyennes à longues
- **Technique ZywOo** : Synchronisation avec peek timing

### 🎪 Adaptation apEX : Flexibilité Tactique

#### **Situational Spraying**
- **Close Range** : Spray complet avec compensation
- **Medium Range** : Bursts contrôlés
- **Long Range** : Taps précis seulement
- **Stress Control** : Maintenir technique sous pression

#### **Team Coordination**
- **Spray Timing** : Synchroniser avec teammates
- **Utility Support** : Utiliser grenades pour spray
- **Trade Setup** : Positionner pour trades faciles

### 🎛️ Precision Magisk : Consistance Technique

#### **Mechanical Consistency**
- **Muscle Memory** : Automatisation des mouvements
- **Crosshair Placement** : Pré-aim optimal
- **Trigger Discipline** : Savoir quand spray/burst/tap

---

## 🎮 3. Pattern de Recul Détaillé

### 📈 Décomposition par Phases

#### **Phase 1 : Balles 1-3 (Contrôle Vertical)**
- **Mouvement** : Tirer vers le bas progressivement
- **Vitesse** : Lente au début, accélération
- **Distance** : 15 pixels vers le bas
- **Difficulté** : Faible (pattern prévisible)

#### **Phase 2 : Balles 4-8 (Transition Gauche)**
- **Mouvement** : Bas + légèrement droite
- **Vitesse** : Maintenir rythme constant
- **Distance** : 10 pixels bas-droite
- **Difficulté** : Modérée (changement direction)

#### **Phase 3 : Balles 9-15 (Compensation Droite)**
- **Mouvement** : Bas + droite vers gauche
- **Vitesse** : Mouvement fluide
- **Distance** : 20 pixels bas-gauche
- **Difficulté** : Élevée (précision requise)

#### **Phase 4 : Balles 16-30 (Pattern Horizontal)**
- **Mouvement** : Alternance gauche-droite
- **Vitesse** : Rapide et précise
- **Distance** : 15 pixels alternés
- **Difficulté** : Très élevée (maîtrise experte)

### 🎯 Techniques de Compensation

#### **Méthode Graduelle**
- **Principe** : Compensation progressive du recul
- **Technique** : Mouvement continu et fluide
- **Avantage** : Contrôle naturel et intuitif
- **Inconvénient** : Nécessite pratique intensive

#### **Méthode Par Segments**
- **Principe** : Découper le pattern en segments
- **Technique** : Mouvements distincts par phase
- **Avantage** : Apprentissage structuré
- **Inconvénient** : Transitions moins fluides

---

## 🏋️ 4. Méthodes d'Entraînement Professionnelles

### 🎯 Routine d'Entraînement Quotidienne

#### **Échauffement (10 min)**
1. **Taps Singles** : 50 tirs précis longue distance
2. **Bursts Courts** : 30 salves de 3 balles
3. **Spray Mur** : 20 sprays complets contre mur

#### **Technique Focus (20 min)**
1. **Pattern Memorization** : 10 minutes répétition pattern
2. **Distance Variation** : 5 minutes courte/moyenne/longue
3. **Movement Integration** : 5 minutes spray + mouvement

#### **Application Réelle (15 min)**
1. **Aim_botz** : 100 éliminations spray uniquement
2. **Recoil Master** : 10 minutes pattern parfait
3. **Deathmatch** : 15 minutes AK-47 seulement

### 📊 Exercices Spécifiques

#### **Exercice 1 : Mur Pattern**
- **Objectif** : Mémoriser le pattern visuellement
- **Méthode** : Spray contre mur, observer impacts
- **Progression** : Pattern de plus en plus serré
- **Durée** : 10 minutes quotidiennes

#### **Exercice 2 : Cibles Multiples**
- **Objectif** : Transitions rapides entre cibles
- **Méthode** : Spray transfer entre bots
- **Progression** : Vitesse et précision accrues
- **Durée** : 15 minutes quotidiennes

#### **Exercice 3 : Mouvement Intégré**
- **Objectif** : Spray pendant déplacement
- **Méthode** : Counter-strafe + spray immédiat
- **Progression** : Fluidité et timing
- **Durée** : 10 minutes quotidiennes

### 🎯 Progression Structurée

#### **Semaine 1 : Fondamentaux**
- **Objectif** : Maîtriser les 15 premières balles
- **Focus** : Pattern vertical et transition
- **Mesure** : 70% des balles dans cercle 10cm
- **Durée** : 45 minutes quotidiennes

#### **Semaine 2 : Pattern Complet**
- **Objectif** : Maîtriser spray 30 balles
- **Focus** : Phase horizontale et consistency
- **Mesure** : 60% des balles dans cercle 15cm
- **Durée** : 50 minutes quotidiennes

#### **Semaine 3 : Application**
- **Objectif** : Intégrer en situation réelle
- **Focus** : Deathmatch et aim maps
- **Mesure** : Kill rate et accuracy stats
- **Durée** : 60 minutes quotidiennes

---

## 🎛️ 5. Techniques Situationnelles

### 🎯 Distances et Adaptations

#### **Courte Distance (0-10m)**
- **Technique** : Spray complet recommandé
- **Compensation** : Pattern full avec timing
- **Avantage** : Dégâts maximum rapide
- **Risque** : Overcommit sur mauvais angle

#### **Moyenne Distance (10-25m)**
- **Technique** : Bursts de 5-8 balles
- **Compensation** : Phases 1-2 du pattern
- **Avantage** : Équilibre précision/DPS
- **Risque** : Timing critique

#### **Longue Distance (25m+)**
- **Technique** : Taps ou bursts courts
- **Compensation** : Contrôle vertical uniquement
- **Avantage** : Précision maximale
- **Risque** : DPS faible

### 🛡️ Spray Défensif vs Offensif

#### **Spray Défensif**
- **Contexte** : Tenir angle, position statique
- **Technique** : Pattern complet maîtrisé
- **Avantage** : Temps de préparation
- **Focus** : Précision et consistency

#### **Spray Offensif**
- **Contexte** : Entry frag, engagement mobile
- **Technique** : Bursts rapides, adaptation
- **Avantage** : Surprise et momentum
- **Focus** : Rapidité et trade setup

---

## 🧠 6. Psychologie et Gestion du Stress

### 🎯 Contrôle Mental

#### **Stress Management**
- **Respiration** : Contrôle respiratoire pendant spray
- **Visualisation** : Imaginer le pattern avant tir
- **Confiance** : Commitment total sur décision
- **Adaptation** : Ajuster selon résultat

#### **Consistency Mentale**
- **Routine** : Même approche chaque spray
- **Patience** : Ne pas rush la compensation
- **Discipline** : Respecter les distances
- **Apprentissage** : Analyser chaque échec

### 🎮 Application en Match

#### **Économie des Balles**
- **Count Mental** : Tracker balles restantes
- **Reload Timing** : Optimiser rechargement
- **Spray Discipline** : Arrêter si rate
- **Utility Backup** : Grenades en support

#### **Teamplay Integration**
- **Communication** : Annoncer spray engagement
- **Positioning** : Angles pour trades
- **Utility Support** : Flashes pour spray
- **Backup Plan** : Fallback après spray

---

## 🔬 7. Analyse et Optimisation

### 📊 Métriques de Performance

#### **Statistiques Clés**
- **Spray Accuracy** : % de balles touchées
- **Pattern Consistency** : Reproduction fidèle
- **Kill Rate** : Éliminations par spray
- **Efficiency** : Balles utilisées par kill

#### **Outils d'Analyse**
- **Aim Lab** : Métriques détaillées
- **Recoil Master** : Pattern accuracy
- **Demo Review** : Analyse post-match
- **Stat Tracking** : Progression longue terme

### 🎯 Optimisation Continue

#### **Ajustements Personnels**
- **Sensitivity** : Optimiser pour pattern
- **Crosshair** : Visibilité pendant spray
- **Hardware** : Souris et tapis adaptés
- **Settings** : FPS stable et input lag

#### **Adaptation Meta**
- **Map Changes** : Ajuster selon environnement
- **Opponent Analysis** : Adapter contre styles
- **Team Strategy** : Intégrer dans tactiques
- **Continuous Learning** : Suivre évolutions

---

## 💡 8. Conseils des Professionnels

### 🏆 Sagesse ZywOo

#### **Philosophie Technique**
- "La perfection vient de la répétition consciente"
- "Chaque spray doit avoir un objectif précis"
- "La patience dans l'apprentissage détermine la vitesse de progression"

#### **Conseils Pratiques**
- **Warm-up** : Toujours commencer par les bases
- **Consistency** : Privilégier régularité sur spectaculaire
- **Adaptation** : Ajuster technique selon situation

### 🎪 Approche apEX

#### **Mindset Compétitif**
- "Spray control = extension de votre game sense"
- "Confiance totale ou pas de spray du tout"
- "L'entraînement quotidien n'est pas optionnel"

#### **Application Tactique**
- **Team First** : Spray pour l'équipe, pas pour stats
- **Communication** : Annoncer intentions spray
- **Backup Plan** : Toujours avoir plan B

### 🎛️ Précision Magisk

#### **Méthode Technique**
- "Muscle memory avant speed"
- "Analyser chaque échec pour amélioration"
- "Qualité de practice > quantité de practice"

#### **Développement Continu**
- **Demo Review** : Analyser chaque spray en match
- **Feedback Loop** : Ajuster technique selon résultats
- **Patience** : Progression long terme

---

## 🔥 Conclusion : Maîtriser l'AK-47

L'**AK-47** n'est pas qu'une arme - c'est l'**expression de votre skill technique**. En maîtrisant ces techniques inspirées de **Team Vitality**, vous transformez chaque spray en démonstration de force.

### 🎯 Points Clés à Retenir
- **Pattern Mastery** : Mémorisation parfaite du recul
- **Situation Awareness** : Adapter technique selon contexte
- **Consistency** : Répétition jusqu'à automatisme
- **Continuous Improvement** : Analyse et optimisation constantes

### 🚀 Prochaines Étapes
1. **Maîtriser** les 15 premières balles parfaitement
2. **Intégrer** le pattern complet progressivement
3. **Appliquer** en situation réelle avec confiance
4. **Analyser** et optimiser continuellement

---

*L'AK-47 parfaitement maîtrisé ne fait pas de vous un meilleur joueur - il révèle le joueur d'élite que vous êtes déjà.* - Philosophy Team Vitality"""

    # Update the tutorial with professional content
    update_result = collection.update_one(
        {'title': 'Contrôle de recul avancé (AK-47)'},
        {
            '$set': {
                'title': 'Contrôle de recul avancé (AK-47)',
                'description': 'Maîtrisez parfaitement le spray pattern AK-47 avec techniques tier 1, mécaniques CS2 2025, et méthodes d\'entraînement professionnelles.',
                'content': professional_content,
                'level': 'expert',
                'game': 'cs2',
                'duration': '40 min',
                'type': 'Guide Technique',
                'author': 'Oupafamilly Pro Team',
                'objectives': [
                    'Maîtriser parfaitement le spray pattern AK-47 en 4 phases distinctes',
                    'Comprendre les mécaniques CS2 2025 et statistiques complètes de l\'arme',
                    'Développer les techniques de compensation et contrôle de recul avancées',
                    'Intégrer les méthodes d\'entraînement professionnelles dans votre routine',
                    'Adapter votre technique selon les distances et situations de match'
                ],
                'tips': [
                    'Entraînez-vous quotidiennement avec la routine structurée de 45 minutes',
                    'Maîtrisez les 15 premières balles avant d\'aborder le pattern complet',
                    'Étudiez les techniques de spray de ZywOo dans ses démos officielles',
                    'Utilisez Recoil Master et aim_botz pour perfectionner votre contrôle',
                    'Adaptez votre technique selon la distance : spray/burst/tap'
                ],
                'image': cs2_image
            }
        }
    )
    
    print(f'Tutorial updated successfully: {update_result.modified_count} document(s) modified')
    print('✅ Professional AK-47 recoil control content with Vitality inspiration applied')
    
else:
    print('❌ Could not find existing tutorial')