#!/usr/bin/env python3
"""
Script pour mettre à jour les images des tutoriels avec les chemins locaux
"""

import asyncio
import sys
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Add parent directory to path to import our modules
sys.path.append(str(Path(__file__).parent / 'backend'))

from backend.models import Game

# Mapping des images locales
LOCAL_IMAGES = {
    'cs2': '/images/tutorials/fps_gaming.jpg',
    'cs2_advanced': '/images/tutorials/gaming_setup.jpg',
    'cs2_pro': '/images/tutorials/tournament.jpg',
    'cs2_expert': '/images/tutorials/pro_area.jpg',
    'wow': '/images/tutorials/gaming_setup.jpg',
    'wow_advanced': '/images/tutorials/esports_pro.jpg',
    'lol': '/images/tutorials/lol_moba.jpg',
    'lol_advanced': '/images/tutorials/esports_pro.jpg',
    'sc2': '/images/tutorials/sc2_strategy.jpg',
    'sc2_advanced': '/images/tutorials/pro_area.jpg',
    'minecraft': '/images/tutorials/minecraft_creative.jpg',
    'minecraft_advanced': '/images/tutorials/gaming_keyboard.jpg'
}

async def update_tutorial_images():
    """Mettre à jour les images des tutoriels avec les chemins locaux."""
    
    # Load environment variables
    ROOT_DIR = Path(__file__).parent / 'backend'
    load_dotenv(ROOT_DIR / '.env')
    
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("🖼️ Mise à jour des images des tutoriels...")
    
    try:
        # Récupérer tous les tutoriels
        tutorials = await db.tutorials.find({}).to_list(None)
        print(f"📚 {len(tutorials)} tutoriels trouvés")
        
        updated_count = 0
        
        for tutorial in tutorials:
            game = tutorial['game']
            level = tutorial['level']
            
            # Déterminer l'image appropriée selon le jeu et le niveau
            if game == 'cs2':
                if level == 'beginner':
                    new_image = LOCAL_IMAGES['cs2']
                elif level == 'intermediate':
                    new_image = LOCAL_IMAGES['cs2_advanced']
                else:  # expert
                    new_image = LOCAL_IMAGES['cs2_expert']
            elif game == 'wow':
                if level == 'beginner':
                    new_image = LOCAL_IMAGES['wow']
                else:
                    new_image = LOCAL_IMAGES['wow_advanced']
            elif game == 'lol':
                if level == 'beginner':
                    new_image = LOCAL_IMAGES['lol']
                else:
                    new_image = LOCAL_IMAGES['lol_advanced']
            elif game == 'sc2':
                if level == 'beginner':
                    new_image = LOCAL_IMAGES['sc2']
                else:
                    new_image = LOCAL_IMAGES['sc2_advanced']
            elif game == 'minecraft':
                if level == 'beginner':
                    new_image = LOCAL_IMAGES['minecraft']
                else:
                    new_image = LOCAL_IMAGES['minecraft_advanced']
            else:
                new_image = LOCAL_IMAGES['cs2']  # fallback
            
            # Mettre à jour l'image du tutoriel
            await db.tutorials.update_one(
                {"_id": tutorial["_id"]},
                {"$set": {"image": new_image}}
            )
            
            updated_count += 1
            print(f"✅ {tutorial['title'][:50]}... → {new_image}")
        
        print(f"\n🎉 {updated_count} tutoriels mis à jour avec succès!")
        print("🖼️ Toutes les images utilisent maintenant les chemins locaux")
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    print("🚀 Mise à jour des images vers chemins locaux...")
    asyncio.run(update_tutorial_images())
    print("✅ Mise à jour terminée !")