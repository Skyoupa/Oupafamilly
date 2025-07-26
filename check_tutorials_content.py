#!/usr/bin/env python3
"""
Script pour vérifier le contenu des tutoriels et corriger les problèmes
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

async def check_and_fix_tutorials():
    """Vérifier et corriger le contenu des tutoriels."""
    
    # Load environment variables
    ROOT_DIR = Path(__file__).parent / 'backend'
    load_dotenv(ROOT_DIR / '.env')
    
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("🔍 Vérification du contenu des tutoriels...")
    
    try:
        # Récupérer tous les tutoriels pour vérification
        all_tutorials = await db.tutorials.find({}).to_list(None)
        
        print(f"📊 Trouvé {len(all_tutorials)} tutoriels à vérifier")
        
        # Vérifier le contenu par jeu
        games = ["cs2", "wow", "lol", "sc2", "minecraft"]
        
        content_issues = []
        image_issues = []
        
        for game in games:
            game_tutorials = [t for t in all_tutorials if t.get('game') == game]
            print(f"\n🎮 {game.upper()} - {len(game_tutorials)} tutoriels:")
            
            for i, tutorial in enumerate(game_tutorials):
                title = tutorial.get('title', 'Sans titre')
                description = tutorial.get('description', 'Sans description')
                content = tutorial.get('content', 'Sans contenu')
                image = tutorial.get('image', 'Pas d\'image')
                level = tutorial.get('level', 'inconnu')
                
                print(f"  [{i+1}] {title}")
                print(f"      Niveau: {level}")
                print(f"      Image: {image}")
                print(f"      Description: {description[:100]}...")
                
                # Vérifier si le contenu semble être en anglais
                english_indicators = ['the ', 'and ', 'with ', 'your ', 'this ', 'that ', 'have ', 'will ', 'can ', 'should ']
                content_lower = content.lower()
                english_count = sum(1 for indicator in english_indicators if indicator in content_lower)
                
                if english_count > 10:  # Si beaucoup de mots anglais
                    content_issues.append({
                        'game': game,
                        'title': title,
                        'id': tutorial.get('_id'),
                        'issue': 'Contenu principalement en anglais'
                    })
                    print(f"      ⚠️  PROBLÈME: Contenu semble être en anglais")
                
                # Vérifier les images
                if 'gaming_setup.jpg' in image or 'esports_pro.jpg' in image:
                    image_issues.append({
                        'game': game,
                        'title': title,
                        'id': tutorial.get('_id'),
                        'current_image': image,
                        'issue': 'Image générique, pas spécifique au jeu'
                    })
                    print(f"      ⚠️  PROBLÈME: Image pas spécifique au jeu")
                
                print()
        
        # Résumé des problèmes
        print(f"\n📋 RÉSUMÉ DES PROBLÈMES DÉTECTÉS:")
        print(f"   📝 Problèmes de contenu: {len(content_issues)}")
        print(f"   🖼️  Problèmes d'images: {len(image_issues)}")
        
        if content_issues:
            print(f"\n📝 PROBLÈMES DE CONTENU:")
            for issue in content_issues:
                print(f"   - {issue['game'].upper()}: {issue['title']} - {issue['issue']}")
        
        if image_issues:
            print(f"\n🖼️  PROBLÈMES D'IMAGES:")
            for issue in image_issues:
                print(f"   - {issue['game'].upper()}: {issue['title']} - {issue['current_image']}")
        
        return content_issues, image_issues
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    print("🔍 Vérification des tutoriels...")
    asyncio.run(check_and_fix_tutorials())
    print("✅ Vérification terminée !")