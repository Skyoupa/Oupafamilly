#!/usr/bin/env python3
"""
Script pour créer des tournois de test avec matchs
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
import uuid

async def create_test_tournaments():
    """Créer des tournois de test avec matchs pour tester la planification."""
    
    # Load environment variables
    load_dotenv('/app/backend/.env')
    
    # Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL')
    if not mongo_url:
        print("❌ MONGO_URL non trouvé dans les variables d'environnement")
        return
    
    client = AsyncIOMotorClient(mongo_url)
    db_name = os.environ.get('DB_NAME', 'oupafamilly')
    db = client[db_name]
    
    try:
        print("🏆 Création de tournois de test...")
        
        # Date de début et fin des tournois
        start_date = datetime.utcnow() + timedelta(days=1)
        end_date = start_date + timedelta(days=7)
        
        # Récupérer l'admin user pour être l'organisateur
        admin_user = await db.users.find_one({"email": "admin@oupafamilly.com"})
        if not admin_user:
            print("❌ Utilisateur admin non trouvé")
            return
        
        organizer_id = admin_user["id"]
        
        # Tournoi 1 : CS2 Championship
        tournament1_id = str(uuid.uuid4())
        tournament1 = {
            "id": tournament1_id,
            "title": "CS2 Championship 2025",
            "description": "Tournoi professionnel Counter-Strike 2 avec 8 équipes",
            "game": "cs2",
            "type": "elimination",
            "status": "active",
            "max_participants": 8,
            "current_participants": 4,
            "tournament_start": start_date,
            "tournament_end": end_date,
            "prize_pool": 5000,
            "organizer_id": organizer_id,
            "rules": "Format BO3, maps Dust2, Inferno, Mirage",
            "bracket_generated": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        await db.tournaments.insert_one(tournament1)
        print(f"✅ Tournoi créé : {tournament1['title']}")
        
        # Créer des matchs pour le tournoi 1
        matches1 = [
            {
                "id": str(uuid.uuid4()),
                "tournament_id": tournament1_id,
                "round_number": 1,
                "match_number": 1,
                "player1_id": "team1",
                "player2_id": "team2",
                "status": "scheduled",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "notes": "Demi-finale 1"
            },
            {
                "id": str(uuid.uuid4()),
                "tournament_id": tournament1_id,
                "round_number": 1,
                "match_number": 2,
                "player1_id": "team3",
                "player2_id": "team4",
                "status": "scheduled",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "notes": "Demi-finale 2"
            },
            {
                "id": str(uuid.uuid4()),
                "tournament_id": tournament1_id,
                "round_number": 2,
                "match_number": 1,
                "player1_id": "winner_match1",
                "player2_id": "winner_match2",
                "status": "pending",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "notes": "Grande finale"
            }
        ]
        
        await db.matches.insert_many(matches1)
        print(f"✅ {len(matches1)} matchs créés pour CS2 Championship")
        
        # Tournoi 2 : Weekly CS2 Cup
        tournament2_id = str(uuid.uuid4())
        tournament2 = {
            "id": tournament2_id,
            "title": "Weekly CS2 Cup",
            "description": "Compétition hebdomadaire pour la communauté",
            "game": "cs2",
            "type": "round_robin",
            "status": "registration",
            "max_participants": 6,
            "current_participants": 6,
            "tournament_start": start_date + timedelta(days=3),
            "tournament_end": end_date + timedelta(days=2),
            "prize_pool": 1000,
            "organizer_id": organizer_id,
            "rules": "Format BO1, maps aléatoires",
            "bracket_generated": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        await db.tournaments.insert_one(tournament2)
        print(f"✅ Tournoi créé : {tournament2['title']}")
        
        # Créer des matchs pour le tournoi 2
        matches2 = [
            {
                "id": str(uuid.uuid4()),
                "tournament_id": tournament2_id,
                "round_number": 1,
                "match_number": 1,
                "player1_id": "team_a",
                "player2_id": "team_b",
                "status": "scheduled",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            },
            {
                "id": str(uuid.uuid4()),
                "tournament_id": tournament2_id,
                "round_number": 1,
                "match_number": 2,
                "player1_id": "team_c",
                "player2_id": "team_d",
                "status": "scheduled",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
        ]
        
        await db.matches.insert_many(matches2)
        print(f"✅ {len(matches2)} matchs créés pour Weekly CS2 Cup")
        
        # Créer quelques équipes de test pour enrichir les noms
        teams = [
            {"id": "team1", "name": "Team Vitality", "created_at": datetime.utcnow()},
            {"id": "team2", "name": "Team G2", "created_at": datetime.utcnow()},
            {"id": "team3", "name": "Team NaVi", "created_at": datetime.utcnow()},
            {"id": "team4", "name": "Team FaZe", "created_at": datetime.utcnow()},
            {"id": "team_a", "name": "Oupafamilly Pros", "created_at": datetime.utcnow()},
            {"id": "team_b", "name": "Silver Legends", "created_at": datetime.utcnow()},
            {"id": "team_c", "name": "Global Elites", "created_at": datetime.utcnow()},
            {"id": "team_d", "name": "Noobs United", "created_at": datetime.utcnow()},
        ]
        
        for team in teams:
            await db.teams.update_one(
                {"id": team["id"]},
                {"$set": team},
                upsert=True
            )
        
        print(f"✅ {len(teams)} équipes créées/mises à jour")
        
        # Statistiques finales
        total_tournaments = await db.tournaments.count_documents({})
        total_matches = await db.matches.count_documents({})
        total_teams = await db.teams.count_documents({})
        
        print(f"\n📊 Données créées :")
        print(f"   🏆 Tournois : {total_tournaments}")
        print(f"   ⚔️ Matchs : {total_matches}")
        print(f"   👥 Équipes : {total_teams}")
        
        print(f"\n🎯 Tournois disponibles pour test :")
        print(f"   1. CS2 Championship 2025 - ID: {tournament1_id[:8]}...")
        print(f"   2. Weekly CS2 Cup - ID: {tournament2_id[:8]}...")
        
        print(f"\n🎉 Tous les tournois de test créés avec succès !")
        print(f"✅ Vous pouvez maintenant tester la planification des matchs dans l'interface")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tournois : {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    print("🏗️ Création de tournois de test pour la planification...")
    asyncio.run(create_test_tournaments())
    print("🎯 Création terminée !")