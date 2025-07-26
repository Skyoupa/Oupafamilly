"""
Script pour initialiser les customs de profils et étiquettes membres dans la marketplace
"""
import asyncio
import os
import sys
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from database import db
import uuid

async def create_profile_customs():
    """Créer les articles de customisation pour les profils."""
    
    customs_items = [
        # === AVATARS CUSTOMS ===
        {
            "id": str(uuid.uuid4()),
            "name": "Avatar Guerrier Elite",
            "description": "Avatar exclusif avec armure dorée et effet de lumière",
            "price": 500,
            "item_type": "avatar",
            "rarity": "epic",
            "is_available": True,
            "is_premium": True,
            "custom_data": {
                "avatar_style": "warrior_elite",
                "color_scheme": "gold",
                "effects": ["glow", "particles"]
            }
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Avatar Cyber Ninja",
            "description": "Avatar futuriste avec effets néon",
            "price": 350,
            "item_type": "avatar",
            "rarity": "rare",
            "is_available": True,
            "custom_data": {
                "avatar_style": "cyber_ninja",
                "color_scheme": "neon_blue",
                "effects": ["neon_glow"]
            }
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Avatar Dragon Master",
            "description": "Avatar avec dragon compagnon animé",
            "price": 750,
            "item_type": "avatar",
            "rarity": "legendary",
            "is_available": True,
            "is_premium": True,
            "custom_data": {
                "avatar_style": "dragon_master",
                "color_scheme": "fire_red",
                "effects": ["dragon_companion", "fire_particles"]
            }
        },
        
        # === BADGES CUSTOMS ===
        {
            "id": str(uuid.uuid4()),
            "name": "Badge Champion Suprême",
            "description": "Badge doré avec couronne et étoiles scintillantes",
            "price": 300,
            "item_type": "badge",
            "rarity": "epic",
            "is_available": True,
            "custom_data": {
                "badge_icon": "crown_stars",
                "color": "#FFD700",
                "animation": "sparkle",
                "text": "CHAMPION"
            }
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Badge Vétéran",
            "description": "Badge bronze pour les anciens membres",
            "price": 150,
            "item_type": "badge",
            "rarity": "common",
            "is_available": True,
            "custom_data": {
                "badge_icon": "shield",
                "color": "#CD7F32",
                "text": "VÉTÉRAN"
            }
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Badge Elite Gaming",
            "description": "Badge violet pour les joueurs d'élite",
            "price": 400,
            "item_type": "badge",
            "rarity": "rare",
            "is_available": True,
            "custom_data": {
                "badge_icon": "gaming_controller",
                "color": "#8A2BE2",
                "animation": "pulse",
                "text": "ELITE"
            }
        },
        
        # === ÉTIQUETTES MEMBRES CUSTOMS ===
        {
            "id": str(uuid.uuid4()),
            "name": "Étiquette Feu",
            "description": "Étiquette rectangulaire rouge avec dégradé de feu",
            "price": 200,
            "item_type": "custom_tag",
            "rarity": "rare",
            "is_available": True,
            "custom_data": {
                "background": "linear-gradient(135deg, #FF6B6B, #FF8E53)",
                "border": "2px solid #FF4757",
                "text_color": "#FFFFFF",
                "font_weight": "bold",
                "effects": ["fire_glow"]
            }
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Étiquette Glace",
            "description": "Étiquette bleue glacée avec effets cristaux",
            "price": 200,
            "item_type": "custom_tag",
            "rarity": "rare",
            "is_available": True,
            "custom_data": {
                "background": "linear-gradient(135deg, #74b9ff, #0984e3)",
                "border": "2px solid #00b894",
                "text_color": "#FFFFFF",
                "font_weight": "bold",
                "effects": ["ice_crystals"]
            }
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Étiquette Forêt",
            "description": "Étiquette verte nature avec motifs organiques",
            "price": 180,
            "item_type": "custom_tag",
            "rarity": "common",
            "is_available": True,
            "custom_data": {
                "background": "linear-gradient(135deg, #00b894, #55a3ff)",
                "border": "2px solid #00cec9",
                "text_color": "#FFFFFF",
                "font_weight": "bold",
                "effects": ["leaf_pattern"]
            }
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Étiquette Cosmic",
            "description": "Étiquette spatiale avec étoiles et galaxies",
            "price": 600,
            "item_type": "custom_tag",
            "rarity": "legendary",
            "is_available": True,
            "is_premium": True,
            "custom_data": {
                "background": "linear-gradient(135deg, #2d3436, #636e72, #74b9ff)",
                "border": "2px solid #a29bfe",
                "text_color": "#FFFFFF",
                "font_weight": "bold",
                "effects": ["stars", "galaxy_swirl"],
                "animation": "cosmic_drift"
            }
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Étiquette Lightning",
            "description": "Étiquette électrique jaune avec éclairs",
            "price": 350,
            "item_type": "custom_tag",
            "rarity": "epic", 
            "is_available": True,
            "custom_data": {
                "background": "linear-gradient(135deg, #fdcb6e, #e17055)",
                "border": "2px solid #f39c12",
                "text_color": "#2d3436",
                "font_weight": "bold",
                "effects": ["lightning_bolts"],
                "animation": "electric_pulse"
            }
        },
        
        # === TITRES PERSONNALISÉS ===
        {
            "id": str(uuid.uuid4()),
            "name": "Titre: Maître des Ombres",
            "description": "Titre mystérieux affiché sous votre nom",
            "price": 250,
            "item_type": "title",
            "rarity": "rare",
            "is_available": True,
            "custom_data": {
                "title_text": "Maître des Ombres",
                "title_color": "#6c5ce7",
                "font_style": "italic"
            }
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Titre: Légende Vivante",
            "description": "Titre légendaire pour les plus grands",
            "price": 800,
            "item_type": "title",
            "rarity": "legendary",
            "is_available": True,
            "is_premium": True,
            "custom_data": {
                "title_text": "Légende Vivante",
                "title_color": "#FFD700",
                "font_style": "bold",
                "effects": ["golden_glow"]
            }
        },
        
        # === THÈMES DE PROFIL ===
        {
            "id": str(uuid.uuid4()),
            "name": "Thème Profil Galaxie",
            "description": "Thème complet avec fond d'espace et effets stellaires",
            "price": 1000,
            "item_type": "theme",
            "rarity": "legendary",
            "is_available": True,
            "is_premium": True,
            "custom_data": {
                "background_image": "galaxy_nebula",
                "color_scheme": "cosmic",
                "effects": ["floating_stars", "nebula_particles"],
                "custom_fonts": True
            }
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Thème Profil Cyberpunk",
            "description": "Thème futuriste avec néons et circuits",
            "price": 700,
            "item_type": "theme", 
            "rarity": "epic",
            "is_available": True,
            "custom_data": {
                "background_image": "cyberpunk_city",
                "color_scheme": "neon",
                "effects": ["neon_lines", "digital_rain"]
            }
        }
    ]
    
    try:
        # Supprimer les anciens customs s'ils existent
        await db.marketplace_items.delete_many({
            "item_type": {"$in": ["avatar", "badge", "custom_tag", "title", "theme"]}
        })
        
        # Insérer les nouveaux customs
        for item in customs_items:
            item["created_at"] = datetime.utcnow()
            item["updated_at"] = datetime.utcnow()
            
        await db.marketplace_items.insert_many(customs_items)
        
        print(f"✅ {len(customs_items)} articles de customisation créés avec succès!")
        print("\nRépartition par type:")
        
        type_counts = {}
        for item in customs_items:
            item_type = item["item_type"]
            type_counts[item_type] = type_counts.get(item_type, 0) + 1
        
        for item_type, count in type_counts.items():
            print(f"  - {item_type}: {count} articles")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des customs: {e}")

async def main():
    print("🎨 Initialisation des customs de profils et étiquettes...")
    await create_profile_customs()
    print("✨ Initialisation terminée!")

if __name__ == "__main__":
    asyncio.run(main())