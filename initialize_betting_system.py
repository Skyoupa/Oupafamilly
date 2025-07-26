import pymongo
from datetime import datetime, timedelta
import uuid
import random

def initialize_betting_system():
    """
    Initialiser le système de paris avec :
    - Quelques tournois de test
    - Marchés de paris correspondants
    """
    
    # Connect to MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['oupafamilly_db']
    
    print("🎲 Initialisation du système de paris...")
    
    # Vérifier s'il y a des tournois existants
    existing_tournaments = db.tournaments.count_documents({})
    
    if existing_tournaments == 0:
        print("📅 Création de tournois de test...")
        
        # Créer quelques tournois de test
        tournaments = [
            {
                "id": str(uuid.uuid4()),
                "title": "Championship CS2 Oupafamilly",
                "description": "Le tournoi principal de CS2 de la communauté",
                "game": "cs2",
                "type": "tournament",
                "max_participants": 16,
                "entry_fee": 0,
                "prize_pool": 1000,
                "status": "registration_open",
                "registration_opens": datetime.utcnow(),
                "registration_closes": datetime.utcnow() + timedelta(days=7),
                "tournament_starts": datetime.utcnow() + timedelta(days=10),
                "tournament_ends": datetime.utcnow() + timedelta(days=12),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Coupe LoL Printemps",
                "description": "Tournoi saisonnier de League of Legends",
                "game": "lol",
                "type": "tournament",
                "max_participants": 8,
                "entry_fee": 0,
                "prize_pool": 500,
                "status": "registration_open",
                "registration_opens": datetime.utcnow(),
                "registration_closes": datetime.utcnow() + timedelta(days=5),
                "tournament_starts": datetime.utcnow() + timedelta(days=8),
                "tournament_ends": datetime.utcnow() + timedelta(days=9),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "title": "WoW Arena Masters",
                "description": "Compétition d'arène World of Warcraft",
                "game": "wow",
                "type": "tournament",
                "max_participants": 12,
                "entry_fee": 0,
                "prize_pool": 750,
                "status": "ongoing",
                "registration_opens": datetime.utcnow() - timedelta(days=5),
                "registration_closes": datetime.utcnow() - timedelta(days=1),
                "tournament_starts": datetime.utcnow(),
                "tournament_ends": datetime.utcnow() + timedelta(days=2),
                "created_at": datetime.utcnow() - timedelta(days=5),
                "updated_at": datetime.utcnow()
            }
        ]
        
        db.tournaments.insert_many(tournaments)
        print(f"  ✅ {len(tournaments)} tournois créés")
        
    else:
        print(f"  ℹ️  Tournois déjà présents ({existing_tournaments} tournois)")
        tournaments = list(db.tournaments.find({}).limit(3))
    
    # Créer des marchés de paris pour ces tournois
    print("💰 Création de marchés de paris...")
    
    existing_markets = db.betting_markets.count_documents({})
    if existing_markets == 0:
        markets = []
        
        for tournament in tournaments:
            # Marché "Vainqueur du tournoi"
            winner_market = {
                "id": str(uuid.uuid4()),
                "tournament_id": tournament["id"],
                "tournament_name": tournament["title"],
                "game": tournament["game"],
                "market_type": "winner",
                "title": f"Vainqueur - {tournament['title']}",
                "description": f"Qui remportera le tournoi {tournament['title']} ?",
                "options": [
                    {"option_id": "team1", "name": "Team Alpha", "odds": 2.5},
                    {"option_id": "team2", "name": "Team Beta", "odds": 3.0},
                    {"option_id": "team3", "name": "Team Gamma", "odds": 4.0},
                    {"option_id": "team4", "name": "Team Delta", "odds": 6.0},
                    {"option_id": "other", "name": "Autre équipe", "odds": 8.0}
                ],
                "total_pool": 0,
                "status": "open" if tournament["status"] in ["registration_open", "ongoing"] else "closed",
                "closes_at": tournament["tournament_starts"] if tournament["tournament_starts"] > datetime.utcnow() else datetime.utcnow() + timedelta(hours=1),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            markets.append(winner_market)
            
            # Marché "Premier match" (pour les tournois en cours ou à venir)
            if tournament["status"] in ["registration_open", "ongoing"]:
                first_match_market = {
                    "id": str(uuid.uuid4()),
                    "tournament_id": tournament["id"],
                    "tournament_name": tournament["title"],
                    "game": tournament["game"],
                    "market_type": "match_result",
                    "title": f"Premier Match - {tournament['title']}",
                    "description": f"Résultat du premier match du tournoi {tournament['title']}",
                    "options": [
                        {"option_id": "team_a", "name": "Team A gagne", "odds": 1.8},
                        {"option_id": "team_b", "name": "Team B gagne", "odds": 2.1}
                    ],
                    "total_pool": 0,
                    "status": "open",
                    "closes_at": tournament["tournament_starts"] if tournament["tournament_starts"] > datetime.utcnow() else datetime.utcnow() + timedelta(minutes=30),
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                markets.append(first_match_market)
            
            # Marché spécial "Performance individuelle"
            if tournament["game"] == "cs2":
                special_market = {
                    "id": str(uuid.uuid4()),
                    "tournament_id": tournament["id"],
                    "tournament_name": tournament["title"],
                    "game": tournament["game"],
                    "market_type": "special",
                    "title": f"Meilleur Joueur - {tournament['title']}",
                    "description": f"Qui sera le MVP du tournoi {tournament['title']} ?",
                    "options": [
                        {"option_id": "player1", "name": "ProPlayer1", "odds": 3.5},
                        {"option_id": "player2", "name": "AceShooter", "odds": 4.0},
                        {"option_id": "player3", "name": "StratMaster", "odds": 5.0},
                        {"option_id": "player4", "name": "ClutchKing", "odds": 6.5}
                    ],
                    "total_pool": 0,
                    "status": "open",
                    "closes_at": tournament["tournament_starts"] if tournament["tournament_starts"] > datetime.utcnow() else datetime.utcnow() + timedelta(hours=2),
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                markets.append(special_market)
        
        if markets:
            db.betting_markets.insert_many(markets)
            print(f"  ✅ {len(markets)} marchés de paris créés")
        
    else:
        print(f"  ℹ️  Marchés déjà présents ({existing_markets} marchés)")
    
    # Créer quelques paris de test pour simuler l'activité
    print("🎯 Création de paris de test...")
    
    existing_bets = db.bets.count_documents({})
    if existing_bets == 0:
        # Obtenir quelques utilisateurs pour créer des paris
        users = list(db.users.find({}).limit(5))
        markets = list(db.betting_markets.find({"status": "open"}).limit(3))
        
        test_bets = []
        
        if users and markets:
            for i, user in enumerate(users[:3]):  # 3 premiers utilisateurs
                for j, market in enumerate(markets[:2]):  # 2 premiers marchés
                    if len(market["options"]) > 0:
                        selected_option = random.choice(market["options"])
                        bet_amount = random.choice([50, 100, 150, 200])
                        
                        bet = {
                            "id": str(uuid.uuid4()),
                            "user_id": user["id"],
                            "user_name": user["username"],
                            "market_id": market["id"],
                            "option_id": selected_option["option_id"],
                            "option_name": selected_option["name"],
                            "amount": bet_amount,
                            "potential_payout": int(bet_amount * selected_option["odds"]),
                            "odds": selected_option["odds"],
                            "status": "active",
                            "placed_at": datetime.utcnow() - timedelta(minutes=random.randint(10, 120))
                        }
                        test_bets.append(bet)
            
            if test_bets:
                db.bets.insert_many(test_bets)
                
                # Mettre à jour les pools des marchés
                for bet in test_bets:
                    db.betting_markets.update_one(
                        {"id": bet["market_id"]},
                        {"$inc": {"total_pool": bet["amount"]}}
                    )
                
                print(f"  ✅ {len(test_bets)} paris de test créés")
            else:
                print("  ⚠️  Pas assez de données pour créer des paris de test")
        else:
            print("  ⚠️  Pas d'utilisateurs ou de marchés pour les paris de test")
    else:
        print(f"  ℹ️  Paris déjà présents ({existing_bets} paris)")
    
    # Statistiques finales
    print("\n📊 Récapitulatif du système de paris:")
    total_tournaments = db.tournaments.count_documents({})
    total_markets = db.betting_markets.count_documents({})
    open_markets = db.betting_markets.count_documents({"status": "open"})
    total_bets = db.bets.count_documents({})
    
    # Calcul du pool total
    total_pool_result = list(db.betting_markets.aggregate([
        {"$group": {"_id": None, "total": {"$sum": "$total_pool"}}}
    ]))
    total_pool = total_pool_result[0]["total"] if total_pool_result else 0
    
    print(f"  🏆 Tournois: {total_tournaments}")
    print(f"  💰 Marchés de paris: {total_markets} (dont {open_markets} ouverts)")
    print(f"  🎯 Paris placés: {total_bets}")
    print(f"  💎 Pool total: {total_pool} coins")
    
    # Créer quelques collections manquantes pour la structure
    collections_to_init = [
        "betting_markets",
        "bets"
    ]
    
    for collection_name in collections_to_init:
        if collection_name not in db.list_collection_names():
            # Créer la collection avec un document temporaire
            db[collection_name].insert_one({"_temp": True, "created_at": datetime.utcnow()})
            # Supprimer le document temporaire
            db[collection_name].delete_one({"_temp": True})
            print(f"  ✅ Collection {collection_name} créée")
    
    print("\n🎉 Système de paris initialisé avec succès !")
    print("\n💡 Fonctionnalités disponibles :")
    print("  - Paris sur les tournois (vainqueur, matchs, spéciaux)")
    print("  - Marchés avec cotes dynamiques")
    print("  - Gestion automatique des gains/pertes")
    print("  - Statistiques et leaderboard des parieurs")
    print("  - Règlement automatique des paris")
    print("  - Intégration avec le système de coins")
    
    return True

if __name__ == '__main__':
    initialize_betting_system()