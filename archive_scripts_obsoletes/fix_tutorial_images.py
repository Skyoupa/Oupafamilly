#!/usr/bin/env python3
"""
Script pour corriger les images des tutoriels et les rendre spécifiques aux jeux
"""

import asyncio
import sys
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Add parent directory to path to import our modules
sys.path.append(str(Path(__file__).parent / 'backend'))

from backend.models import Tutorial, Game

async def fix_tutorial_images():
    """Corriger les images des tutoriels pour qu'elles correspondent aux jeux."""
    
    # Load environment variables
    ROOT_DIR = Path(__file__).parent / 'backend'
    load_dotenv(ROOT_DIR / '.env')
    
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("🖼️  Correction des images des tutoriels...")
    
    try:
        # Images spécifiques par jeu et thème
        game_specific_images = {
            "cs2": [
                '/images/tutorials/cs2_team_strategy.jpg',    # Stratégies d'équipe
                '/images/tutorials/cs2_economy.jpg',          # Économie CS2
                '/images/tutorials/cs2_aim_training.jpg',     # Grenades
                '/images/tutorials/cs2_map_analysis.jpg',     # Mouvement
                '/images/tutorials/cs2_utility.jpg',         # Recul AK-47
                '/images/tutorials/cs2_communication.jpg',    # Smokes avancées
                '/images/tutorials/cs2_antileco.jpg',         # Positionnement
                '/images/tutorials/cs2_retakes.jpg',          # Analyse démos
                '/images/tutorials/cs2_meta.jpg',             # Meta gaming
                '/images/tutorials/cs2_coaching.jpg',         # IGL avancé
                '/images/tutorials/cs2_demo_analysis.jpg',    # Anti-strats
                '/images/tutorials/cs2_mental.jpg'            # Clutch mastery
            ],
            "wow": [
                '/images/tutorials/wow_classes.jpg',          # Classes
                '/images/tutorials/wow_addons.jpg',           # Interface/addons
                '/images/tutorials/wow_farming.jpg',          # Quêtes/leveling
                '/images/tutorials/wow_mechanics.jpg',        # Combat
                '/images/tutorials/wow_dungeons.jpg',         # Donjons
                '/images/tutorials/wow_economy.jpg',          # Professions
                '/images/tutorials/wow_pvp.jpg',              # PvP
                '/images/tutorials/wow_raids.jpg',            # Raids
                '/images/tutorials/wow_builds.jpg',           # DPS/HPS
                '/images/tutorials/wow_mythicplus.jpg',       # Theorycraft
                '/images/tutorials/wow_guild.jpg',            # Leadership
                '/images/tutorials/wow_events.jpg'            # Coaching
            ],
            "lol": [
                '/images/tutorials/lol_lasthit.jpg',          # Dernier hit
                '/images/tutorials/lol_macro.jpg',            # Macro game
                '/images/tutorials/lol_teamfight.jpg',        # Team fighting
                '/images/tutorials/lol_vision.jpg',           # Farming
                '/images/tutorials/lol_laning.jpg',           # Warding
                '/images/tutorials/lol_jungle.jpg',           # Trading
                '/images/tutorials/lol_roaming.jpg',          # Roaming
                '/images/tutorials/lol_builds.jpg',           # Build
                '/images/tutorials/lol_mental.jpg',           # Team fighting
                '/images/tutorials/lol_teamcomp.jpg',         # Macro fin
                '/images/tutorials/lol_replay.jpg',           # Composition
                '/images/tutorials/lol_counterjungle.jpg'     # Analyse replay
            ],
            "sc2": [
                '/images/tutorials/sc2_economy.jpg',          # Bases économiques
                '/images/tutorials/sc2_units.jpg',            # Économie/workers
                '/images/tutorials/sc2_scouting.jpg',         # Scouting
                '/images/tutorials/sc2_micro.jpg',            # Combat/micro
                '/images/tutorials/sc2_buildorders.jpg',      # Build orders
                '/images/tutorials/sc2_tech.jpg',             # Upgrades
                '/images/tutorials/sc2_expansion.jpg',        # Multi-base
                '/images/tutorials/sc2_allins.jpg',           # Timing attacks
                '/images/tutorials/sc2_harass.jpg',           # Macro avancé
                '/images/tutorials/sc2_defense.jpg',          # Build orders (nouveau)
                '/images/tutorials/sc2_combat.jpg',           # Combat avancé (nouveau)
                '/images/tutorials/sc2_replay.jpg'            # Analyse replay (nouveau)
            ],
            "minecraft": [
                '/images/tutorials/minecraft_survival.jpg',    # Survie
                '/images/tutorials/minecraft_building.jpg',    # Craft
                '/images/tutorials/minecraft_exploration.jpg', # Exploration
                '/images/tutorials/minecraft_farms.jpg',       # Farming
                '/images/tutorials/minecraft_redstone.jpg',    # Redstone
                '/images/tutorials/minecraft_architecture.jpg',# Construction
                '/images/tutorials/minecraft_nether.jpg',      # Nether
                '/images/tutorials/minecraft_enchanting.jpg',  # Enchantements
                '/images/tutorials/minecraft_combat.jpg',      # End/Dragon
                '/images/tutorials/minecraft_mods.jpg',        # Farms auto
                '/images/tutorials/minecraft_competitions.jpg',# Mégastructures
                '/images/tutorials/minecraft_servers.jpg'      # Serveurs
            ]
        }
        
        # Corriger les images pour chaque jeu
        corrections_made = 0
        
        for game in ["cs2", "wow", "lol", "sc2", "minecraft"]:
            print(f"\n🎮 Correction des images pour {game.upper()}...")
            
            # Récupérer les tutoriels triés par sort_order
            tutorials = await db.tutorials.find({"game": game}).sort([("sort_order", 1), ("created_at", -1)]).to_list(None)
            game_images = game_specific_images.get(game, [])
            
            for i, tutorial in enumerate(tutorials):
                # Assigner l'image correspondante
                if i < len(game_images):
                    new_image = game_images[i]
                    current_image = tutorial.get('image', 'Pas d\'image')
                    
                    # Mettre à jour seulement si l'image est différente
                    if current_image != new_image:
                        await db.tutorials.update_one(
                            {"_id": tutorial["_id"]},
                            {"$set": {"image": new_image}}
                        )
                        print(f"  ✅ {tutorial.get('title', 'Sans titre')[:50]}...")
                        print(f"     Ancienne: {current_image}")
                        print(f"     Nouvelle: {new_image}")
                        corrections_made += 1
                    else:
                        print(f"  ⏭️  {tutorial.get('title', 'Sans titre')[:50]}... (déjà correcte)")
                else:
                    print(f"  ⚠️  Pas d'image disponible pour: {tutorial.get('title', 'Sans titre')}")
        
        print(f"\n📊 RÉSUMÉ DES CORRECTIONS:")
        print(f"   ✅ {corrections_made} images corrigées")
        
        # Vérification finale
        print(f"\n🔍 Vérification finale...")
        for game in ["cs2", "wow", "lol", "sc2", "minecraft"]:
            game_count = await db.tutorials.count_documents({"game": game})
            missing_images = await db.tutorials.count_documents({"game": game, "$or": [{"image": {"$exists": False}}, {"image": None}, {"image": ""}]})
            print(f"   {game.upper()}: {game_count} tutoriels, {missing_images} sans image")
        
        total_tutorials = await db.tutorials.count_documents({})
        total_missing = await db.tutorials.count_documents({"$or": [{"image": {"$exists": False}}, {"image": None}, {"image": ""}]})
        
        print(f"\n🎯 ÉTAT FINAL:")
        print(f"   📚 Total tutoriels: {total_tutorials}")
        print(f"   🖼️  Tutoriels avec images: {total_tutorials - total_missing}")
        print(f"   ❌ Tutoriels sans image: {total_missing}")
        
        if total_missing == 0:
            print("🎉 PARFAIT! Tous les tutoriels ont maintenant des images spécifiques!")
        else:
            print(f"⚠️  Il reste {total_missing} tutoriels sans image à corriger")
        
        return corrections_made
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    print("🖼️  Correction des images des tutoriels...")
    asyncio.run(fix_tutorial_images())
    print("✅ Corrections terminées !")