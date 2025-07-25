#!/usr/bin/env python3
"""
Script pour nettoyer les tournois non-CS2 et optimiser la base de données 
pour la communauté Oupafamilly centrée sur CS2
"""

import asyncio
import sys
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# Add backend directory to path
sys.path.append('/app/backend')

async def cleanup_non_cs2_tournaments():
    """Supprime tous les tournois qui ne sont pas CS2 et les stats associées"""
    
    # Configuration MongoDB
    MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    DB_NAME = os.getenv('DB_NAME', 'test_database')
    
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    try:
        print("🧹 Nettoyage des données non-CS2...")
        
        # Compter les tournois avant nettoyage
        total_tournaments = await db.tournaments.count_documents({})
        cs2_tournaments = await db.tournaments.count_documents({"game": "cs2"})
        non_cs2_tournaments = total_tournaments - cs2_tournaments
        
        print(f"📊 Tournois actuels: {total_tournaments} total, {cs2_tournaments} CS2, {non_cs2_tournaments} autres jeux")
        
        # Supprimer tous les tournois non-CS2
        if non_cs2_tournaments > 0:
            delete_result = await db.tournaments.delete_many({"game": {"$ne": "cs2"}})
            print(f"❌ Supprimés: {delete_result.deleted_count} tournois non-CS2")
        else:
            print("✅ Aucun tournoi non-CS2 à supprimer")
        
        # Mettre à jour les stats communautaires si nécessaire
        remaining_tournaments = await db.tournaments.count_documents({})
        print(f"🏆 Tournois restants (CS2 uniquement): {remaining_tournaments}")
        
        # Optionnel: Créer un tournoi CS2 de démonstration si aucun n'existe
        if remaining_tournaments == 0:
            print("🎯 Création d'un tournoi CS2 de démonstration...")
            demo_tournament = {
                "id": f"demo_cs2_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "title": "Tournoi CS2 Oupafamilly - Démonstration",
                "description": "Tournoi de démonstration pour la communauté Oupafamilly",
                "game": "cs2",
                "tournament_type": "elimination",
                "status": "draft",
                "max_participants": 16,
                "participants": [],
                "organizer_id": "admin",
                "entry_fee": 0,
                "prize_pool": 50,
                "registration_start": datetime.utcnow(),
                "registration_end": datetime.utcnow().replace(day=datetime.utcnow().day + 7),
                "tournament_start": datetime.utcnow().replace(day=datetime.utcnow().day + 8),
                "rules": """🎯 FORMAT: Élimination directe 5v5
🗺️ MAPS: Mirage, Inferno, Dust2
⏱️ DURÉE: BO1 jusqu'aux demi-finales, BO3 finale
🔫 ARMES: Toutes armes autorisées
📋 RÈGLES: Format compétitif standard CS2""",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            await db.tournaments.insert_one(demo_tournament)
            print("✅ Tournoi de démonstration créé")
        
        print("🎮 Nettoyage terminé - Base de données optimisée pour CS2 uniquement!")
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {str(e)}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(cleanup_non_cs2_tournaments())