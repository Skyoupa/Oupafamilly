"""
🎮 STEAM API INTEGRATION - SYSTÈME ÉLITE
Intégration complète avec l'API Steam pour CS2
"""

import requests
import json
import asyncio
import aiohttp
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
import os
from monitoring import app_logger
from database import db

class SteamAPIManager:
    """Gestionnaire de l'API Steam pour Oupafamilly"""
    
    def __init__(self):
        self.api_key = os.getenv('STEAM_API_KEY', '')
        self.base_url = 'https://api.steampowered.com'
        
        # Game IDs
        self.cs2_app_id = 730  # Counter-Strike 2
        self.cache = {}
        self.cache_ttl = {}
        
        app_logger.info("🎮 Steam API Manager initialisé")
    
    def _get_cache_key(self, endpoint: str, **params) -> str:
        """Génère une clé de cache"""
        params_str = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
        return f"{endpoint}?{params_str}"
    
    def _is_cache_valid(self, key: str) -> bool:
        """Vérifie si le cache est valide"""
        return key in self.cache and key in self.cache_ttl and datetime.now() < self.cache_ttl[key]
    
    def _set_cache(self, key: str, data: Any, ttl_minutes: int = 15):
        """Met en cache des données"""
        self.cache[key] = data
        self.cache_ttl[key] = datetime.now() + timedelta(minutes=ttl_minutes)
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict]:
        """Effectue une requête vers l'API Steam"""
        if not self.api_key:
            app_logger.warning("⚠️ Steam API Key non configurée")
            return None
        
        url = f"{self.base_url}/{endpoint}"
        params['key'] = self.api_key
        
        # Vérifier le cache
        cache_key = self._get_cache_key(endpoint, **params)
        if self._is_cache_valid(cache_key):
            app_logger.info(f"📦 Steam cache hit: {endpoint}")
            return self.cache[cache_key]
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        self._set_cache(cache_key, data)
                        app_logger.info(f"✅ Steam API success: {endpoint}")
                        return data
                    else:
                        app_logger.error(f"❌ Steam API error {response.status}: {endpoint}")
                        
        except Exception as e:
            app_logger.error(f"❌ Steam API exception: {e}")
        
        return None
    
    async def get_player_summaries(self, steam_ids: List[str]) -> Optional[Dict]:
        """Récupère les informations de base des joueurs"""
        steam_ids_str = ','.join(steam_ids)
        
        return await self._make_request(
            'ISteamUser/GetPlayerSummaries/v0002/',
            {'steamids': steam_ids_str}
        )
    
    async def get_player_stats(self, steam_id: str) -> Optional[Dict]:
        """Récupère les statistiques CS2 d'un joueur"""
        return await self._make_request(
            'ISteamUserStats/GetUserStatsForGame/v0002/',
            {'steamid': steam_id, 'appid': self.cs2_app_id}
        )
    
    async def get_player_achievements(self, steam_id: str) -> Optional[Dict]:
        """Récupère les achievements CS2 d'un joueur"""
        return await self._make_request(
            'ISteamUserStats/GetPlayerAchievements/v0001/',
            {'steamid': steam_id, 'appid': self.cs2_app_id}
        )
    
    async def get_recent_games(self, steam_id: str) -> Optional[Dict]:
        """Récupère les jeux récents d'un joueur"""
        return await self._make_request(
            'IPlayerService/GetRecentlyPlayedGames/v0001/',
            {'steamid': steam_id}
        )
    
    async def get_player_bans(self, steam_ids: List[str]) -> Optional[Dict]:
        """Vérifie les bans VAC/Game des joueurs"""
        steam_ids_str = ','.join(steam_ids)
        
        return await self._make_request(
            'ISteamUser/GetPlayerBans/v1/',
            {'steamids': steam_ids_str}
        )
    
    async def get_cs2_match_history(self, steam_id: str) -> Optional[Dict]:
        """Récupère l'historique des matchs CS2 (simulé car pas d'API officielle)"""
        # Dans une vraie implémentation, on utiliserait une API communautaire
        # ou on scraperait les données depuis Steam
        
        app_logger.info(f"🎯 Simulation historique matchs CS2 pour {steam_id}")
        
        # Données simulées pour la démo
        return {
            "matches": [
                {
                    "match_id": "123456789",
                    "date": datetime.now().isoformat(),
                    "map": "de_dust2",
                    "score": "16-12",
                    "result": "win",
                    "kills": 24,
                    "deaths": 18,
                    "assists": 7,
                    "mvp": True,
                    "rank": "Gold Nova III"
                },
                {
                    "match_id": "123456788",
                    "date": (datetime.now() - timedelta(days=1)).isoformat(),
                    "map": "de_mirage",
                    "score": "13-16",
                    "result": "loss",
                    "kills": 19,
                    "deaths": 21,
                    "assists": 5,
                    "mvp": False,
                    "rank": "Gold Nova III"
                }
            ]
        }

class SteamProfileVerifier:
    """Vérificateur de profils Steam pour Oupafamilly"""
    
    def __init__(self):
        self.steam_api = SteamAPIManager()
    
    async def verify_steam_profile(self, steam_id: str, user_id: str) -> Dict[str, Any]:
        """Vérifie et enrichit un profil Steam"""
        verification_result = {
            "verified": False,
            "verification_level": "none",
            "profile_data": {},
            "cs2_stats": {},
            "security_status": "unknown",
            "badges": [],
            "warnings": []
        }
        
        try:
            # 1. Vérifier l'existence du profil
            profile_data = await self.steam_api.get_player_summaries([steam_id])
            if not profile_data or not profile_data.get('response', {}).get('players'):
                verification_result["warnings"].append("❌ Profil Steam introuvable")
                return verification_result
            
            player = profile_data['response']['players'][0]
            verification_result["profile_data"] = player
            verification_result["verified"] = True
            
            # 2. Vérifier les bans VAC/Game
            bans_data = await self.steam_api.get_player_bans([steam_id])
            if bans_data and bans_data.get('players'):
                ban_info = bans_data['players'][0]
                
                if ban_info.get('VACBanned') or ban_info.get('NumberOfGameBans', 0) > 0:
                    verification_result["security_status"] = "banned"
                    verification_result["warnings"].append("⚠️ Bans détectés sur le compte")
                    verification_result["verification_level"] = "restricted"
                else:
                    verification_result["security_status"] = "clean"
                    verification_result["verification_level"] = "verified"
            
            # 3. Récupérer les stats CS2
            cs2_stats = await self.steam_api.get_player_stats(steam_id)
            if cs2_stats and cs2_stats.get('playerstats', {}).get('stats'):
                stats = cs2_stats['playerstats']['stats']
                
                # Parser les stats importantes
                parsed_stats = self._parse_cs2_stats(stats)
                verification_result["cs2_stats"] = parsed_stats
                
                # Validation niveau de jeu
                if parsed_stats.get('total_kills', 0) > 1000:
                    verification_result["verification_level"] = "experienced"
                    verification_result["badges"].append("🎯 Joueur Expérimenté")
                
                if parsed_stats.get('total_wins', 0) > 100:
                    verification_result["badges"].append("🏆 Vétéran CS2")
            
            # 4. Vérifier les achievements
            achievements = await self.steam_api.get_player_achievements(steam_id)
            if achievements and achievements.get('playerstats', {}).get('achievements'):
                achievement_count = len([a for a in achievements['playerstats']['achievements'] if a.get('achieved')])
                
                if achievement_count > 50:
                    verification_result["badges"].append("🏅 Collectionneur d'Achievements")
                
                verification_result["profile_data"]["cs2_achievements"] = achievement_count
            
            # 5. Sauvegarder dans la base de données
            await self._save_steam_verification(user_id, steam_id, verification_result)
            
            app_logger.info(f"✅ Profil Steam vérifié: {steam_id} -> {verification_result['verification_level']}")
            
        except Exception as e:
            app_logger.error(f"❌ Erreur vérification Steam: {e}")
            verification_result["warnings"].append(f"Erreur technique: {str(e)}")
        
        return verification_result
    
    def _parse_cs2_stats(self, stats: List[Dict]) -> Dict[str, Any]:
        """Parse les statistiques CS2 brutes"""
        parsed = {}
        
        stat_mapping = {
            'total_kills': 'total_kills',
            'total_deaths': 'total_deaths', 
            'total_wins': 'total_wins',
            'total_rounds_played': 'total_rounds_played',
            'total_time_played': 'total_time_played',
            'total_headshot_kills': 'total_headshot_kills',
            'total_shots_fired': 'total_shots_fired',
            'total_shots_hit': 'total_shots_hit'
        }
        
        for stat in stats:
            name = stat.get('name', '')
            value = stat.get('value', 0)
            
            if name in stat_mapping:
                parsed[stat_mapping[name]] = value
        
        # Calculs dérivés
        if parsed.get('total_kills') and parsed.get('total_deaths'):
            parsed['kd_ratio'] = round(parsed['total_kills'] / parsed['total_deaths'], 2)
        
        if parsed.get('total_headshot_kills') and parsed.get('total_kills'):
            parsed['headshot_percentage'] = round((parsed['total_headshot_kills'] / parsed['total_kills']) * 100, 2)
        
        if parsed.get('total_shots_hit') and parsed.get('total_shots_fired'):
            parsed['accuracy'] = round((parsed['total_shots_hit'] / parsed['total_shots_fired']) * 100, 2)
        
        return parsed
    
    async def _save_steam_verification(self, user_id: str, steam_id: str, verification_data: Dict):
        """Sauvegarde les données de vérification Steam"""
        try:
            steam_profile = {
                "user_id": user_id,
                "steam_id": steam_id,
                "verification_data": verification_data,
                "verified_at": datetime.utcnow(),
                "last_updated": datetime.utcnow()
            }
            
            # Upsert dans la collection steam_profiles
            await db.steam_profiles.update_one(
                {"user_id": user_id},
                {"$set": steam_profile},
                upsert=True
            )
            
            # Mettre à jour le profil utilisateur avec le badge Steam
            if verification_data["verified"]:
                await db.users.update_one(
                    {"id": user_id},
                    {"$set": {
                        "steam_verified": True,
                        "steam_id": steam_id,
                        "steam_verification_level": verification_data["verification_level"]
                    }}
                )
            
        except Exception as e:
            app_logger.error(f"❌ Erreur sauvegarde Steam: {e}")

class SteamStatsUpdater:
    """Mise à jour automatique des stats Steam"""
    
    def __init__(self):
        self.steam_api = SteamAPIManager()
        self.verifier = SteamProfileVerifier()
    
    async def update_all_steam_profiles(self):
        """Met à jour tous les profils Steam enregistrés"""
        app_logger.info("🔄 Mise à jour globale profils Steam...")
        
        try:
            # Récupérer tous les utilisateurs avec Steam ID
            steam_users = await db.users.find({"steam_verified": True}).to_list(None)
            
            updated_count = 0
            for user in steam_users:
                try:
                    steam_id = user.get('steam_id')
                    if steam_id:
                        await self.verifier.verify_steam_profile(steam_id, user['id'])
                        updated_count += 1
                        
                        # Pause pour éviter la limite de rate
                        await asyncio.sleep(1)
                        
                except Exception as e:
                    app_logger.error(f"❌ Erreur mise à jour Steam user {user['id']}: {e}")
            
            app_logger.info(f"✅ Mise à jour Steam terminée: {updated_count} profils")
            
        except Exception as e:
            app_logger.error(f"❌ Erreur mise à jour globale Steam: {e}")
    
    async def get_steam_leaderboard(self, stat_name: str = 'total_kills', limit: int = 20) -> List[Dict]:
        """Génère un leaderboard basé sur les stats Steam"""
        try:
            pipeline = [
                {"$match": {"verification_data.verified": True}},
                {"$project": {
                    "user_id": 1,
                    "steam_id": 1,
                    "username": {"$arrayElemAt": [{"$split": ["$verification_data.profile_data.personaname", " "]}, 0]},
                    "stat_value": f"$verification_data.cs2_stats.{stat_name}",
                    "verification_level": "$verification_data.verification_level"
                }},
                {"$match": {"stat_value": {"$exists": True, "$gt": 0}}},
                {"$sort": {"stat_value": -1}},
                {"$limit": limit}
            ]
            
            results = await db.steam_profiles.aggregate(pipeline).to_list(None) 
            
            app_logger.info(f"📊 Steam leaderboard généré: {len(results)} entrées pour {stat_name}")
            return results
            
        except Exception as e:
            app_logger.error(f"❌ Erreur leaderboard Steam: {e}")
            return []

# Instances globales
steam_api_manager = SteamAPIManager()
steam_profile_verifier = SteamProfileVerifier()
steam_stats_updater = SteamStatsUpdater()

# Fonctions utilitaires
async def verify_user_steam_profile(user_id: str, steam_id: str) -> Dict[str, Any]:
    """Point d'entrée pour vérifier un profil Steam"""
    return await steam_profile_verifier.verify_steam_profile(steam_id, user_id)

async def get_user_steam_stats(user_id: str) -> Optional[Dict]:
    """Récupère les stats Steam d'un utilisateur"""
    try:
        steam_profile = await db.steam_profiles.find_one({"user_id": user_id})
        if steam_profile and steam_profile.get('verification_data'):
            return steam_profile['verification_data']
        return None
    except Exception as e:
        app_logger.error(f"❌ Erreur récupération stats Steam: {e}")
        return None

async def update_steam_profiles_task():
    """Tâche périodique de mise à jour des profils Steam"""
    await steam_stats_updater.update_all_steam_profiles()

app_logger.info("🎮 Steam API Integration chargée !")