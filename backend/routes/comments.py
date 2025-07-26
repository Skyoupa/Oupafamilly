from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from models import (
    User, UserComment, UserCommentCreate, TeamComment, TeamCommentCreate
)
from auth import get_current_active_user, is_admin, is_moderator_or_admin
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/comments", tags=["Comments & Ratings"])

# Get database from database module
from database import db

# Commentaires sur les utilisateurs

@router.post("/user", response_model=UserComment)
async def create_user_comment(
    comment_data: UserCommentCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Créer un commentaire sur un utilisateur."""
    try:
        # Vérifier que l'utilisateur cible existe
        target_user = await db.users.find_one({"id": comment_data.target_user_id})
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        
        # Empêcher les auto-commentaires
        if comment_data.target_user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vous ne pouvez pas vous commenter vous-même"
            )
        
        # Vérifier si l'utilisateur a déjà commenté cet utilisateur
        existing_comment = await db.user_comments.find_one({
            "target_user_id": comment_data.target_user_id,
            "author_id": current_user.id
        })
        
        if existing_comment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vous avez déjà commenté cet utilisateur"
            )
        
        # Créer le commentaire
        new_comment = UserComment(
            **comment_data.dict(),
            author_id=current_user.id,
            author_name=current_user.username
        )
        
        await db.user_comments.insert_one(new_comment.dict())
        
        # Mettre à jour les statistiques du profil cible
        await update_user_rating_stats(comment_data.target_user_id)
        
        # Donner des coins et XP à l'auteur du commentaire
        await reward_user_for_comment(current_user.id, current_user.username)
        
        # Créer une activité dans le feed
        await create_activity_feed_entry(
            current_user.id,
            current_user.username,
            "comment",
            f"A commenté {target_user['username']}",
            f"Note: {comment_data.rating}/5 étoiles",
            comment_data.target_user_id
        )
        
        logger.info(f"Commentaire créé par {current_user.username} sur {target_user['username']}")
        
        return new_comment
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la création du commentaire: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la création du commentaire"
        )

@router.get("/user/{user_id}", response_model=List[UserComment])
async def get_user_comments(
    user_id: str,
    limit: int = Query(20, le=100),
    skip: int = Query(0, ge=0)
):
    """Obtenir les commentaires d'un utilisateur."""
    try:
        comments = await db.user_comments.find({
            "target_user_id": user_id,
            "is_public": True,
            "is_approved": True
        }).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
        
        return [UserComment(**comment) for comment in comments]
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des commentaires: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des commentaires"
        )

@router.put("/user/{comment_id}")
async def update_user_comment(
    comment_id: str,
    content: str,
    rating: int,
    current_user: User = Depends(get_current_active_user)
):
    """Modifier un commentaire utilisateur."""
    try:
        # Vérifier que le commentaire existe et appartient à l'utilisateur
        comment_data = await db.user_comments.find_one({"id": comment_id})
        if not comment_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Commentaire non trouvé"
            )
        
        if comment_data["author_id"] != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous ne pouvez modifier que vos propres commentaires"
            )
        
        # Valider la note
        if rating < 1 or rating > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La note doit être entre 1 et 5"
            )
        
        # Mettre à jour le commentaire
        await db.user_comments.update_one(
            {"id": comment_id},
            {
                "$set": {
                    "content": content[:500],  # Limiter la longueur
                    "rating": rating,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        # Mettre à jour les statistiques du profil cible
        await update_user_rating_stats(comment_data["target_user_id"])
        
        logger.info(f"Commentaire {comment_id} modifié par {current_user.username}")
        
        return {"message": "Commentaire mis à jour avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la modification du commentaire: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la modification du commentaire"
        )

@router.delete("/user/{comment_id}")
async def delete_user_comment(
    comment_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Supprimer un commentaire utilisateur."""
    try:
        # Vérifier que le commentaire existe
        comment_data = await db.user_comments.find_one({"id": comment_id})
        if not comment_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Commentaire non trouvé"
            )
        
        # Vérifier les permissions (auteur ou admin)
        if comment_data["author_id"] != current_user.id and not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous ne pouvez supprimer que vos propres commentaires"
            )
        
        # Supprimer le commentaire
        await db.user_comments.delete_one({"id": comment_id})
        
        # Mettre à jour les statistiques du profil cible
        await update_user_rating_stats(comment_data["target_user_id"])
        
        logger.info(f"Commentaire {comment_id} supprimé par {current_user.username}")
        
        return {"message": "Commentaire supprimé avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du commentaire: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la suppression du commentaire"
        )

# Commentaires sur les équipes

@router.post("/team", response_model=TeamComment)
async def create_team_comment(
    comment_data: TeamCommentCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Créer un commentaire sur une équipe."""
    try:
        # Vérifier que l'équipe existe
        team = await db.teams.find_one({"id": comment_data.team_id})
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Équipe non trouvée"
            )
        
        # Vérifier si l'utilisateur a déjà commenté cette équipe
        existing_comment = await db.team_comments.find_one({
            "team_id": comment_data.team_id,
            "author_id": current_user.id
        })
        
        if existing_comment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vous avez déjà commenté cette équipe"
            )
        
        # Créer le commentaire
        new_comment = TeamComment(
            **comment_data.dict(),
            author_id=current_user.id,
            author_name=current_user.username
        )
        
        await db.team_comments.insert_one(new_comment.dict())
        
        # Mettre à jour les statistiques de l'équipe
        await update_team_rating_stats(comment_data.team_id)
        
        # Donner des coins et XP à l'auteur du commentaire
        await reward_user_for_comment(current_user.id, current_user.username)
        
        logger.info(f"Commentaire d'équipe créé par {current_user.username} sur {team['name']}")
        
        return new_comment
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la création du commentaire d'équipe: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la création du commentaire d'équipe"
        )

@router.get("/team/{team_id}", response_model=List[TeamComment])
async def get_team_comments(
    team_id: str,
    limit: int = Query(20, le=100),
    skip: int = Query(0, ge=0)
):
    """Obtenir les commentaires d'une équipe."""
    try:
        comments = await db.team_comments.find({
            "team_id": team_id,
            "is_public": True,
            "is_approved": True
        }).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
        
        return [TeamComment(**comment) for comment in comments]
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des commentaires d'équipe: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des commentaires d'équipe"
        )

# Statistiques des commentaires

@router.get("/stats/user/{user_id}")
async def get_user_comment_stats(user_id: str):
    """Obtenir les statistiques des commentaires d'un utilisateur."""
    try:
        # Profil de l'utilisateur avec stats
        profile = await db.user_profiles.find_one({"user_id": user_id})
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profil utilisateur non trouvé"
            )
        
        # Nombre total de commentaires reçus
        total_comments = await db.user_comments.count_documents({
            "target_user_id": user_id,
            "is_public": True,
            "is_approved": True
        })
        
        # Distribution des notes
        rating_distribution = {}
        for rating in range(1, 6):
            count = await db.user_comments.count_documents({
                "target_user_id": user_id,
                "rating": rating,
                "is_public": True,
                "is_approved": True
            })
            rating_distribution[f"{rating}_stars"] = count
        
        return {
            "user_id": user_id,
            "total_comments": total_comments,
            "average_rating": profile.get("average_rating", 0.0),
            "total_ratings": profile.get("total_ratings", 0),
            "rating_distribution": rating_distribution
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des stats de commentaires: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des statistiques"
        )

@router.get("/stats/team/{team_id}")
async def get_team_comment_stats(team_id: str):
    """Obtenir les statistiques des commentaires d'une équipe."""
    try:
        # Nombre total de commentaires reçus
        total_comments = await db.team_comments.count_documents({
            "team_id": team_id,
            "is_public": True,
            "is_approved": True
        })
        
        # Calcul de la moyenne des notes
        pipeline = [
            {"$match": {"team_id": team_id, "is_public": True, "is_approved": True}},
            {"$group": {"_id": None, "avg_rating": {"$avg": "$rating"}, "total": {"$sum": 1}}}
        ]
        
        result = await db.team_comments.aggregate(pipeline).to_list(1)
        avg_rating = result[0]["avg_rating"] if result else 0.0
        
        # Distribution des notes
        rating_distribution = {}
        for rating in range(1, 6):
            count = await db.team_comments.count_documents({
                "team_id": team_id,
                "rating": rating,
                "is_public": True,
                "is_approved": True
            })
            rating_distribution[f"{rating}_stars"] = count
        
        return {
            "team_id": team_id,
            "total_comments": total_comments,
            "average_rating": round(avg_rating, 1) if avg_rating else 0.0,
            "rating_distribution": rating_distribution
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des stats de commentaires d'équipe: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des statistiques d'équipe"
        )

# Modération (Admin seulement)

@router.get("/moderation/pending")
async def get_pending_comments(
    current_user: User = Depends(get_current_active_user),
    limit: int = Query(20, le=100),
    skip: int = Query(0, ge=0)
):
    """Obtenir les commentaires en attente de modération (admin seulement)."""
    if not is_moderator_or_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès modérateur requis"
        )
    
    try:
        # Commentaires utilisateurs en attente
        user_comments = await db.user_comments.find({
            "is_approved": False
        }).sort("created_at", -1).skip(skip).limit(limit//2).to_list(limit//2)
        
        # Commentaires équipes en attente
        team_comments = await db.team_comments.find({
            "is_approved": False
        }).sort("created_at", -1).skip(skip).limit(limit//2).to_list(limit//2)
        
        return {
            "user_comments": [UserComment(**comment) for comment in user_comments],
            "team_comments": [TeamComment(**comment) for comment in team_comments]
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des commentaires en attente: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des commentaires"
        )

@router.put("/moderation/approve/{comment_type}/{comment_id}")
async def approve_comment(
    comment_type: str,  # "user" ou "team"
    comment_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Approuver un commentaire (modérateur seulement)."""
    if not is_moderator_or_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès modérateur requis"
        )
    
    try:
        collection_name = "user_comments" if comment_type == "user" else "team_comments"
        
        result = await db[collection_name].update_one(
            {"id": comment_id},
            {
                "$set": {
                    "is_approved": True,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Commentaire non trouvé"
            )
        
        logger.info(f"Commentaire {comment_id} approuvé par {current_user.username}")
        
        return {"message": "Commentaire approuvé avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de l'approbation du commentaire: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de l'approbation du commentaire"
        )

# Fonctions utilitaires

async def update_user_rating_stats(user_id: str):
    """Mettre à jour les statistiques de notation d'un utilisateur."""
    try:
        # Calculer la moyenne et le total des notes
        pipeline = [
            {"$match": {"target_user_id": user_id, "is_public": True, "is_approved": True}},
            {"$group": {"_id": None, "avg_rating": {"$avg": "$rating"}, "total": {"$sum": 1}}}
        ]
        
        result = await db.user_comments.aggregate(pipeline).to_list(1)
        
        if result:
            avg_rating = result[0]["avg_rating"]
            total_ratings = result[0]["total"]
        else:
            avg_rating = 0.0
            total_ratings = 0
        
        # Mettre à jour le profil
        await db.user_profiles.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "average_rating": round(avg_rating, 1),
                    "total_ratings": total_ratings,
                    "comments_received": total_ratings,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour des stats de notation: {str(e)}")

async def update_team_rating_stats(team_id: str):
    """Mettre à jour les statistiques de notation d'une équipe."""
    try:
        # Calculer la moyenne des notes de l'équipe
        pipeline = [
            {"$match": {"team_id": team_id, "is_public": True, "is_approved": True}},
            {"$group": {"_id": None, "avg_rating": {"$avg": "$rating"}, "total": {"$sum": 1}}}
        ]
        
        result = await db.team_comments.aggregate(pipeline).to_list(1)
        
        if result:
            avg_rating = result[0]["avg_rating"]
            total_comments = result[0]["total"]
            
            # Mettre à jour l'équipe avec les stats
            await db.teams.update_one(
                {"id": team_id},
                {
                    "$set": {
                        "average_rating": round(avg_rating, 1),
                        "total_comments": total_comments,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
        
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour des stats d'équipe: {str(e)}")

async def reward_user_for_comment(user_id: str, username: str):
    """Récompenser un utilisateur pour avoir écrit un commentaire."""
    try:
        # Donner 5 coins et 2 XP pour un commentaire
        from models import CoinTransaction
        
        transaction = CoinTransaction(
            user_id=user_id,
            amount=5,
            transaction_type="comment_reward",
            description="Récompense pour commentaire constructif"
        )
        
        await db.coin_transactions.insert_one(transaction.dict())
        
        # Mettre à jour le profil
        await db.user_profiles.update_one(
            {"user_id": user_id},
            {
                "$inc": {
                    "coins": 5,
                    "total_coins_earned": 5,
                    "experience_points": 2
                },
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        # Vérifier montée de niveau
        from routes.currency import check_level_up
        await check_level_up(user_id, username)
        
    except Exception as e:
        logger.error(f"Erreur lors de la récompense pour commentaire: {str(e)}")

async def create_activity_feed_entry(user_id: str, username: str, activity_type: str, title: str, description: str, reference_id: str = None):
    """Créer une entrée dans le feed d'activité."""
    try:
        from models import ActivityFeed
        activity = ActivityFeed(
            user_id=user_id,
            user_name=username,
            activity_type=activity_type,
            title=title,
            description=description,
            reference_id=reference_id
        )
        
        await db.activity_feed.insert_one(activity.dict())
        
    except Exception as e:
        logger.error(f"Erreur lors de la création d'activité feed: {str(e)}")