#!/usr/bin/env python3
"""
Script d'initialisation pour créer un utilisateur administrateur par défaut
pour une communauté Oupafamilly naissante.
"""

import asyncio
import os
import sys
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Add parent directory to path to import our modules
sys.path.append(str(Path(__file__).parent))

from models import User, UserProfile, UserRole, UserStatus
from auth import get_password_hash

async def create_admin_user():
    """Créer un utilisateur administrateur par défaut."""
    
    # Load environment variables
    ROOT_DIR = Path(__file__).parent
    load_dotenv(ROOT_DIR / '.env')
    
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    try:
        # Check if admin already exists
        existing_admin = await db.users.find_one({"role": "admin"})
        if existing_admin:
            print("❌ Un administrateur existe déjà dans la base de données.")
            print(f"   Administrateur existant: {existing_admin['username']} ({existing_admin['email']})")
            return
        
        # Admin user data - customize these values
        admin_data = {
            "username": "admin",
            "email": "admin@oupafamilly.com",
            "password": "Oupafamilly2024!",  # Change this in production!
            "display_name": "Administrateur Oupafamilly"
        }
        
        print("🚀 Création de l'utilisateur administrateur par défaut...")
        print(f"   Username: {admin_data['username']}")
        print(f"   Email: {admin_data['email']}")
        print(f"   ⚠️  Mot de passe temporaire: {admin_data['password']}")
        
        # Create admin user
        hashed_password = get_password_hash(admin_data["password"])
        admin_user = User(
            username=admin_data["username"],
            email=admin_data["email"],
            hashed_password=hashed_password,
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            is_verified=True
        )
        
        # Insert admin user
        await db.users.insert_one(admin_user.dict())
        
        # Create admin profile
        admin_profile = UserProfile(
            user_id=admin_user.id,
            display_name=admin_data["display_name"],
            bio="Administrateur de la communauté Oupafamilly",
            favorite_games=["cs2", "lol", "wow"]
        )
        
        await db.user_profiles.insert_one(admin_profile.dict())
        
        print("✅ Utilisateur administrateur créé avec succès!")
        print("\n📋 Détails de connexion:")
        print(f"   Email: {admin_data['email']}")
        print(f"   Mot de passe: {admin_data['password']}")
        print("\n🔒 IMPORTANT: Changez ce mot de passe lors de votre première connexion!")
        print("\n🎯 Prochaines étapes:")
        print("   1. Connectez-vous avec ces identifiants")
        print("   2. Changez le mot de passe administrateur")
        print("   3. Complétez votre profil")
        print("   4. Créez des annonces de bienvenue")
        print("   5. Configurez les premiers tournois")
        
        # Create a welcome announcement
        from models import News
        welcome_news = News(
            title="🎉 Bienvenue dans la communauté Oupafamilly!",
            content="""
Salut à tous et bienvenues dans notre nouvelle communauté gaming Oupafamilly! 🎮

Cette communauté a été créée pour rassembler les passionnés de jeux vidéo dans une ambiance conviviale et familiale. Que vous soyez débutant ou expert, vous avez votre place ici !

## Nos valeurs:
- 🎯 Fun avant tout
- 🏆 Compétition saine
- 😌 Zéro stress
- 👨‍👩‍👧‍👦 Esprit famille

## Nos jeux:
- Counter-Strike 2
- World of Warcraft  
- League of Legends
- StarCraft II
- Minecraft

N'hésitez pas à compléter votre profil, rejoindre nos discussions et participer aux prochains tournois!

L'aventure Oupafamilly commence maintenant! 🚀
            """,
            summary="Annonce de bienvenue pour la nouvelle communauté Oupafamilly",
            author_id=admin_user.id,
            is_published=True,
            is_pinned=True,
            tags=["bienvenue", "communauté", "important"]
        )
        
        await db.news.insert_one(welcome_news.dict())
        
        print("📰 Annonce de bienvenue créée!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'administrateur: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    print("🔧 Initialisation de la communauté Oupafamilly...")
    asyncio.run(create_admin_user())
    print("🎉 Initialisation terminée!")