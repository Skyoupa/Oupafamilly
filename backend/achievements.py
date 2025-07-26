"""
🏆 SYSTÈME D'ACHIEVEMENTS/BADGES ÉLITE
Enrichit le système existant sans rien modifier
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timedelta
from enum import Enum
import uuid
from dataclasses import dataclass
from models import User, Game
from database import db
from monitoring import app_logger, log_user_action

class BadgeCategory(str, Enum):
    """Catégories de badges"""
    GAMING = "gaming"           # Performance gaming
    COMMUNITY = "community"     # Engagement communauté  
    ECONOMIC = "economic"       # Système économique
    SOCIAL = "social"          # Interactions sociales
    COMPETITIVE = "competitive" # Compétitions
    LOYALTY = "loyalty"        # Fidélité
    SPECIAL = "special"        # Events spéciaux
    ACHIEVEMENT = "achievement" # Accomplissements généraux

class BadgeRarity(str, Enum):
    """Rareté des badges"""
    COMMON = "common"       # 70% des joueurs peuvent l'avoir
    RARE = "rare"          # 30% des joueurs  
    EPIC = "epic"          # 10% des joueurs
    LEGENDARY = "legendary" # 3% des joueurs
    MYTHIC = "mythic"      # 0.5% des joueurs (très rare)

class Badge(BaseModel):
    """Modèle de badge"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str                           # Nom du badge
    description: str                    # Description  
    category: BadgeCategory            # Catégorie
    rarity: BadgeRarity                # Rareté
    icon: str                          # Emoji/icon
    criteria: Dict[str, Any]           # Critères pour obtenir
    xp_reward: int = 0                 # XP bonus
    coins_reward: int = 0              # Coins bonus
    hidden: bool = False               # Badge caché jusqu'à obtention
    stackable: bool = False            # Peut être obtenu plusieurs fois
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserBadge(BaseModel):
    """Badge obtenu par un utilisateur"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    badge_id: str
    obtained_at: datetime = Field(default_factory=datetime.utcnow)
    progress: Dict[str, Any] = Field(default_factory=dict)
    count: int = 1                     # Pour badges stackables
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Quest(BaseModel):
    """Modèle de quête/défi"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    category: BadgeCategory
    difficulty: BadgeRarity           # Difficulté = rareté
    requirements: Dict[str, Any]       # Ce qui doit être fait
    rewards: Dict[str, Any]           # Récompenses (coins, xp, badges)
    duration_hours: int = 24          # Durée en heures (24h = quotidien)
    is_daily: bool = True             # Quête quotidienne ou permanente
    active_from: datetime = Field(default_factory=datetime.utcnow)
    active_until: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserQuest(BaseModel):
    """Progression d'un utilisateur sur une quête"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    quest_id: str
    progress: Dict[str, Any] = Field(default_factory=dict)
    completed: bool = False
    completed_at: Optional[datetime] = None
    claimed_rewards: bool = False
    started_at: datetime = Field(default_factory=datetime.utcnow)

class AchievementEngine:
    """Moteur d'achievements intelligent"""
    
    def __init__(self):
        self.badges_registry = {}
        self.load_all_badges()
    
    def load_all_badges(self):
        """Charge tous les badges dans le registre"""
        self.badges_registry = {
            # 🎮 GAMING BADGES
            "first_tournament_win": Badge(
                name="Première Victoire",
                description="Remporte ton premier tournoi !",
                category=BadgeCategory.GAMING,
                rarity=BadgeRarity.COMMON,
                icon="🏆",
                criteria={"tournament_wins": 1},
                xp_reward=100,
                coins_reward=50
            ),
            
            "cs2_specialist": Badge(
                name="Spécialiste CS2",
                description="Participe à 5 tournois CS2",
                category=BadgeCategory.GAMING,
                rarity=BadgeRarity.RARE,
                icon="🔫",
                criteria={"cs2_tournaments": 5},
                xp_reward=200,
                coins_reward=100
            ),
            
            "clutch_master": Badge(
                name="Maître du Clutch",
                description="Badge légendaire pour performances exceptionnelles",
                category=BadgeCategory.GAMING,
                rarity=BadgeRarity.LEGENDARY,
                icon="⚡",
                criteria={"clutch_rounds": 10},
                xp_reward=500,
                coins_reward=300,
                hidden=True
            ),
            
            "tournament_veteran": Badge(
                name="Vétéran des Tournois",
                description="Participe à 25 tournois",
                category=BadgeCategory.COMPETITIVE,
                rarity=BadgeRarity.EPIC,
                icon="🎖️",
                criteria={"tournaments_participated": 25},
                xp_reward=300,
                coins_reward=200
            ),
            
            # 💰 ECONOMIC BADGES
            "first_purchase": Badge(
                name="Premier Achat",
                description="Effectue ton premier achat sur le marketplace",
                category=BadgeCategory.ECONOMIC,
                rarity=BadgeRarity.COMMON,
                icon="🛒",
                criteria={"marketplace_purchases": 1},
                xp_reward=50,
                coins_reward=25
            ),
            
            "coin_collector": Badge(
                name="Collectionneur de Coins",
                description="Accumule 1000 coins",
                category=BadgeCategory.ECONOMIC,
                rarity=BadgeRarity.RARE,
                icon="💰",
                criteria={"total_coins_earned": 1000},
                xp_reward=150,
                coins_reward=75
            ),
            
            "big_spender": Badge(
                name="Gros Dépensier",
                description="Dépense 5000 coins au total",
                category=BadgeCategory.ECONOMIC,
                rarity=BadgeRarity.EPIC,
                icon="💸",
                criteria={"total_coins_spent": 5000},
                xp_reward=250,
                coins_reward=150
            ),
            
            "marketplace_king": Badge(
                name="Roi du Marketplace",
                description="Possède 50 objets différents",
                category=BadgeCategory.ECONOMIC,
                rarity=BadgeRarity.LEGENDARY,
                icon="👑",
                criteria={"unique_items_owned": 50},
                xp_reward=400,
                coins_reward=250
            ),
            
            # 🤝 COMMUNITY BADGES
            "first_comment": Badge(
                name="Premier Commentaire",
                description="Écris ton premier commentaire",
                category=BadgeCategory.COMMUNITY,
                rarity=BadgeRarity.COMMON,
                icon="💬",
                criteria={"comments_posted": 1},
                xp_reward=25,
                coins_reward=10
            ),
            
            "conversationalist": Badge(
                name="Bavard",
                description="Écris 100 commentaires",
                category=BadgeCategory.COMMUNITY,
                rarity=BadgeRarity.RARE,
                icon="🗣️",
                criteria={"comments_posted": 100},
                xp_reward=200,
                coins_reward=100
            ),
            
            "community_helper": Badge(
                name="Aide Communautaire",
                description="Reçois 50 likes sur tes commentaires",
                category=BadgeCategory.SOCIAL,
                rarity=BadgeRarity.RARE,
                icon="🤝",
                criteria={"comment_likes_received": 50},
                xp_reward=180,
                coins_reward=90
            ),
            
            "recruiter": Badge(
                name="Recruteur",
                description="Invite 5 nouveaux membres",
                category=BadgeCategory.COMMUNITY,
                rarity=BadgeRarity.EPIC,
                icon="📨",
                criteria={"referrals": 5},
                xp_reward=300,
                coins_reward=200
            ),
            
            # ⚡ LOYALTY BADGES
            "daily_visitor": Badge(
                name="Visiteur Quotidien",
                description="Connecte-toi 7 jours consécutifs",
                category=BadgeCategory.LOYALTY,
                rarity=BadgeRarity.COMMON,
                icon="📅",
                criteria={"consecutive_days": 7},
                xp_reward=100,
                coins_reward=50
            ),
            
            "week_warrior": Badge(
                name="Guerrier de la Semaine",
                description="Connecte-toi 30 jours consécutifs",
                category=BadgeCategory.LOYALTY,
                rarity=BadgeRarity.RARE,
                icon="🔥",
                criteria={"consecutive_days": 30},
                xp_reward=250,
                coins_reward=150
            ),
            
            "loyalty_legend": Badge(
                name="Légende de Loyauté",
                description="Connecte-toi 365 jours consécutifs",
                category=BadgeCategory.LOYALTY,
                rarity=BadgeRarity.MYTHIC,
                icon="💎",
                criteria={"consecutive_days": 365},
                xp_reward=1000,
                coins_reward=500,
                hidden=True
            ),
            
            # 🏅 COMPETITIVE BADGES  
            "betting_genius": Badge(
                name="Génie des Paris",
                description="Gagne 10 paris consécutifs",
                category=BadgeCategory.COMPETITIVE,
                rarity=BadgeRarity.LEGENDARY,
                icon="🧠",
                criteria={"consecutive_bet_wins": 10},
                xp_reward=400,
                coins_reward=250,
                hidden=True
            ),
            
            "tournament_organizer": Badge(
                name="Organisateur de Tournoi",
                description="Organise ton premier tournoi",
                category=BadgeCategory.COMPETITIVE,
                rarity=BadgeRarity.EPIC,
                icon="🎪",
                criteria={"tournaments_organized": 1},
                xp_reward=300,
                coins_reward=200
            ),
            
            # ⭐ SPECIAL BADGES
            "early_adopter": Badge(
                name="Adopteur Précoce",
                description="L'un des 100 premiers membres",
                category=BadgeCategory.SPECIAL,
                rarity=BadgeRarity.MYTHIC,
                icon="🌟",
                criteria={"user_rank": 100},
                xp_reward=500,
                coins_reward=300,
                hidden=True
            ),
            
            "beta_tester": Badge(
                name="Beta Testeur",
                description="Participe aux tests de nouvelles fonctionnalités",
                category=BadgeCategory.SPECIAL,
                rarity=BadgeRarity.LEGENDARY,
                icon="🧪",
                criteria={"beta_features_tested": 1},
                xp_reward=200,
                coins_reward=150
            ),
            
            # 🎊 ACHIEVEMENT BADGES
            "completionist": Badge(
                name="Perfectionniste",
                description="Obtiens 25 badges différents",
                category=BadgeCategory.ACHIEVEMENT,
                rarity=BadgeRarity.MYTHIC,
                icon="🎯",
                criteria={"unique_badges": 25},
                xp_reward=800,
                coins_reward=400,
                hidden=True
            ),
            
            "social_butterfly": Badge(
                name="Papillon Social",
                description="Interagis avec 50 membres différents",
                category=BadgeCategory.SOCIAL,
                rarity=BadgeRarity.RARE,
                icon="🦋",
                criteria={"unique_interactions": 50},
                xp_reward=150,
                coins_reward=75
            ),
        }
    
    async def check_and_award_badges(self, user_id: str, trigger_event: str = None, event_data: Dict[str, Any] = None):
        """Vérifie et attribue les badges mérités"""
        try:
            # Récupérer données utilisateur
            user_data = await db.users.find_one({"id": user_id})
            if not user_data:
                return []
            
            # Récupérer badges déjà obtenus
            existing_badges = await db.user_badges.find({"user_id": user_id}).to_list(None)
            existing_badge_ids = [badge["badge_id"] for badge in existing_badges]
            
            new_badges = []
            
            # Vérifier chaque badge
            for badge_id, badge in self.badges_registry.items():
                if badge_id in existing_badge_ids and not badge.stackable:
                    continue
                
                # Vérifier les critères
                if await self._check_badge_criteria(user_id, badge, user_data):
                    # Attribuer le badge
                    user_badge = UserBadge(
                        user_id=user_id,
                        badge_id=badge_id,
                        metadata=event_data or {}
                    )
                    
                    await db.user_badges.insert_one(user_badge.dict())
                    
                    # Donner les récompenses
                    await self._give_rewards(user_id, badge)
                    
                    new_badges.append(badge)
                    
                    # Log l'obtention
                    log_user_action(user_id, "badge_earned", {
                        "badge_name": badge.name,
                        "badge_rarity": badge.rarity,
                        "xp_reward": badge.xp_reward,
                        "coins_reward": badge.coins_reward
                    })
                    
                    app_logger.info(f"🏆 Badge '{badge.name}' attribué à l'utilisateur {user_id}")
            
            return new_badges
            
        except Exception as e:
            app_logger.error(f"Erreur vérification badges: {str(e)}")
            return []
    
    async def _check_badge_criteria(self, user_id: str, badge: Badge, user_data: Dict[str, Any]) -> bool:
        """Vérifie si les critères d'un badge sont remplis"""
        try:
            for criterion, required_value in badge.criteria.items():
                
                if criterion == "tournament_wins":
                    # Compter les victoires de tournoi
                    wins = await db.tournament_results.count_documents({
                        "winner_id": user_id
                    })
                    if wins < required_value:
                        return False
                
                elif criterion == "cs2_tournaments":
                    # Compter participations tournois CS2
                    count = await db.tournament_participants.count_documents({
                        "user_id": user_id,
                        "tournament_game": "cs2"
                    })
                    if count < required_value:
                        return False
                
                elif criterion == "tournaments_participated":
                    # Compter toutes participations
                    count = await db.tournament_participants.count_documents({
                        "user_id": user_id
                    })
                    if count < required_value:
                        return False
                
                elif criterion == "marketplace_purchases":
                    # Compter achats marketplace
                    count = await db.transactions.count_documents({
                        "user_id": user_id,
                        "transaction_type": "marketplace_purchase"
                    })
                    if count < required_value:
                        return False
                
                elif criterion == "total_coins_earned":
                    # Total coins gagnés
                    pipeline = [
                        {"$match": {"user_id": user_id, "amount": {"$gt": 0}}},
                        {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
                    ]
                    result = await db.transactions.aggregate(pipeline).to_list(1)
                    total = result[0]["total"] if result else 0
                    if total < required_value:
                        return False
                
                elif criterion == "total_coins_spent":
                    # Total coins dépensés
                    pipeline = [
                        {"$match": {"user_id": user_id, "amount": {"$lt": 0}}},
                        {"$group": {"_id": None, "total": {"$sum": {"$abs": "$amount"}}}}
                    ]
                    result = await db.transactions.aggregate(pipeline).to_list(1)
                    total = result[0]["total"] if result else 0
                    if total < required_value:
                        return False
                
                elif criterion == "comments_posted":
                    # Compter commentaires
                    count = await db.comments.count_documents({"user_id": user_id})
                    if count < required_value:
                        return False
                
                elif criterion == "consecutive_days":
                    # Vérifier jours consécutifs (implémentation simplifiée)
                    # Dans une vraie implémentation, on trackerat les connexions quotidiennes
                    return True  # Placeholder pour l'exemple
                
                elif criterion == "unique_items_owned":
                    # Compter objets uniques possédés
                    user_inventory = user_data.get("inventory", {})
                    unique_items = len(user_inventory)
                    if unique_items < required_value:
                        return False
                
                elif criterion == "user_rank":
                    # Vérifier rang d'inscription (100 premiers)
                    user_count_before = await db.users.count_documents({
                        "created_at": {"$lt": user_data.get("created_at")}
                    })
                    if user_count_before >= required_value:
                        return False
            
            return True
            
        except Exception as e:
            app_logger.error(f"Erreur vérification critères badge: {str(e)}")
            return False
    
    async def _give_rewards(self, user_id: str, badge: Badge):
        """Donne les récompenses du badge"""
        try:
            # Donner XP
            if badge.xp_reward > 0:
                await db.users.update_one(
                    {"id": user_id},
                    {"$inc": {"xp": badge.xp_reward}}
                )
            
            # Donner coins
            if badge.coins_reward > 0:
                await db.users.update_one(
                    {"id": user_id},
                    {"$inc": {"coins": badge.coins_reward}}
                )
                
                # Enregistrer transaction
                from models import CoinTransaction
                transaction = CoinTransaction(
                    user_id=user_id,
                    amount=badge.coins_reward,
                    transaction_type="badge_reward",
                    description=f"Badge obtenu : {badge.name}"
                )
                await db.coin_transactions.insert_one(transaction.dict())
            
        except Exception as e:
            app_logger.error(f"Erreur attribution récompenses: {str(e)}")

# Instance globale du moteur d'achievements
achievement_engine = AchievementEngine()

# Fonctions d'API publiques
async def trigger_achievement_check(user_id: str, event: str = None, data: Dict[str, Any] = None) -> List[Badge]:
    """Déclenche une vérification des achievements pour un utilisateur"""
    return await achievement_engine.check_and_award_badges(user_id, event, data)

async def get_user_badges(user_id: str) -> List[Dict[str, Any]]:
    """Récupère tous les badges d'un utilisateur avec détails"""
    try:
        user_badges = await db.user_badges.find({"user_id": user_id}).to_list(None)
        
        enriched_badges = []
        for user_badge in user_badges:
            badge_info = achievement_engine.badges_registry.get(user_badge["badge_id"])
            if badge_info:
                enriched_badges.append({
                    "id": user_badge["id"],
                    "badge_id": user_badge["badge_id"],
                    "name": badge_info.name,
                    "description": badge_info.description,
                    "category": badge_info.category,
                    "rarity": badge_info.rarity,
                    "icon": badge_info.icon,
                    "obtained_at": user_badge["obtained_at"],
                    "count": user_badge.get("count", 1)
                })
        
        return enriched_badges
        
    except Exception as e:
        app_logger.error(f"Erreur récupération badges utilisateur: {str(e)}")
        return []

async def get_all_badges() -> List[Badge]:
    """Récupère tous les badges disponibles"""
    return list(achievement_engine.badges_registry.values())

async def get_badge_progress(user_id: str, badge_id: str) -> Dict[str, Any]:
    """Récupère la progression vers un badge spécifique"""
    try:
        badge = achievement_engine.badges_registry.get(badge_id)
        if not badge:
            return {}
        
        # Calculer progression (implémentation simplifiée)
        user_data = await db.users.find_one({"id": user_id})
        if not user_data:
            return {}
        
        progress = {}
        total_criteria = len(badge.criteria)
        completed_criteria = 0
        
        for criterion, required_value in badge.criteria.items():
            current_value = await _get_current_criterion_value(user_id, criterion)
            progress[criterion] = {
                "current": current_value,
                "required": required_value,
                "completed": current_value >= required_value
            }
            if current_value >= required_value:
                completed_criteria += 1
        
        return {
            "badge_id": badge_id,
            "badge_name": badge.name,
            "overall_progress": completed_criteria / total_criteria,
            "criteria_progress": progress,
            "completed": completed_criteria == total_criteria
        }
        
    except Exception as e:
        app_logger.error(f"Erreur calcul progression badge: {str(e)}")
        return {}

async def _get_current_criterion_value(user_id: str, criterion: str) -> int:
    """Récupère la valeur actuelle d'un critère pour un utilisateur"""
    # Implémentation simplifiée - dans la vraie vie, on calculera les vraies valeurs
    if criterion == "tournament_wins":
        return await db.tournament_results.count_documents({"winner_id": user_id})
    elif criterion == "comments_posted":
        return await db.comments.count_documents({"user_id": user_id})
    elif criterion == "marketplace_purchases":
        return await db.transactions.count_documents({
            "user_id": user_id,
            "transaction_type": "marketplace_purchase"
        })
    else:
        return 0  # Placeholder