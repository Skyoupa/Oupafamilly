"""
🏆 API ENDPOINTS POUR SYSTÈME D'ACHIEVEMENTS
Enrichit l'API existante sans rien modifier
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict, Any, Optional
from models import User
from auth import get_current_active_user, is_admin
from achievements import (
    trigger_achievement_check, get_user_badges, get_all_badges,
    get_badge_progress, achievement_engine, Badge, BadgeCategory, BadgeRarity
)
from monitoring import log_user_action, app_logger
from datetime import datetime

router = APIRouter(prefix="/achievements", tags=["Achievements & Badges"])

@router.get("/my-badges")
async def get_my_badges(current_user: User = Depends(get_current_active_user)):
    """Récupère tous les badges de l'utilisateur connecté"""
    try:
        badges = await get_user_badges(current_user.id)
        
        # Statistiques des badges
        stats = {
            "total_badges": len(badges),
            "by_rarity": {},
            "by_category": {},
            "total_xp_from_badges": 0,
            "total_coins_from_badges": 0
        }
        
        for badge in badges:
            rarity = badge["rarity"]
            category = badge["category"]
            
            stats["by_rarity"][rarity] = stats["by_rarity"].get(rarity, 0) + 1
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
        
        # Calculer XP et coins totaux des badges (approximation)
        for badge in badges:
            badge_info = achievement_engine.badges_registry.get(badge["badge_id"])
            if badge_info:
                stats["total_xp_from_badges"] += badge_info.xp_reward
                stats["total_coins_from_badges"] += badge_info.coins_reward
        
        log_user_action(current_user.id, "viewed_badges", {"badges_count": len(badges)})
        
        return {
            "badges": badges,
            "statistics": stats,
            "user_id": current_user.id,
            "username": current_user.username
        }
        
    except Exception as e:
        app_logger.error(f"Erreur récupération badges utilisateur: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des badges"
        )

@router.get("/user/{user_id}/badges")
async def get_user_badges_public(
    user_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Récupère les badges publics d'un autre utilisateur"""
    try:
        badges = await get_user_badges(user_id)
        
        # Filtrer seulement les badges non-cachés ou déjà obtenus
        public_badges = [badge for badge in badges if not achievement_engine.badges_registry.get(badge["badge_id"], Badge()).hidden]
        
        return {
            "user_id": user_id,
            "badges": public_badges,
            "total_badges": len(public_badges)
        }
        
    except Exception as e:
        app_logger.error(f"Erreur récupération badges publics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des badges"
        )

@router.get("/available")
async def get_available_badges(
    category: Optional[BadgeCategory] = None,
    rarity: Optional[BadgeRarity] = None,
    show_hidden: bool = False,
    current_user: User = Depends(get_current_active_user)
):
    """Récupère tous les badges disponibles avec filtres"""
    try:
        all_badges = await get_all_badges()
        
        # Récupérer les badges déjà obtenus par l'utilisateur
        user_badges = await get_user_badges(current_user.id)
        obtained_badge_ids = [badge["badge_id"] for badge in user_badges]
        
        # Filtrer les badges
        filtered_badges = []
        for badge in all_badges:
            # Filtrer par catégorie
            if category and badge.category != category:
                continue
            
            # Filtrer par rareté
            if rarity and badge.rarity != rarity:
                continue
            
            # Filtrer les badges cachés
            if badge.hidden and not show_hidden and badge.id not in obtained_badge_ids:
                continue
            
            # Enrichir avec le statut d'obtention
            badge_dict = badge.dict()
            badge_dict["obtained"] = badge.id in obtained_badge_ids
            badge_dict["obtainable"] = not badge.hidden or badge.id in obtained_badge_ids
            
            filtered_badges.append(badge_dict)
        
        # Trier par rareté puis par nom
        rarity_order = {
            BadgeRarity.COMMON: 0,
            BadgeRarity.RARE: 1,
            BadgeRarity.EPIC: 2,
            BadgeRarity.LEGENDARY: 3,
            BadgeRarity.MYTHIC: 4
        }
        
        filtered_badges.sort(key=lambda x: (rarity_order.get(x["rarity"], 0), x["name"]))
        
        return {
            "badges": filtered_badges,
            "total": len(filtered_badges),
            "filters_applied": {
                "category": category,
                "rarity": rarity,
                "show_hidden": show_hidden
            }
        }
        
    except Exception as e:
        app_logger.error(f"Erreur récupération badges disponibles: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des badges disponibles"
        )

@router.get("/progress/{badge_id}")
async def get_badge_progress_endpoint(
    badge_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Récupère la progression vers un badge spécifique"""
    try:
        if badge_id not in achievement_engine.badges_registry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Badge non trouvé"
            )
        
        progress = await get_badge_progress(current_user.id, badge_id)
        
        if not progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Impossible de calculer la progression"
            )
        
        return progress
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Erreur calcul progression badge: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors du calcul de la progression"
        )

@router.post("/check")
async def trigger_achievement_check_endpoint(
    current_user: User = Depends(get_current_active_user)
):
    """Déclenche manuellement une vérification des achievements"""
    try:
        new_badges = await trigger_achievement_check(current_user.id)
        
        app_logger.info(f"Vérification manuelle achievements pour {current_user.username}, {len(new_badges)} nouveaux badges")
        
        return {
            "message": f"Vérification terminée, {len(new_badges)} nouveaux badges obtenus !",
            "new_badges": [
                {
                    "name": badge.name,
                    "description": badge.description,
                    "rarity": badge.rarity,
                    "icon": badge.icon,
                    "xp_reward": badge.xp_reward,
                    "coins_reward": badge.coins_reward
                }
                for badge in new_badges
            ]
        }
        
    except Exception as e:
        app_logger.error(f"Erreur vérification manuelle achievements: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la vérification des achievements"
        )

@router.get("/leaderboard")
async def get_achievements_leaderboard(
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user)
):
    """Classement des joueurs par nombre de badges"""
    try:
        # Agrégation MongoDB pour compter les badges par utilisateur
        pipeline = [
            {
                "$group": {
                    "_id": "$user_id",
                    "badge_count": {"$sum": 1},
                    "last_badge": {"$max": "$obtained_at"}
                }
            },
            {"$sort": {"badge_count": -1, "last_badge": -1}},
            {"$limit": limit}
        ]
        
        from database import db
        leaderboard_data = await db.user_badges.aggregate(pipeline).to_list(limit)
        
        # Enrichir avec les informations utilisateur
        enriched_leaderboard = []
        for entry in leaderboard_data:
            user_data = await db.users.find_one({"id": entry["_id"]})
            if user_data:
                # Récupérer le badge le plus rare
                user_badges = await get_user_badges(entry["_id"])
                rarest_badge = None
                if user_badges:
                    rarity_order = {"common": 0, "rare": 1, "epic": 2, "legendary": 3, "mythic": 4}
                    rarest_badge = max(user_badges, key=lambda b: rarity_order.get(b["rarity"], 0))
                
                enriched_leaderboard.append({
                    "rank": len(enriched_leaderboard) + 1,
                    "user_id": entry["_id"],
                    "username": user_data.get("username", "Inconnu"),
                    "badge_count": entry["badge_count"],
                    "last_badge_date": entry["last_badge"],
                    "rarest_badge": rarest_badge,
                    "level": user_data.get("level", 1),
                    "is_current_user": entry["_id"] == current_user.id
                })
        
        # Trouver le rang de l'utilisateur actuel
        current_user_rank = None
        for i, entry in enumerate(enriched_leaderboard):
            if entry["is_current_user"]:
                current_user_rank = i + 1
                break
        
        return {
            "leaderboard": enriched_leaderboard,
            "current_user_rank": current_user_rank,
            "total_users": len(enriched_leaderboard)
        }
        
    except Exception as e:
        app_logger.error(f"Erreur génération leaderboard achievements: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la génération du classement"
        )

@router.get("/stats")
async def get_achievements_global_stats():
    """Statistiques globales du système d'achievements"""
    try:
        from database import db
        
        # Stats de base
        total_badges_available = len(achievement_engine.badges_registry)
        total_badges_earned = await db.user_badges.count_documents({})
        total_users_with_badges = len(await db.user_badges.distinct("user_id"))
        
        # Distribution par rareté
        rarity_stats = {}
        for badge in achievement_engine.badges_registry.values():
            rarity_stats[badge.rarity] = rarity_stats.get(badge.rarity, 0) + 1
        
        # Top 3 badges les plus obtenus
        pipeline = [
            {"$group": {"_id": "$badge_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 3}
        ]
        
        top_badges_data = await db.user_badges.aggregate(pipeline).to_list(3)
        top_badges = []
        for entry in top_badges_data:
            badge_info = achievement_engine.badges_registry.get(entry["_id"])
            if badge_info:
                top_badges.append({
                    "badge_name": badge_info.name,
                    "badge_icon": badge_info.icon,
                    "times_earned": entry["count"]
                })
        
        return {
            "total_badges_available": total_badges_available,
            "total_badges_earned": total_badges_earned,
            "total_users_with_badges": total_users_with_badges,
            "average_badges_per_user": total_badges_earned / max(total_users_with_badges, 1),
            "rarity_distribution": rarity_stats,
            "most_popular_badges": top_badges
        }
        
    except Exception as e:
        app_logger.error(f"Erreur stats globales achievements: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des statistiques"
        )

# Routes admin
@router.get("/admin/all-user-badges")
async def admin_get_all_user_badges(
    current_user: User = Depends(get_current_active_user)
):
    """Admin: Récupère tous les badges de tous les utilisateurs"""
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès administrateur requis"
        )
    
    try:
        from database import db
        
        pipeline = [
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
                    "user_id": 1,
                    "badge_id": 1,
                    "obtained_at": 1,
                    "username": {"$arrayElemAt": ["$user_info.username", 0]}
                }
            },
            {"$sort": {"obtained_at": -1}}
        ]
        
        all_badges = await db.user_badges.aggregate(pipeline).to_list(1000)
        
        # Enrichir avec info badge
        for badge in all_badges:
            badge_info = achievement_engine.badges_registry.get(badge["badge_id"])
            if badge_info:
                badge["badge_name"] = badge_info.name
                badge["badge_rarity"] = badge_info.rarity
                badge["badge_icon"] = badge_info.icon
        
        return {
            "all_user_badges": all_badges,
            "total": len(all_badges)
        }
        
    except Exception as e:
        app_logger.error(f"Erreur admin badges: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur administrateur"
        )

@router.post("/admin/award-badge")
async def admin_award_badge(
    user_id: str,
    badge_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Admin: Attribuer manuellement un badge à un utilisateur"""
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès administrateur requis"
        )
    
    try:
        if badge_id not in achievement_engine.badges_registry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Badge non trouvé"
            )
        
        # Vérifier que l'utilisateur existe
        from database import db
        user_exists = await db.users.find_one({"id": user_id})
        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        
        # Attribuer le badge
        badge_info = achievement_engine.badges_registry[badge_id]
        await achievement_engine._give_rewards(user_id, badge_info)
        
        from achievements import UserBadge
        user_badge = UserBadge(
            user_id=user_id,
            badge_id=badge_id,
            metadata={"awarded_by_admin": current_user.id}
        )
        
        await db.user_badges.insert_one(user_badge.dict())
        
        log_user_action(current_user.id, "admin_award_badge", {
            "target_user": user_id,
            "badge_name": badge_info.name
        })
        
        return {
            "message": f"Badge '{badge_info.name}' attribué avec succès !",
            "badge_name": badge_info.name,
            "awarded_to": user_exists.get("username", "Utilisateur")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Erreur attribution badge admin: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de l'attribution du badge"
        )