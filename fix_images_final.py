#!/usr/bin/env python3
"""
Script pour corriger définitivement les images des tutoriels
"""

import asyncio
import sys
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

async def fix_tutorial_images_final():
    """Corriger définitivement les images des tutoriels."""
    
    # Load environment variables
    ROOT_DIR = Path(__file__).parent / 'backend'
    load_dotenv(ROOT_DIR / '.env')
    
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("🖼️ Correction finale des images des tutoriels...")
    
    # Images locales par jeu et niveau
    image_mapping = {
        ('cs2', 'beginner'): '/images/tutorials/fps_gaming.jpg',
        ('cs2', 'intermediate'): '/images/tutorials/gaming_setup.jpg',
        ('cs2', 'expert'): '/images/tutorials/pro_area.jpg',
        ('wow', 'beginner'): '/images/tutorials/gaming_setup.jpg',
        ('wow', 'intermediate'): '/images/tutorials/esports_pro.jpg',
        ('wow', 'expert'): '/images/tutorials/esports_pro.jpg',
        ('lol', 'beginner'): '/images/tutorials/lol_moba.jpg',
        ('lol', 'intermediate'): '/images/tutorials/esports_pro.jpg',
        ('lol', 'expert'): '/images/tutorials/tournament.jpg',
    }
    
    try:
        tutorials = await db.tutorials.find({}).to_list(None)
        print(f"📚 {len(tutorials)} tutoriels trouvés")
        
        updated_count = 0
        
        for tutorial in tutorials:
            game = tutorial.get('game')
            level = tutorial.get('level')
            
            # Déterminer l'image appropriée
            image_key = (game, level)
            new_image = image_mapping.get(image_key, '/images/tutorials/gaming_setup.jpg')
            
            # Mettre à jour le tutoriel
            result = await db.tutorials.update_one(
                {"_id": tutorial["_id"]},
                {"$set": {"image": new_image}}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                print(f"✅ {tutorial.get('title', 'Unknown')[:40]}... → {new_image}")
        
        print(f"\n🎉 {updated_count} tutoriels mis à jour avec succès!")
        
        # Vérification
        sample_tutorial = await db.tutorials.find_one({})
        print(f"📋 Vérification: {sample_tutorial.get('title', 'Unknown')[:30]}... image = {sample_tutorial.get('image', 'None')}")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(fix_tutorial_images_final())