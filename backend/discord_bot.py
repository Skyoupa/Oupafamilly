"""
🤖 OUPAFAMILLY DISCORD BOT - SYSTÈME ÉLITE
Bot Discord intégré pour la communauté gaming
"""

import discord
from discord.ext import commands, tasks
import asyncio
import aiohttp
import os
import json
from datetime import datetime, timedelta
import logging
from typing import Optional, Dict, Any

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('oupafamilly_bot')

class OupafamillyBot(commands.Bot):
    """Bot Discord pour la communauté Oupafamilly"""
    
    def __init__(self):
        # Configuration des intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        super().__init__(
            command_prefix='!of ',
            intents=intents,
            description='🎮 Bot officiel Oupafamilly - Communauté Gaming Élite'
        )
        
        # Configuration
        self.api_base = os.getenv('OUPAFAMILLY_API_URL', 'http://localhost:8001/api')
        self.website_url = os.getenv('OUPAFAMILLY_WEB_URL', 'http://localhost:3000')
        
        # Cache pour les données
        self.cache = {}
        self.cache_ttl = {}
        
        # Couleurs du thème
        self.colors = {
            'primary': 0x3B82F6,
            'success': 0x10B981,
            'warning': 0xF59E0B,
            'error': 0xEF4444,
            'info': 0x8B5CF6
        }
        
    async def setup_hook(self):
        """Initialisation du bot"""
        logger.info("🚀 Initialisation du bot Oupafamilly...")
        
        # Démarrer les tâches périodiques
        self.update_cache.start()
        self.send_daily_stats.start()
        
        logger.info("✅ Bot Oupafamilly prêt !")
    
    async def on_ready(self):
        """Événement quand le bot est connecté"""
        logger.info(f'🤖 {self.user} connecté à Discord!')
        logger.info(f'📊 Serveurs: {len(self.guilds)}')
        
        # Statut du bot
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="la communauté Oupafamilly 🎮"
        )
        await self.change_presence(activity=activity)
    
    async def api_request(self, endpoint: str, method: str = 'GET', data: dict = None) -> Optional[Dict[Any, Any]]:
        """Requête vers l'API Oupafamilly"""
        url = f"{self.api_base}/{endpoint.lstrip('/')}"
        
        try:
            async with aiohttp.ClientSession() as session:
                if method == 'GET':
                    async with session.get(url) as response:
                        if response.status == 200:
                            return await response.json()
                elif method == 'POST':
                    async with session.post(url, json=data) as response:
                        if response.status == 200:
                            return await response.json()
                        
        except Exception as e:
            logger.error(f"❌ Erreur API {endpoint}: {e}")
            
        return None
    
    def get_cached_data(self, key: str) -> Optional[Dict[Any, Any]]:
        """Récupère des données du cache si valides"""
        if key in self.cache and key in self.cache_ttl:
            if datetime.now() < self.cache_ttl[key]:
                return self.cache[key]
        return None
    
    def set_cached_data(self, key: str, data: Dict[Any, Any], ttl_minutes: int = 5):
        """Met en cache des données"""
        self.cache[key] = data
        self.cache_ttl[key] = datetime.now() + timedelta(minutes=ttl_minutes)
    
    @tasks.loop(minutes=5)
    async def update_cache(self):
        """Met à jour le cache périodiquement"""
        try:
            # Cache des leaderboards
            leaderboard = await self.api_request('elo/leaderboard')
            if leaderboard:
                self.set_cached_data('leaderboard', leaderboard, 5)
            
            # Cache des tournois
            tournaments = await self.api_request('tournaments/current')
            if tournaments:
                self.set_cached_data('tournaments', tournaments, 2)
                
        except Exception as e:
            logger.error(f"❌ Erreur mise à jour cache: {e}")
    
    @tasks.loop(hours=24)
    async def send_daily_stats(self):
        """Envoie les statistiques quotidiennes"""
        try:
            # Récupérer les stats du jour
            stats = await self.api_request('admin/daily-stats')
            if not stats:
                return
            
            # Trouver le canal d'annonces
            for guild in self.guilds:
                channel = discord.utils.get(guild.channels, name='annonces-oupafamilly')
                if channel:
                    embed = self.create_daily_stats_embed(stats)
                    await channel.send(embed=embed)
                    
        except Exception as e:
            logger.error(f"❌ Erreur stats quotidiennes: {e}")
    
    def create_daily_stats_embed(self, stats: dict) -> discord.Embed:
        """Crée l'embed des statistiques quotidiennes"""
        embed = discord.Embed(
            title="📊 Statistiques Quotidiennes Oupafamilly",
            description="Résumé de l'activité de la communauté",
            color=self.colors['primary'],
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="🎮 Joueurs Actifs",
            value=f"**{stats.get('active_players', 0)}** joueurs",
            inline=True
        )
        
        embed.add_field(
            name="🏆 Badges Obtenus",
            value=f"**{stats.get('badges_earned', 0)}** nouveaux badges",
            inline=True
        )
        
        embed.add_field(
            name="⚡ Tournois",
            value=f"**{stats.get('tournaments_completed', 0)}** terminés",
            inline=True
        )
        
        embed.set_footer(text="Oupafamilly Elite Gaming", icon_url=self.user.avatar.url if self.user.avatar else None)
        
        return embed

# ==============================================
# COMMANDES DU BOT
# ==============================================

@commands.command(name='stats')
async def user_stats(ctx, user_mention: str = None):
    """Affiche les statistiques d'un joueur"""
    bot = ctx.bot
    
    # Déterminer l'utilisateur
    if user_mention:
        # Extraire l'ID Discord de la mention
        user_id = user_mention.strip('<@!>')
        # Dans une vraie implémentation, il faudrait mapper Discord ID -> User ID Oupafamilly
        username = f"User_{user_id[-4:]}"  # Placeholder
    else:
        username = f"User_{ctx.author.id}"
    
    # Récupérer les stats depuis l'API
    user_data = await bot.api_request(f'users/{username}/profile')
    if not user_data:
        embed = discord.Embed(
            title="❌ Utilisateur introuvable",
            description="Cet utilisateur n'est pas enregistré sur Oupafamilly.",
            color=bot.colors['error']
        )
        await ctx.send(embed=embed)
        return
    
    # Créer l'embed des stats
    embed = discord.Embed(
        title=f"📊 Profil de {user_data.get('username', username)}",
        description="Statistiques Oupafamilly",
        color=bot.colors['primary']
    )
    
    embed.add_field(
        name="🏆 Niveau",
        value=f"**{user_data.get('level', 1)}**",
        inline=True
    )
    
    embed.add_field(
        name="🎯 ELO",
        value=f"**{user_data.get('elo', 1200)}** points",
        inline=True
    )
    
    embed.add_field(
        name="💰 Coins",
        value=f"**{user_data.get('coins', 0)}** coins",
        inline=True
    )
    
    embed.add_field(
        name="🏅 Badges",
        value=f"**{user_data.get('badges_count', 0)}** obtenus",
        inline=True
    )
    
    embed.add_field(
        name="🎮 Tournois",
        value=f"**{user_data.get('tournaments_won', 0)}** victoires",
        inline=True
    )
    
    embed.add_field(
        name="📈 Progression",
        value=f"**{user_data.get('xp', 0)}** XP",
        inline=True
    )
    
    embed.set_footer(text=f"Rejoignez nous sur {bot.website_url}")
    
    await ctx.send(embed=embed)

@commands.command(name='leaderboard', aliases=['top', 'classement'])
async def leaderboard(ctx, limit: int = 10):
    """Affiche le classement ELO"""
    bot = ctx.bot
    
    if limit > 20:
        limit = 20
    
    # Récupérer le leaderboard (cache ou API)
    leaderboard_data = bot.get_cached_data('leaderboard')
    if not leaderboard_data:
        leaderboard_data = await bot.api_request('elo/leaderboard')
        if leaderboard_data:
            bot.set_cached_data('leaderboard', leaderboard_data)
    
    if not leaderboard_data or not leaderboard_data.get('players'):
        embed = discord.Embed(
            title="❌ Données indisponibles",
            description="Impossible de récupérer le classement.",
            color=bot.colors['error']
        )
        await ctx.send(embed=embed)
        return
    
    # Créer l'embed du classement
    embed = discord.Embed(
        title="🏆 Classement ELO Oupafamilly",
        description=f"Top {limit} joueurs",
        color=bot.colors['primary']
    )
    
    players = leaderboard_data['players'][:limit]
    
    # Émojis pour le podium
    medals = ['🥇', '🥈', '🥉']
    
    for i, player in enumerate(players):
        rank = i + 1
        medal = medals[i] if i < 3 else f"{rank}."
        
        username = player.get('username', f"Joueur_{rank}")
        elo = player.get('elo_rating', 0)
        tier = player.get('tier', 'Bronze')
        
        embed.add_field(
            name=f"{medal} {username}",
            value=f"**{elo}** ELO ({tier})",
            inline=False
        )
    
    embed.set_footer(text="Rejoignez la compétition sur Oupafamilly !")
    
    await ctx.send(embed=embed)

@commands.command(name='tournaments', aliases=['tournois'])
async def tournaments(ctx):
    """Affiche les tournois en cours"""
    bot = ctx.bot
    
    # Récupérer les tournois
    tournaments_data = bot.get_cached_data('tournaments')
    if not tournaments_data:
        tournaments_data = await bot.api_request('tournaments/current')
        if tournaments_data:
            bot.set_cached_data('tournaments', tournaments_data)
    
    if not tournaments_data or not tournaments_data.get('tournaments'):
        embed = discord.Embed(
            title="📅 Aucun tournoi actif",
            description="Aucun tournoi n'est actuellement en cours.",
            color=bot.colors['info']
        )
        await ctx.send(embed=embed)
        return
    
    # Créer l'embed des tournois
    embed = discord.Embed(
        title="⚡ Tournois CS2 en Cours",
        description="Rejoignez la compétition !",
        color=bot.colors['success']
    )
    
    for tournament in tournaments_data['tournaments'][:5]:  # Limite à 5
        name = tournament.get('name', 'Tournoi Sans Nom')
        participants = tournament.get('participants_count', 0)
        max_participants = tournament.get('max_participants', 'Illimité')
        prize = tournament.get('prize_pool', '0 coins')
        status = tournament.get('status', 'En cours')
        
        status_emoji = {
            'registration': '📝',
            'in_progress': '⚡',
            'completed': '🏁'
        }.get(status, '❓')
        
        embed.add_field(
            name=f"{status_emoji} {name}",
            value=f"**Participants:** {participants}/{max_participants}\n**Prix:** {prize}\n**Statut:** {status}",
            inline=True
        )
    
    embed.add_field(
        name="🔗 S'inscrire",
        value=f"[Rejoindre un tournoi]({bot.website_url}/communaute)",
        inline=False
    )
    
    await ctx.send(embed=embed)

@commands.command(name='badges')
async def badges(ctx, user_mention: str = None):
    """Affiche les badges d'un joueur"""
    bot = ctx.bot
    
    # Déterminer l'utilisateur
    if user_mention:
        user_id = user_mention.strip('<@!>')
        username = f"User_{user_id[-4:]}"
    else:
        username = f"User_{ctx.author.id}"
    
    # Récupérer les badges
    badges_data = await bot.api_request(f'achievements/user/{username}/badges')
    if not badges_data or not badges_data.get('badges'):
        embed = discord.Embed(
            title="🏅 Aucun badge",
            description="Cet utilisateur n'a pas encore obtenu de badges.",
            color=bot.colors['info']
        )
        await ctx.send(embed=embed)
        return
    
    # Créer l'embed des badges
    embed = discord.Embed(
        title=f"🏅 Badges de {username}",
        description=f"**{len(badges_data['badges'])}** badges obtenus",
        color=bot.colors['success']
    )
    
    # Grouper par rareté
    rarity_groups = {}
    for badge in badges_data['badges']:
        rarity = badge.get('rarity', 'common')
        if rarity not in rarity_groups:
            rarity_groups[rarity] = []
        rarity_groups[rarity].append(badge)
    
    # Émojis par rareté
    rarity_emojis = {
        'common': '⚪',
        'rare': '🔵',
        'epic': '🟣',
        'legendary': '🟡',
        'mythic': '🔴'
    }
    
    for rarity, badges in rarity_groups.items():
        emoji = rarity_emojis.get(rarity, '⚪')
        badge_names = [badge.get('name', 'Badge') for badge in badges[:5]]  # Limite à 5
        
        embed.add_field(
            name=f"{emoji} {rarity.title()} ({len(badges)})",
            value="\n".join([f"• {name}" for name in badge_names]),
            inline=True
        )
    
    await ctx.send(embed=embed)

@commands.command(name='help', aliases=['aide'])
async def help_command(ctx):
    """Affiche l'aide du bot"""
    bot = ctx.bot
    
    embed = discord.Embed(
        title="🤖 Oupafamilly Bot - Aide",
        description="Commandes disponibles pour la communauté gaming",
        color=bot.colors['primary']
    )
    
    commands_list = [
        ("!of stats [@user]", "📊 Affiche les statistiques d'un joueur"),
        ("!of leaderboard [limit]", "🏆 Classement ELO (max 20)"),
        ("!of tournaments", "⚡ Tournois CS2 en cours"),
        ("!of badges [@user]", "🏅 Badges obtenus par un joueur"),
        ("!of help", "❓ Affiche cette aide")
    ]
    
    for command, description in commands_list:
        embed.add_field(
            name=command,
            value=description,
            inline=False
        )
    
    embed.add_field(
        name="🔗 Liens Utiles",
        value=f"• [Site Web]({bot.website_url})\n• [Communauté]({bot.website_url}/communaute)\n• [Tournois]({bot.website_url}/communaute?tab=tournaments)",
        inline=False
    )
    
    embed.set_footer(text="Oupafamilly Elite Gaming Community")
    
    await ctx.send(embed=embed)

# Ajouter les commandes au bot
def setup_commands(bot):
    """Configure les commandes du bot"""
    bot.add_command(user_stats)
    bot.add_command(leaderboard) 
    bot.add_command(tournaments)
    bot.add_command(badges)
    bot.add_command(help_command)

# ==============================================
# POINT D'ENTRÉE
# ==============================================

async def main():
    """Point d'entrée principal"""
    # Token Discord (à définir dans .env)
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error("❌ DISCORD_BOT_TOKEN non défini !")
        return
    
    # Créer et configurer le bot
    bot = OupafamillyBot()
    setup_commands(bot)
    
    try:
        logger.info("🚀 Démarrage du bot Discord...")
        await bot.start(token)
    except discord.LoginFailure:
        logger.error("❌ Token Discord invalide !")
    except Exception as e:
        logger.error(f"❌ Erreur démarrage bot: {e}")
    finally:
        await bot.close()

if __name__ == '__main__':
    asyncio.run(main())