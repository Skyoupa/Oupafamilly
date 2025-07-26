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
    get_badge_progress, achievement_engine, Badge, BadgeCategory, BadgeRarity,
    QuestEngine
)
from monitoring import log_user_action, app_logger
from datetime import datetime

router = APIRouter(prefix="/achievements", tags=["Achievements & Badges"])

# =====================================================
# QUEST/DAILY CHALLENGE ENDPOINTS
# =====================================================

@router.get("/quests/daily")
async def get_daily_quests(current_user: User = Depends(get_current_active_user)):
    """Récupère les quêtes quotidiennes actives pour l'utilisateur"""
    try:
        from achievements import QuestEngine
        from datetime import datetime, timedelta
        
        # Initialiser le moteur de quêtes
        quest_engine = QuestEngine()
        
        # Récupérer les quêtes quotidiennes pour aujourd'hui
        today = datetime.utcnow().date()
        daily_quests = await quest_engine.get_daily_quests_for_date(today)
        
        # Récupérer la progression de l'utilisateur pour ces quêtes
        user_quests = []
        for quest in daily_quests:
            progress = await quest_engine.get_user_quest_progress(current_user.id, quest.id)
            quest_dict = quest.dict()
            quest_dict.update({
                "user_progress": progress.get("progress", {}),
                "completed": progress.get("completed", False),
                "rewards_claimed": progress.get("rewards_claimed", False),
                "completion_percentage": progress.get("completion_percentage", 0.0)
            })
            user_quests.append(quest_dict)
        
        # Statistiques globales des quêtes
        completed_today = sum(1 for q in user_quests if q["completed"])
        total_rewards_available = sum(
            quest["rewards"].get("coins", 0) + quest["rewards"].get("xp", 0)
            for quest in user_quests
        )
        
        return {
            "daily_quests": user_quests,
            "date": today.isoformat(),
            "total_quests": len(user_quests),
            "completed_quests": completed_today,
            "completion_rate": completed_today / max(len(user_quests), 1),
            "total_rewards_available": total_rewards_available,
            "next_reset": f"{(datetime.utcnow() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()}Z"
        }
        
    except Exception as e:
        app_logger.error(f"Erreur récupération quêtes quotidiennes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des quêtes quotidiennes"
        )

@router.post("/quests/{quest_id}/claim")
async def claim_quest_rewards(
    quest_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Réclamer les récompenses d'une quête terminée"""
    try:
        from achievements import QuestEngine
        
        quest_engine = QuestEngine()
        
        # Vérifier que la quête est terminée et que les récompenses ne sont pas déjà réclamées
        progress = await quest_engine.get_user_quest_progress(current_user.id, quest_id)
        
        if not progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quête non trouvée ou pas commencée"
            )
        
        if not progress.get("completed", False):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cette quête n'est pas encore terminée"
            )
        
        if progress.get("rewards_claimed", False):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Les récompenses ont déjà été réclamées pour cette quête"
            )
        
        # Réclamer les récompenses
        claimed_rewards = await quest_engine.claim_quest_rewards(current_user.id, quest_id)
        
        log_user_action(current_user.id, "quest_rewards_claimed", {
            "quest_id": quest_id,
            "rewards": claimed_rewards
        })
        
        return {
            "message": "Récompenses réclamées avec succès !",
            "rewards": claimed_rewards,
            "quest_id": quest_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Erreur réclamation récompenses quête: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la réclamation des récompenses"
        )

@router.get("/quests/my-progress")
async def get_my_quest_progress(current_user: User = Depends(get_current_active_user)):
    """Récupère l'historique et la progression de toutes les quêtes de l'utilisateur"""
    try:
        from database import db
        from datetime import datetime, timedelta
        
        # Récupérer l'historique des quêtes (7 derniers jours)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        
        pipeline = [
            {
                "$match": {
                    "user_id": current_user.id,
                    "started_at": {"$gte": seven_days_ago}
                }
            },
            {
                "$lookup": {
                    "from": "quests",
                    "localField": "quest_id",
                    "foreignField": "id",
                    "as": "quest_info"
                }
            },
            {
                "$sort": {"started_at": -1}
            }
        ]
        
        user_quests = await db.user_quests.aggregate(pipeline).to_list(100)
        
        # Enrichir avec les informations des quêtes
        enriched_quests = []
        for user_quest in user_quests:
            quest_info = user_quest.get("quest_info", [{}])[0] if user_quest.get("quest_info") else {}
            
            enriched_quests.append({
                "quest_id": user_quest["quest_id"],
                "quest_name": quest_info.get("name", "Quête inconnue"),
                "quest_description": quest_info.get("description", ""),
                "difficulty": quest_info.get("difficulty", "common"),
                "progress": user_quest.get("progress", {}),
                "completed": user_quest.get("completed", False),
                "completed_at": user_quest.get("completed_at"),
                "rewards_claimed": user_quest.get("rewards_claimed", False),
                "started_at": user_quest["started_at"],
                "quest_date": user_quest["started_at"].date().isoformat() if "started_at" in user_quest else None
            })
        
        # Statistiques globales
        total_completed = sum(1 for q in enriched_quests if q["completed"])
        total_rewards_claimed = sum(1 for q in enriched_quests if q["rewards_claimed"])
        
        # Streak de jours consécutifs avec quêtes complétées
        quest_streak = await _calculate_quest_streak(current_user.id)
        
        return {
            "quest_history": enriched_quests,
            "statistics": {
                "total_quests_started": len(enriched_quests),
                "total_completed": total_completed,
                "total_rewards_claimed": total_rewards_claimed,
                "completion_rate": total_completed / max(len(enriched_quests), 1),
                "current_streak": quest_streak,
                "last_7_days": len(enriched_quests)
            }
        }
        
    except Exception as e:
        app_logger.error(f"Erreur récupération progression quêtes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération de la progression"
        )

@router.get("/quests/leaderboard")
async def get_quest_leaderboard(
    period: str = Query("week", regex="^(daily|week|month|all)$"),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user)
):
    """Classement des joueurs par quêtes complétées"""
    try:
        from database import db
        from datetime import datetime, timedelta
        
        # Définir la période
        now = datetime.utcnow()
        if period == "daily":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "week":
            start_date = now - timedelta(days=7)
        elif period == "month":
            start_date = now - timedelta(days=30)
        else:  # all
            start_date = datetime.min
        
        # Pipeline d'agrégation pour le classement
        pipeline = [
            {
                "$match": {
                    "completed": True,
                    "completed_at": {"$gte": start_date}
                }
            },
            {
                "$group": {
                    "_id": "$user_id",
                    "quests_completed": {"$sum": 1},
                    "last_completion": {"$max": "$completed_at"},
                    "rewards_claimed_count": {"$sum": {"$cond": ["$rewards_claimed", 1, 0]}}
                }
            },
            {"$sort": {"quests_completed": -1, "last_completion": -1}},
            {"$limit": limit}
        ]
        
        leaderboard_data = await db.user_quests.aggregate(pipeline).to_list(limit)
        
        # Enrichir avec les informations utilisateur
        enriched_leaderboard = []
        for i, entry in enumerate(leaderboard_data):
            user_data = await db.users.find_one({"id": entry["_id"]})
            if user_data:
                enriched_leaderboard.append({
                    "rank": i + 1,
                    "user_id": entry["_id"],
                    "username": user_data.get("username", "Inconnu"),
                    "quests_completed": entry["quests_completed"],
                    "rewards_claimed": entry["rewards_claimed_count"],
                    "last_completion": entry["last_completion"],
                    "level": user_data.get("level", 1),
                    "is_current_user": entry["_id"] == current_user.id
                })
        
        # Trouver le rang de l'utilisateur actuel
        current_user_rank = None
        for entry in enriched_leaderboard:
            if entry["is_current_user"]:
                current_user_rank = entry["rank"]
                break
        
        return {
            "leaderboard": enriched_leaderboard,
            "period": period,
            "current_user_rank": current_user_rank,
            "total_players": len(enriched_leaderboard)
        }
        
    except Exception as e:
        app_logger.error(f"Erreur génération leaderboard quêtes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la génération du classement"
        )

async def _calculate_quest_streak(user_id: str) -> int:
    """Calcule le nombre de jours consécutifs avec quêtes complétées"""
    try:
        from database import db
        from datetime import datetime, timedelta
        
        # Récupérer les quêtes complétées par jour, triées par date décroissante
        pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "completed": True
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$completed_at"
                        }
                    },
                    "quests_completed": {"$sum": 1}
                }
            },
            {"$sort": {"_id": -1}}
        ]
        
        daily_completions = await db.user_quests.aggregate(pipeline).to_list(365)
        
        if not daily_completions:
            return 0
        
        # Calculer le streak
        streak = 0
        current_date = datetime.utcnow().date()
        
        for daily_data in daily_completions:
            completion_date_str = daily_data["_id"]
            completion_date = datetime.strptime(completion_date_str, "%Y-%m-%d").date()
            
            # Vérifier si c'est le jour actuel ou le jour suivant dans le streak
            expected_date = current_date - timedelta(days=streak)
            
            if completion_date == expected_date:
                streak += 1
            else:
                break
        
        return streak
        
    except Exception as e:
        app_logger.error(f"Erreur calcul streak quêtes: {str(e)}")
        return 0

# =====================================================
# ACHIEVEMENT/BADGE ENDPOINTS (existing)
# =====================================================

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
        public_badges = []
        for badge in badges:
            badge_info = achievement_engine.badges_registry.get(badge["badge_id"])
            if badge_info and not badge_info.hidden:
                public_badges.append(badge)
        
        # Récupérer le nom d'utilisateur
        from database import db
        user_data = await db.users.find_one({"id": user_id})
        username = user_data.get("username", "Utilisateur") if user_data else "Utilisateur"
        
        return {
            "user_id": user_id,
            "username": username,
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
        
        # Enrichir avec info badge et convertir ObjectId
        for badge in all_badges:
            # Convertir ObjectId en string
            if "_id" in badge:
                badge["_id"] = str(badge["_id"])
            
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