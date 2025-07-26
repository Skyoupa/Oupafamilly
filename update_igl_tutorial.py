import pymongo
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['oupafamilly_db']
collection = db['tutorials']

# Get a working CS2 tutorial image
working_tutorial = collection.find_one({'game': 'cs2', 'title': 'Stratégies d\'équipe et coordination'})
if working_tutorial:
    cs2_image = working_tutorial.get('image', '')
    print(f'Found CS2 image: {len(cs2_image)} characters')
    
    # Clean content without problematic formatting
    clean_content = """# 🎯 IGL Avancé et Leadership d'Équipe - Guide Professionnel CS2

## 🌟 Introduction : Le Rôle de l'IGL Elite

L'**In-Game Leader (IGL)** représente l'âme stratégique d'une équipe CS2. Inspiré par les légendes comme **FalleN**, **karrigan** et **gla1ve**, ce guide vous enseignera les techniques avancées utilisées par les équipes Tier 1 comme **Astralis**, **FaZe Clan** et **NAVI**.

---

## 🧠 1. Psychologie du Leadership Professionnel

### 🎭 Gestion des Émotions d'Équipe
- **Contrôle du Momentum** : Gérer les montées d'adrénaline et les phases de découragement
- **Communication Positive** : Transformer les erreurs en apprentissages constructifs
- **Gestion du Stress** : Techniques de respiration et de visualisation utilisées par les pros

### 🔥 Motivation et Cohésion
- **Confiance Collective** : Construire une mentalité de victoire
- **Responsabilisation** : Donner des rôles clairs et valoriser chaque joueur
- **Résilience** : Rebondir après des défaites ou des rounds perdus

---

## 📞 2. Stratégies de Calling Avancées

### 🎯 Calling Pré-Établi vs Dynamique

#### **Système Astralis** (Calling Structuré)
- **Protocoles Fixes** : Setups précis pour chaque situation
- **Timings Parfaits** : Synchronisation des utilities et des mouvements
- **Adaptations Minimales** : Exécution parfaite des stratégies préparées

#### **Système FaZe** (Calling Créatif)
- **Liberté Individuelle** : Laisser les stars s'exprimer dans le cadre tactique
- **Adaptations Rapides** : Changements de plans en fonction des opportunités
- **Calling Intuitif** : Ressentir le flow du match et adapter

### 📊 Lecture de Jeu Professionnelle

#### **Analyse des Patterns Ennemis**
- **Tendances Économiques** : Prédire les buys adverses
- **Rotations Habituelles** : Identifier les mouvements récurrents
- **Adaptation aux Styles** : Ajuster face aux équipes agressives/passives

#### **Information Gathering**
- **Maximiser les Picks** : Utiliser chaque élimination pour collecter des infos
- **Utility Usage** : Analyser l'utilisation des grenades adverses
- **Fake Reads** : Détecter les feints et les rotations

---

## ⚡ 3. Adaptation Mid-Round Elite

### 🔄 Techniques d'Adaptation Instantanée

#### **Système de Calling Réactif**
- **Calls de Backup** : Toujours avoir un plan B prêt
- **Rotations Express** : Changement de bombsite en moins de 10 secondes
- **Stack Adaptatif** : Renforcer les positions selon les lectures

#### **Gestion des Situations Inattendues**
- **Man Advantage** : Exploiter immédiatement les 5v4 et 4v3
- **Utility Disadvantage** : Compenser le manque de grenades
- **Time Management** : Gérer le temps selon les scenarios

### 🎮 Exemples Concrets de Mid-Round Calls

#### **Scenario 1: Rush B Détecté**
**Call 1**: "3 B détectés, ROTATE A maintenant!"
**Call 2**: "Faux contact B, prenez A fast avec smoke-flash"
**Call 3**: "Timing parfait, ils sont encore en rotation"

#### **Scenario 2: Pick Long Obtenu**
**Call 1**: "Pick long confirmé, on prend long control"
**Call 2**: "Smoke CT, je veux short clear en même temps"
**Call 3**: "Attention rotate, ils vont stack A"

---

## 🏆 4. Gestion d'Équipe Professionnelle

### 👥 Dynamique d'Équipe Optimale

#### **Rôles et Responsabilités**
- **Entry Fragger** : Motivation et soutien psychologique
- **Support** : Reconnaissance de l'impact silencieux
- **AWPer** : Gestion de la pression et des attentes
- **Lurker** : Communication et timing d'intervention

#### **Résolution de Conflits**
- **Médiation Active** : Résoudre les tensions rapidement
- **Focus sur l'Objectif** : Ramener l'attention sur la victoire
- **Discussions Post-Match** : Adresser les problèmes hors du match

### 📈 Développement Individuel

#### **Coaching Personnalisé**
- **Analyse des Demos** : Revoir les rounds avec chaque joueur
- **Objectifs Spécifiques** : Fixer des goals individuels mesurables
- **Encouragement Constructif** : Valoriser les progrès et corriger les erreurs

---

## 🧪 5. Préparation Tactique Avancée

### 🎯 Anti-Stratting Professionnel

#### **Étude des Adversaires**
- **Analyse Vidéo** : Décortiquer les demos des équipes adverses
- **Patterns Identification** : Identifier les habitudes tactiques
- **Contre-Mesures** : Développer des stratégies spécifiques

#### **Adaptations Cartographiques**
- **Meta Understanding** : Comprendre les évolutions du jeu
- **Utility Innovations** : Créer de nouveaux setups
- **Timing Mastery** : Perfectionner les timings d'exécution

### 🛡️ Gestion Économique Elite

#### **Macro-Gestion**
- **Force-Buy Windows** : Identifier les opportunités de force
- **Save Strategies** : Optimiser les rounds d'économie
- **Utility Investment** : Prioriser les achats selon les stratégies

---

## 📊 6. Outils et Techniques Professionnelles

### 💻 Analyse de Performance

#### **Metrics Clés**
- **Round Win Rate** : Taux de victoire par type de round
- **Adaptation Speed** : Rapidité d'ajustement tactique
- **Team Cohesion** : Mesure de la coordination d'équipe

#### **Outils Recommandés**
- **Démo Analysis** : Logiciels de review approfondie
- **Stat Tracking** : Suivi des performances individuelles
- **Communication Analysis** : Évaluation de la qualité des calls

### 🎧 Communication Professionnelle

#### **Protocoles de Communication**
- **Clear Calls** : Informations concises et actionables
- **Timing Perfect** : Calls au bon moment, pas trop tôt ni trop tard
- **Positive Reinforcement** : Encouragement constant de l'équipe

---

## 🎖️ 7. Exercices Pratiques d'IGL

### 🏋️ Entraînement Quotidien

#### **Routine d'Échauffement IGL**
1. **5 min** : Révision des strats de base
2. **10 min** : Analyse rapide des demos récentes
3. **15 min** : Practice des calls vocaux
4. **10 min** : Visualisation des scenarios de match

#### **Exercises Spécifiques**
- **Decision Making** : Scenarios de choix rapides
- **Pressure Calling** : Calls sous pression temporelle
- **Adaptation Drills** : Changements de stratégies improvisés

### 🎯 Challenges d'Amélioration

#### **Semaine 1** : Fondamentaux
- Perfectionnement des calls de base
- Travail sur la clarté de communication
- Développement de la lecture de jeu

#### **Semaine 2** : Adaptation
- Exercises de mid-round calling
- Scenarios d'adaptation rapide
- Gestion des situations inattendues

#### **Semaine 3** : Leadership
- Travail sur la motivation d'équipe
- Résolution de conflits simulés
- Développement du charisme

---

## 🔥 Conclusion : Devenir un IGL d'Exception

L'IGL d'élite combine **intelligence tactique**, **leadership naturel** et **adaptation constante**. En maîtrisant ces compétences inspirées des meilleurs professionnels, vous transformerez votre équipe en une machine de guerre redoutable.

### 🎯 Points Clés à Retenir
- **Préparation** : 70% du succès se joue avant le match
- **Adaptation** : 30% dans la capacité à s'ajuster en temps réel
- **Leadership** : L'aspect humain est aussi important que le tactique
- **Pratique** : Les skills d'IGL se développent avec l'expérience

### 🚀 Prochaines Étapes
1. **Analyser** vos propres demos en tant qu'IGL
2. **Identifier** vos points d'amélioration prioritaires
3. **Pratiquer** les exercices recommandés quotidiennement
4. **Appliquer** progressivement les techniques en match

---

*Un grand IGL ne fait pas que diriger son équipe - il inspire ses coéquipiers à devenir la meilleure version d'eux-mêmes.* - Philosophy des IGLs professionnels"""

    # Update the tutorial with clean content and proper CS2 image
    update_result = collection.update_one(
        {'title': 'IGL avancé et leadership d\'équipe'},
        {
            '$set': {
                'content': clean_content,
                'image': cs2_image
            }
        }
    )
    
    print(f'Tutorial updated: {update_result.modified_count} document(s) modified')
    print('✅ Content cleaned and CS2 image applied')
    
else:
    print('❌ Could not find working CS2 tutorial for image reference')