import pymongo
from datetime import datetime

def initialize_community_features():
    """
    Initialiser les nouvelles fonctionnalités communautaires :
    - Marketplace avec des articles de base
    - Mise à jour des profils existants avec les nouvelles propriétés
    """
    
    # Connect to MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['oupafamilly_db']
    
    print("🚀 Initialisation des fonctionnalités communautaires...")
    
    # 1. Mettre à jour tous les profils existants avec les nouvelles propriétés
    print("📋 Mise à jour des profils utilisateurs...")
    
    profiles = list(db.user_profiles.find({}))
    for profile in profiles:
        update_data = {}
        
        # Ajouter les nouvelles propriétés si elles n'existent pas
        if "coins" not in profile:
            update_data["coins"] = 100  # 100 coins de départ
        if "total_coins_earned" not in profile:
            update_data["total_coins_earned"] = 100
        if "experience_points" not in profile:
            update_data["experience_points"] = 0
        if "level" not in profile:
            update_data["level"] = 1
        if "badges" not in profile:
            update_data["badges"] = []
        if "achievements" not in profile:
            update_data["achievements"] = []
        if "comments_received" not in profile:
            update_data["comments_received"] = 0
        if "average_rating" not in profile:
            update_data["average_rating"] = 0.0
        if "total_ratings" not in profile:
            update_data["total_ratings"] = 0
        
        if update_data:
            update_data["updated_at"] = datetime.utcnow()
            db.user_profiles.update_one(
                {"id": profile["id"]},
                {"$set": update_data}
            )
            print(f"  ✅ Profil mis à jour: {profile.get('display_name', 'N/A')}")
    
    # 2. Créer des articles de marketplace de base
    print("🛒 Création d'articles de marketplace...")
    
    marketplace_items = [
        {
            "id": "avatar_001",
            "name": "Avatar Guerrier",
            "description": "Un avatar épique de guerrier pour se démarquer",
            "item_type": "avatar",
            "price": 150,
            "image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
            "is_available": True,
            "is_premium": False,
            "created_at": datetime.utcnow()
        },
        {
            "id": "badge_001",
            "name": "Badge Champion",
            "description": "Badge doré pour les vrais champions",
            "item_type": "badge",
            "price": 100,
            "image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
            "is_available": True,
            "is_premium": False,
            "created_at": datetime.utcnow()
        },
        {
            "id": "title_001",
            "name": "Titre 'Vétéran'",
            "description": "Titre spécial pour les membres vétérans",
            "item_type": "title",
            "price": 200,
            "image_url": None,
            "is_available": True,
            "is_premium": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": "banner_001",
            "name": "Bannière CS2",
            "description": "Bannière de profil aux couleurs de CS2",
            "item_type": "banner",
            "price": 250,
            "image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
            "is_available": True,
            "is_premium": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": "emote_001",
            "name": "Emote GG",
            "description": "Emote personnalisé pour féliciter",
            "item_type": "emote",
            "price": 50,
            "image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
            "is_available": True,
            "is_premium": False,
            "created_at": datetime.utcnow()
        },
        {
            "id": "avatar_002",
            "name": "Avatar Mage",
            "description": "Avatar mystique pour les stratèges",
            "item_type": "avatar",
            "price": 180,
            "image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
            "is_available": True,
            "is_premium": True,
            "created_at": datetime.utcnow()
        },
        {
            "id": "badge_002",
            "name": "Badge Légende",
            "description": "Badge exclusif pour les légendes de la communauté",
            "item_type": "badge",
            "price": 300,
            "image_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
            "is_available": True,
            "is_premium": True,
            "created_at": datetime.utcnow()
        }
    ]
    
    # Vérifier si des articles existent déjà pour éviter les doublons
    existing_items = db.marketplace_items.count_documents({})
    if existing_items == 0:
        db.marketplace_items.insert_many(marketplace_items)
        print(f"  ✅ {len(marketplace_items)} articles ajoutés à la marketplace")
    else:
        print(f"  ℹ️  Marketplace déjà initialisée ({existing_items} articles)")
    
    # 3. Créer des défis de base
    print("🏆 Création de défis communautaires...")
    
    challenges = [
        {
            "id": "daily_login",
            "title": "Connexion Quotidienne",
            "description": "Se connecter tous les jours pendant 7 jours",
            "challenge_type": "daily",
            "requirements": {"consecutive_days": 7},
            "rewards": {"coins": 100, "xp": 50},
            "is_active": True,
            "start_date": datetime.utcnow(),
            "end_date": None,
            "created_at": datetime.utcnow()
        },
        {
            "id": "first_comment",
            "title": "Premier Commentaire",
            "description": "Écrire votre premier commentaire sur un profil",
            "challenge_type": "achievement",
            "requirements": {"comments_written": 1},
            "rewards": {"coins": 25, "xp": 10},
            "is_active": True,
            "start_date": datetime.utcnow(),
            "end_date": None,
            "created_at": datetime.utcnow()
        },
        {
            "id": "social_butterfly",
            "title": "Papillon Social",
            "description": "Écrire 10 commentaires constructifs",
            "challenge_type": "achievement",
            "requirements": {"comments_written": 10},
            "rewards": {"coins": 150, "xp": 75, "badge": "Social"},
            "is_active": True,
            "start_date": datetime.utcnow(),
            "end_date": None,
            "created_at": datetime.utcnow()
        }
    ]
    
    existing_challenges = db.challenges.count_documents({})
    if existing_challenges == 0:
        db.challenges.insert_many(challenges)
        print(f"  ✅ {len(challenges)} défis créés")
    else:
        print(f"  ℹ️  Défis déjà initialisés ({existing_challenges} défis)")
    
    # 4. Statistiques finales
    print("\n📊 Récapitulatif de l'initialisation:")
    total_users = db.users.count_documents({})
    total_profiles = db.user_profiles.count_documents({})
    total_marketplace_items = db.marketplace_items.count_documents({})
    total_challenges = db.challenges.count_documents({})
    
    print(f"  👥 Utilisateurs: {total_users}")
    print(f"  📋 Profils: {total_profiles}")
    print(f"  🛒 Articles marketplace: {total_marketplace_items}")
    print(f"  🏆 Défis: {total_challenges}")
    
    # 5. Créer quelques messages dans les collections manquantes pour la structure
    print("\n🔧 Création des collections de base...")
    
    collections_to_init = [
        "coin_transactions",
        "user_comments", 
        "team_comments",
        "chat_messages",
        "private_messages",
        "user_inventory",
        "activity_feed",
        "user_challenges"
    ]
    
    for collection_name in collections_to_init:
        if collection_name not in db.list_collection_names():
            # Créer la collection avec un document temporaire
            db[collection_name].insert_one({"_temp": True, "created_at": datetime.utcnow()})
            # Supprimer le document temporaire
            db[collection_name].delete_one({"_temp": True})
            print(f"  ✅ Collection {collection_name} créée")
    
    print("\n🎉 Initialisation des fonctionnalités communautaires terminée !")
    print("\n💡 Nouvelles fonctionnalités disponibles :")
    print("  - Système de monnaie virtuelle (coins)")
    print("  - Marketplace avec avatars, badges, titres")
    print("  - Système de commentaires et évaluations")
    print("  - Système XP et niveaux")
    print("  - Défis et achievements")
    print("  - Activity feed pour le social")
    
    return True

if __name__ == '__main__':
    initialize_community_features()