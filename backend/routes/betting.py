from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from models import User
from auth import get_current_active_user, is_admin
from datetime import datetime, timedelta
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/betting", tags=["Betting System"])

# Get database from database module
from database import db

# Modèles pour le système de paris

class BettingMarket(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tournament_id: str
    tournament_name: str
    game: str
    market_type: str  # "winner", "match_result", "special"
    title: str
    description: str
    options: List[Dict[str, Any]]  # [{"option_id": "team1", "name": "Team A", "odds": 1.5}]
    total_pool: int = 0  # Total des coins misés
    status: str = "open"  # "open", "closed", "settled", "cancelled"
    closes_at: datetime
    settles_at: Optional[datetime] = None
    winning_option: Optional[str] = None
    match_id: Optional[str] = None  # Pour les paris sur matches individuels
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class BettingMarketCreate(BaseModel):
    tournament_id: str
    market_type: str
    title: str
    description: str
    options: List[Dict[str, Any]]
    closes_at: datetime
    match_id: Optional[str] = None

class Bet(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    user_name: str
    market_id: str
    option_id: str
    option_name: str
    amount: int  # Montant en coins
    potential_payout: int  # Gain potentiel
    odds: float
    status: str = "active"  # "active", "won", "lost", "cancelled"
    placed_at: datetime = Field(default_factory=datetime.utcnow)
    settled_at: Optional[datetime] = None

class BetCreate(BaseModel):
    market_id: str
    option_id: str
    amount: int

class BettingStats(BaseModel):
    user_id: str
    total_bets: int = 0
    total_amount_bet: int = 0
    total_winnings: int = 0
    total_losses: int = 0
    win_rate: float = 0.0
    profit_loss: int = 0
    best_bet: Dict[str, Any] = {}
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Fonctions pour créer automatiquement les marchés de paris

async def create_tournament_betting_markets(tournament_id: str):
    """Créer automatiquement les marchés de paris pour un tournoi et ses matches."""
    try:
        # Récupérer le tournoi
        tournament = await db.tournaments.find_one({"id": tournament_id})
        if not tournament:
            return
        
        tournament_name = tournament.get("title", "Tournoi")
        game = tournament.get("game", "esports")
        
        # 1. Marché principal : Gagnant du tournoi
        participants = tournament.get("participants", [])
        if len(participants) >= 2:
            winner_options = []
            base_odds = 2.0  # Cotes de base
            
            for participant_id in participants:
                # Récupérer le nom du participant (équipe ou joueur)
                participant_name = await get_participant_name(participant_id)
                winner_options.append({
                    "option_id": participant_id,
                    "name": participant_name,
                    "odds": base_odds + (len(participants) * 0.1)  # Cotes ajustées selon nb participants
                })
            
            # Créer le marché gagnant
            winner_market = BettingMarket(
                tournament_id=tournament_id,
                tournament_name=tournament_name,
                game=game,
                market_type="winner",
                title=f"Gagnant du tournoi: {tournament_name}",
                description=f"Qui remportera le tournoi {tournament_name} ?",
                options=winner_options,
                closes_at=tournament.get("start_date", datetime.utcnow() + timedelta(hours=1))
            )
            
            await db.betting_markets.insert_one(winner_market.dict())
            logger.info(f"Marché gagnant créé pour tournoi {tournament_id}")
        
        # 2. Marchés pour les matches individuels
        matches = await db.matches.find({"tournament_id": tournament_id}).to_list(100)
        
        for match in matches:
            if match.get("status") == "scheduled":
                # Créer marché pour ce match
                match_options = []
                player1_name = await get_participant_name(match.get("player1_id"))
                player2_name = await get_participant_name(match.get("player2_id"))
                
                match_options.extend([
                    {
                        "option_id": match.get("player1_id"),
                        "name": player1_name,
                        "odds": 1.8
                    },
                    {
                        "option_id": match.get("player2_id"), 
                        "name": player2_name,
                        "odds": 1.8
                    }
                ])
                
                match_market = BettingMarket(
                    tournament_id=tournament_id,
                    tournament_name=tournament_name,
                    game=game,
                    market_type="match_result",
                    title=f"Match: {player1_name} vs {player2_name}",
                    description=f"Qui gagnera ce match du tournoi {tournament_name} ?",
                    options=match_options,
                    match_id=match.get("id"),
                    closes_at=match.get("scheduled_at", datetime.utcnow() + timedelta(hours=1))
                )
                
                await db.betting_markets.insert_one(match_market.dict())
                logger.info(f"Marché match créé pour {player1_name} vs {player2_name}")
        
        return True
        
    except Exception as e:
        logger.error(f"Erreur création marchés tournoi {tournament_id}: {str(e)}")
        return False

async def get_participant_name(participant_id: str) -> str:
    """Récupérer le nom d'un participant (équipe ou joueur)."""
    try:
        # Chercher d'abord dans les équipes
        team = await db.teams.find_one({"id": participant_id})
        if team:
            return team.get("name", f"Équipe {participant_id[:8]}")
        
        # Sinon chercher dans les utilisateurs
        user = await db.users.find_one({"id": participant_id})
        if user:
            return user.get("username", f"Joueur {participant_id[:8]}")
        
        return f"Participant {participant_id[:8]}"
        
    except:
        return f"Participant {participant_id[:8]}"

@router.post("/markets/tournament/{tournament_id}")
async def create_tournament_markets(
    tournament_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Créer les marchés de paris pour un tournoi (admin seulement)."""
    try:
        if not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Seuls les admins peuvent créer des marchés de paris"
            )
        
        success = await create_tournament_betting_markets(tournament_id)
        
        if success:
            return {"message": "Marchés de paris créés avec succès pour le tournoi"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erreur lors de la création des marchés"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur création marchés: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la création des marchés"
        )

# Endpoints des marchés de paris

@router.get("/markets", response_model=List[BettingMarket])
async def get_betting_markets(
    status: Optional[str] = None,
    game: Optional[str] = None,
    limit: int = Query(20, le=100),
    skip: int = Query(0, ge=0)
):
    """Obtenir les marchés de paris disponibles."""
    try:
        filter_dict = {}
        if status:
            filter_dict["status"] = status
        if game:
            filter_dict["game"] = game
        
        markets = await db.betting_markets.find(filter_dict).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
        
        # Enrichir avec des statistiques
        enriched_markets = []
        for market_data in markets:
            market = BettingMarket(**market_data)
            
            # Compter le nombre de parieurs
            bet_count = await db.bets.count_documents({"market_id": market.id})
            
            # Calculer la distribution des paris par option
            option_distribution = {}
            for option in market.options:
                option_bets = await db.bets.count_documents({
                    "market_id": market.id,
                    "option_id": option["option_id"]
                })
                
                option_amount = await db.bets.aggregate([
                    {"$match": {"market_id": market.id, "option_id": option["option_id"]}},
                    {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
                ]).to_list(1)
                
                total_amount = option_amount[0]["total"] if option_amount else 0
                option_distribution[option["option_id"]] = {
                    "bet_count": option_bets,
                    "total_amount": total_amount
                }
            
            market_dict = market.dict()
            market_dict["bet_count"] = bet_count
            market_dict["option_distribution"] = option_distribution
            
            enriched_markets.append(market_dict)
        
        return enriched_markets
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des marchés de paris: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des marchés de paris"
        )

@router.get("/markets/{market_id}", response_model=BettingMarket)
async def get_betting_market(market_id: str):
    """Obtenir un marché de pari spécifique."""
    try:
        market_data = await db.betting_markets.find_one({"id": market_id})
        if not market_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Marché de pari non trouvé"
            )
        
        return BettingMarket(**market_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du marché: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération du marché"
        )

@router.post("/markets", response_model=BettingMarket)
async def create_betting_market(
    market_data: BettingMarketCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Créer un nouveau marché de pari (admin seulement)."""
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès administrateur requis"
        )
    
    try:
        # Vérifier que le tournoi existe
        tournament = await db.tournaments.find_one({"id": market_data.tournament_id})
        if not tournament:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournoi non trouvé"
            )
        
        # Créer le marché
        new_market = BettingMarket(
            **market_data.dict(),
            tournament_name=tournament["title"],
            game=tournament["game"]
        )
        
        await db.betting_markets.insert_one(new_market.dict())
        
        logger.info(f"Marché de pari créé par {current_user.username}: {market_data.title}")
        
        return new_market
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la création du marché: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la création du marché"
        )

# Endpoints des paris

@router.post("/bets", response_model=Bet)
async def place_bet(
    bet_data: BetCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Placer un pari."""
    try:
        # Vérifier que le marché existe et est ouvert
        market_data = await db.betting_markets.find_one({"id": bet_data.market_id})
        if not market_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Marché de pari non trouvé"
            )
        
        market = BettingMarket(**market_data)
        
        if market.status != "open":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ce marché de pari est fermé"
            )
        
        if datetime.utcnow() >= market.closes_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La période de paris est terminée"
            )
        
        # Vérifier que l'option existe
        option = None
        for opt in market.options:
            if opt["option_id"] == bet_data.option_id:
                option = opt
                break
        
        if not option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Option de pari non trouvée"
            )
        
        # Vérifier le solde de l'utilisateur
        from routes.currency import get_current_balance
        current_balance = await get_current_balance(current_user.id)
        
        if current_balance < bet_data.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Solde insuffisant. Solde: {current_balance} coins, Pari: {bet_data.amount} coins"
            )
        
        # Vérifier les limites de pari
        if bet_data.amount < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Montant minimum de pari: 10 coins"
            )
        
        max_bet = min(current_balance, 1000)  # Max 1000 coins par pari
        if bet_data.amount > max_bet:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Montant maximum de pari: {max_bet} coins"
            )
        
        # Vérifier si l'utilisateur a déjà parié sur ce marché
        existing_bet = await db.bets.find_one({
            "user_id": current_user.id,
            "market_id": bet_data.market_id
        })
        
        if existing_bet:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vous avez déjà parié sur ce marché"
            )
        
        # Calculer les cotes et le gain potentiel
        odds = option.get("odds", 2.0)
        potential_payout = int(bet_data.amount * odds)
        
        # Créer le pari
        new_bet = Bet(
            user_id=current_user.id,
            user_name=current_user.username,
            market_id=bet_data.market_id,
            option_id=bet_data.option_id,
            option_name=option["name"],
            amount=bet_data.amount,
            potential_payout=potential_payout,
            odds=odds
        )
        
        # Sauvegarder le pari
        await db.bets.insert_one(new_bet.dict())
        
        # Débiter les coins de l'utilisateur
        from models import CoinTransaction
        transaction = CoinTransaction(
            user_id=current_user.id,
            amount=-bet_data.amount,
            transaction_type="bet_placed",
            description=f"Pari sur '{option['name']}' - {market.title}",
            reference_id=new_bet.id
        )
        
        await db.coin_transactions.insert_one(transaction.dict())
        
        await db.user_profiles.update_one(
            {"user_id": current_user.id},
            {
                "$inc": {"coins": -bet_data.amount},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        # Mettre à jour le pool total du marché
        await db.betting_markets.update_one(
            {"id": bet_data.market_id},
            {
                "$inc": {"total_pool": bet_data.amount},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        # Créer une activité
        from routes.activity import create_automatic_activity
        await create_automatic_activity(
            user_id=current_user.id,
            user_name=current_user.username,
            activity_type="bet_placed",
            title="🎲 Nouveau pari !",
            description=f"A parié {bet_data.amount} coins sur '{option['name']}' dans {market.title}",
            reference_id=new_bet.id
        )
        
        logger.info(f"Pari placé par {current_user.username}: {bet_data.amount} coins sur {option['name']}")
        
        return new_bet
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors du placement du pari: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors du placement du pari"
        )

@router.get("/bets/my-bets", response_model=List[Bet])
async def get_my_bets(
    current_user: User = Depends(get_current_active_user),
    status: Optional[str] = None,
    limit: int = Query(20, le=100),
    skip: int = Query(0, ge=0)
):
    """Obtenir mes paris."""
    try:
        filter_dict = {"user_id": current_user.id}
        if status:
            filter_dict["status"] = status
        
        bets = await db.bets.find(filter_dict).sort("placed_at", -1).skip(skip).limit(limit).to_list(limit)
        
        return [Bet(**bet) for bet in bets]
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des paris: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des paris"
        )

@router.get("/bets/stats")
async def get_betting_stats(current_user: User = Depends(get_current_active_user)):
    """Obtenir les statistiques de paris de l'utilisateur."""
    try:
        # Statistiques générales
        total_bets = await db.bets.count_documents({"user_id": current_user.id})
        
        # Montant total parié
        total_bet_pipeline = [
            {"$match": {"user_id": current_user.id}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        total_bet_result = await db.bets.aggregate(total_bet_pipeline).to_list(1)
        total_amount_bet = total_bet_result[0]["total"] if total_bet_result else 0
        
        # Paris gagnés et perdus
        won_bets = await db.bets.count_documents({"user_id": current_user.id, "status": "won"})
        lost_bets = await db.bets.count_documents({"user_id": current_user.id, "status": "lost"})
        
        # Gains totaux
        winnings_pipeline = [
            {"$match": {"user_id": current_user.id, "status": "won"}},
            {"$group": {"_id": None, "total": {"$sum": "$potential_payout"}}}
        ]
        winnings_result = await db.bets.aggregate(winnings_pipeline).to_list(1)
        total_winnings = winnings_result[0]["total"] if winnings_result else 0
        
        # Pertes totales
        losses_pipeline = [
            {"$match": {"user_id": current_user.id, "status": "lost"}},
            {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
        ]
        losses_result = await db.bets.aggregate(losses_pipeline).to_list(1)
        total_losses = losses_result[0]["total"] if losses_result else 0
        
        # Taux de victoire
        win_rate = (won_bets / total_bets * 100) if total_bets > 0 else 0
        
        # Profit/Perte
        profit_loss = total_winnings - total_losses
        
        # Meilleur pari
        best_bet_data = await db.bets.find({
            "user_id": current_user.id,
            "status": "won"
        }).sort("potential_payout", -1).limit(1).to_list(1)
        
        best_bet = {}
        if best_bet_data:
            best_bet = {
                "option_name": best_bet_data[0]["option_name"],
                "amount": best_bet_data[0]["amount"],
                "payout": best_bet_data[0]["potential_payout"],
                "odds": best_bet_data[0]["odds"]
            }
        
        return {
            "user_id": current_user.id,
            "total_bets": total_bets,
            "total_amount_bet": total_amount_bet,
            "total_winnings": total_winnings,
            "total_losses": total_losses,
            "won_bets": won_bets,
            "lost_bets": lost_bets,
            "win_rate": round(win_rate, 1),
            "profit_loss": profit_loss,
            "best_bet": best_bet
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des statistiques: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des statistiques"
        )

# Administration des paris

@router.put("/markets/{market_id}/close")
async def close_betting_market(
    market_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Fermer un marché de pari (admin seulement)."""
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès administrateur requis"
        )
    
    try:
        result = await db.betting_markets.update_one(
            {"id": market_id},
            {
                "$set": {
                    "status": "closed",
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Marché non trouvé"
            )
        
        logger.info(f"Marché {market_id} fermé par {current_user.username}")
        
        return {"message": "Marché fermé avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la fermeture du marché: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la fermeture du marché"
        )

@router.put("/markets/{market_id}/settle")
async def settle_betting_market(
    market_id: str,
    winning_option_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Régler un marché de pari (admin seulement)."""
    if not is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès administrateur requis"
        )
    
    try:
        # Vérifier que le marché existe
        market_data = await db.betting_markets.find_one({"id": market_id})
        if not market_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Marché non trouvé"
            )
        
        market = BettingMarket(**market_data)
        
        # Vérifier que l'option gagnante existe
        winning_option = None
        for option in market.options:
            if option["option_id"] == winning_option_id:
                winning_option = option
                break
        
        if not winning_option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Option gagnante non trouvée"
            )
        
        # Mettre à jour le marché
        await db.betting_markets.update_one(
            {"id": market_id},
            {
                "$set": {
                    "status": "settled",
                    "winning_option": winning_option_id,
                    "settles_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        # Traiter tous les paris de ce marché
        all_bets = await db.bets.find({"market_id": market_id}).to_list(1000)
        
        winners_count = 0
        total_payouts = 0
        
        for bet_data in all_bets:
            bet = Bet(**bet_data)
            
            if bet.option_id == winning_option_id:
                # Pari gagnant
                await db.bets.update_one(
                    {"id": bet.id},
                    {
                        "$set": {
                            "status": "won",
                            "settled_at": datetime.utcnow()
                        }
                    }
                )
                
                # Payer les gains
                from models import CoinTransaction
                payout_transaction = CoinTransaction(
                    user_id=bet.user_id,
                    amount=bet.potential_payout,
                    transaction_type="bet_won",
                    description=f"Gains du pari sur '{winning_option['name']}' - {market.title}",
                    reference_id=bet.id
                )
                
                await db.coin_transactions.insert_one(payout_transaction.dict())
                
                await db.user_profiles.update_one(
                    {"user_id": bet.user_id},
                    {
                        "$inc": {
                            "coins": bet.potential_payout,
                            "total_coins_earned": bet.potential_payout
                        },
                        "$set": {"updated_at": datetime.utcnow()}
                    }
                )
                
                # Créer une activité de victoire
                from routes.activity import create_automatic_activity
                await create_automatic_activity(
                    user_id=bet.user_id,
                    user_name=bet.user_name,
                    activity_type="bet_won",
                    title="🎉 Pari gagnant !",
                    description=f"A gagné {bet.potential_payout} coins en pariant sur '{winning_option['name']}'",
                    reference_id=bet.id
                )
                
                winners_count += 1
                total_payouts += bet.potential_payout
                
            else:
                # Pari perdant
                await db.bets.update_one(
                    {"id": bet.id},
                    {
                        "$set": {
                            "status": "lost",
                            "settled_at": datetime.utcnow()
                        }
                    }
                )
        
        logger.info(f"Marché {market_id} réglé par {current_user.username}: {winners_count} gagnants, {total_payouts} coins distribués")
        
        return {
            "message": "Marché réglé avec succès",
            "winning_option": winning_option["name"],
            "winners_count": winners_count,
            "total_payouts": total_payouts
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors du règlement du marché: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors du règlement du marché"
        )

@router.get("/leaderboard")
async def get_betting_leaderboard():
    """Obtenir le classement des parieurs."""
    try:
        # Calculer les profits de chaque utilisateur
        pipeline = [
            {
                "$group": {
                    "_id": "$user_id",
                    "user_name": {"$first": "$user_name"},
                    "total_bets": {"$sum": 1},
                    "total_bet_amount": {"$sum": "$amount"},
                    "won_bets": {
                        "$sum": {"$cond": [{"$eq": ["$status", "won"]}, 1, 0]}
                    },
                    "total_winnings": {
                        "$sum": {"$cond": [{"$eq": ["$status", "won"]}, "$potential_payout", 0]}
                    },
                    "total_losses": {
                        "$sum": {"$cond": [{"$eq": ["$status", "lost"]}, "$amount", 0]}
                    }
                }
            },
            {
                "$addFields": {
                    "profit_loss": {"$subtract": ["$total_winnings", "$total_losses"]},
                    "win_rate": {
                        "$cond": [
                            {"$eq": ["$total_bets", 0]},
                            0,
                            {"$multiply": [{"$divide": ["$won_bets", "$total_bets"]}, 100]}
                        ]
                    }
                }
            },
            {"$sort": {"profit_loss": -1}},
            {"$limit": 20}
        ]
        
        leaderboard = await db.bets.aggregate(pipeline).to_list(20)
        
        # Ajouter les rangs
        for i, player in enumerate(leaderboard):
            player["rank"] = i + 1
            player["win_rate"] = round(player["win_rate"], 1)
        
        return {"leaderboard": leaderboard}
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du classement: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération du classement"
        )

@router.get("/stats/global")
async def get_global_betting_stats():
    """Obtenir les statistiques globales des paris."""
    try:
        # Statistiques générales
        total_markets = await db.betting_markets.count_documents({})
        active_markets = await db.betting_markets.count_documents({"status": "open"})
        total_bets = await db.bets.count_documents({})
        
        # Pool total
        total_pool_pipeline = [
            {"$group": {"_id": None, "total": {"$sum": "$total_pool"}}}
        ]
        total_pool_result = await db.betting_markets.aggregate(total_pool_pipeline).to_list(1)
        total_pool = total_pool_result[0]["total"] if total_pool_result else 0
        
        # Parieurs uniques
        unique_bettors = len(await db.bets.distinct("user_id"))
        
        # Jeux les plus populaires
        game_stats = await db.betting_markets.aggregate([
            {"$group": {"_id": "$game", "market_count": {"$sum": 1}}},
            {"$sort": {"market_count": -1}}
        ]).to_list(10)
        
        # Statistiques des dernières 24h
        yesterday = datetime.utcnow() - timedelta(days=1)
        bets_24h = await db.bets.count_documents({"placed_at": {"$gte": yesterday}})
        
        return {
            "total_markets": total_markets,
            "active_markets": active_markets,
            "total_bets": total_bets,
            "total_pool": total_pool,
            "unique_bettors": unique_bettors,
            "bets_24h": bets_24h,
            "popular_games": [
                {"game": stat["_id"], "markets": stat["market_count"]}
                for stat in game_stats
            ]
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des stats globales: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des statistiques globales"
        )