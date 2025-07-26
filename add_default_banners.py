"""
Script pour ajouter 3 bannières de base à tous les membres existants et nouveaux
"""
import asyncio
import os
import sys
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from database import db
import uuid

async def create_default_banners():
    """Créer les 3 bannières de base par défaut."""
    
    default_banners = [
        {
            "id": "default_banner_blue",
            "name": "Bannière Bleue Classique",
            "description": "Bannière de base élégante aux couleurs bleues",
            "price": 0,  # Gratuite
            "item_type": "banner",
            "rarity": "common",
            "is_available": False,  # Ne s'affiche pas dans la marketplace
            "is_default": True,
            "custom_data": {
                "background": "linear-gradient(135deg, #3b82f6, #1e40af)",
                "pattern": "geometric",
                "color_scheme": "blue"
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": "default_banner_green",
            "name": "Bannière Verte Nature",
            "description": "Bannière de base aux couleurs de la nature",
            "price": 0,  # Gratuite
            "item_type": "banner",
            "rarity": "common",
            "is_available": False,  # Ne s'affiche pas dans la marketplace
            "is_default": True,
            "custom_data": {
                "background": "linear-gradient(135deg, #10b981, #059669)",
                "pattern": "organic",
                "color_scheme": "green"
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "id": "default_banner_purple",
            "name": "Bannière Violette Royale",
            "description": "Bannière de base aux couleurs royales",
            "price": 0,  # Gratuite
            "item_type": "banner",
            "rarity": "common",
            "is_available": False,  # Ne s'affiche pas dans la marketplace
            "is_default": True,
            "custom_data": {
                "background": "linear-gradient(135deg, #8b5cf6, #7c3aed)",
                "pattern": "royal",
                "color_scheme": "purple"
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    # Supprimer les anciennes bannières par défaut si elles existent
    await db.marketplace_items.delete_many({"is_default": True})
    
    # Insérer les nouvelles bannières par défaut
    await db.marketplace_items.insert_many(default_banners)
    
    print(f"✅ {len(default_banners)} bannières par défaut créées")
    return default_banners

async def add_default_banners_to_users():
    """Ajouter les bannières par défaut à tous les utilisateurs existants."""
    
    # Récupérer tous les utilisateurs
    users = await db.users.find({}).to_list(1000)
    print(f"📋 {len(users)} utilisateurs trouvés")
    
    # Récupérer les bannières par défaut
    default_banners = await db.marketplace_items.find({"is_default": True}).to_list(10)
    
    users_updated = 0
    banners_added = 0
    
    for user in users:
        user_id = user["id"]
        
        for banner in default_banners:
            # Vérifier si l'utilisateur possède déjà cette bannière
            existing = await db.user_inventory.find_one({
                "user_id": user_id,
                "item_id": banner["id"]
            })
            
            if not existing:
                # Ajouter la bannière à l'inventaire
                inventory_item = {
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "item_id": banner["id"],
                    "item_name": banner["name"],
                    "item_type": "banner",
                    "item_data": banner["custom_data"],
                    "is_equipped": False,
                    "is_default": True,
                    "purchased_at": datetime.utcnow()
                }
                
                await db.user_inventory.insert_one(inventory_item)
                banners_added += 1
        
        users_updated += 1
        
        # Équiper la première bannière par défaut si l'utilisateur n'a aucune bannière équipée
        equipped_banner = await db.user_inventory.find_one({
            "user_id": user_id,
            "item_type": "banner",
            "is_equipped": True
        })
        
        if not equipped_banner:
            # Équiper la première bannière bleue par défaut
            first_banner = await db.user_inventory.find_one({
                "user_id": user_id,
                "item_id": "default_banner_blue"
            })
            
            if first_banner:
                await db.user_inventory.update_one(
                    {"id": first_banner["id"]},
                    {"$set": {"is_equipped": True}}
                )
                
                # Mettre à jour le profil
                await db.user_profiles.update_one(
                    {"user_id": user_id},
                    {"$set": {"equipped_banner": default_banners[0]["custom_data"]}},
                    upsert=True
                )
                
                print(f"  👤 {user.get('username', 'User')} - Bannière bleue équipée par défaut")
    
    print(f"✅ {users_updated} utilisateurs mis à jour")
    print(f"✅ {banners_added} bannières ajoutées au total")

async def setup_new_user_defaults():
    """Configuration pour que les nouveaux utilisateurs reçoivent automatiquement les bannières."""
    print("💡 IMPORTANT: Pour les nouveaux utilisateurs, ajoutez ce code dans votre système d'inscription:")
    print("""
# Dans auth.py ou lors de la création d'un nouveau profil utilisateur :

async def give_default_items_to_new_user(user_id: str):
    try:
        # Récupérer les bannières par défaut
        default_banners = await db.marketplace_items.find({"is_default": True}).to_list(10)
        
        for banner in default_banners:
            inventory_item = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "item_id": banner["id"],
                "item_name": banner["name"],
                "item_type": "banner",
                "item_data": banner["custom_data"],
                "is_equipped": banner["id"] == "default_banner_blue",  # Équiper la bleue par défaut
                "is_default": True,
                "purchased_at": datetime.utcnow()
            }
            
            await db.user_inventory.insert_one(inventory_item)
        
        # Équiper la bannière bleue par défaut
        await db.user_profiles.update_one(
            {"user_id": user_id},
            {"$set": {"equipped_banner": default_banners[0]["custom_data"]}},
            upsert=True
        )
        
    except Exception as e:
        logger.error(f"Erreur ajout items par défaut: {e}")
""")

async def main():
    print("🎨 Création et distribution des bannières par défaut...")
    
    # 1. Créer les bannières par défaut
    await create_default_banners()
    
    # 2. Les ajouter à tous les utilisateurs existants
    await add_default_banners_to_users()
    
    # 3. Afficher les instructions pour les nouveaux utilisateurs
    await setup_new_user_defaults()
    
    print("\n🎉 Configuration terminée!")
    print("📋 Résumé:")
    print("   - 3 bannières par défaut créées (Bleue, Verte, Violette)")
    print("   - Bannières ajoutées à tous les utilisateurs existants")
    print("   - Bannière bleue équipée par défaut pour chaque utilisateur")
    print("   - Les bannières par défaut ne s'affichent pas dans la marketplace")

if __name__ == "__main__":
    asyncio.run(main())