#!/usr/bin/env python3
"""
Script pour télécharger des images spécifiques et enrichir le contenu des tutoriels
"""

import requests
import os
from pathlib import Path
import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Add parent directory to path to import our modules
sys.path.append(str(Path(__file__).parent / 'backend'))

from backend.models import Tutorial, Game

def download_image(url, filename):
    """Télécharger une image depuis une URL"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Créer le dossier s'il n'existe pas
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error downloading {url}: {str(e)}")
        return False

def setup_specific_game_images():
    """Télécharger des images spécifiques pour chaque jeu."""
    
    images_dir = Path("/app/frontend/public/images/tutorials")
    images_dir.mkdir(parents=True, exist_ok=True)
    
    print("🖼️  Téléchargement d'images spécifiques par jeu...")
    
    # Images spécifiques par jeu
    game_images = {
        # CS2 - FPS/Tactical
        "cs2_fps_1.jpg": "https://images.unsplash.com/photo-1639931897192-caa5fe8a628c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwxfHxGUFMlMjBnYW1pbmd8ZW58MHx8fHwxNzUzNDkxNjYwfDA&ixlib=rb-4.1.0&q=85",
        "cs2_fps_2.jpg": "https://images.unsplash.com/photo-1639931875444-cd9fe48fb4b4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHwyfHxGUFMlMjBnYW1pbmd8ZW58MHx8fHwxNzUzNDkxNjYwfDA&ixlib=rb-4.1.0&q=85",
        "cs2_tactical_1.jpg": "https://images.unsplash.com/photo-1748950363681-8f1eb9b416f7?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2MzR8MHwxfHNlYXJjaHwxfHx0YWN0aWNhbCUyMHNob290ZXJ8ZW58MHx8fHwxNzUzNDkxNjY3fDA&ixlib=rb-4.1.0&q=85",
        "cs2_tactical_2.jpg": "https://images.unsplash.com/photo-1637594439872-44d1b1fe0a0b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2MzR8MHwxfHNlYXJjaHwyfHx0YWN0aWNhbCUyMHNob290ZXJ8ZW58MHx8fHwxNzUzNDkxNjY3fDA&ixlib=rb-4.1.0&q=85",
        "cs2_gaming.jpg": "https://images.unsplash.com/photo-1639931561959-36ea34c1731f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzZ8MHwxfHNlYXJjaHw0fHxGUFMlMjBnYW1pbmd8ZW58MHx8fHwxNzUzNDkxNjYwfDA&ixlib=rb-4.1.0&q=85",
        
        # WoW - Fantasy/MMORPG
        "wow_fantasy_1.jpg": "https://images.unsplash.com/photo-1735720518793-804614ff5c48?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwxfHxmYW50YXN5JTIwZ2FtaW5nfGVufDB8fHx8MTc1MzQ5MTcwNHww&ixlib=rb-4.1.0&q=85",
        "wow_fantasy_2.jpg": "https://images.unsplash.com/photo-1735720521030-ca66be3e1f62?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwzfHxmYW50YXN5JTIwZ2FtaW5nfGVufDB8fHx8MTc1MzQ5MTcwNHww&ixlib=rb-4.1.0&q=85",
        "wow_character.jpg": "https://images.unsplash.com/photo-1735720518631-60257e2fde92?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHw0fHxmYW50YXN5JTIwZ2FtaW5nfGVufDB8fHx8MTc1MzQ5MTcwNHww&ixlib=rb-4.1.0&q=85",
        "wow_medieval_1.jpg": "https://images.unsplash.com/photo-1654200746517-58c5e09a9663?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODB8MHwxfHNlYXJjaHwzfHxtZWRpZXZhbCUyMGZhbnRhc3l8ZW58MHx8fHwxNzUzNDkxNzExfDA&ixlib=rb-4.1.0&q=85",
        "wow_warrior.jpg": "https://images.unsplash.com/photo-1677537946959-9038a59d5da5?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODB8MHwxfHNlYXJjaHw0fHxtZWRpZXZhbCUyMGZhbnRhc3l8ZW58MHx8fHwxNzUzNDkxNzExfDA&ixlib=rb-4.1.0&q=85"
    }
    
    # Télécharger toutes les images
    success_count = 0
    total_count = len(game_images)
    
    for filename, url in game_images.items():
        filepath = images_dir / filename
        if download_image(url, str(filepath)):
            success_count += 1
    
    print(f"\n📊 Résultats téléchargement images spécifiques:")
    print(f"   ✅ Réussis: {success_count}/{total_count}")
    
    return success_count == total_count

# Contenu enrichi et professionnel pour chaque niveau
PROFESSIONAL_CONTENT = {
    "cs2_advanced": {
        "team_strategy": """
# 🎯 Stratégies d'Équipe CS2 - Coordination Professionnelle Tier 1

## 🤝 Architecture de Communication Tactique

### 📡 **Système de Communication Hiérarchique**
```
Structure IGL (In-Game Leader) :
┌─ IGL Principal
├─ Entry Fragger (Information rapide)
├─ Support Player (Utility caller)
├─ AWPer (Map control intel)
└─ Lurker (Flank information)

Protocols de Communication :
• 3-second rule : Info critique en 3s maximum
• Callout standard : Position-Arme-HP-Équipement
• Silent periods : Clutch situations (1v1, 1v2)
• Post-round debrief : 30s analyse constructive
• Economic calls : Buy/save decisions collectives

Information Hierarchy :
1. Immediate threats (contact ennemi)
2. Economic intel (équipement adversaire)
3. Positional updates (rotations ennemies)
4. Strategic suggestions (strat calls)
5. Motivational support (moral boost)
```

### ⚡ **Exécution Stratégique Professionnelle**
```
Default Setup (Base stratégique) :
• 2-1-2 formation initiale (A-Mid-B)
• Information gathering phase (0-30s)
• Utility staging (smoke/flash preparation)
• Economic assessment (enemy buy patterns)
• Dynamic adaptation (mid-round changes)

Fast Execute Protocols :
1. Pre-utility deployment (smokes/flashes)
2. Synchronized entry (2-3s window)
3. Trade frag guarantees (follow-up kills)
4. Site control establishment (angles cleared)
5. Post-plant positioning (retake defense)

Anti-stratégique (Counter-tactics) :
• Pattern recognition (enemy habits)
• Fake execution (misdirection)
• Stack adaptation (overload defense)
• Economic disruption (force buys)
• Psychological warfare (timing changes)
```

## 🧠 Macro-Stratégies Avancées

### 📊 **Gestion Économique d'Équipe**
```
Economic Phases Analysis :
Phase 1 : Pistol + 3 rounds (0-4 rounds)
Phase 2 : First gun rounds (4-8 rounds)
Phase 3 : Economic stabilization (8-12 rounds)
Phase 4 : Late game adaptation (12+ rounds)

Buy Round Coordination :
• Full buy threshold : $4750+ per player
• Rifle allocation : AK/M4 + armor + utility
• Role-specific equipment : AWP for dedicated sniper
• Utility distribution : Smokes (IGL), Flashes (Entry), HE (Support)
• Save coordination : Synchronized eco rounds

Force Buy Strategies :
• Calculated risks : Win probability analysis
• Utility prioritization : Essential smokes only
• Position adaptation : Close-range focus
• Economic punishment : Maximize enemy losses
• Recovery planning : Next round buy calculation
```

### 🎮 **Advanced Map Control**
```
Territory Control Matrix :
A Site Control :
├─ Long A dominance (rifle duels)
├─ Catwalk control (connector denial)
├─ Site anchoring (crossfire setup)
└─ Rotation support (quick backup)

Mid Map Control :
├─ Xbox control (central position)
├─ Tunnels pressure (B site support)
├─ Catwalk/connector (A site rotation)
└─ Information gathering (enemy movements)

Rotation Timing :
• Fast rotates : 15-20 seconds (through mid)
• Safe rotates : 25-30 seconds (long route)
• Economic rotates : Save equipment priority
• Information rotates : Confirmed enemy position
• Fake rotates : Misdirection tactics
```

## 🏆 Execution de Niveau Professionnel

### ⚔️ **Protocols de Combat Avancés**
```
Entry Fragging Mastery :
• Pre-aiming angles (crosshair placement)
• Shoulder peeking (information gathering)
• Wide swing timing (peek advantage)
• Counter-strafe precision (accuracy maintenance)
• Trade kill positioning (teammate support)

Support Play Excellence :
• Utility timing (synchronized deployment)
• Refrag positioning (immediate backup)
• Information relay (concise callouts)
• Economic sacrifice (team benefit priority)
• Clutch setup (1vX preparation)

AWP Integration :
• Pick timing (aggressive vs passive)
• Fallback positions (survival priority)
• Economic impact (high-value eliminations)
• Map control (long angles)
• Team coordination (rifle support)
```

### 🧩 **Adaptabilité Stratégique**
```
Mid-Round Adaptation :
• Read enemy patterns (habit recognition)
• Counter unexpected strategies (flexibility)
• Information integration (decision making)
• Risk assessment (calculated plays)
• Team communication (clear direction)

Momentum Management :
• Winning streak exploitation (pressure maintenance)
• Losing streak recovery (mental reset)
• Economic swing timing (force/save decisions)
• Psychological pressure (enemy tilt induction)
• Confidence building (positive reinforcement)
```

Cette approche stratégique professionnelle transforme une équipe de joueurs individuels en machine tactique redoutable !
        """,
        
        "advanced_mechanics": """
# ⚡ Mécaniques Avancées CS2 - Maîtrise Technique Expert

## 🎯 Aiming et Précision de Niveau Professionnel

### 🔫 **Spray Control Mastery (Patterns de Recul)**
```
AK-47 Spray Pattern (30 Balles) :
Balles 1-7 : Vertical ascendant (contrôle vers le bas)
├─ Sensibilité : 0.2-0.3 multiplicateur
├─ Timing : 0.1s par correction
├─ Précision : 95%+ sur 7 premières balles
└─ Distance : Efficace jusqu'à 35m

Balles 8-15 : Horizontal gauche puis droit
├─ Mouvement : Compensation latérale
├─ Technique : Counter-strafe + spray
├─ Applications : Multi-frags rapides
└─ Training : Aim_botz 1000 kills/jour

Balles 16-30 : Pattern chaotique
├─ Utilisation : Spray through smoke
├─ Technique : Zone spraying
├─ Efficacité : 30% accuracy maximum
└─ Recommendation : Burst fire preferred

M4A4/M4A1-S Optimization :
• Pattern plus prévisible (easier control)
• Damage drop-off considération (range factor)
• Rate of fire advantage (faster TTK)
• Silencer impact (M4A1-S stealth benefit)
• Armor penetration calculation (economic factor)
```

### 🎮 **Movement Mechanics Expert**
```
Counter-Strafing Perfection :
• Input timing : <50ms reaction
• Velocity zeroing : Instant accuracy
• Strafe + opposite key : Momentum cancellation
• Pre-aiming integration : Crosshair placement
• Muscle memory development : 10,000+ repetitions

Bunny Hopping Mechanics :
┌─ Air strafing (mouse movement synchronization)
├─ Scroll wheel binding (timing optimization)
├─ Velocity maintenance (speed preservation)
├─ Map geometry exploitation (surface analysis)
└─ Practical applications (escape/positioning)

Advanced Movement Techniques :
• Long jumping : Distance maximization
• Strafe jumping : Speed building
• Edge bug exploitation : Hitbox manipulation  
• Crouch peeking : Profile reduction
• Jump scouting : Information gathering

Positioning Micro-adjustments :
• Angle advantage seeking (geometric superiority)
• Cover utilization (damage mitigation)
• Escape route planning (survival priority)
• Crossfire setup (teammate coordination)
• Information positions (map knowledge)
```

## 🧠 Game Sense et Prise de Décision

### 📊 **Information Processing Avancé**
```
Audio Analysis Expert :
┌─ Footstep identification (surface materials)
├─ Distance calculation (volume analysis)
├─ Direction pinpointing (stereo positioning)
├─ Multiple player tracking (count estimation)
└─ Weapon identification (sound signatures)

Visual Information Processing :
• Minimap integration (teammate positions)
• Health/armor assessment (combat readiness)
• Economic evaluation (buy round identification)
• Utility tracking (grenade counts)
• Time management (round timer awareness)

Predictive Analysis :
• Enemy pattern recognition (habit exploitation)
• Economic prediction (next round buys)
• Rotation timing (movement anticipation)
• Utility usage forecasting (grenade deployment)
• Risk/reward calculation (engagement decisions)
```

### ⚔️ **Combat Decision Trees**
```
Engagement Decision Matrix :
High Advantage (HP>75, Good position) :
├─ Aggressive peek (information/frag seeking)
├─ Utility usage (maximize advantage)
├─ Trade frag setup (teammate coordination)
└─ Map control extension (territory gain)

Neutral Situation (HP 50-75, Standard position) :
├─ Information gathering (safe peeking)
├─ Utility conservation (economic consideration)
├─ Positioning improvement (angle seeking)
└─ Team coordination (collective advantage)

Disadvantaged (HP<50, Poor position) :
├─ Survival priority (damage avoidance)
├─ Information value (team benefit)
├─ Utility disruption (enemy utility waste)
└─ Economic preservation (save priority)

Clutch Situations (1vX) :
• Isolation tactics (separate enemies)
• Time management (defuse/plant pressure)
• Information denial (silent play)
• Positioning rotation (unpredictability)
• Psychological warfare (fake sounds/movement)
```

## 💡 Utility Usage Expert

### 💣 **Grenade Mastery Professionnelle**
```
Smoke Grenade Advanced :
Lineup Precision :
├─ Pixel-perfect throws (128-tick accuracy)
├─ One-way smoke setups (vision advantage)
├─ Retake smokes (post-plant scenarios)
├─ Fake execute smokes (misdirection)
└─ Molotov extinguishing (utility interaction)

Timing Synchronization :
• Team execute coordination (simultaneous deployment)
• Mid-round adaptation (dynamic smoking)
• Economic efficiency (utility conservation)
• Information gathering (smoke and peek)
• Counter-utility usage (enemy grenade negation)

Flashbang Mastery :
Pop Flash Techniques :
├─ Wall bouncing (unpredictable trajectory)
├─ Timing synchronization (peek coordination)
├─ Counter-flash setups (enemy flash negation)
├─ Multi-flash sequences (sustained advantage)
└─ Team flash protocols (coordination)

HE Grenade Optimization :
• Damage calculation (armor/health consideration)
• Economic impact (force buy inducement)
• Area denial (positioning control)
• Multi-hit potential (grouped enemies)
• Combo execution (molotov + HE synergy)
```

Cette maîtrise technique sépare les joueurs compétents des vrais professionnels du CS2 !
        """
    }
}

async def enrich_tutorial_content():
    """Enrichir massivement le contenu des tutoriels."""
    
    # Load environment variables
    ROOT_DIR = Path(__file__).parent / 'backend'
    load_dotenv(ROOT_DIR / '.env')
    
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("📚 Enrichissement massif du contenu des tutoriels...")
    
    try:
        # Nouvelles images spécifiques par jeu
        game_image_mapping = {
            "cs2": [
                '/images/tutorials/cs2_fps_1.jpg',
                '/images/tutorials/cs2_fps_2.jpg', 
                '/images/tutorials/cs2_tactical_1.jpg',
                '/images/tutorials/cs2_tactical_2.jpg',
                '/images/tutorials/cs2_gaming.jpg',
                '/images/tutorials/cs2_fps_1.jpg',  # Répéter pour avoir assez
                '/images/tutorials/cs2_fps_2.jpg',
                '/images/tutorials/cs2_tactical_1.jpg',
                '/images/tutorials/cs2_tactical_2.jpg',
                '/images/tutorials/cs2_gaming.jpg',
                '/images/tutorials/cs2_fps_1.jpg',
                '/images/tutorials/cs2_fps_2.jpg'
            ],
            "wow": [
                '/images/tutorials/wow_fantasy_1.jpg',
                '/images/tutorials/wow_fantasy_2.jpg',
                '/images/tutorials/wow_character.jpg',
                '/images/tutorials/wow_medieval_1.jpg',
                '/images/tutorials/wow_warrior.jpg',
                '/images/tutorials/wow_fantasy_1.jpg',  # Répéter
                '/images/tutorials/wow_fantasy_2.jpg',
                '/images/tutorials/wow_character.jpg',
                '/images/tutorials/wow_medieval_1.jpg',
                '/images/tutorials/wow_warrior.jpg',
                '/images/tutorials/wow_fantasy_1.jpg',
                '/images/tutorials/wow_fantasy_2.jpg'
            ]
        }
        
        enriched_count = 0
        
        # Enrichir le contenu par jeu
        for game in ["cs2", "wow"]:  # Commencer par CS2 et WoW
            print(f"\n🎮 Enrichissement contenu {game.upper()}...")
            
            tutorials = await db.tutorials.find({"game": game}).sort([("sort_order", 1)]).to_list(None)
            game_images = game_image_mapping.get(game, [])
            
            for i, tutorial in enumerate(tutorials):
                title = tutorial.get('title', '')
                level = tutorial.get('level', 'beginner')
                
                # Générer contenu enrichi basé sur le niveau
                if level in ['intermediate', 'expert']:
                    # Contenu très enrichi pour les niveaux avancés
                    if "stratégie" in title.lower() or "équipe" in title.lower():
                        new_content = PROFESSIONAL_CONTENT["cs2_advanced"]["team_strategy"]
                    else:
                        new_content = generate_ultra_rich_content(title, game, level)
                    
                    # Assigner nouvelle image spécifique
                    if i < len(game_images):
                        new_image = game_images[i]
                        
                        # Mettre à jour contenu et image
                        await db.tutorials.update_one(
                            {"_id": tutorial["_id"]},
                            {"$set": {
                                "content": new_content,
                                "image": new_image
                            }}
                        )
                        
                        print(f"   ✅ ENRICHI: {title[:50]}... ({len(new_content)} chars, {level})")
                        enriched_count += 1
                    
        print(f"\n📊 ENRICHISSEMENT TERMINÉ:")
        print(f"   ✅ {enriched_count} tutoriels massivement enrichis")
        print(f"   🎯 Contenu professionnel de niveau expert")
        print(f"   🖼️  Images spécifiques aux jeux assignées")
        
        return enriched_count
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        raise
    finally:
        client.close()

def generate_ultra_rich_content(title, game, level):
    """Générer un contenu ultra-riche et professionnel."""
    
    return f"""
# 🏆 {title} - Guide Expert Professionnel

## 🎯 Analyse Technique Approfondie

### 📊 **Métriques de Performance Avancées**
```
Objectifs de Maîtrise :
• Niveau Expert : 95%+ consistency rate
• Temps d'apprentissage : 40-60 heures pratique
• Performance benchmark : Top 10% joueurs
• Application compétitive : Niveau semi-pro
• Évolution continue : Amélioration 2%/semaine

Métriques Mesurables :
├─ Précision technique : 90%+ execution rate
├─ Vitesse d'exécution : <0.5s reaction time
├─ Adaptabilité : 5+ variations maîtrisées
├─ Consistency : 85%+ success rate match
└─ Innovation : 2+ techniques personnelles

Standards Professionnels :
• Mechanical skill : Muscle memory parfaite
• Game sense : Prédiction 3+ moves ahead
• Decision making : <200ms optimal choices
• Team integration : Leadership capability
• Meta understanding : Current + future trends
```

### ⚡ **Techniques de Niveau Mondial**
```
Approche Systématique :
Phase 1 - Foundation Building (Semaines 1-2) :
├─ Théorie complète (100% concepts)
├─ Démonstration pratique (observation active)
├─ Pratique guidée (correction immédiate)
├─ Feedback integration (amélioration continue)
└─ Foundation testing (validation acquis)

Phase 2 - Skill Development (Semaines 3-6) :
├─ Technique refinement (perfectionnement)
├─ Speed building (vitesse progressive)
├─ Pressure training (situation stress)
├─ Variation mastery (adaptabilité)
└─ Integration practice (application réelle)

Phase 3 - Expert Mastery (Semaines 7-12) :
├─ Innovation development (créativité)
├─ Teaching others (consolidation)
├─ Competition application (test réel)
├─ Continuous optimization (amélioration)
└─ Meta contribution (communauté)
```

## 🧠 Psychologie de la Performance

### 🎭 **Mental Game Expert**
```
Concentration Management :
• Flow state achievement (zone performance)
• Distraction elimination (focus maintenance)
• Pressure handling (clutch situations)
• Confidence building (success reinforcement)
• Tilt recovery (emotional control)

Performance Psychology :
├─ Pre-game preparation (mental routine)
├─ In-game awareness (situational consciousness)
├─ Post-game analysis (objective review)
├─ Long-term development (growth mindset)
└─ Peak performance (consistency optimization)

Competitive Mindset :
• Continuous improvement (never satisfied)
• Failure learning (mistake analysis)
• Success humility (room for growth)
• Pressure embrace (challenge excitement)
• Innovation drive (creative problem solving)
```

### 📈 **Progression Méthodologique**
```
Training Schedule Elite :
Quotidien (2-3 heures) :
├─ Warm-up technique (30 min)
├─ Focused practice (90 min)
├─ Application games (60 min)
├─ Analysis review (15 min)
└─ Cool-down reflection (15 min)

Hebdomadaire :
├─ New technique learning (2 sessions)
├─ Intensive practice (4 sessions)
├─ Competition application (1 session)
├─ Review and adjustment (1 session)
└─ Rest and recovery (1 jour)

Mensuel :
├─ Skill assessment (benchmark testing)
├─ Goal adjustment (target refinement)
├─ Method optimization (approach improvement)
├─ Meta adaptation (trend following)
└─ Teaching practice (knowledge consolidation)
```

## 🏆 Application Compétitive

### ⚔️ **Strategies de Niveau Professionnel**
```
Tournament Preparation :
• Opponent analysis (weakness identification)
• Strategy preparation (multiple plans)
• Team coordination (role optimization)
• Mental preparation (confidence building)
• Equipment optimization (performance maximization)

Match Execution :
├─ Opening adaptation (read opponent)
├─ Mid-game adjustment (strategy evolution)
├─ Closing efficiency (victory securing)
├─ Pressure management (clutch performance)
└─ Communication excellence (team synergy)

Post-Match Analysis :
• Performance review (objective assessment)
• Improvement identification (weak points)
• Success reinforcement (strength consolidation)
• Next match preparation (continuous adaptation)
• Long-term development (career planning)
```

### 🎯 **Innovation et Créativité**
```
Meta Evolution :
• Trend identification (early adoption)
• Counter-development (anticipation)
• Innovation creation (original techniques)
• Community contribution (knowledge sharing)
• Teaching excellence (master demonstration)

Personal Style Development :
├─ Strength amplification (natural talents)
├─ Weakness compensation (smart adaptation)
├─ Signature techniques (unique identity)
├─ Versatility maintenance (adaptability)
└─ Leadership development (team influence)
```

Ce niveau de maîtrise représente l'élite absolue - seuls les plus dédiés l'atteignent !
    """

if __name__ == "__main__":
    print("🚀 Mise à niveau images spécifiques et contenu enrichi...")
    
    # Télécharger les nouvelles images
    images_success = setup_specific_game_images()
    
    if images_success:
        print("✅ Images spécifiques téléchargées avec succès")
    
    # Enrichir le contenu
    asyncio.run(enrich_tutorial_content())
    print("✅ Enrichissement terminé !")