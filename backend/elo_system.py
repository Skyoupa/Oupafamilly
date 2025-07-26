"""
📊 SYSTÈME ELO AUTOMATIQUE PROFESSIONNEL
Calcul intelligent du classement des joueurs basé sur performances tournois
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum
import uuid
import math
from database import db
from monitoring import app_logger, log_user_action

class EloTier(str, Enum):
    """Niveaux ELO avec paliers"""
    BRONZE = "bronze"        # 0-999
    SILVER = "silver"        # 1000-1199
    GOLD = "gold"           # 1200-1399
    PLATINUM = "platinum"   # 1400-1599
    DIAMOND = "diamond"     # 1600-1799
    MASTER = "master"       # 1800-1999
    GRANDMASTER = "grandmaster"  # 2000-2199
    CHALLENGER = "challenger"    # 2200+

class GameMode(str, Enum):
    """Modes de jeu pour ELO séparé"""
    SOLO = "solo"           # 1v1
    TEAM = "team"           # Équipes
    TOURNAMENT = "tournament" # Tournois

class EloRating(BaseModel):
    """Modèle de rating ELO détaillé"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    game: str  # cs2, lol, etc.
    mode: GameMode
    rating: int = 1200
    peak_rating: int = 1200
    matches_played: int = 0
    wins: int = 0
    losses: int = 0
    win_rate: float = 0.0
    tier: EloTier = EloTier.SILVER
    tier_progress: int = 0  # Progression dans le tier (0-100%)
    season: str = "2025-S1"
    last_match_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class EloMatch(BaseModel):
    """Match pour calcul ELO"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    match_id: str  # ID du match original
    tournament_id: Optional[str] = None
    game: str
    mode: GameMode
    winner_id: str
    loser_id: str
    winner_rating_before: int
    loser_rating_before: int
    winner_rating_after: int
    loser_rating_after: int
    rating_change: int  # Changement pour le gagnant (+) et perdant (-)
    match_importance: float = 1.0  # Multiplicateur d'importance (tournoi > match normal)
    season: str = "2025-S1"
    played_at: datetime = Field(default_factory=datetime.utcnow)

class SeasonStats(BaseModel):
    """Statistiques saisonnières"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    season: str
    game: str
    starting_elo: int = 1200
    current_elo: int = 1200
    peak_elo: int = 1200
    matches_played: int = 0
    wins: int = 0
    losses: int = 0
    tournament_wins: int = 0
    tournament_participations: int = 0
    highest_tier_reached: EloTier = EloTier.SILVER
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class EloEngine:
    """Moteur de calcul ELO intelligent"""
    
    def __init__(self):
        self.K_FACTOR_BASE = 32  # Facteur K de base
        self.CURRENT_SEASON = "2025-S1"
        self.DECAY_THRESHOLD_DAYS = 30  # Seuil de déclin d'inactivité
        self.DECAY_AMOUNT = 25  # Points perdus par période d'inactivité
    
    def get_elo_tier(self, rating: int) -> Tuple[EloTier, int]:
        """Retourne le tier et la progression basé sur le rating"""
        if rating < 1000:
            return EloTier.BRONZE, min(100, int((rating / 1000) * 100))
        elif rating < 1200:
            return EloTier.SILVER, int(((rating - 1000) / 200) * 100)
        elif rating < 1400:
            return EloTier.GOLD, int(((rating - 1200) / 200) * 100)
        elif rating < 1600:
            return EloTier.PLATINUM, int(((rating - 1400) / 200) * 100)
        elif rating < 1800:
            return EloTier.DIAMOND, int(((rating - 1600) / 200) * 100)
        elif rating < 2000:
            return EloTier.MASTER, int(((rating - 1800) / 200) * 100)
        elif rating < 2200:
            return EloTier.GRANDMASTER, int(((rating - 2000) / 200) * 100)
        else:
            return EloTier.CHALLENGER, min(100, int(((rating - 2200) / 300) * 100))
    
    def calculate_k_factor(self, rating: int, matches_played: int, is_tournament: bool = False) -> int:
        """Calcule le facteur K adaptatif"""
        base_k = self.K_FACTOR_BASE
        
        # Nouveaux joueurs : K plus élevé pour progression rapide
        if matches_played < 10:
            base_k = 48
        elif matches_played < 30:
            base_k = 40
        
        # Joueurs haute ELO : K plus faible pour stabilité
        if rating > 2000:
            base_k = int(base_k * 0.75)
        elif rating > 1800:
            base_k = int(base_k * 0.85)
        
        # Bonus tournois
        if is_tournament:
            base_k = int(base_k * 1.5)
        
        return max(16, min(50, base_k))  # Limité entre 16 et 50
    
    def calculate_expected_score(self, rating_a: int, rating_b: int) -> float:
        """Calcule le score attendu pour le joueur A contre B"""
        return 1.0 / (1.0 + math.pow(10, (rating_b - rating_a) / 400.0))
    
    def calculate_rating_change(
        self,
        winner_rating: int,
        loser_rating: int,
        winner_matches: int = 50,
        loser_matches: int = 50,
        is_tournament: bool = False,
        match_importance: float = 1.0
    ) -> Tuple[int, int]:
        """Calcule les nouveaux ratings après un match"""
        
        # Calcul des scores attendus
        winner_expected = self.calculate_expected_score(winner_rating, loser_rating)
        loser_expected = 1.0 - winner_expected
        
        # Facteurs K adaptatifs
        winner_k = self.calculate_k_factor(winner_rating, winner_matches, is_tournament)
        loser_k = self.calculate_k_factor(loser_rating, loser_matches, is_tournament)
        
        # Changements de rating (gagnant score = 1, perdant score = 0)
        winner_change = int(winner_k * match_importance * (1.0 - winner_expected))
        loser_change = -int(loser_k * match_importance * (0.0 - loser_expected))
        
        # Nouveaux ratings
        new_winner_rating = max(800, winner_rating + winner_change)  # Minimum 800
        new_loser_rating = max(800, loser_rating + loser_change)
        
        return new_winner_rating, new_loser_rating
    
    async def process_match_result(
        self,
        winner_id: str,
        loser_id: str,
        game: str,
        mode: GameMode = GameMode.TOURNAMENT,
        match_id: str = None,
        tournament_id: str = None,
        is_tournament: bool = True,
        match_importance: float = 1.0
    ) -> Dict[str, Any]:
        """Traite le résultat d'un match et met à jour les ELO"""
        try:
            # Récupérer ou créer les ratings ELO des joueurs
            winner_elo = await self._get_or_create_elo_rating(winner_id, game, mode)
            loser_elo = await self._get_or_create_elo_rating(loser_id, game, mode)
            
            # Sauvegarder les ratings avant modification
            winner_rating_before = winner_elo["rating"]
            loser_rating_before = loser_elo["rating"]
            
            # Calculer les nouveaux ratings
            new_winner_rating, new_loser_rating = self.calculate_rating_change(
                winner_rating_before,
                loser_rating_before,
                winner_elo["matches_played"],
                loser_elo["matches_played"],
                is_tournament,
                match_importance
            )
            
            # Changements de rating
            winner_change = new_winner_rating - winner_rating_before
            loser_change = new_loser_rating - loser_rating_before
            
            # Mettre à jour les ratings dans la base
            await self._update_elo_rating(winner_id, game, mode, new_winner_rating, True)
            await self._update_elo_rating(loser_id, game, mode, new_loser_rating, False)
            
            # Enregistrer le match ELO
            elo_match = EloMatch(
                match_id=match_id or str(uuid.uuid4()),
                tournament_id=tournament_id,
                game=game,
                mode=mode,
                winner_id=winner_id,
                loser_id=loser_id,
                winner_rating_before=winner_rating_before,
                loser_rating_before=loser_rating_before,
                winner_rating_after=new_winner_rating,
                loser_rating_after=new_loser_rating,
                rating_change=winner_change,
                match_importance=match_importance,
                season=self.CURRENT_SEASON
            )
            
            await db.elo_matches.insert_one(elo_match.dict())
            
            # Log des changements
            log_user_action(winner_id, "elo_rating_updated", {
                "game": game,
                "mode": mode.value,
                "old_rating": winner_rating_before,
                "new_rating": new_winner_rating,
                "change": winner_change,
                "result": "win"
            })
            
            log_user_action(loser_id, "elo_rating_updated", {
                "game": game,
                "mode": mode.value,
                "old_rating": loser_rating_before,
                "new_rating": new_loser_rating,
                "change": loser_change,
                "result": "loss"
            })
            
            app_logger.info(f"ELO mis à jour: {winner_id} ({winner_rating_before} -> {new_winner_rating}, +{winner_change}) vs {loser_id} ({loser_rating_before} -> {new_loser_rating}, {loser_change})")
            
            return {
                "winner": {
                    "user_id": winner_id,
                    "rating_before": winner_rating_before,
                    "rating_after": new_winner_rating,
                    "change": winner_change
                },
                "loser": {
                    "user_id": loser_id,
                    "rating_before": loser_rating_before,
                    "rating_after": new_loser_rating,
                    "change": loser_change
                },
                "match_id": elo_match.id
            }
            
        except Exception as e:
            app_logger.error(f"Erreur traitement match ELO: {str(e)}")
            raise
    
    async def _get_or_create_elo_rating(self, user_id: str, game: str, mode: GameMode) -> Dict[str, Any]:
        """Récupère ou crée le rating ELO d'un utilisateur"""
        try:
            # Chercher rating existant
            rating = await db.elo_ratings.find_one({
                "user_id": user_id,
                "game": game,
                "mode": mode.value,
                "season": self.CURRENT_SEASON
            })
            
            if rating:
                return rating
            
            # Créer nouveau rating
            new_rating = EloRating(
                user_id=user_id,
                game=game,
                mode=mode,
                season=self.CURRENT_SEASON
            )
            
            await db.elo_ratings.insert_one(new_rating.dict())
            return new_rating.dict()
            
        except Exception as e:
            app_logger.error(f"Erreur get/create ELO rating: {str(e)}")
            raise
    
    async def _update_elo_rating(self, user_id: str, game: str, mode: GameMode, new_rating: int, won: bool):
        """Met à jour le rating ELO d'un utilisateur"""
        try:
            # Calculer tier et progression
            tier, tier_progress = self.get_elo_tier(new_rating)
            
            # Préparer la mise à jour
            update_data = {
                "$set": {
                    "rating": new_rating,
                    "tier": tier.value,
                    "tier_progress": tier_progress,
                    "last_match_date": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                },
                "$inc": {
                    "matches_played": 1,
                    "wins" if won else "losses": 1
                },
                "$max": {
                    "peak_rating": new_rating
                }
            }
            
            # Mettre à jour le taux de victoire
            current_rating = await db.elo_ratings.find_one({
                "user_id": user_id,
                "game": game,
                "mode": mode.value,
                "season": self.CURRENT_SEASON
            })
            
            if current_rating:
                total_matches = current_rating.get("matches_played", 0) + 1
                current_wins = current_rating.get("wins", 0) + (1 if won else 0)
                win_rate = (current_wins / total_matches) if total_matches > 0 else 0.0
                update_data["$set"]["win_rate"] = round(win_rate, 3)
            
            await db.elo_ratings.update_one(
                {
                    "user_id": user_id,
                    "game": game,
                    "mode": mode.value,
                    "season": self.CURRENT_SEASON
                },
                update_data
            )
            
            # Mettre à jour le profil utilisateur principal avec l'ELO global
            await self._update_user_main_elo(user_id, new_rating)
            
        except Exception as e:
            app_logger.error(f"Erreur mise à jour ELO rating: {str(e)}")
            raise
    
    async def _update_user_main_elo(self, user_id: str, new_rating: int):
        """Met à jour l'ELO principal dans le profil utilisateur"""
        try:
            # Récupérer l'ELO le plus élevé de l'utilisateur (tous jeux confondus)
            pipeline = [
                {"$match": {"user_id": user_id, "season": self.CURRENT_SEASON}},
                {"$group": {"_id": None, "max_rating": {"$max": "$rating"}}}
            ]
            
            result = await db.elo_ratings.aggregate(pipeline).to_list(1)
            highest_rating = result[0]["max_rating"] if result else new_rating
            
            # Calculer tier global
            tier, tier_progress = self.get_elo_tier(highest_rating)
            
            # Mettre à jour le profil utilisateur
            await db.user_profiles.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "elo_rating": highest_rating,
                        "peak_elo": {"$max": ["$peak_elo", highest_rating]},
                        "elo_tier": tier.value,
                        "elo_tier_progress": tier_progress,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
        except Exception as e:
            app_logger.error(f"Erreur mise à jour ELO principal: {str(e)}")
    
    async def get_user_elo_profile(self, user_id: str) -> Dict[str, Any]:
        """Récupère le profil ELO complet d'un utilisateur"""
        try:
            # Récupérer tous les ratings de l'utilisateur
            user_ratings = await db.elo_ratings.find({
                "user_id": user_id,
                "season": self.CURRENT_SEASON
            }).to_list(100)
            
            if not user_ratings:
                return {"user_id": user_id, "ratings": [], "overall_rating": 1200}
            
            # Calculer les statistiques globales
            total_matches = sum(r.get("matches_played", 0) for r in user_ratings)
            total_wins = sum(r.get("wins", 0) for r in user_ratings)
            overall_win_rate = (total_wins / total_matches) if total_matches > 0 else 0.0
            highest_rating = max(r.get("rating", 1200) for r in user_ratings)
            peak_rating = max(r.get("peak_rating", 1200) for r in user_ratings)
            
            # Tier global
            tier, tier_progress = self.get_elo_tier(highest_rating)
            
            # Récupérer l'historique récent des matchs
            recent_matches = await db.elo_matches.find({
                "$or": [
                    {"winner_id": user_id},
                    {"loser_id": user_id}
                ]
            }).sort("played_at", -1).limit(10).to_list(10)
            
            return {
                "user_id": user_id,
                "season": self.CURRENT_SEASON,
                "overall_rating": highest_rating,
                "peak_rating": peak_rating,
                "tier": tier.value,
                "tier_progress": tier_progress,
                "total_matches": total_matches,
                "total_wins": total_wins,
                "total_losses": total_matches - total_wins,
                "overall_win_rate": round(overall_win_rate, 3),
                "ratings_by_game": {
                    f"{r['game']}_{r['mode']}": {
                        "rating": r["rating"],
                        "matches": r.get("matches_played", 0),
                        "wins": r.get("wins", 0),
                        "losses": r.get("losses", 0),
                        "win_rate": r.get("win_rate", 0.0),
                        "tier": r.get("tier", "silver"),
                        "peak": r.get("peak_rating", 1200)
                    }
                    for r in user_ratings
                },
                "recent_matches": [
                    {
                        "match_id": m["match_id"],
                        "game": m["game"],
                        "mode": m["mode"],
                        "result": "win" if m["winner_id"] == user_id else "loss",
                        "rating_change": m["rating_change"] if m["winner_id"] == user_id else -m["rating_change"],
                        "opponent_id": m["loser_id"] if m["winner_id"] == user_id else m["winner_id"],
                        "date": m["played_at"]
                    }
                    for m in recent_matches
                ]
            }
            
        except Exception as e:
            app_logger.error(f"Erreur récupération profil ELO: {str(e)}")
            return {"user_id": user_id, "error": str(e)}
    
    async def get_elo_leaderboard(
        self,
        game: str = None,
        mode: GameMode = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Récupère le leaderboard ELO"""
        try:
            # Construire la requête
            query = {"season": self.CURRENT_SEASON}
            if game:
                query["game"] = game
            if mode:
                query["mode"] = mode.value
            
            # Pipeline d'agrégation pour le classement
            pipeline = [
                {"$match": query},
                {"$sort": {"rating": -1}},
                {"$limit": limit},
                {
                    "$lookup": {
                        "from": "users",
                        "localField": "user_id",
                        "foreignField": "id",
                        "as": "user_info"
                    }
                },
                {
                    "$project": {
                        "_id": 0,  # Exclude MongoDB ObjectId
                        "user_id": 1,
                        "game": 1,
                        "mode": 1,
                        "rating": 1,
                        "peak_rating": 1,
                        "tier": 1,
                        "tier_progress": 1,
                        "matches_played": 1,
                        "wins": 1,
                        "losses": 1,
                        "win_rate": 1,
                        "last_match_date": 1,
                        "username": {"$arrayElemAt": ["$user_info.username", 0]},
                        "display_name": {"$arrayElemAt": ["$user_info.display_name", 0]}
                    }
                }
            ]
            
            leaderboard_data = await db.elo_ratings.aggregate(pipeline).to_list(limit)
            
            # Enrichir avec le rang
            enriched_leaderboard = []
            for i, entry in enumerate(leaderboard_data):
                entry["rank"] = i + 1
                entry["username"] = entry.get("username", "Inconnu")
                entry["display_name"] = entry.get("display_name", entry.get("username", "Inconnu"))
                enriched_leaderboard.append(entry)
            
            return enriched_leaderboard
            
        except Exception as e:
            app_logger.error(f"Erreur génération leaderboard ELO: {str(e)}")
            return []
    
    async def apply_inactivity_decay(self):
        """Applique la dégradation d'ELO pour inactivité"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=self.DECAY_THRESHOLD_DAYS)
            
            # Trouver les joueurs inactifs avec ELO > 1200 (pour éviter de pénaliser les débutants)
            inactive_players = await db.elo_ratings.find({
                "last_match_date": {"$lt": cutoff_date},
                "rating": {"$gt": 1200},
                "season": self.CURRENT_SEASON
            }).to_list(1000)
            
            decay_count = 0
            for player in inactive_players:
                new_rating = max(1200, player["rating"] - self.DECAY_AMOUNT)
                if new_rating < player["rating"]:
                    # Appliquer la dégradation
                    tier, tier_progress = self.get_elo_tier(new_rating)
                    
                    await db.elo_ratings.update_one(
                        {"_id": player["_id"]},
                        {
                            "$set": {
                                "rating": new_rating,
                                "tier": tier.value,
                                "tier_progress": tier_progress,
                                "updated_at": datetime.utcnow()
                            }
                        }
                    )
                    
                    # Log de la dégradation
                    log_user_action(player["user_id"], "elo_decay_applied", {
                        "old_rating": player["rating"],
                        "new_rating": new_rating,
                        "decay_amount": player["rating"] - new_rating
                    })
                    
                    decay_count += 1
            
            app_logger.info(f"Dégradation ELO appliquée à {decay_count} joueurs inactifs")
            return decay_count
            
        except Exception as e:
            app_logger.error(f"Erreur application dégradation ELO: {str(e)}")
            return 0

# Instance globale du moteur ELO
elo_engine = EloEngine()

# Fonctions d'API publiques
async def process_tournament_match(winner_id: str, loser_id: str, game: str, tournament_id: str, match_id: str = None):
    """Traite un match de tournoi pour le calcul ELO"""
    return await elo_engine.process_match_result(
        winner_id=winner_id,
        loser_id=loser_id,
        game=game,
        mode=GameMode.TOURNAMENT,
        match_id=match_id,
        tournament_id=tournament_id,
        is_tournament=True,
        match_importance=1.5  # Les tournois ont plus d'importance
    )

async def process_regular_match(winner_id: str, loser_id: str, game: str, match_id: str = None, importance: float = 1.0):
    """Traite un match normal pour le calcul ELO"""
    return await elo_engine.process_match_result(
        winner_id=winner_id,
        loser_id=loser_id,
        game=game,
        mode=GameMode.SOLO,
        match_id=match_id,
        is_tournament=False,
        match_importance=importance
    )

async def get_user_elo_complete(user_id: str):
    """Récupère le profil ELO complet d'un utilisateur"""
    return await elo_engine.get_user_elo_profile(user_id)

async def get_elo_rankings(game: str = None, limit: int = 100):
    """Récupère le classement ELO"""
    return await elo_engine.get_elo_leaderboard(game=game, limit=limit)