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
                id="first_tournament_win",
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
                id="cs2_specialist",
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
            
            # 🚀 NOUVEAUX BADGES ÉLITE - EXTENSIONS
            
            # 🎯 BADGES PRÉCISION GAMING
            "sharpshooter": Badge(
                name="Tireur d'Élite",
                description="Maintiens 70%+ de précision sur 10 matchs",
                category=BadgeCategory.GAMING,
                rarity=BadgeRarity.EPIC,
                icon="🎯",
                criteria={"accuracy_matches": 10, "min_accuracy": 70},
                xp_reward=350,
                coins_reward=200
            ),
            
            "headshot_king": Badge(
                name="Roi du Headshot",
                description="Réalise 100 headshots au total",
                category=BadgeCategory.GAMING,
                rarity=BadgeRarity.RARE,
                icon="💀",
                criteria={"total_headshots": 100},
                xp_reward=250,
                coins_reward=150
            ),
            
            "clutch_master": Badge(
                name="Maître du Clutch",
                description="Gagne 5 situations 1v3+",
                category=BadgeCategory.GAMING,
                rarity=BadgeRarity.LEGENDARY,
                icon="⚡",
                criteria={"clutch_wins": 5},
                xp_reward=500,
                coins_reward=300,
                hidden=True
            ),
            
            "ace_collector": Badge(
                name="Collectionneur d'Ace",
                description="Réalise 10 Ace (5 kills/rond)",
                category=BadgeCategory.GAMING,
                rarity=BadgeRarity.LEGENDARY,
                icon="🃏",
                criteria={"total_aces": 10},
                xp_reward=400,
                coins_reward=250,
                hidden=True
            ),
            
            # 💰 BADGES ÉCONOMIQUES AVANCÉS
            "coin_saver": Badge(
                name="Économe",
                description="Accumule 1000 coins sans dépenser",
                category=BadgeCategory.ECONOMIC,
                rarity=BadgeRarity.RARE,
                icon="🪙",
                criteria={"max_coins_saved": 1000},
                xp_reward=200,
                coins_reward=100
            ),
            
            "big_spender": Badge(
                name="Gros Dépensier",
                description="Dépense 5000 coins au total",
                category=BadgeCategory.ECONOMIC,
                rarity=BadgeRarity.EPIC,
                icon="💸",
                criteria={"total_coins_spent": 5000},
                xp_reward=300,
                coins_reward=200
            ),
            
            "marketplace_mogul": Badge(
                name="Magnat du Marché",
                description="Achète 25 objets différents",
                category=BadgeCategory.ECONOMIC,
                rarity=BadgeRarity.EPIC,
                icon="🏪",
                criteria={"unique_items_bought": 25},
                xp_reward=350,
                coins_reward=250
            ),
            
            "daily_bonus_streak": Badge(
                name="Fidèle Collecteur",
                description="Collecte le bonus quotidien 30 jours d'affilée",
                category=BadgeCategory.ECONOMIC,
                rarity=BadgeRarity.RARE,
                icon="🗓️",
                criteria={"daily_bonus_streak": 30},
                xp_reward=250,
                coins_reward=200
            ),
            
            # 🏆 BADGES COMPÉTITIFS AVANCÉS
            "tournament_destroyer": Badge(
                name="Destructeur de Tournoi",
                description="Gagne 3 tournois consécutifs",
                category=BadgeCategory.COMPETITIVE,
                rarity=BadgeRarity.MYTHIC,
                icon="🏆",
                criteria={"consecutive_tournament_wins": 3},
                xp_reward=800,
                coins_reward=500,
                hidden=True
            ),
            
            "bracket_buster": Badge(
                name="Briseur de Bracket",
                description="Élimine le favori #1 du tournoi",
                category=BadgeCategory.COMPETITIVE,
                rarity=BadgeRarity.LEGENDARY,
                icon="💥",
                criteria={"upset_victories": 1},
                xp_reward=400,
                coins_reward=300
            ),
            
            "underdog_hero": Badge(
                name="Héros de l'Underdog",
                description="Gagne en étant classé dernier",
                category=BadgeCategory.COMPETITIVE,
                rarity=BadgeRarity.EPIC,
                icon="🦸",
                criteria={"underdog_wins": 1},
                xp_reward=350,
                coins_reward=250
            ),
            
            "comeback_king": Badge(
                name="Roi du Comeback",
                description="Remonte de 10+ points de retard",
                category=BadgeCategory.COMPETITIVE,
                rarity=BadgeRarity.RARE,
                icon="📈",
                criteria={"comeback_victories": 5},
                xp_reward=300,
                coins_reward=200
            ),
            
            # 👥 BADGES SOCIAUX COMMUNAUTAIRES
            "mentor": Badge(
                name="Mentor de la Communauté",
                description="Aide 10 nouveaux joueurs",
                category=BadgeCategory.SOCIAL,
                rarity=BadgeRarity.EPIC,
                icon="🎓",
                criteria={"players_mentored": 10},
                xp_reward=400,
                coins_reward=250
            ),
            
            "party_starter": Badge(
                name="Lanceur de Soirée",
                description="Organise 5 événements communautaires",
                category=BadgeCategory.SOCIAL,
                rarity=BadgeRarity.LEGENDARY,
                icon="🎉",
                criteria={"events_organized": 5},
                xp_reward=500,
                coins_reward=350
            ),
            
            "peace_maker": Badge(
                name="Pacificateur",
                description="Résous 3 conflits communautaires",
                category=BadgeCategory.SOCIAL,
                rarity=BadgeRarity.RARE,
                icon="🕊️",
                criteria={"conflicts_resolved": 3},
                xp_reward=250,
                coins_reward=150
            ),
            
            "wingman": Badge(
                name="Ailier Parfait",
                description="Forme 5 équipes qui gagnent ensemble",
                category=BadgeCategory.SOCIAL,
                rarity=BadgeRarity.EPIC,
                icon="🤝",
                criteria={"successful_team_formations": 5},
                xp_reward=350,
                coins_reward=200
            ),
            
            # 🔥 BADGES STREAKS & PERFORMANCES
            "unstoppable": Badge(
                name="Inarrêtable",
                description="Gagne 15 matchs consécutifs",
                category=BadgeCategory.GAMING,
                rarity=BadgeRarity.LEGENDARY,
                icon="🔥",
                criteria={"match_win_streak": 15},
                xp_reward=600,
                coins_reward=400,
                hidden=True
            ),
            
            "flawless_victory": Badge(
                name="Victoire Parfaite",
                description="Gagne un match sans mourir",
                category=BadgeCategory.GAMING,
                rarity=BadgeRarity.RARE,
                icon="✨",
                criteria={"flawless_matches": 1},
                xp_reward=200,
                coins_reward=100
            ),
            
            "marathon_gamer": Badge(
                name="Gamer Marathon",
                description="Joue 12h en une journée",
                category=BadgeCategory.GAMING,
                rarity=BadgeRarity.EPIC,
                icon="⏰",
                criteria={"daily_playtime_hours": 12},
                xp_reward=300,
                coins_reward=200
            ),
            
            "night_owl": Badge(
                name="Oiseau de Nuit",
                description="Joue entre 2h et 6h du matin",
                category=BadgeCategory.GAMING,
                rarity=BadgeRarity.COMMON,
                icon="🦉",
                criteria={"night_sessions": 10},
                xp_reward=150,
                coins_reward=75
            ),
            
            # 💎 BADGES RARETÉ ULTIME
            "legendary_status": Badge(
                name="Statut Légendaire",
                description="Atteins le niveau 50",
                category=BadgeCategory.ACHIEVEMENT,
                rarity=BadgeRarity.MYTHIC,
                icon="👑",
                criteria={"user_level": 50},
                xp_reward=1000,
                coins_reward=750,
                hidden=True
            ),
            
            "badge_collector": Badge(
                name="Collectionneur Ultime",
                description="Obtiens 50 badges différents",
                category=BadgeCategory.ACHIEVEMENT,
                rarity=BadgeRarity.MYTHIC,
                icon="🏅",
                criteria={"unique_badges": 50},
                xp_reward=1200,
                coins_reward=800,
                hidden=True
            ),
            
            # 🎨 BADGES CRÉATIVITÉ
            "content_creator": Badge(
                name="Créateur de Contenu",
                description="Écris 25 guides/tutoriels",
                category=BadgeCategory.COMMUNITY,
                rarity=BadgeRarity.LEGENDARY,
                icon="📝",
                criteria={"guides_written": 25},
                xp_reward=500,
                coins_reward=350
            ),
            
            "screenshot_artist": Badge(
                name="Artiste Screenshot",
                description="Partage 50 captures d'écran",
                category=BadgeCategory.COMMUNITY,
                rarity=BadgeRarity.RARE,
                icon="📸",
                criteria={"screenshots_shared": 50},
                xp_reward=200,
                coins_reward=100
            ),
            
            # 🌟 BADGES ÉVÉNEMENTS SPÉCIAUX
            "holiday_champion": Badge(
                name="Champion des Fêtes",
                description="Gagne un tournoi spécial fêtes",
                category=BadgeCategory.SPECIAL,
                rarity=BadgeRarity.LEGENDARY,
                icon="🎄",
                criteria={"holiday_tournament_wins": 1},
                xp_reward=400,
                coins_reward=300
            ),
            
            "anniversary_veteran": Badge(
                name="Vétéran Anniversaire",
                description="Présent lors du 1er anniversaire",
                category=BadgeCategory.SPECIAL,
                rarity=BadgeRarity.MYTHIC,
                icon="🎂",
                criteria={"anniversary_participation": 1},
                xp_reward=500,
                coins_reward=400,
                hidden=True
            ),
            
            # 🎯 BADGES PRÉCISION AVANCÉE
            "spray_control_master": Badge(
                name="Maître du Spray Control",
                description="Maintiens 95%+ de précision spray",
                category=BadgeCategory.GAMING,
                rarity=BadgeRarity.LEGENDARY,
                icon="🎪",
                criteria={"spray_control_accuracy": 95},
                xp_reward=450,
                coins_reward=300,
                hidden=True
            ),
            
            "reaction_time_god": Badge(
                name="Dieu du Temps de Réaction",
                description="Temps de réaction moyen < 200ms",
                category=BadgeCategory.GAMING,
                rarity=BadgeRarity.MYTHIC,
                icon="⚡",
                criteria={"avg_reaction_time": 200},
                xp_reward=800,
                coins_reward=500,
                hidden=True
            ),
            
            # 💪 BADGES ENDURANCE & PROGRESSION
            "iron_will": Badge(
                name="Volonté de Fer",
                description="Joue malgré 10 défaites consécutives",
                category=BadgeCategory.LOYALTY,
                rarity=BadgeRarity.RARE,
                icon="🛡️",
                criteria={"perseverance_losses": 10},
                xp_reward=300,
                coins_reward=200
            ),
            
            "phoenix": Badge(
                name="Phénix",
                description="Remonte de Bronze à Gold en une saison",
                category=BadgeCategory.COMPETITIVE,
                rarity=BadgeRarity.EPIC,
                icon="🔥",
                criteria={"rank_improvement": "bronze_to_gold"},
                xp_reward=400,
                coins_reward=300
            ),
            
            # 🎲 BADGES CHANCE & STATISTIQUES
            "lucky_seven": Badge(
                name="Sept Chanceux",
                description="Gagne 7 paris avec cote 7:1+",
                category=BadgeCategory.COMPETITIVE,
                rarity=BadgeRarity.LEGENDARY,
                icon="🍀",
                criteria={"high_odds_wins": 7},
                xp_reward=500,
                coins_reward=400,
                hidden=True
            ),
            
            "statistician": Badge(
                name="Statisticien",
                description="Analyse 100 matchs en détail",
                category=BadgeCategory.COMPETITIVE,
                rarity=BadgeRarity.RARE,
                icon="📊",
                criteria={"matches_analyzed": 100},
                xp_reward=250,
                coins_reward=150
            ),
            
            # 🌟 BADGES MYTHIQUES EXCLUSIFS ÉLITE
            "oupafamilly_legend": Badge(
                name="Légende d'Oupafamilly",
                description="Atteins le statut ultime avec 100+ badges",
                category=BadgeCategory.ACHIEVEMENT,
                rarity=BadgeRarity.MYTHIC,
                icon="🌟",
                criteria={"unique_badges": 100},
                xp_reward=2000,
                coins_reward=1000,
                hidden=True
            ),
            
            "perfect_player": Badge(
                name="Joueur Parfait",
                description="100% winrate sur 20 matchs + 90%+ précision",
                category=BadgeCategory.GAMING,
                rarity=BadgeRarity.MYTHIC,
                icon="💎",
                criteria={"perfect_streak": 20, "min_accuracy": 90},
                xp_reward=1500,
                coins_reward=900,
                hidden=True
            ),
            
            "community_god": Badge(
                name="Dieu de la Communauté",
                description="Mentor 100+ joueurs + organise 25+ événements",
                category=BadgeCategory.SOCIAL,
                rarity=BadgeRarity.MYTHIC,
                icon="👑",
                criteria={"players_mentored": 100, "events_organized": 25},
                xp_reward=1800,
                coins_reward=1200,
                hidden=True
            ),
            
            "tournament_emperor": Badge(
                name="Empereur des Tournois",
                description="Gagne 50 tournois différents",
                category=BadgeCategory.COMPETITIVE,
                rarity=BadgeRarity.MYTHIC,
                icon="🏛️",
                criteria={"tournament_wins": 50},
                xp_reward=2500,
                coins_reward=1500,
                hidden=True
            ),
            
            "economic_mastermind": Badge(
                name="Génie Économique",
                description="Accumule 100,000 coins + 1000 transactions",
                category=BadgeCategory.ECONOMIC,
                rarity=BadgeRarity.MYTHIC,
                icon="💰",
                criteria={"total_coins_earned": 100000, "transactions_made": 1000},
                xp_reward=2200,
                coins_reward=1300,
                hidden=True
            ),
            
            "immortal_gaming": Badge(
                name="Gaming Immortel",
                description="500+ Ace + 1000+ Clutch + 50+ Flawless",
                category=BadgeCategory.GAMING,
                rarity=BadgeRarity.MYTHIC,
                icon="⚡",
                criteria={"total_aces": 500, "clutch_wins": 1000, "flawless_matches": 50},
                xp_reward=3000,
                coins_reward=2000,
                hidden=True
            ),
            
            "founder": Badge(
                name="Fondateur",
                description="L'un des 10 premiers membres d'Oupafamilly",
                category=BadgeCategory.SPECIAL,
                rarity=BadgeRarity.MYTHIC,
                icon="🏛️",
                criteria={"user_rank": 10},
                xp_reward=5000,
                coins_reward=3000,
                hidden=True
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
                
                # 🆕 NOUVEAUX CRITÈRES BADGES ÉLITE
                
                elif criterion == "max_coins_saved":
                    # Maximum de coins économisés
                    current_coins = user_data.get("coins", 0)
                    if current_coins < required_value:
                        return False
                
                elif criterion == "unique_items_bought":
                    # Articles uniques achetés
                    pipeline = [
                        {"$match": {"user_id": user_id, "transaction_type": "marketplace_purchase"}},
                        {"$group": {"_id": "$item_id"}},
                        {"$count": "unique_items"}
                    ]
                    result = await db.transactions.aggregate(pipeline).to_list(1)
                    count = result[0]["unique_items"] if result else 0
                    if count < required_value:
                        return False
                
                elif criterion == "consecutive_tournament_wins":
                    # Victoires consécutives de tournois
                    # Dans une vraie implémentation, on trackerat la streak
                    return False  # Placeholder - nécessite tracking des streaks
                
                elif criterion == "daily_bonus_streak":
                    # Streak bonus quotidien
                    streak = user_data.get("daily_bonus_streak", 0)
                    if streak < required_value:
                        return False
                
                elif criterion == "total_headshots":
                    # Total headshots (stats gaming)
                    stats = user_data.get("gaming_stats", {})
                    headshots = stats.get("total_headshots", 0)
                    if headshots < required_value:
                        return False
                
                elif criterion == "clutch_wins":
                    # Situations clutch gagnées
                    stats = user_data.get("gaming_stats", {})
                    clutches = stats.get("clutch_wins", 0)
                    if clutches < required_value:
                        return False
                
                elif criterion == "total_aces":
                    # Total Ace réalisés
                    stats = user_data.get("gaming_stats", {})
                    aces = stats.get("total_aces", 0)
                    if aces < required_value:
                        return False
                
                elif criterion == "match_win_streak":
                    # Streak victoires matchs
                    stats = user_data.get("gaming_stats", {})
                    streak = stats.get("current_win_streak", 0)
                    if streak < required_value:
                        return False
                
                elif criterion == "consecutive_bet_wins":
                    # Paris gagnés consécutifs
                    betting_stats = user_data.get("betting_stats", {})
                    streak = betting_stats.get("consecutive_wins", 0)
                    if streak < required_value:
                        return False
                
                elif criterion == "players_mentored":
                    # Joueurs mentorés
                    mentoring = user_data.get("mentoring_stats", {})
                    count = mentoring.get("players_helped", 0)
                    if count < required_value:
                        return False
                
                elif criterion == "events_organized":
                    # Événements organisés
                    events = await db.events.count_documents({"organizer_id": user_id})
                    if events < required_value:
                        return False
                
                elif criterion == "user_level":
                    # Niveau utilisateur
                    level = user_data.get("level", 1)
                    if level < required_value:
                        return False
                
                elif criterion == "unique_badges":
                    # Badges uniques obtenus
                    badge_count = await db.user_badges.count_documents({"user_id": user_id})
                    if badge_count < required_value:
                        return False
                
                elif criterion == "guides_written":
                    # Guides/tutoriels écrits
                    guides = await db.user_guides.count_documents({"author_id": user_id})
                    if guides < required_value:
                        return False
                
                elif criterion == "screenshots_shared":
                    # Screenshots partagés
                    screenshots = await db.user_screenshots.count_documents({"user_id": user_id})
                    if screenshots < required_value:
                        return False
                
                elif criterion == "accuracy_matches":
                    # Matchs avec précision élevée
                    stats = user_data.get("gaming_stats", {})
                    accuracy_matches = stats.get("high_accuracy_matches", 0)
                    if accuracy_matches < required_value:
                        return False
                
                elif criterion == "min_accuracy":
                    # Précision minimale requise
                    stats = user_data.get("gaming_stats", {})
                    avg_accuracy = stats.get("average_accuracy", 0)
                    if avg_accuracy < required_value:
                        return False
                
                elif criterion == "daily_playtime_hours":
                    # Temps de jeu quotidien
                    today_playtime = user_data.get("today_playtime_hours", 0)
                    if today_playtime < required_value:
                        return False
                
                elif criterion == "night_sessions":
                    # Sessions nocturnes
                    stats = user_data.get("gaming_stats", {})
                    night_sessions = stats.get("night_sessions", 0)
                    if night_sessions < required_value:
                        return False
                
                elif criterion == "flawless_matches":
                    # Matchs sans mort
                    stats = user_data.get("gaming_stats", {})
                    flawless = stats.get("flawless_victories", 0)
                    if flawless < required_value:
                        return False
                
                elif criterion == "upset_victories":
                    # Victoires inattendues
                    stats = user_data.get("competitive_stats", {})
                    upsets = stats.get("upset_victories", 0)
                    if upsets < required_value:
                        return False
                
                elif criterion == "underdog_wins":
                    # Victoires en underdog
                    stats = user_data.get("competitive_stats", {})
                    underdog_wins = stats.get("underdog_wins", 0)
                    if underdog_wins < required_value:
                        return False
                
                elif criterion == "comeback_victories":
                    # Victoires en remontée
                    stats = user_data.get("competitive_stats", {})
                    comebacks = stats.get("comeback_victories", 0)
                    if comebacks < required_value:
                        return False
                
                elif criterion == "high_odds_wins":
                    # Paris gagnés à haute cote
                    betting_stats = user_data.get("betting_stats", {})
                    high_odds_wins = betting_stats.get("high_odds_wins", 0)
                    if high_odds_wins < required_value:
                        return False
                
                elif criterion == "matches_analyzed":
                    # Matchs analysés en détail
                    analysis_count = await db.match_analyses.count_documents({"analyst_id": user_id})
                    if analysis_count < required_value:
                        return False
                
                elif criterion == "spray_control_accuracy":
                    # Précision du spray control
                    stats = user_data.get("gaming_stats", {})
                    spray_accuracy = stats.get("spray_control_accuracy", 0)
                    if spray_accuracy < required_value:
                        return False
                
                elif criterion == "avg_reaction_time":
                    # Temps de réaction moyen (plus petit = meilleur)
                    stats = user_data.get("gaming_stats", {})
                    reaction_time = stats.get("avg_reaction_time_ms", 999)
                    if reaction_time > required_value:  # Inverse : plus petit = meilleur
                        return False
                
                elif criterion == "perseverance_losses":
                    # Persévérance après défaites
                    stats = user_data.get("mental_stats", {})
                    max_loss_streak = stats.get("max_loss_streak_endured", 0)
                    if max_loss_streak < required_value:
                        return False
                
                elif criterion == "rank_improvement":
                    # Amélioration de rang
                    elo_history = user_data.get("elo_history", [])
                    if required_value == "bronze_to_gold":
                        # Vérifier s'il est passé de Bronze à Gold
                        if not self._check_rank_progression(elo_history, "bronze", "gold"):
                            return False
                
                elif criterion == "holiday_tournament_wins":
                    # Tournois spéciaux gagnés
                    wins = await db.tournament_results.count_documents({
                        "winner_id": user_id,
                        "tournament_type": "holiday_special"
                    })
                    if wins < required_value:
                        return False
                
                elif criterion == "anniversary_participation":
                    # Participation événement anniversaire
                    participation = user_data.get("special_events", {}).get("anniversary_2024", False)
                    if not participation:
                        return False
                
                # 🆕 CRITÈRES BADGES MYTHIQUES ÉLITE
                
                elif criterion == "perfect_streak":
                    # Streak parfaite (wins + précision)
                    stats = user_data.get("gaming_stats", {})
                    perfect_streak = stats.get("perfect_match_streak", 0)
                    if perfect_streak < required_value:
                        return False
                
                elif criterion == "transactions_made":
                    # Total transactions effectuées
                    transaction_count = await db.transactions.count_documents({"user_id": user_id})
                    if transaction_count < required_value:
                        return False
            
            return True
            
        except Exception as e:
            app_logger.error(f"Erreur vérification critères badge: {str(e)}")
            return False
    
    def _check_rank_progression(self, elo_history: List[Dict], start_rank: str, end_rank: str) -> bool:
        """Vérifie si l'utilisateur a progressé d'un rang à un autre"""
        if not elo_history or len(elo_history) < 2:
            return False
        
        rank_values = {
            "bronze": 0, "silver": 1000, "gold": 1200, 
            "platinum": 1400, "diamond": 1600, "master": 1800,
            "grandmaster": 2000, "challenger": 2200
        }
        
        start_value = rank_values.get(start_rank, 0)
        end_value = rank_values.get(end_rank, 9999)
        
        # Chercher le point le plus bas et le plus haut
        min_elo = min(entry.get("elo", 0) for entry in elo_history)
        max_elo = max(entry.get("elo", 0) for entry in elo_history)
        
        return min_elo <= start_value and max_elo >= end_value
    
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

# =====================================================
# QUEST ENGINE - Système de Quêtes Quotidiennes
# =====================================================

class QuestEngine:
    """Moteur de quêtes quotidiennes intelligent"""
    
    def __init__(self):
        self.daily_quests_pool = self._initialize_quest_pool()
    
    def _initialize_quest_pool(self) -> Dict[str, Quest]:
        """Initialise le pool de quêtes quotidiennes"""
        return {
            # 🎮 Gaming Quests
            "play_tournament": Quest(
                name="Participe à un Tournoi",
                description="Inscris-toi et joue dans au moins un tournoi aujourd'hui",
                category=BadgeCategory.GAMING,
                difficulty=BadgeRarity.COMMON,
                requirements={"tournament_participation": 1},
                rewards={"coins": 25, "xp": 50},
                duration_hours=24
            ),
            
            "win_matches": Quest(
                name="Remporte 3 Matchs",
                description="Gagne 3 matchs dans des tournois ou parties classées",
                category=BadgeCategory.COMPETITIVE,
                difficulty=BadgeRarity.RARE,
                requirements={"matches_won": 3},
                rewards={"coins": 50, "xp": 100},
                duration_hours=24
            ),
            
            "cs2_specialist_daily": Quest(
                name="Spécialiste CS2 du Jour",
                description="Joue 2 parties de CS2 avec de bonnes performances",
                category=BadgeCategory.GAMING,
                difficulty=BadgeRarity.COMMON,
                requirements={"cs2_matches": 2, "min_kdr": 1.0},
                rewards={"coins": 30, "xp": 60},
                duration_hours=24
            ),
            
            # 💰 Economic Quests
            "spend_coins": Quest(
                name="Investisseur du Jour",
                description="Dépense 100 coins dans le marketplace",
                category=BadgeCategory.ECONOMIC,
                difficulty=BadgeRarity.COMMON,
                requirements={"coins_spent": 100},
                rewards={"coins": 20, "xp": 40},
                duration_hours=24
            ),
            
            "marketplace_explorer": Quest(
                name="Explorateur du Marketplace",
                description="Achète 2 objets différents dans le marketplace",
                category=BadgeCategory.ECONOMIC,
                difficulty=BadgeRarity.RARE,
                requirements={"marketplace_purchases": 2},
                rewards={"coins": 40, "xp": 80},
                duration_hours=24
            ),
            
            "coin_collector_daily": Quest(
                name="Collectionneur Quotidien",
                description="Accumule 150 coins à travers diverses activités",
                category=BadgeCategory.ECONOMIC,
                difficulty=BadgeRarity.EPIC,
                requirements={"coins_earned": 150},
                rewards={"coins": 75, "xp": 120},
                duration_hours=24
            ),
            
            # 🤝 Community Quests
            "social_butterfly": Quest(
                name="Papillon Social",
                description="Écris 5 commentaires positifs sur des profils",
                category=BadgeCategory.SOCIAL,
                difficulty=BadgeRarity.COMMON,
                requirements={"comments_posted": 5, "min_rating": 4},
                rewards={"coins": 25, "xp": 50},
                duration_hours=24
            ),
            
            "chat_active": Quest(
                name="Bavard Communautaire",
                description="Envoie 10 messages dans le chat de la communauté",
                category=BadgeCategory.COMMUNITY,
                difficulty=BadgeRarity.COMMON,
                requirements={"chat_messages": 10},
                rewards={"coins": 20, "xp": 30},
                duration_hours=24
            ),
            
            "helper": Quest(
                name="Aide Communautaire",
                description="Aide 3 nouveaux membres (commentaires, messages privés)",
                category=BadgeCategory.COMMUNITY,
                difficulty=BadgeRarity.RARE,
                requirements={"help_interactions": 3},
                rewards={"coins": 60, "xp": 100},
                duration_hours=24
            ),
            
            # 🎯 Betting & Strategy Quests
            "smart_bettor": Quest(
                name="Parieur Intelligent",
                description="Place 3 paris avec des cotes différentes",
                category=BadgeCategory.COMPETITIVE,
                difficulty=BadgeRarity.RARE,
                requirements={"bets_placed": 3, "different_odds": True},
                rewards={"coins": 45, "xp": 90},
                duration_hours=24
            ),
            
            "risk_manager": Quest(
                name="Gestionnaire de Risque",
                description="Gagne au moins 1 pari sur 3 placés aujourd'hui",
                category=BadgeCategory.COMPETITIVE,
                difficulty=BadgeRarity.EPIC,
                requirements={"bets_placed": 3, "min_win_rate": 0.33},
                rewards={"coins": 80, "xp": 150},
                duration_hours=24
            ),
            
            # ⭐ Special Daily Quests
            "perfect_day": Quest(
                name="Journée Parfaite",
                description="Complète 4 autres quêtes quotidiennes aujourd'hui",
                category=BadgeCategory.SPECIAL,
                difficulty=BadgeRarity.LEGENDARY,
                requirements={"daily_quests_completed": 4},
                rewards={"coins": 200, "xp": 300, "bonus_badge": "daily_completionist"},
                duration_hours=24
            ),
            
            "early_bird": Quest(
                name="Lève-tôt",
                description="Connecte-toi avant 8h du matin et joue 30 minutes",
                category=BadgeCategory.LOYALTY,
                difficulty=BadgeRarity.RARE,
                requirements={"early_login": True, "playtime_minutes": 30},
                rewards={"coins": 50, "xp": 75},
                duration_hours=24
            ),
            
            "night_owl": Quest(
                name="Chouette Nocturne",
                description="Joue entre 22h et 2h du matin pendant 45 minutes",
                category=BadgeCategory.LOYALTY,
                difficulty=BadgeRarity.RARE,
                requirements={"night_play": True, "playtime_minutes": 45},
                rewards={"coins": 55, "xp": 80},
                duration_hours=24
            ),
            
            # 🔥 Weekly Special Quests (appear certain days)
            "weekend_warrior": Quest(
                name="Guerrier du Week-end",
                description="Participe à 3 tournois ce week-end",
                category=BadgeCategory.COMPETITIVE,
                difficulty=BadgeRarity.EPIC,
                requirements={"weekend_tournaments": 3},
                rewards={"coins": 100, "xp": 200},
                duration_hours=48,  # Week-end
                is_daily=False
            ),
            
            "monday_motivation": Quest(
                name="Motivation du Lundi",
                description="Commence la semaine fort : 2 tournois + 5 commentaires",
                category=BadgeCategory.LOYALTY,
                difficulty=BadgeRarity.EPIC,
                requirements={"tournaments": 2, "comments": 5},
                rewards={"coins": 80, "xp": 150},
                duration_hours=24
            )
        }
    
    async def get_daily_quests_for_date(self, target_date) -> List[Quest]:
        """Génère les quêtes quotidiennes pour une date donnée"""
        try:
            from datetime import datetime
            import hashlib
            
            # Créer une seed basée sur la date pour avoir des quêtes cohérentes
            date_str = target_date.isoformat()
            seed = int(hashlib.md5(date_str.encode()).hexdigest()[:8], 16)
            
            # Sélectionner 5 quêtes pour aujourd'hui (mix équilibré)
            all_daily_quests = [q for q in self.daily_quests_pool.values() if q.is_daily]
            
            # Algorithme de sélection basé sur la seed
            selected_quests = []
            
            # 1. Toujours inclure une quête community (engagement)
            community_quests = [q for q in all_daily_quests if q.category in [BadgeCategory.COMMUNITY, BadgeCategory.SOCIAL]]
            if community_quests:
                selected_quests.append(community_quests[seed % len(community_quests)])
            
            # 2. Inclure une quête gaming
            gaming_quests = [q for q in all_daily_quests if q.category in [BadgeCategory.GAMING, BadgeCategory.COMPETITIVE]]
            if gaming_quests:
                selected_quests.append(gaming_quests[(seed + 1) % len(gaming_quests)])
            
            # 3. Inclure une quête economic
            economic_quests = [q for q in all_daily_quests if q.category == BadgeCategory.ECONOMIC]
            if economic_quests:
                selected_quests.append(economic_quests[(seed + 2) % len(economic_quests)])
            
            # 4. Sélectionner 2 quêtes aléatoires parmi les restantes
            remaining_quests = [q for q in all_daily_quests if q not in selected_quests]
            if len(remaining_quests) >= 2:
                selected_quests.append(remaining_quests[(seed + 3) % len(remaining_quests)])
                selected_quests.append(remaining_quests[(seed + 4) % len(remaining_quests)])
            
            # Quêtes spéciales selon le jour de la semaine
            weekday = target_date.weekday()  # 0 = Lundi, 6 = Dimanche
            
            if weekday == 0:  # Lundi
                monday_quest = self.daily_quests_pool.get("monday_motivation")
                if monday_quest and monday_quest not in selected_quests:
                    selected_quests.append(monday_quest)
            
            elif weekday in [5, 6]:  # Week-end
                weekend_quest = self.daily_quests_pool.get("weekend_warrior")
                if weekend_quest and weekend_quest not in selected_quests:
                    selected_quests.append(weekend_quest)
            
            # Mettre à jour les dates d'activité
            today_start = datetime.combine(target_date, datetime.min.time())
            for quest in selected_quests:
                quest.active_from = today_start
                quest.active_until = today_start.replace(hour=23, minute=59, second=59)
            
            return selected_quests[:6]  # Maximum 6 quêtes par jour
            
        except Exception as e:
            app_logger.error(f"Erreur génération quêtes quotidiennes: {str(e)}")
            return []
    
    async def get_user_quest_progress(self, user_id: str, quest_id: str) -> Dict[str, Any]:
        """Récupère la progression d'un utilisateur sur une quête"""
        try:
            # Récupérer la progression de l'utilisateur
            user_quest = await db.user_quests.find_one({
                "user_id": user_id,
                "quest_id": quest_id
            })
            
            if not user_quest:
                # Créer une entrée vide si elle n'existe pas
                from achievements import UserQuest
                new_user_quest = UserQuest(
                    user_id=user_id,
                    quest_id=quest_id
                )
                await db.user_quests.insert_one(new_user_quest.dict())
                return {
                    "progress": {},
                    "completed": False,
                    "rewards_claimed": False,
                    "completion_percentage": 0.0
                }
            
            # Calculer le pourcentage de complétion
            quest = self.daily_quests_pool.get(quest_id)
            if not quest:
                return user_quest
            
            completion_percentage = await self._calculate_quest_completion_percentage(user_id, quest, user_quest.get("progress", {}))
            
            return {
                "progress": user_quest.get("progress", {}),
                "completed": user_quest.get("completed", False),
                "rewards_claimed": user_quest.get("rewards_claimed", False),
                "completion_percentage": completion_percentage,
                "started_at": user_quest.get("started_at"),
                "completed_at": user_quest.get("completed_at")
            }
            
        except Exception as e:
            app_logger.error(f"Erreur récupération progression quête: {str(e)}")
            return {}
    
    async def _calculate_quest_completion_percentage(self, user_id: str, quest: Quest, current_progress: Dict[str, Any]) -> float:
        """Calcule le pourcentage de complétion d'une quête"""
        try:
            total_requirements = len(quest.requirements)
            completed_requirements = 0
            
            for requirement, target_value in quest.requirements.items():
                current_value = current_progress.get(requirement, 0)
                
                if requirement in ["tournament_participation", "matches_won", "cs2_matches"]:
                    # Compter depuis les stats actuelles de l'utilisateur
                    if current_value >= target_value:
                        completed_requirements += 1
                    
                elif requirement in ["coins_spent", "coins_earned"]:
                    # Compter depuis les transactions du jour
                    if current_value >= target_value:
                        completed_requirements += 1
                        
                elif requirement in ["comments_posted", "chat_messages"]:
                    # Compter depuis l'activité du jour
                    if current_value >= target_value:
                        completed_requirements += 1
                
                elif requirement == "daily_quests_completed":
                    # Compter les autres quêtes terminées aujourd'hui
                    other_completed = await self._count_user_daily_quests_completed(user_id)
                    if other_completed >= target_value:
                        completed_requirements += 1
                
                else:
                    # Pour les autres critères, utiliser la valeur actuelle
                    if isinstance(target_value, bool):
                        if current_value is True:
                            completed_requirements += 1
                    else:
                        if current_value >= target_value:
                            completed_requirements += 1
            
            return completed_requirements / max(total_requirements, 1)
            
        except Exception as e:
            app_logger.error(f"Erreur calcul pourcentage quête: {str(e)}")
            return 0.0
    
    async def claim_quest_rewards(self, user_id: str, quest_id: str) -> Dict[str, Any]:
        """Réclame les récompenses d'une quête terminée"""
        try:
            quest = self.daily_quests_pool.get(quest_id)
            if not quest:
                raise ValueError("Quête non trouvée")
            
            # Marquer les récompenses comme réclamées
            await db.user_quests.update_one(
                {"user_id": user_id, "quest_id": quest_id},
                {"$set": {"rewards_claimed": True}}
            )
            
            # Donner les récompenses
            rewards_given = {}
            
            # Coins
            if "coins" in quest.rewards:
                coins_reward = quest.rewards["coins"]
                await db.users.update_one(
                    {"id": user_id},
                    {"$inc": {"coins": coins_reward}}
                )
                
                # Enregistrer la transaction
                from models import CoinTransaction
                transaction = CoinTransaction(
                    user_id=user_id,
                    amount=coins_reward,
                    transaction_type="quest_reward",
                    description=f"Quête terminée : {quest.name}"
                )
                await db.coin_transactions.insert_one(transaction.dict())
                rewards_given["coins"] = coins_reward
            
            # XP
            if "xp" in quest.rewards:
                xp_reward = quest.rewards["xp"]
                await db.users.update_one(
                    {"id": user_id},
                    {"$inc": {"xp": xp_reward}}
                )
                rewards_given["xp"] = xp_reward
            
            # Badge bonus (si applicable)
            if "bonus_badge" in quest.rewards:
                bonus_badge_id = quest.rewards["bonus_badge"]
                if bonus_badge_id in achievement_engine.badges_registry:
                    # Attribuer le badge bonus
                    await achievement_engine.check_and_award_badges(user_id, "quest_bonus", {"quest_id": quest_id})
                    rewards_given["bonus_badge"] = bonus_badge_id
            
            log_user_action(user_id, "quest_completed", {
                "quest_name": quest.name,
                "rewards": rewards_given
            })
            
            return rewards_given
            
        except Exception as e:
            app_logger.error(f"Erreur réclamation récompenses quête: {str(e)}")
            raise
    
    async def _count_user_daily_quests_completed(self, user_id: str) -> int:
        """Compte le nombre de quêtes quotidiennes terminées aujourd'hui par un utilisateur"""
        try:
            from datetime import datetime
            today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            
            count = await db.user_quests.count_documents({
                "user_id": user_id,
                "completed": True,
                "completed_at": {"$gte": today_start}
            })
            
            return count
            
        except Exception as e:
            app_logger.error(f"Erreur comptage quêtes quotidiennes: {str(e)}")
            return 0

# Instance globale du moteur de quêtes
quest_engine = QuestEngine()

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