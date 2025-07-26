#!/usr/bin/env python3
"""
📊 INITIALISATION SYSTÈME ELO
Script pour initialiser les collections MongoDB et données d'exemple pour le système ELO
"""

import asyncio
import sys
import os
import random
sys.path.append('/app/backend')

from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import uuid
from typing import Dict, Any, List

# Configuration de la base de données
from database import db, client

async def create_elo_collections():
    """Créer les collections nécessaires pour le système ELO"""
    try:
        print("🗄️ Création des collections pour le système ELO...")
        
        # 1. Collection pour les ratings ELO des utilisateurs
        await db.create_collection("elo_ratings")
        print("  ✅ Collection 'elo_ratings' créée")
        
        # 2. Collection pour l'historique des matchs ELO
        await db.create_collection("elo_matches")
        print("  ✅ Collection 'elo_matches' créée")
        
        # 3. Collection pour les stats saisonnières
        await db.create_collection("season_stats")
        print("  ✅ Collection 'season_stats' créée")
        
        # 4. Créer les index pour optimiser les performances
        await create_elo_indexes()
        
        return True
        
    except Exception as e:
        if "already exists" in str(e).lower():
            print("  ℹ️ Collections déjà existantes")
            return True
        else:
            print(f"  ❌ Erreur création collections: {str(e)}")
            return False

async def create_elo_indexes():
    """Créer les index optimisés pour le système ELO"""
    try:
        print("📚 Création des index pour optimiser les performances...")
        
        # Index pour elo_ratings
        await db.elo_ratings.create_index([("user_id", 1), ("game", 1), ("mode", 1), ("season", 1)], unique=True)
        await db.elo_ratings.create_index([("rating", -1)])  # Pour leaderboards
        await db.elo_ratings.create_index([("tier", 1)])
        await db.elo_ratings.create_index([("last_match_date", 1)])  # Pour déclin d'inactivité
        await db.elo_ratings.create_index([("season", 1)])
        
        # Index pour elo_matches
        await db.elo_matches.create_index([("winner_id", 1), ("played_at", -1)])
        await db.elo_matches.create_index([("loser_id", 1), ("played_at", -1)])
        await db.elo_matches.create_index([("match_id", 1)])
        await db.elo_matches.create_index([("tournament_id", 1)])
        await db.elo_matches.create_index([("game", 1), ("played_at", -1)])
        await db.elo_matches.create_index([("season", 1)])
        
        # Index pour season_stats
        await db.season_stats.create_index([("user_id", 1), ("season", 1), ("game", 1)], unique=True)
        
        print("  ✅ Index créés avec succès")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur création index: {str(e)}")
        return False

async def initialize_user_elo_ratings():
    """Initialiser les ratings ELO de base pour les utilisateurs existants"""
    try:
        print("👥 Initialisation des ratings ELO pour les utilisateurs existants...")
        
        # Récupérer tous les utilisateurs
        users = await db.users.find({"role": {"$ne": "admin"}}).to_list(1000)
        
        if not users:
            print("  ℹ️ Aucun utilisateur trouvé")
            return True
        
        CURRENT_SEASON = "2025-S1"
        games = ["cs2", "lol", "wow", "sc2", "minecraft"]
        mode = "tournament"
        
        ratings_created = 0
        
        for user in users:
            user_id = user["id"]
            username = user.get("username", "Utilisateur")
            
            # Créer un rating ELO principal pour CS2 (jeu principal)
            main_rating = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "game": "cs2",
                "mode": mode,
                "rating": random.randint(1100, 1300),  # Variation réaliste autour de 1200
                "peak_rating": 1200,
                "matches_played": random.randint(0, 5),  # Nouveaux joueurs
                "wins": 0,
                "losses": 0,
                "win_rate": 0.0,
                "tier": "silver",
                "tier_progress": random.randint(0, 100),
                "season": CURRENT_SEASON,
                "last_match_date": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # Ajuster peak_rating au rating initial
            main_rating["peak_rating"] = main_rating["rating"]
            
            # Calculer le tier correct
            rating = main_rating["rating"]
            if rating < 1000:
                main_rating["tier"] = "bronze"
            elif rating < 1200:
                main_rating["tier"] = "silver"
            elif rating < 1400:
                main_rating["tier"] = "gold"
            else:
                main_rating["tier"] = "platinum"
            
            try:
                # Insérer seulement si n'existe pas déjà
                existing = await db.elo_ratings.find_one({
                    "user_id": user_id,
                    "game": "cs2",
                    "mode": mode,
                    "season": CURRENT_SEASON
                })
                
                if not existing:
                    await db.elo_ratings.insert_one(main_rating)
                    ratings_created += 1
                    
                    # Mettre à jour le profil utilisateur avec l'ELO initial
                    await db.user_profiles.update_one(
                        {"user_id": user_id},
                        {
                            "$set": {
                                "elo_rating": rating,
                                "peak_elo": rating,
                                "elo_tier": main_rating["tier"],
                                "elo_tier_progress": main_rating["tier_progress"],
                                "updated_at": datetime.utcnow()
                            }
                        },
                        upsert=True
                    )
                
            except Exception as e:
                print(f"  ❌ Erreur pour {username}: {str(e)}")
                continue
        
        print(f"  ✅ {ratings_created} ratings ELO créés pour {len(users)} utilisateurs")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur initialisation ratings utilisateurs: {str(e)}")
        return False

async def create_sample_elo_matches():
    """Créer quelques matchs d'exemple pour démonstration"""
    try:
        print("⚔️ Création de matchs d'exemple...")
        
        # Vérifier s'il y a déjà des matchs
        existing_matches = await db.elo_matches.count_documents({})
        if existing_matches > 0:
            print(f"  ℹ️ {existing_matches} matchs déjà présents")
            return True
        
        # Récupérer quelques utilisateurs
        users = await db.users.find({"role": {"$ne": "admin"}}).limit(6).to_list(6)
        if len(users) < 2:
            print("  ℹ️ Pas assez d'utilisateurs pour créer des matchs d'exemple")
            return True
        
        matches_created = 0
        CURRENT_SEASON = "2025-S1"
        
        # Créer 3 matchs d'exemple
        for i in range(3):
            if i * 2 + 1 >= len(users):
                break
                
            winner = users[i * 2]
            loser = users[i * 2 + 1]
            
            # Récupérer les ratings actuels
            winner_rating_doc = await db.elo_ratings.find_one({
                "user_id": winner["id"],
                "game": "cs2",
                "season": CURRENT_SEASON
            })
            
            loser_rating_doc = await db.elo_ratings.find_one({
                "user_id": loser["id"],
                "game": "cs2",
                "season": CURRENT_SEASON
            })
            
            if not winner_rating_doc or not loser_rating_doc:
                continue
            
            winner_rating = winner_rating_doc["rating"]
            loser_rating = loser_rating_doc["rating"]
            
            # Simuler un changement de rating simple
            rating_change = random.randint(15, 35)
            new_winner_rating = winner_rating + rating_change
            new_loser_rating = max(800, loser_rating - rating_change)
            
            # Créer le match d'exemple
            sample_match = {
                "id": str(uuid.uuid4()),
                "match_id": f"sample_match_{i + 1}",
                "tournament_id": None,
                "game": "cs2",
                "mode": "tournament",
                "winner_id": winner["id"],
                "loser_id": loser["id"],
                "winner_rating_before": winner_rating,
                "loser_rating_before": loser_rating,
                "winner_rating_after": new_winner_rating,
                "loser_rating_after": new_loser_rating,
                "rating_change": rating_change,
                "match_importance": 1.0,
                "season": CURRENT_SEASON,
                "played_at": datetime.utcnow() - timedelta(days=random.randint(1, 7))
            }
            
            await db.elo_matches.insert_one(sample_match)
            
            # Mettre à jour les ratings des joueurs
            await db.elo_ratings.update_one(
                {"user_id": winner["id"], "game": "cs2", "season": CURRENT_SEASON},
                {
                    "$set": {
                        "rating": new_winner_rating,
                        "peak_rating": max(winner_rating_doc.get("peak_rating", winner_rating), new_winner_rating),
                        "last_match_date": sample_match["played_at"],
                        "updated_at": datetime.utcnow()
                    },
                    "$inc": {"matches_played": 1, "wins": 1}
                }
            )
            
            await db.elo_ratings.update_one(
                {"user_id": loser["id"], "game": "cs2", "season": CURRENT_SEASON},
                {
                    "$set": {
                        "rating": new_loser_rating,
                        "last_match_date": sample_match["played_at"],
                        "updated_at": datetime.utcnow()
                    },
                    "$inc": {"matches_played": 1, "losses": 1}
                }
            )
            
            matches_created += 1
            
            print(f"    Match {i + 1}: {winner.get('username', 'User1')} bat {loser.get('username', 'User2')} ({winner_rating} -> {new_winner_rating}, {loser_rating} -> {new_loser_rating})")
        
        print(f"  ✅ {matches_created} matchs d'exemple créés")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur création matchs d'exemple: {str(e)}")
        return False

async def verify_elo_system():
    """Vérifier que le système ELO est bien configuré"""
    try:
        print("🔍 Vérification du système ELO...")
        
        # Vérifier les collections
        collections = await db.list_collection_names()
        required_collections = ["elo_ratings", "elo_matches", "season_stats"]
        
        for collection in required_collections:
            if collection in collections:
                count = await db[collection].count_documents({})
                print(f"  ✅ Collection '{collection}': {count} documents")
            else:
                print(f"  ❌ Collection '{collection}' manquante")
                return False
        
        # Vérifier les index
        elo_ratings_indexes = await db.elo_ratings.list_indexes().to_list(100)
        print(f"  ✅ {len(elo_ratings_indexes)} index créés pour elo_ratings")
        
        elo_matches_indexes = await db.elo_matches.list_indexes().to_list(100)
        print(f"  ✅ {len(elo_matches_indexes)} index créés pour elo_matches")
        
        # Statistiques des ratings
        total_ratings = await db.elo_ratings.count_documents({})
        if total_ratings > 0:
            avg_rating = await db.elo_ratings.aggregate([
                {"$group": {"_id": None, "avg": {"$avg": "$rating"}}}
            ]).to_list(1)
            
            avg_rating_value = avg_rating[0]["avg"] if avg_rating else 1200
            print(f"  📊 Rating ELO moyen: {avg_rating_value:.1f}")
            
            # Distribution par tier
            tier_pipeline = [
                {"$group": {"_id": "$tier", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            tier_dist = await db.elo_ratings.aggregate(tier_pipeline).to_list(10)
            print(f"  🏆 Distribution par tier:")
            for tier_info in tier_dist:
                print(f"      {tier_info['_id'].capitalize()}: {tier_info['count']} joueurs")
        
        print("📊 Système ELO prêt à l'emploi !")
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur vérification: {str(e)}")
        return False

async def main():
    """Fonction principale d'initialisation"""
    print("📊 INITIALISATION DU SYSTÈME ELO AUTOMATIQUE")
    print("=" * 60)
    
    try:
        # Tester la connexion à la base de données
        await db.command("ping")
        print("✅ Connexion à MongoDB réussie")
        
        # Étapes d'initialisation
        steps = [
            ("Création des collections", create_elo_collections),
            ("Initialisation ratings utilisateurs", initialize_user_elo_ratings),
            ("Matchs d'exemple", create_sample_elo_matches),
            ("Vérification système", verify_elo_system)
        ]
        
        for step_name, step_func in steps:
            print(f"\n📋 {step_name}...")
            success = await step_func()
            if not success:
                print(f"❌ Échec de l'étape: {step_name}")
                return False
        
        print("\n" + "=" * 60)
        print("🎉 INITIALISATION DU SYSTÈME ELO TERMINÉE AVEC SUCCÈS !")
        print("\nNouvelles fonctionnalités disponibles:")
        print("  📊 Système de classement ELO complet")
        print("  🏆 8 tiers de classement (Bronze à Challenger)")
        print("  ⚔️ Traitement automatique des résultats de matchs")
        print("  📈 Historique détaillé des matchs et évolution ELO")
        print("  🎯 Classements par jeu et mode de jeu")
        print("  👨‍💼 Interface d'administration pour gestion manuelle")
        print("  🔄 Système de dégradation pour inactivité")
        print("  🏅 Intégration automatique avec les tournois")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR FATALE: {str(e)}")
        return False
    
    finally:
        client.close()

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)