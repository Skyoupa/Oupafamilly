from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from models import (
    User, CoinTransaction, CoinTransactionCreate, MarketplaceItem, 
    MarketplaceItemCreate, UserInventory
)
from auth import get_current_active_user, is_admin
from datetime import datetime, timedelta
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/currency", tags=["Currency & Marketplace"])

# Get database from database module
from database import db

# Fonction pour récompenser les participants de tournoi
async def reward_tournament_participants(tournament_id: str, participants: List[str], winner_id: str = None):
    """Récompenser automatiquement les participants et le gagnant d'un tournoi."""
    try:
        # Récompenses selon le type et l'importance du tournoi
        tournament = await db.tournaments.find_one({"id": tournament_id})
        if not tournament:
            return
        
        # Déterminer les récompenses selon le tournoi
        max_participants = tournament.get("max_participants", 8)
        tournament_name = tournament.get("title", "Tournoi")
        
        # Récompenses de base (réduites pour équilibrer l'économie)
        participation_reward = 15  # 15 coins pour participer (au lieu de 20)
        victory_reward = 75        # 75 coins pour gagner (au lieu de 100)
        
        # Bonus selon la taille du tournoi
        if max_participants >= 16:
            participation_reward = 25  # Récompense augmentée pour gros tournois
            victory_reward = 150
        elif max_participants >= 8:
            participation_reward = 20
            victory_reward = 100
        
        # Récompenser tous les participants
        for participant_id in participants:
            # Créer transaction de participation
            participation_transaction = CoinTransaction(
                user_id=participant_id,
                amount=participation_reward,
                transaction_type="tournament_participation",
                description=f"Participation au tournoi: {tournament_name}",
                reference_id=tournament_id
            )
            
            await db.coin_transactions.insert_one(participation_transaction.dict())
            
            # Mettre à jour le profil
            await db.user_profiles.update_one(
                {"user_id": participant_id},
                {
                    "$inc": {
                        "coins": participation_reward,
                        "total_coins_earned": participation_reward,
                        "experience_points": 10  # 10 XP pour participation
                    },
                    "$set": {"updated_at": datetime.utcnow()}
                },
                upsert=True
            )
        
        # Récompenser le gagnant s'il y en a un
        if winner_id and winner_id in participants:
            victory_transaction = CoinTransaction(
                user_id=winner_id,
                amount=victory_reward,
                transaction_type="tournament_victory",
                description=f"Victoire du tournoi: {tournament_name}",
                reference_id=tournament_id
            )
            
            await db.coin_transactions.insert_one(victory_transaction.dict())
            
            # Bonus gagnant
            await db.user_profiles.update_one(
                {"user_id": winner_id},
                {
                    "$inc": {
                        "coins": victory_reward,
                        "total_coins_earned": victory_reward,
                        "experience_points": 50  # 50 XP bonus victoire
                    },
                    "$set": {"updated_at": datetime.utcnow()}
                },
                upsert=True
            )
            
            # Vérifier montée de niveau
            await check_level_up(winner_id, "winner")
        
        logger.info(f"Récompenses distribuées pour tournoi {tournament_id}: {len(participants)} participants, gagnant: {winner_id}")
        
    except Exception as e:
        logger.error(f"Erreur lors de la distribution des récompenses tournoi: {str(e)}")

from pydantic import BaseModel
from typing import List, Optional

class TournamentRewardsRequest(BaseModel):
    participants: List[str]
    winner_id: Optional[str] = None

@router.post("/tournament-rewards/{tournament_id}")
async def distribute_tournament_rewards(
    tournament_id: str,
    request: TournamentRewardsRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Distribuer les récompenses d'un tournoi (admin seulement)."""
    try:
        if not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Seuls les admins peuvent distribuer les récompenses"
            )
        
        await reward_tournament_participants(tournament_id, request.participants, request.winner_id)
        
        return {
            "message": "Récompenses distribuées avec succès",
            "participants_rewarded": len(request.participants),
            "winner": request.winner_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur distribution récompenses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la distribution des récompenses"
        )

@router.get("/balance")
async def get_user_balance(current_user: User = Depends(get_current_active_user)):
    """Obtenir le solde de coins de l'utilisateur."""
    try:
        profile = await db.user_profiles.find_one({"user_id": current_user.id})
        if not profile:
            # Créer un profil par défaut avec 100 coins
            from models import UserProfile
            default_profile = UserProfile(
                user_id=current_user.id,
                display_name=current_user.username,
                coins=100,
                total_coins_earned=100
            )
            await db.user_profiles.insert_one(default_profile.dict())
            profile = default_profile.dict()
        
        return {
            "user_id": current_user.id,
            "username": current_user.username,
            "balance": profile.get("coins", 0),
            "total_earned": profile.get("total_coins_earned", 0),
            "level": profile.get("level", 1),
            "experience_points": profile.get("experience_points", 0)
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du solde: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération du solde"
        )

@router.get("/transactions", response_model=List[CoinTransaction])
async def get_user_transactions(
    current_user: User = Depends(get_current_active_user),
    limit: int = Query(20, le=100),
    skip: int = Query(0, ge=0)
):
    """Obtenir l'historique des transactions de coins de l'utilisateur."""
    try:
        transactions = await db.coin_transactions.find({
            "user_id": current_user.id
        }).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
        
        return [CoinTransaction(**transaction) for transaction in transactions]
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des transactions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des transactions"
        )

@router.post("/earn")
async def earn_coins(
    transaction_data: CoinTransactionCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Gagner des coins (pour les actions automatiques du système)."""
    try:
        # Vérifier que le montant est positif
        if transaction_data.amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le montant doit être positif pour gagner des coins"
            )
        
        # Créer la transaction
        transaction = CoinTransaction(
            **transaction_data.dict(),
            user_id=current_user.id
        )
        
        # Enregistrer la transaction
        await db.coin_transactions.insert_one(transaction.dict())
        
        # Mettre à jour le solde de l'utilisateur
        await db.user_profiles.update_one(
            {"user_id": current_user.id},
            {
                "$inc": {
                    "coins": transaction_data.amount,
                    "total_coins_earned": transaction_data.amount
                },
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        # Créer une activité dans le feed
        await create_activity_feed_entry(
            current_user.id,
            current_user.username,
            "coin_earned",
            f"A gagné {transaction_data.amount} coins",
            f"{transaction_data.description}",
            transaction_data.reference_id
        )
        
        logger.info(f"Utilisateur {current_user.username} a gagné {transaction_data.amount} coins: {transaction_data.description}")
        
        return {
            "message": f"Vous avez gagné {transaction_data.amount} coins !",
            "transaction": transaction,
            "new_balance": await get_current_balance(current_user.id)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors du gain de coins: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors du gain de coins"
        )

@router.post("/spend")
async def spend_coins(
    transaction_data: CoinTransactionCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Dépenser des coins."""
    try:
        # Vérifier que le montant est négatif (dépense)
        if transaction_data.amount >= 0:
            transaction_data.amount = -abs(transaction_data.amount)
        
        # Vérifier le solde
        current_balance = await get_current_balance(current_user.id)
        if current_balance < abs(transaction_data.amount):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solde insuffisant pour cette transaction"
            )
        
        # Créer la transaction
        transaction = CoinTransaction(
            **transaction_data.dict(),
            user_id=current_user.id
        )
        
        # Enregistrer la transaction
        await db.coin_transactions.insert_one(transaction.dict())
        
        # Mettre à jour le solde de l'utilisateur
        await db.user_profiles.update_one(
            {"user_id": current_user.id},
            {
                "$inc": {"coins": transaction_data.amount},  # Négatif pour dépense
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        logger.info(f"Utilisateur {current_user.username} a dépensé {abs(transaction_data.amount)} coins: {transaction_data.description}")
        
        return {
            "message": f"Vous avez dépensé {abs(transaction_data.amount)} coins.",
            "transaction": transaction,
            "new_balance": await get_current_balance(current_user.id)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la dépense de coins: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la dépense de coins"
        )

@router.post("/daily-bonus")
async def claim_daily_bonus(current_user: User = Depends(get_current_active_user)):
    """Réclamer le bonus quotidien de connexion."""
    try:
        # Vérifier si l'utilisateur a déjà réclamé son bonus aujourd'hui
        today = datetime.utcnow().date()
        today_start = datetime.combine(today, datetime.min.time())
        
        existing_bonus = await db.coin_transactions.find_one({
            "user_id": current_user.id,
            "transaction_type": "daily_bonus",
            "created_at": {"$gte": today_start}
        })
        
        if existing_bonus:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vous avez déjà réclamé votre bonus quotidien aujourd'hui"
            )
        
        # Calculer le bonus (base réduite 5, +1 par niveau pour équilibrer l'économie)
        profile = await db.user_profiles.find_one({"user_id": current_user.id})
        user_level = profile.get("level", 1) if profile else 1
        bonus_amount = 5 + (user_level * 1)  # Base 5 + 1 par niveau (au lieu de 10 + 2)
        
        # Créer la transaction de bonus
        transaction = CoinTransaction(
            user_id=current_user.id,
            amount=bonus_amount,
            transaction_type="daily_bonus",
            description=f"Bonus quotidien de connexion (Niveau {user_level})"
        )
        
        await db.coin_transactions.insert_one(transaction.dict())
        
        # Mettre à jour le solde et donner de l'XP
        await db.user_profiles.update_one(
            {"user_id": current_user.id},
            {
                "$inc": {
                    "coins": bonus_amount,
                    "total_coins_earned": bonus_amount,
                    "experience_points": 5  # 5 XP pour la connexion quotidienne
                },
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        # Vérifier si l'utilisateur monte de niveau
        await check_level_up(current_user.id, current_user.username)
        
        logger.info(f"Utilisateur {current_user.username} a réclamé son bonus quotidien: {bonus_amount} coins")
        
        return {
            "message": f"Bonus quotidien réclamé ! +{bonus_amount} coins et +5 XP",
            "bonus_amount": bonus_amount,
            "new_balance": await get_current_balance(current_user.id)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la réclamation du bonus quotidien: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la réclamation du bonus quotidien"
        )

@router.get("/marketplace")
async def get_marketplace_items(
    item_type: Optional[str] = None,
    limit: int = Query(20, le=100),
    skip: int = Query(0, ge=0)
):
    """Obtenir les articles disponibles dans la marketplace."""
    try:
        filter_dict = {"is_available": True}
        if item_type:
            filter_dict["item_type"] = item_type
        
        items = await db.marketplace_items.find(filter_dict).skip(skip).limit(limit).to_list(limit)
        
        # Convertir en format simple pour éviter les erreurs de modèle
        marketplace_items = []
        for item in items:
            marketplace_item = {
                "id": item.get("id"),
                "name": item.get("name"),
                "description": item.get("description"),
                "item_type": item.get("item_type"),
                "price": item.get("price"),
                "image_url": item.get("image_url"),
                "is_available": item.get("is_available", True),
                "is_premium": item.get("is_premium", False),
                "rarity": item.get("rarity", "common"),
                "custom_data": item.get("custom_data", {}),
                "created_at": item.get("created_at")
            }
            marketplace_items.append(marketplace_item)
        
        return marketplace_items
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des articles marketplace: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des articles"
        )

@router.post("/marketplace/buy/{item_id}")
async def buy_marketplace_item(
    item_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Acheter un article de la marketplace."""
    try:
        # Récupérer l'article
        item_data = await db.marketplace_items.find_one({"id": item_id})
        if not item_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article non trouvé"
            )
        
        item = MarketplaceItem(**item_data)
        
        if not item.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cet article n'est plus disponible"
            )
        
        # Vérifier si l'utilisateur possède déjà cet article
        existing_item = await db.user_inventory.find_one({
            "user_id": current_user.id,
            "item_id": item_id
        })
        
        if existing_item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vous possédez déjà cet article"
            )
        
        # Vérifier le solde
        current_balance = await get_current_balance(current_user.id)
        if current_balance < item.price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Solde insuffisant. Prix: {item.price} coins, Solde: {current_balance} coins"
            )
        
        # Effectuer l'achat
        # 1. Créer la transaction de dépense
        transaction = CoinTransaction(
            user_id=current_user.id,
            amount=-item.price,
            transaction_type="marketplace_purchase",
            description=f"Achat: {item.name}",
            reference_id=item_id
        )
        
        await db.coin_transactions.insert_one(transaction.dict())
        
        # 2. Ajouter l'article à l'inventaire
        inventory_item = UserInventory(
            user_id=current_user.id,
            item_id=item_id,
            item_name=item.name,
            item_type=item.item_type
        )
        
        await db.user_inventory.insert_one(inventory_item.dict())
        
        # 3. Mettre à jour le solde
        await db.user_profiles.update_one(
            {"user_id": current_user.id},
            {
                "$inc": {"coins": -item.price},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        logger.info(f"Utilisateur {current_user.username} a acheté {item.name} pour {item.price} coins")
        
        return {
            "message": f"Achat réussi ! Vous avez acheté {item.name}",
            "item": item,
            "cost": item.price,
            "new_balance": await get_current_balance(current_user.id)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de l'achat: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de l'achat"
        )

@router.get("/inventory", response_model=List[UserInventory])
async def get_user_inventory(current_user: User = Depends(get_current_active_user)):
    """Obtenir l'inventaire de l'utilisateur."""
    try:
        inventory = await db.user_inventory.find({
            "user_id": current_user.id
        }).sort("purchased_at", -1).to_list(100)
        
        return [UserInventory(**item) for item in inventory]
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'inventaire: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération de l'inventaire"
        )

@router.get("/leaderboard/richest")
async def get_richest_players():
    """Obtenir le classement des joueurs les plus riches."""
    try:
        profiles = await db.user_profiles.find({}).sort("coins", -1).limit(20).to_list(20)
        
        leaderboard = []
        for i, profile in enumerate(profiles, 1):
            user_data = await db.users.find_one({"id": profile["user_id"]})
            if user_data:
                leaderboard.append({
                    "rank": i,
                    "username": user_data["username"],
                    "display_name": profile.get("display_name", user_data["username"]),
                    "coins": profile.get("coins", 0),
                    "level": profile.get("level", 1),
                    "total_earned": profile.get("total_coins_earned", 0)
                })
        
        return {"leaderboard": leaderboard}
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du classement: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération du classement"
        )

# Fonctions utilitaires
async def get_current_balance(user_id: str) -> int:
    """Obtenir le solde actuel d'un utilisateur."""
    profile = await db.user_profiles.find_one({"user_id": user_id})
    return profile.get("coins", 0) if profile else 0

async def check_level_up(user_id: str, username: str):
    """Vérifier si l'utilisateur monte de niveau."""
    profile = await db.user_profiles.find_one({"user_id": user_id})
    if not profile:
        return
    
    current_xp = profile.get("experience_points", 0)
    current_level = profile.get("level", 1)
    
    # Calcul du niveau (100 XP pour niveau 2, puis +50 XP par niveau)
    required_xp = 100 + (current_level - 1) * 50
    
    if current_xp >= required_xp:
        new_level = current_level + 1
        
        # Bonus de coins pour montée de niveau
        level_bonus = new_level * 20
        
        await db.user_profiles.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "level": new_level,
                    "updated_at": datetime.utcnow()
                },
                "$inc": {
                    "coins": level_bonus,
                    "total_coins_earned": level_bonus
                }
            }
        )
        
        # Créer transaction pour le bonus de niveau
        level_transaction = CoinTransaction(
            user_id=user_id,
            amount=level_bonus,
            transaction_type="level_up",
            description=f"Bonus montée de niveau {new_level}",
            reference_id=f"level_{new_level}"
        )
        
        await db.coin_transactions.insert_one(level_transaction.dict())
        
        # Créer une activité dans le feed
        await create_activity_feed_entry(
            user_id,
            username,
            "level_up",
            f"Niveau {new_level} atteint !",
            f"A atteint le niveau {new_level} et gagné {level_bonus} coins bonus"
        )

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

# Admin endpoints
@router.post("/admin/create-marketplace-item")
async def create_marketplace_item(
    item_data: MarketplaceItemCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Créer un nouvel article pour la marketplace (admin seulement)."""
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès administrateur requis"
        )
    
    try:
        new_item = MarketplaceItem(**item_data.dict())
        await db.marketplace_items.insert_one(new_item.dict())
        
        logger.info(f"Nouvel article marketplace créé: {item_data.name} par {current_user.username}")
        
        return new_item
        
    except Exception as e:
        logger.error(f"Erreur lors de la création d'article marketplace: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la création de l'article"
        )

@router.post("/admin/give-coins/{user_id}")
async def admin_give_coins(
    user_id: str,
    amount: int,
    reason: str,
    current_user: User = Depends(get_current_active_user)
):
    """Donner des coins à un utilisateur (admin seulement)."""
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès administrateur requis"
        )
    
    try:
        # Vérifier que l'utilisateur existe
        target_user = await db.users.find_one({"id": user_id})
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        
        # Créer la transaction
        transaction = CoinTransaction(
            user_id=user_id,
            amount=amount,
            transaction_type="admin_grant",
            description=f"Accordé par admin: {reason}",
            reference_id=current_user.id
        )
        
        await db.coin_transactions.insert_one(transaction.dict())
        
        # Mettre à jour le solde
        await db.user_profiles.update_one(
            {"user_id": user_id},
            {
                "$inc": {
                    "coins": amount,
                    "total_coins_earned": amount if amount > 0 else 0
                },
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        logger.info(f"Admin {current_user.username} a donné {amount} coins à {target_user['username']}: {reason}")
        
        return {
            "message": f"Accordé {amount} coins à {target_user['username']}",
            "transaction": transaction
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de l'attribution de coins par admin: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de l'attribution de coins"
        )