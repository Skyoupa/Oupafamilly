import pymongo
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['oupafamilly_db']
collection = db['tutorials']

# Get the existing tutorial to keep the same image
existing_tutorial = collection.find_one({'title': 'Économie CS2 : comprendre les achats'})
if existing_tutorial:
    cs2_image = existing_tutorial.get('image', '')
    print(f'Found existing tutorial with image: {len(cs2_image)} characters')
    
    # Professional content for CS2 economy
    professional_content = """# 💰 Économie CS2 : Comprendre les Achats - Guide Professionnel 2025

## 🌟 Introduction : L'Art de la Gestion Économique Elite

La **gestion économique** sépare les équipes amateurs des équipes **Tier 1** comme **Astralis**, **FaZe Clan** et **NAVI**. En CS2 2025, maîtriser l'économie signifie contrôler le rythme du match et maximiser vos chances de victoire.

---

## 💸 1. Système Économique CS2 2025

### 🎯 Base du Système Financier

#### **Argent Initial et Plafond**
- **Départ** : 800$ par joueur au début de chaque mi-temps
- **Plafond maximum** : 16 000$ par joueur
- **Objectif** : Optimiser chaque dollar pour maximiser l'impact

#### **Revenus par Actions**
- **Victoire de round** : 3 250$ par joueur
- **Défaite de round** : 1 400$ (1ère défaite) → 3 400$ (5ème défaite consécutive)
- **Plant de bombe** : 300$ au planteur + 800$ à l'équipe (même si round perdu)
- **Désamorçage** : 300$ au désamorceur

#### **Récompenses d'Élimination**
- **Pistolets** : 300$ (CZ-75: 100$, Desert Eagle: 230$)
- **Shotguns** : 900$
- **SMGs** : 600$ (P90: 300$)
- **Rifles** : 300$
- **AWP** : 100$
- **Couteau** : 1 500$

---

## 🎯 2. Stratégies Économiques Tier 1

### 🏆 Méthodes des Équipes Professionnelles

#### **Système Astralis** (Discipline Économique)
- **Patience Économique** : Sacrifier un round pour un meilleur achat
- **Maximisation Utility** : Prioriser les grenades sur les armes
- **Risques Calculés** : Force-buys uniquement avec avantage tactique

#### **Système FaZe** (Économie Agressive)
- **Économie Star Player** : Prioriser l'équipement des stars
- **Forces Opportunistes** : Force-buys basés sur les momentum
- **Drops d'Armes** : Partage d'armes pour optimiser l'équipe

#### **Système NAVI** (Flexibilité Économique)
- **Économie Adaptive** : Ajustement selon l'adversaire
- **Achats Basés Information** : Achats basés sur les lectures
- **Perturbation Eco** : Perturbation de l'économie adverse

### 📊 Patterns Économiques Professionnels

#### **Cycle Économique Standard**
1. **Round Pistol** : Investissement initial crucial
2. **Round Conversion** : Capitaliser sur la victoire pistol
3. **Décision Force/Eco** : Choix stratégique après défaite
4. **Achat Complet** : Maximiser les chances avec équipement complet

#### **Gestion des Bonus de Défaite**
- **1ère défaite** : 1 400$ → Possible force-buy
- **2ème défaite** : 1 900$ → Accumulation recommandée
- **3ème défaite** : 2 400$ → Préparation full buy
- **4ème défaite** : 2 900$ → Full buy garanti
- **5ème défaite** : 3 400$ → Bonus maximum

---

## 🔫 3. Types de Rounds Économiques

### 💪 Rounds Achat Complet

#### **Équipement Standard T-Side**
- **Fusils** : AK-47 (2 700$) pour tous
- **Armure** : Kevlar + Casque (1 000$)
- **Utilities** : Smoke (300$), Flash (200$), HE (300$), Molotov (400$)
- **Total par joueur** : ~4 900$

#### **Équipement Standard CT-Side**
- **Fusils** : M4A4/M4A1-S (3 100$) + 1 AWP (4 750$)
- **Armure** : Kevlar + Casque (1 000$)
- **Utilities** : Smoke (300$), Flash (200$), HE (300$), Incendiary (600$)
- **Kit** : Kit de Désamorçage (400$)
- **Total par joueur** : ~5 500$

### 🎯 Rounds Force Buy

#### **Force Buy T-Side**
- **Galil AR** (2 000$) ou **FAMAS** (2 050$)
- **Armure** : Kevlar seul (650$)
- **Utilities limitées** : 1-2 grenades maximum
- **Total par joueur** : ~3 000$

#### **Force Buy CT-Side**
- **UMP-45** (1 200$) ou **MP9** (1 250$)
- **Armure** : Kevlar + Casque (1 000$)
- **Utilities** : Smoke + Flash (500$)
- **Total par joueur** : ~2 750$

### 💡 Rounds Eco

#### **Eco Strict**
- **Pistolet de base** : Glock/USP-S (0$)
- **Armure optionnelle** : Kevlar (650$)
- **Utilities minimales** : 1 grenade maximum
- **Total par joueur** : 0-950$

#### **Eco Amélioré**
- **Pistolet amélioré** : P250 (300$) ou Five-SeveN (500$)
- **Armure** : Kevlar (650$)
- **Utilities** : 1-2 grenades
- **Total par joueur** : 1 200-1 500$

---

## 🧠 4. Décisions Économiques Avancées

### 🎯 Lecture de l'Économie Adverse

#### **Indicateurs Économiques**
- **Armes sauvées** : Nombre d'armes conservées
- **Achats visibles** : Utilities et équipement aperçus
- **Patterns de rounds** : Historique des achats adverses

#### **Prédictions Économiques**
- **Après victoire** : Adversaire probable en achat complet
- **Après défaite** : Possibilité d'achat forcé ou eco
- **Séquence de défaites** : Calcul des bonus accumés

### 🔄 Adaptation Économique

#### **Réaction aux Eco Adverses**
- **Setup Anti-Eco** : Positions pour contrer les rushes
- **Conservation Utility** : Économiser les grenades
- **Positionnement Armes** : Éviter les drops d'armes

#### **Réaction aux Achats Forcés**
- **Respect Distance** : Éviter les duels proche
- **Usage Utility** : Maximiser l'usage des grenades
- **Focus Crossfire** : Coordination défensive renforcée

---

## 💼 5. Gestion Budgétaire par Situation

### 🎯 Scenarios Économiques Courants

#### **Scénario 1 : Victoire Pistol**
**Situation** : Équipe gagne le round pistolet
**Décision** : 
- **Achat SMGs** : UMP-45, MP9 pour les kill rewards
- **Armure Complète** : Kevlar + Casque pour survivabilité
- **Utilities** : Smoke + Flash pour contrôle

**Objectif** : Maximiser les kill rewards SMG pour l'économie

#### **Scénario 2 : Défaite Pistol**
**Situation** : Équipe perd le round pistolet
**Décision** : 
- **Eco Strict** : Pistolet de base + Armure
- **Achat 1 Fusil** : Pour 1 joueur si possible
- **Concentration Utilities** : Concentrer les grenades

**Objectif** : Perturber l'économie adverse et préparer round 3

#### **Scénario 3 : Fin de Mi-Temps**
**Situation** : Derniers rounds avant changement
**Décision** : 
- **Dépenser Maximum** : Utiliser tout l'argent disponible
- **Drops d'Armes** : Partager les armes chères
- **Spam Utility** : Utiliser toutes les grenades

**Objectif** : Maximiser l'impact avant reset économique

### 🏆 Stratégies Avancées

#### **Guerre Économique**
- **Perturbation Eco** : Forcer l'adversaire en eco
- **Déni d'Argent** : Limiter les kill rewards adverses
- **Contrôle d'Armes** : Récupérer les armes ennemies

#### **Gestion Économique d'Équipe**
- **Achats par Rôle** : Prioriser selon les rôles
- **Partage d'Armes** : Drops stratégiques d'armes
- **Distribution Utility** : Répartition optimale des grenades

---

## 📊 6. Calculs Économiques Pratiques

### 💰 Formules de Base

#### **Calcul Possibilité Achat Forcé**
```
Argent Total Équipe ÷ 5 = Budget par joueur
Si Budget > 2 500$ → Achat Forcé possible
Si Budget < 2 500$ → Eco recommandé
```

#### **Calcul Préparation Achat Complet**
```
Argent Actuel + Bonus Défaite = Budget Round Suivant
Si Budget > 4 500$ (T) ou 5 500$ (CT) → Achat Complet possible
```

#### **Calcul Dégâts Économiques**
```
Armes Perdues × Valeur = Dégâts Économiques
AK-47 perdue = 2 700$ de dégâts
AWP perdue = 4 750$ de dégâts
```

### 📈 Optimisation Économique

#### **Maximiser les Kill Rewards**
- **Usage SMG** : Utiliser les SMGs sur eco rounds
- **Positionnement Shotgun** : Placer les shotguns sur angles close
- **Sélection d'Armes** : Choisir selon les kill rewards

#### **Minimiser les Pertes Économiques**
- **Saves d'Armes** : Sauvegarder les armes chères
- **Timing Utility** : Utiliser les grenades avant de mourir
- **Stratégie de Drop** : Partager avant engagement risqué

---

## 🎯 7. Entraînement Économique

### 🏋️ Exercices Pratiques

#### **Exercice 1 : Calcul Rapide**
1. **Situation** : Équipe a perdu 3 rounds consécutifs
2. **Calcul** : Budget disponible pour chaque joueur
3. **Décision** : Achat forcé ou eco selon budget
4. **Répétition** : 10 scénarios différents

#### **Exercice 2 : Lecture Adverse**
1. **Observation** : Analyser les achats adverses
2. **Prédiction** : Anticiper le prochain round adverse
3. **Adaptation** : Ajuster sa stratégie d'achat
4. **Validation** : Vérifier les prédictions

#### **Exercice 3 : Optimisation Équipe**
1. **Situation** : Budget limité pour l'équipe
2. **Répartition** : Distribuer l'argent selon les rôles
3. **Priorisation** : Déterminer qui achète quoi
4. **Exécution** : Tester l'efficacité en match

### 📚 Routine d'Amélioration

#### **Analyse Quotidienne**
- **Review Économique** : Analyser ses décisions d'achat
- **Reconnaissance Patterns** : Identifier les patterns adverses
- **Pratique Calculs** : Entraîner les calculs rapides

#### **Amélioration Hebdomadaire**
- **Analyse Démo** : Étudier l'économie en demo
- **Discussion Équipe** : Discuter des stratégies économiques
- **Mises à Jour Méta** : S'adapter aux évolutions économiques

---

## 🔥 Conclusion : Maîtriser l'Économie CS2

L'**économie CS2** n'est pas juste de l'argent - c'est un **système stratégique complexe** qui détermine le rythme et l'issue des matchs. En maîtrisant ces principes utilisés par les équipes Tier 1, vous transformez chaque dollar en avantage tactique.

### 🎯 Points Clés à Retenir
- **Discipline Économique** : Chaque achat doit avoir une raison stratégique
- **Lecture Adverse** : Anticiper les décisions économiques adverses
- **Optimisation Équipe** : Maximiser l'efficacité collective
- **Adaptation Constante** : Ajuster selon les situations

### 🚀 Prochaines Étapes
1. **Pratiquer** les calculs économiques rapides
2. **Analyser** l'économie dans vos demos
3. **Développer** votre lecture économique adverse
4. **Optimiser** la gestion économique d'équipe

---

*Dans CS2, l'économie n'est pas juste une ressource - c'est une arme stratégique qui sépare les bons joueurs des champions.* - Philosophy des équipes Tier 1"""

    # Update the tutorial with professional content
    update_result = collection.update_one(
        {'title': 'Économie CS2 : comprendre les achats'},
        {
            '$set': {
                'title': 'Économie CS2 : comprendre les achats',
                'description': 'Maîtrisez l\'économie CS2 2025 avec stratégies pro tier 1 : force-buy, save rounds, et gestion budgétaire optimale.',
                'content': professional_content,
                'level': 'intermediate',
                'game': 'cs2',
                'duration': '30 min',
                'type': 'Guide Économique',
                'author': 'Oupafamilly Pro Team',
                'objectives': [
                    'Maîtriser parfaitement le système économique CS2 avec revenus et bonus',
                    'Comprendre les cycles économiques et la gestion des bonus de défaite',
                    'Développer les stratégies de Force-Buy et Save rounds des équipes Tier 1',
                    'Apprendre à lire l\'économie adverse et adapter ses décisions d\'achat',
                    'Optimiser la gestion budgétaire d\'équipe et le partage d\'armes stratégique'
                ],
                'tips': [
                    'Analysez toujours l\'économie adverse avant vos décisions d\'achat',
                    'Utilisez les SMGs lors des eco rounds pour maximiser les kill rewards',
                    'Étudiez les patterns économiques d\'Astralis, FaZe et NAVI',
                    'Maîtrisez les calculs économiques rapides pour les décisions instantanées',
                    'Coordonnez les achats d\'équipe selon les rôles et priorités tactiques'
                ],
                'image': cs2_image
            }
        }
    )
    
    print(f'Tutorial updated successfully: {update_result.modified_count} document(s) modified')
    print('✅ Professional CS2 economy content applied')
    
else:
    print('❌ Could not find existing tutorial')