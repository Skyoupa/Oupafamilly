from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from models import User, ActivityFeed, ActivityFeedCreate
from auth import get_current_active_user, is_admin
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/activity", tags=["Activity Feed"])

# Get database from database module
from database import db

@router.get("/feed", response_model=List[ActivityFeed])
async def get_activity_feed(
    current_user: User = Depends(get_current_active_user),
    activity_type: Optional[str] = None,
    limit: int = Query(50, le=100),
    skip: int = Query(0, ge=0)
):
    """Obtenir le feed d'activité de la communauté."""
    try:
        filter_dict = {"is_public": True}
        
        if activity_type:
            filter_dict["activity_type"] = activity_type
        
        activities = await db.activity_feed.find(filter_dict).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
        
        # Enrichir avec des informations utilisateur
        enriched_activities = []
        for activity_data in activities:
            activity = ActivityFeed(**activity_data)
            
            # Ajouter des informations sur les likes
            is_liked = current_user.id in activity.likes
            like_count = len(activity.likes)
            
            activity_dict = activity.dict()
            activity_dict["is_liked"] = is_liked
            activity_dict["like_count"] = like_count
            
            # Ajouter des détails selon le type d'activité
            if activity.activity_type == "tournament_win" and activity.reference_id:
                tournament = await db.tournaments.find_one({"id": activity.reference_id})
                if tournament:
                    activity_dict["tournament_name"] = tournament.get("title", "")
                    activity_dict["tournament_game"] = tournament.get("game", "")
            
            elif activity.activity_type == "team_join" and activity.reference_id:
                team = await db.teams.find_one({"id": activity.reference_id})
                if team:
                    activity_dict["team_name"] = team.get("name", "")
                    activity_dict["team_game"] = team.get("game", "")
            
            elif activity.activity_type == "level_up":
                profile = await db.user_profiles.find_one({"user_id": activity.user_id})
                if profile:
                    activity_dict["current_level"] = profile.get("level", 1)
            
            enriched_activities.append(activity_dict)
        
        return enriched_activities
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du feed d'activité: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération du feed d'activité"
        )

@router.get("/my-feed", response_model=List[ActivityFeed])
async def get_my_activity_feed(
    current_user: User = Depends(get_current_active_user),
    limit: int = Query(20, le=50),
    skip: int = Query(0, ge=0)
):
    """Obtenir le feed d'activité personnel de l'utilisateur."""
    try:
        activities = await db.activity_feed.find({
            "user_id": current_user.id
        }).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
        
        return [ActivityFeed(**activity) for activity in activities]
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du feed personnel: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération du feed personnel"
        )

@router.post("/", response_model=ActivityFeed)
async def create_activity(
    activity_data: ActivityFeedCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Créer une nouvelle activité (pour les événements manuels)."""
    try:
        new_activity = ActivityFeed(
            **activity_data.dict(),
            user_id=current_user.id,
            user_name=current_user.username
        )
        
        await db.activity_feed.insert_one(new_activity.dict())
        
        logger.info(f"Activité créée par {current_user.username}: {activity_data.title}")
        
        return new_activity
        
    except Exception as e:
        logger.error(f"Erreur lors de la création d'activité: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la création d'activité"
        )

@router.post("/{activity_id}/like")
async def like_activity(
    activity_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Liker/Unliker une activité."""
    try:
        # Vérifier que l'activité existe
        activity_data = await db.activity_feed.find_one({"id": activity_id})
        if not activity_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activité non trouvée"
            )
        
        activity = ActivityFeed(**activity_data)
        
        # Vérifier si déjà liké
        if current_user.id in activity.likes:
            # Retirer le like
            await db.activity_feed.update_one(
                {"id": activity_id},
                {"$pull": {"likes": current_user.id}}
            )
            action = "unliked"
            new_like_count = len(activity.likes) - 1
        else:
            # Ajouter le like
            await db.activity_feed.update_one(
                {"id": activity_id},
                {"$addToSet": {"likes": current_user.id}}
            )
            action = "liked"
            new_like_count = len(activity.likes) + 1
            
            # Récompenser l'auteur de l'activité (si ce n'est pas soi-même)
            if activity.user_id != current_user.id:
                await reward_for_activity_engagement(activity.user_id, "received_like")
        
        logger.info(f"Activité {activity_id} {action} par {current_user.username}")
        
        return {
            "message": f"Activité {action}",
            "like_count": new_like_count,
            "is_liked": action == "liked"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors du like d'activité: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors du like d'activité"
        )

@router.get("/trending")
async def get_trending_activities():
    """Obtenir les activités tendance (les plus likées des dernières 24h)."""
    try:
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        # Utiliser aggregation pour trier par nombre de likes
        pipeline = [
            {"$match": {
                "is_public": True,
                "created_at": {"$gte": yesterday}
            }},
            {"$addFields": {
                "like_count": {"$size": "$likes"}
            }},
            {"$sort": {"like_count": -1}},
            {"$limit": 20}
        ]
        
        trending = await db.activity_feed.aggregate(pipeline).to_list(20)
        
        # Enrichir avec des informations utilisateur
        enriched_trending = []
        for activity_data in trending:
            activity = ActivityFeed(**activity_data)
            activity_dict = activity.dict()
            activity_dict["like_count"] = len(activity.likes)
            enriched_trending.append(activity_dict)
        
        return {"trending_activities": enriched_trending}
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des activités tendance: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des activités tendance"
        )

@router.get("/stats")
async def get_activity_stats():
    """Obtenir les statistiques du feed d'activité."""
    try:
        # Statistiques générales
        total_activities = await db.activity_feed.count_documents({"is_public": True})
        
        # Activités des dernières 24h
        yesterday = datetime.utcnow() - timedelta(days=1)
        activities_24h = await db.activity_feed.count_documents({
            "is_public": True,
            "created_at": {"$gte": yesterday}
        })
        
        # Types d'activités les plus populaires
        pipeline = [
            {"$match": {"is_public": True}},
            {"$group": {
                "_id": "$activity_type",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        
        activity_types = await db.activity_feed.aggregate(pipeline).to_list(10)
        
        # Utilisateurs les plus actifs
        pipeline_users = [
            {"$match": {
                "is_public": True,
                "created_at": {"$gte": yesterday}
            }},
            {"$group": {
                "_id": "$user_id",
                "user_name": {"$first": "$user_name"},
                "activity_count": {"$sum": 1}
            }},
            {"$sort": {"activity_count": -1}},
            {"$limit": 10}
        ]
        
        active_users = await db.activity_feed.aggregate(pipeline_users).to_list(10)
        
        return {
            "total_activities": total_activities,
            "activities_24h": activities_24h,
            "popular_activity_types": [
                {"type": item["_id"], "count": item["count"]} 
                for item in activity_types
            ],
            "most_active_users": [
                {
                    "user_id": item["_id"],
                    "username": item["user_name"],
                    "activity_count": item["activity_count"]
                }
                for item in active_users
            ]
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des stats d'activité: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des statistiques"
        )

@router.delete("/{activity_id}")
async def delete_activity(
    activity_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Supprimer une activité."""
    try:
        # Vérifier que l'activité existe
        activity_data = await db.activity_feed.find_one({"id": activity_id})
        if not activity_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activité non trouvée"
            )
        
        # Vérifier les permissions
        if activity_data["user_id"] != current_user.id and not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous ne pouvez supprimer que vos propres activités"
            )
        
        # Supprimer l'activité
        await db.activity_feed.delete_one({"id": activity_id})
        
        logger.info(f"Activité {activity_id} supprimée par {current_user.username}")
        
        return {"message": "Activité supprimée avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la suppression d'activité: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la suppression d'activité"
        )

# Endpoints pour créer automatiquement des activités lors d'événements

async def create_automatic_activity(user_id: str, user_name: str, activity_type: str, title: str, description: str, reference_id: str = None, is_public: bool = True):
    """Fonction utilitaire pour créer automatiquement des activités."""
    try:
        activity = ActivityFeed(
            user_id=user_id,
            user_name=user_name,
            activity_type=activity_type,
            title=title,
            description=description,
            reference_id=reference_id,
            is_public=is_public
        )
        
        await db.activity_feed.insert_one(activity.dict())
        
        logger.info(f"Activité automatique créée pour {user_name}: {title}")
        return activity
        
    except Exception as e:
        logger.error(f"Erreur lors de la création d'activité automatique: {str(e)}")
        return None

# Fonctions spécialisées pour différents types d'événements

async def create_tournament_win_activity(user_id: str, user_name: str, tournament_id: str, tournament_name: str, game: str):
    """Créer une activité pour une victoire de tournoi."""
    await create_automatic_activity(
        user_id=user_id,
        user_name=user_name,
        activity_type="tournament_win",
        title=f"🏆 Victoire de tournoi !",
        description=f"A remporté le tournoi '{tournament_name}' en {game.upper()}",
        reference_id=tournament_id
    )

async def create_team_join_activity(user_id: str, user_name: str, team_id: str, team_name: str, game: str):
    """Créer une activité pour rejoindre une équipe."""
    await create_automatic_activity(
        user_id=user_id,
        user_name=user_name,
        activity_type="team_join",
        title=f"🎮 Nouvelle équipe !",
        description=f"A rejoint l'équipe '{team_name}' en {game.upper()}",
        reference_id=team_id
    )

async def create_level_up_activity(user_id: str, user_name: str, new_level: int):
    """Créer une activité pour une montée de niveau."""
    await create_automatic_activity(
        user_id=user_id,
        user_name=user_name,
        activity_type="level_up",
        title=f"⬆️ Niveau {new_level} atteint !",
        description=f"A atteint le niveau {new_level} grâce à son activité dans la communauté"
    )

async def create_achievement_activity(user_id: str, user_name: str, achievement_name: str, achievement_description: str):
    """Créer une activité pour un achievement."""
    await create_automatic_activity(
        user_id=user_id,
        user_name=user_name,
        activity_type="achievement",
        title=f"🏅 Achievement débloqué !",
        description=f"A débloqué '{achievement_name}' - {achievement_description}"
    )

async def create_comment_activity(user_id: str, user_name: str, target_user_name: str, rating: int):
    """Créer une activité pour un commentaire."""
    stars = "⭐" * rating
    await create_automatic_activity(
        user_id=user_id,
        user_name=user_name,
        activity_type="comment",
        title=f"💬 Nouveau commentaire",
        description=f"A laissé un commentaire {stars} sur le profil de {target_user_name}"
    )

async def create_marketplace_purchase_activity(user_id: str, user_name: str, item_name: str, item_type: str, price: int):
    """Créer une activité pour un achat marketplace."""
    icons = {
        "avatar": "🎭",
        "badge": "🏷️",
        "title": "👑",
        "banner": "🖼️",
        "emote": "😀"
    }
    icon = icons.get(item_type, "🛒")
    
    await create_automatic_activity(
        user_id=user_id,
        user_name=user_name,
        activity_type="purchase",
        title=f"{icon} Nouvel achat !",
        description=f"A acheté '{item_name}' pour {price} coins"
    )

# Fonctions utilitaires

async def reward_for_activity_engagement(user_id: str, engagement_type: str):
    """Récompenser un utilisateur pour l'engagement avec les activités."""
    try:
        # Limiter les récompenses d'engagement par jour
        today = datetime.utcnow().date()
        today_start = datetime.combine(today, datetime.min.time())
        
        today_engagement_rewards = await db.coin_transactions.count_documents({
            "user_id": user_id,
            "transaction_type": "activity_engagement",
            "created_at": {"$gte": today_start}
        })
        
        if today_engagement_rewards >= 10:  # Max 10 récompenses par jour
            return
        
        # Récompenses selon le type d'engagement
        rewards = {
            "received_like": {"coins": 1, "xp": 1, "description": "Like reçu sur une activité"}
        }
        
        reward = rewards.get(engagement_type)
        if not reward:
            return
        
        # Créer la transaction
        from models import CoinTransaction
        
        transaction = CoinTransaction(
            user_id=user_id,
            amount=reward["coins"],
            transaction_type="activity_engagement",
            description=reward["description"]
        )
        
        await db.coin_transactions.insert_one(transaction.dict())
        
        # Mettre à jour le profil
        await db.user_profiles.update_one(
            {"user_id": user_id},
            {
                "$inc": {
                    "coins": reward["coins"],
                    "total_coins_earned": reward["coins"],
                    "experience_points": reward["xp"]
                },
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de la récompense d'engagement: {str(e)}")

# Endpoint admin pour nettoyer les anciennes activités

@router.delete("/admin/cleanup")
async def cleanup_old_activities(
    days: int = Query(30, ge=7, le=365),
    current_user: User = Depends(get_current_active_user)
):
    """Nettoyer les anciennes activités (admin seulement)."""
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès administrateur requis"
        )
    
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        result = await db.activity_feed.delete_many({
            "created_at": {"$lt": cutoff_date}
        })
        
        logger.info(f"Nettoyage des activités : {result.deleted_count} activités supprimées (>{days} jours)")
        
        return {
            "message": f"Nettoyage terminé",
            "deleted_count": result.deleted_count,
            "days_threshold": days
        }
        
    except Exception as e:
        logger.error(f"Erreur lors du nettoyage des activités: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors du nettoyage des activités"
        )