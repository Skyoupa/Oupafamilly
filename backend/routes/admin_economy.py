from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from models import User, MarketplaceItem, MarketplaceItemCreate
from auth import get_current_active_user, is_admin
from datetime import datetime, timedelta
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/economy", tags=["Admin Economy"])

# Get database from database module
from database import db

# Modèles pour l'administration économique

class EconomyStats(BaseModel):
    total_coins_in_circulation: int
    total_transactions: int
    daily_bonus_claims: int
    marketplace_sales: int
    betting_pool: int
    top_earners: List[Dict[str, Any]]
    economy_health: str

class AdminMarketplaceItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: int
    item_type: str  # "avatar", "badge", "title", "theme", "custom_tag"
    rarity: str = "common"  # "common", "rare", "epic", "legendary"
    is_available: bool = True
    is_premium: bool = False
    stock: Optional[int] = None
    icon_url: Optional[str] = None
    custom_data: Dict[str, Any] = {}  # Données spécifiques selon le type
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MarketplaceItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    is_available: Optional[bool] = None
    stock: Optional[int] = None
    custom_data: Optional[Dict[str, Any]] = None

class BettingMarketManagement(BaseModel):
    id: str
    tournament_name: str
    title: str
    status: str
    total_pool: int
    bet_count: int
    created_at: datetime

# Dashboard économique

@router.get("/stats", response_model=EconomyStats)
async def get_economy_stats(current_user: User = Depends(get_current_active_user)):
    """Obtenir les statistiques générales de l'économie."""
    try:
        if not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux administrateurs"
            )
        
        # Total des coins en circulation
        total_coins_result = await db.user_profiles.aggregate([
            {"$group": {"_id": None, "total": {"$sum": "$coins"}}}
        ]).to_list(1)
        total_coins = total_coins_result[0]["total"] if total_coins_result else 0
        
        # Total des transactions
        total_transactions = await db.coin_transactions.count_documents({})
        
        # Bonus quotidiens réclamés aujourd'hui
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        daily_bonus_today = await db.coin_transactions.count_documents({
            "transaction_type": "daily_bonus",
            "created_at": {"$gte": today_start}
        })
        
        # Ventes marketplace
        marketplace_sales = await db.coin_transactions.count_documents({
            "transaction_type": "marketplace_purchase"
        })
        
        # Pool total des paris
        betting_pool_result = await db.betting_markets.aggregate([
            {"$group": {"_id": None, "total": {"$sum": "$total_pool"}}}
        ]).to_list(1)
        betting_pool = betting_pool_result[0]["total"] if betting_pool_result else 0
        
        # Top 5 des plus gros gagnants
        top_earners_data = await db.user_profiles.find({}).sort("total_coins_earned", -1).limit(5).to_list(5)
        top_earners = []
        for profile in top_earners_data:
            user = await db.users.find_one({"id": profile["user_id"]})
            if user:
                top_earners.append({
                    "username": user["username"],
                    "total_earned": profile.get("total_coins_earned", 0),
                    "current_balance": profile.get("coins", 0),
                    "level": profile.get("level", 1)
                })
        
        # Santé de l'économie (simple indicateur)
        economy_health = "Healthy"
        if total_coins < 1000:
            economy_health = "Low"
        elif total_coins > 100000:
            economy_health = "High"
        
        return EconomyStats(
            total_coins_in_circulation=total_coins,
            total_transactions=total_transactions,
            daily_bonus_claims=daily_bonus_today,
            marketplace_sales=marketplace_sales,
            betting_pool=betting_pool,
            top_earners=top_earners,
            economy_health=economy_health
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur récupération stats économie: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des statistiques"
        )

@router.get("/transactions")
async def get_all_transactions(
    transaction_type: Optional[str] = None,
    limit: int = Query(50, le=200),
    skip: int = Query(0, ge=0),
    current_user: User = Depends(get_current_active_user)
):
    """Obtenir toutes les transactions (admin seulement)."""
    try:
        if not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux administrateurs"
            )
        
        filter_dict = {}
        if transaction_type:
            filter_dict["transaction_type"] = transaction_type
        
        transactions = await db.coin_transactions.find(filter_dict).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
        
        # Enrichir avec les noms d'utilisateur et convertir en modèles
        from models import CoinTransaction
        enriched_transactions = []
        for transaction in transactions:
            user = await db.users.find_one({"id": transaction["user_id"]})
            # Convert to CoinTransaction model to handle serialization
            transaction_model = CoinTransaction(**transaction)
            transaction_dict = transaction_model.dict()
            transaction_dict["username"] = user["username"] if user else "Unknown"
            enriched_transactions.append(transaction_dict)
        
        return enriched_transactions
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur récupération transactions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des transactions"
        )

# Gestion Marketplace

@router.get("/marketplace/items", response_model=List[AdminMarketplaceItem])
async def get_admin_marketplace_items(
    current_user: User = Depends(get_current_active_user)
):
    """Obtenir tous les articles de la marketplace pour administration."""
    try:
        if not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux administrateurs"
            )
        
        items = await db.marketplace_items.find({}).to_list(100)
        return [AdminMarketplaceItem(**item) for item in items]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur récupération articles admin: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des articles"
        )

@router.post("/marketplace/items", response_model=AdminMarketplaceItem)
async def create_marketplace_item(
    item_data: AdminMarketplaceItem,
    current_user: User = Depends(get_current_active_user)
):
    """Créer un nouvel article dans la marketplace."""
    try:
        if not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux administrateurs"
            )
        
        # Vérifier que l'article n'existe pas déjà
        existing_item = await db.marketplace_items.find_one({"name": item_data.name})
        if existing_item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un article avec ce nom existe déjà"
            )
        
        # Créer l'article
        new_item = AdminMarketplaceItem(**item_data.dict())
        await db.marketplace_items.insert_one(new_item.dict())
        
        logger.info(f"Nouvel article marketplace créé: {new_item.name} par {current_user.username}")
        
        return new_item
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur création article marketplace: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la création de l'article"
        )

@router.put("/marketplace/items/{item_id}")
async def update_marketplace_item(
    item_id: str,
    item_data: MarketplaceItemUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Mettre à jour un article de la marketplace."""
    try:
        if not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux administrateurs"
            )
        
        # Vérifier que l'article existe
        existing_item = await db.marketplace_items.find_one({"id": item_id})
        if not existing_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article non trouvé"
            )
        
        # Préparer les données de mise à jour
        update_data = {k: v for k, v in item_data.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow()
        
        # Mettre à jour l'article
        await db.marketplace_items.update_one(
            {"id": item_id},
            {"$set": update_data}
        )
        
        logger.info(f"Article marketplace mis à jour: {item_id} par {current_user.username}")
        
        return {"message": "Article mis à jour avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur mise à jour article: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la mise à jour de l'article"
        )

@router.delete("/marketplace/items/{item_id}")
async def delete_marketplace_item(
    item_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Supprimer un article de la marketplace."""
    try:
        if not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux administrateurs"
            )
        
        # Vérifier que l'article existe
        existing_item = await db.marketplace_items.find_one({"id": item_id})
        if not existing_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article non trouvé"
            )
        
        # Supprimer l'article
        await db.marketplace_items.delete_one({"id": item_id})
        
        logger.info(f"Article marketplace supprimé: {item_id} par {current_user.username}")
        
        return {"message": "Article supprimé avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur suppression article: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la suppression de l'article"
        )

# Gestion des paris

@router.get("/betting/markets", response_model=List[BettingMarketManagement])
async def get_admin_betting_markets(
    current_user: User = Depends(get_current_active_user)
):
    """Obtenir tous les marchés de paris pour administration."""
    try:
        if not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux administrateurs"
            )
        
        markets = await db.betting_markets.find({}).sort("created_at", -1).to_list(100)
        
        admin_markets = []
        for market in markets:
            # Compter le nombre de paris
            bet_count = await db.bets.count_documents({"market_id": market["id"]})
            
            admin_markets.append(BettingMarketManagement(
                id=market["id"],
                tournament_name=market["tournament_name"],
                title=market["title"],
                status=market["status"],
                total_pool=market["total_pool"],
                bet_count=bet_count,
                created_at=market["created_at"]
            ))
        
        return admin_markets
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur récupération marchés admin: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des marchés"
        )

@router.post("/betting/markets/{market_id}/close")
async def close_betting_market(
    market_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Fermer un marché de paris (plus de nouveaux paris)."""
    try:
        if not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux administrateurs"
            )
        
        # Mettre à jour le statut
        result = await db.betting_markets.update_one(
            {"id": market_id},
            {"$set": {"status": "closed", "updated_at": datetime.utcnow()}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Marché non trouvé"
            )
        
        logger.info(f"Marché de paris fermé: {market_id} par {current_user.username}")
        
        return {"message": "Marché fermé avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur fermeture marché: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la fermeture du marché"
        )

@router.post("/betting/markets/{market_id}/settle")
async def settle_betting_market(
    market_id: str,
    winning_option: str,
    current_user: User = Depends(get_current_active_user)
):
    """Résoudre un marché de paris et distribuer les gains."""
    try:
        if not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès réservé aux administrateurs"
            )
        
        # Récupérer le marché
        market = await db.betting_markets.find_one({"id": market_id})
        if not market:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Marché non trouvé"
            )
        
        # Vérifier que l'option gagnante existe
        winning_option_exists = any(opt["option_id"] == winning_option for opt in market["options"])
        if not winning_option_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Option gagnante invalide"
            )
        
        # Récupérer tous les paris sur ce marché
        all_bets = await db.bets.find({"market_id": market_id}).to_list(1000)
        
        # Séparer les paris gagnants et perdants
        winning_bets = [bet for bet in all_bets if bet["option_id"] == winning_option]
        losing_bets = [bet for bet in all_bets if bet["option_id"] != winning_option]
        
        # Calculer les gains
        total_pool = sum(bet["amount"] for bet in all_bets)
        winning_pool = sum(bet["amount"] for bet in winning_bets)
        
        if winning_pool > 0:
            # Distribuer les gains proportionnellement
            for bet in winning_bets:
                # Récupérer la mise + part proportionnelle du pool des perdants
                proportion = bet["amount"] / winning_pool
                total_payout = bet["amount"] + int((total_pool - winning_pool) * proportion)
                
                # Créditer le compte
                from routes.currency import CoinTransaction
                payout_transaction = CoinTransaction(
                    user_id=bet["user_id"],
                    amount=total_payout,
                    transaction_type="betting_win",
                    description=f"Gain pari: {market['title']}",
                    reference_id=market_id
                )
                
                await db.coin_transactions.insert_one(payout_transaction.dict())
                await db.user_profiles.update_one(
                    {"user_id": bet["user_id"]},
                    {"$inc": {"coins": total_payout, "total_coins_earned": total_payout}}
                )
                
                # Marquer le pari comme gagné
                await db.bets.update_one(
                    {"id": bet["id"]},
                    {"$set": {"status": "won", "settled_at": datetime.utcnow()}}
                )
        
        # Marquer les paris perdants
        for bet in losing_bets:
            await db.bets.update_one(
                {"id": bet["id"]},
                {"$set": {"status": "lost", "settled_at": datetime.utcnow()}}
            )
        
        # Marquer le marché comme résolu
        await db.betting_markets.update_one(
            {"id": market_id},
            {
                "$set": {
                    "status": "settled",
                    "winning_option": winning_option,
                    "settles_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        logger.info(f"Marché résolu: {market_id}, gagnant: {winning_option}, {len(winning_bets)} gagnants, {len(losing_bets)} perdants")
        
        return {
            "message": "Marché résolu avec succès",
            "winning_bets": len(winning_bets),
            "losing_bets": len(losing_bets),
            "total_payout": total_pool
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur résolution marché: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la résolution du marché"
        )