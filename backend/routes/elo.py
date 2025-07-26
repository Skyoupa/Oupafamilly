"""
📊 API ENDPOINTS POUR SYSTÈME ELO
Endpoints pour consultation et gestion du système de classement ELO
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict, Any, Optional
from models import User
from auth import get_current_active_user, is_admin
from elo_system import (
    elo_engine, EloTier, GameMode,
    get_user_elo_complete, get_elo_rankings,
    process_tournament_match, process_regular_match
)
from monitoring import log_user_action, app_logger
from database import db
from datetime import datetime

router = APIRouter(prefix="/elo", tags=["ELO Rating System"])

# =====================================================
# PUBLIC ELO ENDPOINTS
# =====================================================

@router.get("/profile/{user_id}")
async def get_user_elo_profile(
    user_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Récupère le profil ELO complet d'un utilisateur"""
    try:
        elo_profile = await get_user_elo_complete(user_id)
        
        if not elo_profile or "error" in elo_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profil ELO non trouvé ou erreur de récupération"
            )
        
        # Enrichir avec les informations utilisateur
        user_data = await db.users.find_one({"id": user_id})
        if user_data:
            elo_profile["username"] = user_data.get("username", "Inconnu")
            elo_profile["display_name"] = user_data.get("display_name", user_data.get("username", "Inconnu"))
        
        log_user_action(current_user.id, "viewed_elo_profile", {"target_user": user_id})
        
        return elo_profile
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Erreur récupération profil ELO: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération du profil ELO"
        )

@router.get("/my-profile")
async def get_my_elo_profile(current_user: User = Depends(get_current_active_user)):
    """Récupère le profil ELO de l'utilisateur connecté"""
    return await get_user_elo_profile(current_user.id, current_user)

@router.get("/leaderboard")
async def get_elo_leaderboard(
    game: Optional[str] = Query(None, regex="^(cs2|lol|wow|sc2|minecraft)$"),
    mode: Optional[GameMode] = None,
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(get_current_active_user)
):
    """Récupère le classement ELO avec filtres"""
    try:
        leaderboard = await get_elo_rankings(game=game, limit=limit)
        
        # Trouver la position de l'utilisateur actuel
        current_user_rank = None
        current_user_rating = None
        
        for entry in leaderboard:
            if entry["user_id"] == current_user.id:
                current_user_rank = entry["rank"]
                current_user_rating = entry["rating"]
                entry["is_current_user"] = True
                break
            else:
                entry["is_current_user"] = False
        
        # Si l'utilisateur n'est pas dans le top, récupérer sa position
        if current_user_rank is None:
            user_elo = await get_user_elo_complete(current_user.id)
            if user_elo and "overall_rating" in user_elo:
                current_user_rating = user_elo["overall_rating"]
                
                # Compter combien d'utilisateurs ont un rating supérieur
                query = {"season": elo_engine.CURRENT_SEASON, "rating": {"$gt": current_user_rating}}
                if game:
                    query["game"] = game
                if mode:
                    query["mode"] = mode.value
                
                higher_rated_count = await db.elo_ratings.count_documents(query)
                current_user_rank = higher_rated_count + 1
        
        # Statistiques globales du leaderboard
        if leaderboard:
            avg_rating = sum(entry["rating"] for entry in leaderboard) / len(leaderboard)
            tier_distribution = {}
            for entry in leaderboard:
                tier = entry.get("tier", "silver")
                tier_distribution[tier] = tier_distribution.get(tier, 0) + 1
        else:
            avg_rating = 1200
            tier_distribution = {}
        
        return {
            "leaderboard": leaderboard,
            "filters": {
                "game": game,
                "mode": mode.value if mode else None,
                "limit": limit
            },
            "current_user": {
                "rank": current_user_rank,
                "rating": current_user_rating,
                "user_id": current_user.id
            },
            "statistics": {
                "total_players": len(leaderboard),
                "average_rating": round(avg_rating, 1),
                "tier_distribution": tier_distribution
            }
        }
        
    except Exception as e:
        app_logger.error(f"Erreur génération leaderboard ELO: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la génération du classement"
        )

@router.get("/tiers")
async def get_elo_tiers():
    """Récupère la liste des tiers ELO avec leurs seuils"""
    try:
        tiers = [
            {"tier": EloTier.BRONZE, "min_rating": 0, "max_rating": 999, "color": "#CD7F32"},
            {"tier": EloTier.SILVER, "min_rating": 1000, "max_rating": 1199, "color": "#C0C0C0"},
            {"tier": EloTier.GOLD, "min_rating": 1200, "max_rating": 1399, "color": "#FFD700"},
            {"tier": EloTier.PLATINUM, "min_rating": 1400, "max_rating": 1599, "color": "#E5E4E2"},
            {"tier": EloTier.DIAMOND, "min_rating": 1600, "max_rating": 1799, "color": "#B9F2FF"},
            {"tier": EloTier.MASTER, "min_rating": 1800, "max_rating": 1999, "color": "#9966CC"},
            {"tier": EloTier.GRANDMASTER, "min_rating": 2000, "max_rating": 2199, "color": "#FF6B6B"},
            {"tier": EloTier.CHALLENGER, "min_rating": 2200, "max_rating": None, "color": "#FF0000"}
        ]
        
        # Compter les joueurs dans chaque tier
        for tier_info in tiers:
            query = {
                "season": elo_engine.CURRENT_SEASON,
                "rating": {"$gte": tier_info["min_rating"]}
            }
            if tier_info["max_rating"]:
                query["rating"]["$lte"] = tier_info["max_rating"]
            
            player_count = await db.elo_ratings.count_documents(query)
            tier_info["player_count"] = player_count
        
        return {
            "tiers": tiers,
            "current_season": elo_engine.CURRENT_SEASON
        }
        
    except Exception as e:
        app_logger.error(f"Erreur récupération tiers ELO: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des tiers"
        )

@router.get("/match-history/{user_id}")
async def get_user_elo_match_history(
    user_id: str,
    limit: int = Query(20, ge=1, le=100),
    game: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """Récupère l'historique des matchs ELO d'un utilisateur"""
    try:
        # Construire la requête
        query = {
            "$or": [
                {"winner_id": user_id},
                {"loser_id": user_id}
            ]
        }
        
        if game:
            query["game"] = game
        
        # Récupérer l'historique
        matches = await db.elo_matches.find(query).sort("played_at", -1).limit(limit).to_list(limit)
        
        # Enrichir les données
        enriched_matches = []
        for match in matches:
            is_winner = match["winner_id"] == user_id
            opponent_id = match["loser_id"] if is_winner else match["winner_id"]
            
            # Récupérer les infos de l'adversaire
            opponent = await db.users.find_one({"id": opponent_id})
            opponent_name = opponent.get("username", "Inconnu") if opponent else "Inconnu"
            
            rating_change = match["rating_change"] if is_winner else -match["rating_change"]
            
            enriched_matches.append({
                "match_id": match["match_id"],
                "game": match["game"],
                "mode": match["mode"],
                "result": "win" if is_winner else "loss",
                "opponent_id": opponent_id,
                "opponent_name": opponent_name,
                "rating_before": match["winner_rating_before"] if is_winner else match["loser_rating_before"],
                "rating_after": match["winner_rating_after"] if is_winner else match["loser_rating_after"],
                "rating_change": rating_change,
                "match_importance": match.get("match_importance", 1.0),
                "tournament_id": match.get("tournament_id"),
                "played_at": match["played_at"],
                "season": match.get("season", "2025-S1")
            })
        
        # Statistiques de l'historique
        wins = sum(1 for m in enriched_matches if m["result"] == "win")
        losses = len(enriched_matches) - wins
        win_rate = (wins / len(enriched_matches)) if enriched_matches else 0.0
        
        avg_rating_change = sum(abs(m["rating_change"]) for m in enriched_matches) / len(enriched_matches) if enriched_matches else 0
        
        return {
            "matches": enriched_matches,
            "statistics": {
                "total_matches": len(enriched_matches),
                "wins": wins,
                "losses": losses,
                "win_rate": round(win_rate, 3),
                "average_rating_change": round(avg_rating_change, 1)
            },
            "filters": {
                "game": game,
                "limit": limit
            }
        }
        
    except Exception as e:
        app_logger.error(f"Erreur récupération historique matchs ELO: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération de l'historique"
        )

@router.get("/my-match-history")
async def get_my_elo_match_history(
    limit: int = Query(20, ge=1, le=100),
    game: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """Récupère l'historique des matchs ELO de l'utilisateur connecté"""
    return await get_user_elo_match_history(current_user.id, limit, game, current_user)

@router.get("/statistics")
async def get_elo_global_statistics():
    """Statistiques globales du système ELO"""
    try:
        # Statistiques générales
        total_players = await db.elo_ratings.count_documents({"season": elo_engine.CURRENT_SEASON})
        total_matches = await db.elo_matches.count_documents({"season": elo_engine.CURRENT_SEASON})
        
        # Distribution par tier
        tier_stats = {}
        for tier in EloTier:
            min_rating, max_rating = _get_tier_range(tier)
            query = {
                "season": elo_engine.CURRENT_SEASON,
                "rating": {"$gte": min_rating}
            }
            if max_rating:
                query["rating"]["$lte"] = max_rating
            
            count = await db.elo_ratings.count_documents(query)
            tier_stats[tier.value] = count
        
        # Joueurs les plus actifs
        most_active_pipeline = [
            {"$match": {"season": elo_engine.CURRENT_SEASON}},
            {"$sort": {"matches_played": -1}},
            {"$limit": 5},
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
                    "username": {"$arrayElemAt": ["$user_info.username", 0]},
                    "rating": 1,
                    "matches_played": 1,
                    "wins": 1,
                    "win_rate": 1
                }
            }
        ]
        
        most_active = await db.elo_ratings.aggregate(most_active_pipeline).to_list(5)
        
        # Rating moyen par jeu
        avg_by_game_pipeline = [
            {"$match": {"season": elo_engine.CURRENT_SEASON}},
            {
                "$group": {
                    "_id": "$game",
                    "avg_rating": {"$avg": "$rating"},
                    "player_count": {"$sum": 1},
                    "max_rating": {"$max": "$rating"}
                }
            },
            {"$sort": {"player_count": -1}}
        ]
        
        game_stats = await db.elo_ratings.aggregate(avg_by_game_pipeline).to_list(10)
        
        return {
            "overview": {
                "total_players": total_players,
                "total_matches": total_matches,
                "current_season": elo_engine.CURRENT_SEASON
            },
            "tier_distribution": tier_stats,
            "most_active_players": most_active,
            "statistics_by_game": [
                {
                    "game": stat["_id"],
                    "average_rating": round(stat["avg_rating"], 1),
                    "player_count": stat["player_count"],
                    "highest_rating": stat["max_rating"]
                }
                for stat in game_stats
            ]
        }
        
    except Exception as e:
        app_logger.error(f"Erreur statistiques globales ELO: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la génération des statistiques"
        )

# =====================================================
# ADMIN ELO ENDPOINTS
# =====================================================

@router.post("/admin/process-match")
async def admin_process_match(
    winner_id: str,
    loser_id: str,
    game: str,
    tournament_id: Optional[str] = None,
    match_id: Optional[str] = None,
    is_tournament: bool = True,
    importance: float = 1.0,
    current_user: User = Depends(get_current_active_user)
):
    """Admin: Traiter manuellement un résultat de match pour l'ELO"""
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès administrateur requis"
        )
    
    try:
        # Vérifier que les utilisateurs existent
        winner = await db.users.find_one({"id": winner_id})
        loser = await db.users.find_one({"id": loser_id})
        
        if not winner or not loser:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Un ou plusieurs utilisateurs non trouvés"
            )
        
        # Traiter le match
        if is_tournament and tournament_id:
            result = await process_tournament_match(winner_id, loser_id, game, tournament_id, match_id)
        else:
            result = await process_regular_match(winner_id, loser_id, game, match_id, importance)
        
        log_user_action(current_user.id, "admin_elo_match_processed", {
            "winner_id": winner_id,
            "loser_id": loser_id,
            "game": game,
            "tournament_id": tournament_id
        })
        
        return {
            "message": "Match traité avec succès",
            "result": result,
            "winner_name": winner.get("username", "Inconnu"),
            "loser_name": loser.get("username", "Inconnu")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Erreur traitement match admin: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors du traitement du match"
        )

@router.post("/admin/reset-user-elo")
async def admin_reset_user_elo(
    user_id: str,
    new_rating: int = 1200,
    current_user: User = Depends(get_current_active_user)
):
    """Admin: Réinitialiser l'ELO d'un utilisateur"""
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès administrateur requis"
        )
    
    try:
        # Vérifier que l'utilisateur existe
        user = await db.users.find_one({"id": user_id})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        
        # Réinitialiser tous les ratings de l'utilisateur
        tier, tier_progress = elo_engine.get_elo_tier(new_rating)
        
        result = await db.elo_ratings.update_many(
            {"user_id": user_id, "season": elo_engine.CURRENT_SEASON},
            {
                "$set": {
                    "rating": new_rating,
                    "peak_rating": new_rating,
                    "tier": tier.value,
                    "tier_progress": tier_progress,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        log_user_action(current_user.id, "admin_elo_reset", {
            "target_user": user_id,
            "new_rating": new_rating
        })
        
        return {
            "message": f"ELO de {user.get('username', 'utilisateur')} réinitialisé à {new_rating}",
            "ratings_updated": result.modified_count
        }
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Erreur réinitialisation ELO admin: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la réinitialisation"
        )

@router.post("/admin/apply-decay")
async def admin_apply_elo_decay(current_user: User = Depends(get_current_active_user)):
    """Admin: Appliquer manuellement la dégradation d'ELO pour inactivité"""
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès administrateur requis"
        )
    
    try:
        decay_count = await elo_engine.apply_inactivity_decay()
        
        log_user_action(current_user.id, "admin_elo_decay_applied", {
            "players_affected": decay_count
        })
        
        return {
            "message": f"Dégradation ELO appliquée à {decay_count} joueurs inactifs",
            "players_affected": decay_count
        }
        
    except Exception as e:
        app_logger.error(f"Erreur application dégradation ELO admin: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de l'application de la dégradation"
        )

def _get_tier_range(tier: EloTier) -> tuple:
    """Retourne les seuils min/max d'un tier"""
    ranges = {
        EloTier.BRONZE: (0, 999),
        EloTier.SILVER: (1000, 1199),
        EloTier.GOLD: (1200, 1399),
        EloTier.PLATINUM: (1400, 1599),
        EloTier.DIAMOND: (1600, 1799),
        EloTier.MASTER: (1800, 1999),
        EloTier.GRANDMASTER: (2000, 2199),
        EloTier.CHALLENGER: (2200, None)
    }
    return ranges.get(tier, (1200, 1399))