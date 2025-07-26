#!/usr/bin/env python3
"""
🎯 INITIALISATION SYSTÈME DE QUÊTES QUOTIDIENNES
Script pour initialiser les collections MongoDB nécessaires au système de quêtes
"""

import asyncio
import sys
import os
sys.path.append('/app/backend')

from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import uuid
from typing import Dict, Any

# Configuration de la base de données
from database import db, client

async def create_quest_collections():
    """Créer les collections nécessaires pour le système de quêtes"""
    try:
        print("🗄️ Création des collections pour le système de quêtes...")
        
        # 1. Collection pour les quêtes (templates de quêtes)
        await db.create_collection("quests")
        print("  ✅ Collection 'quests' créée")
        
        # 2. Collection pour la progression des utilisateurs sur les quêtes
        await db.create_collection("user_quests")
        print("  ✅ Collection 'user_quests' créée")
        
        # 3. Créer les index pour optimiser les performances
        await create_quest_indexes()
        
        return True
        
    except Exception as e:
        if "already exists" in str(e).lower():
            print("  ℹ️ Collections déjà existantes")
            return True
        else:
            print(f"  ❌ Erreur création collections: {str(e)}")
            return False

async def create_quest_indexes():
    """Créer les index optimisés pour les quêtes"""
    try:
        print("📚 Création des index pour optimiser les performances...")
        
        # Index pour user_quests
        await db.user_quests.create_index([("user_id", 1), ("quest_id", 1)], unique=True)
        await db.user_quests.create_index([("user_id", 1), ("completed", 1)])
        await db.user_quests.create_index([("completed_at", -1)])
        await db.user_quests.create_index([("started_at", -1)])
        
        # Index pour quests
        await db.quests.create_index([("is_daily", 1)])
        await db.quests.create_index([("category", 1)])
        await db.quests.create_index([("active_from", 1), ("active_until", 1)])
        
        print("  ✅ Index créés avec succès")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur création index: {str(e)}")
        return False

async def seed_sample_quest_data():
    """Insérer quelques données de test pour les quêtes"""
    try:
        print("🌱 Initialisation de données d'exemple pour les quêtes...")
        
        # Vérifier si des quêtes existent déjà
        existing_quests = await db.quests.count_documents({})
        if existing_quests > 0:
            print(f"  ℹ️ {existing_quests} quêtes déjà présentes")
            return True
        
        # Créer quelques quêtes d'exemple pour aujourd'hui
        today = datetime.utcnow()
        sample_quests = [
            {
                "id": str(uuid.uuid4()),
                "name": "Participez à un Tournoi",
                "description": "Inscrivez-vous et jouez dans au moins un tournoi aujourd'hui",
                "category": "gaming",
                "difficulty": "common",
                "requirements": {"tournament_participation": 1},
                "rewards": {"coins": 25, "xp": 50},
                "duration_hours": 24,
                "is_daily": True,
                "active_from": today.replace(hour=0, minute=0, second=0, microsecond=0),
                "active_until": today.replace(hour=23, minute=59, second=59, microsecond=999999),
                "created_at": today
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Papillon Social",
                "description": "Écrivez 3 commentaires positifs sur des profils",
                "category": "social",
                "difficulty": "common",
                "requirements": {"comments_posted": 3, "min_rating": 4},
                "rewards": {"coins": 20, "xp": 40},
                "duration_hours": 24,
                "is_daily": True,
                "active_from": today.replace(hour=0, minute=0, second=0, microsecond=0),
                "active_until": today.replace(hour=23, minute=59, second=59, microsecond=999999),
                "created_at": today
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Explorateur du Marketplace",
                "description": "Achetez un objet dans le marketplace",
                "category": "economic",
                "difficulty": "common",
                "requirements": {"marketplace_purchases": 1},
                "rewards": {"coins": 15, "xp": 30},
                "duration_hours": 24,
                "is_daily": True,
                "active_from": today.replace(hour=0, minute=0, second=0, microsecond=0),
                "active_until": today.replace(hour=23, minute=59, second=59, microsecond=999999),
                "created_at": today
            },
        ]
        
        # Insérer les quêtes d'exemple
        result = await db.quests.insert_many(sample_quests)
        print(f"  ✅ {len(result.inserted_ids)} quêtes d'exemple créées")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur initialisation données d'exemple: {str(e)}")
        return False

async def create_sample_user_quest_progress():
    """Créer quelques exemples de progression d'utilisateur"""
    try:
        print("👤 Initialisation progression d'exemple...")
        
        # Récupérer un utilisateur de test
        sample_user = await db.users.find_one({"role": {"$ne": "admin"}})
        if not sample_user:
            print("  ℹ️ Aucun utilisateur de test trouvé")
            return True
        
        user_id = sample_user["id"]
        
        # Récupérer une quête d'exemple
        sample_quest = await db.quests.find_one({"is_daily": True})
        if not sample_quest:
            print("  ℹ️ Aucune quête d'exemple trouvée")
            return True
        
        # Créer une progression partielle
        user_quest = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "quest_id": sample_quest["id"],
            "progress": {"tournament_participation": 0},
            "completed": False,
            "completed_at": None,
            "rewards_claimed": False,
            "started_at": datetime.utcnow()
        }
        
        # Insérer seulement si n'existe pas déjà
        existing_progress = await db.user_quests.find_one({
            "user_id": user_id,
            "quest_id": sample_quest["id"]
        })
        
        if not existing_progress:
            await db.user_quests.insert_one(user_quest)
            print(f"  ✅ Progression d'exemple créée pour {sample_user.get('username', 'utilisateur')}")
        else:
            print("  ℹ️ Progression d'exemple déjà existante")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur création progression d'exemple: {str(e)}")
        return False

async def verify_quest_system():
    """Vérifier que le système de quêtes est bien configuré"""
    try:
        print("🔍 Vérification du système de quêtes...")
        
        # Vérifier les collections
        collections = await db.list_collection_names()
        required_collections = ["quests", "user_quests"]
        
        for collection in required_collections:
            if collection in collections:
                count = await db[collection].count_documents({})
                print(f"  ✅ Collection '{collection}': {count} documents")
            else:
                print(f"  ❌ Collection '{collection}' manquante")
                return False
        
        # Vérifier les index
        user_quests_indexes = await db.user_quests.list_indexes().to_list(100)
        print(f"  ✅ {len(user_quests_indexes)} index créés pour user_quests")
        
        quests_indexes = await db.quests.list_indexes().to_list(100)
        print(f"  ✅ {len(quests_indexes)} index créés pour quests")
        
        print("🎯 Système de quêtes prêt à l'emploi !")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur vérification: {str(e)}")
        return False

async def main():
    """Fonction principale d'initialisation"""
    print("🎯 INITIALISATION DU SYSTÈME DE QUÊTES QUOTIDIENNES")
    print("=" * 60)
    
    try:
        # Tester la connexion à la base de données
        await db.command("ping")
        print("✅ Connexion à MongoDB réussie")
        
        # Étapes d'initialisation
        steps = [
            ("Création des collections", create_quest_collections),
            ("Données d'exemple", seed_sample_quest_data),
            ("Progression d'exemple", create_sample_user_quest_progress),
            ("Vérification système", verify_quest_system)
        ]
        
        for step_name, step_func in steps:
            print(f"\n📋 {step_name}...")
            success = await step_func()
            if not success:
                print(f"❌ Échec de l'étape: {step_name}")
                return False
        
        print("\n" + "=" * 60)
        print("🎉 INITIALISATION DU SYSTÈME DE QUÊTES TERMINÉE AVEC SUCCÈS !")
        print("\nNouvelles fonctionnalités disponibles:")
        print("  📅 Quêtes quotidiennes dynamiques")
        print("  🎯 Progression détaillée par utilisateur")
        print("  🏆 Système de récompenses automatiques")
        print("  📊 Classements et statistiques de quêtes")
        print("  🔄 Rotation automatique des quêtes quotidiennes")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR FATALE: {str(e)}")
        return False
    
    finally:
        client.close()

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)