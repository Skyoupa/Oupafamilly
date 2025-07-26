"""
🎮 ROUTES STEAM API - INTÉGRATION ÉLITE
Endpoints pour l'intégration Steam dans Oupafamilly
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from auth import get_current_user
from steam_integration import (
    verify_user_steam_profile,
    get_user_steam_stats,
    steam_stats_updater,
    steam_api_manager
)
from monitoring import app_logger, log_user_action
from database import db
import re

router = APIRouter(prefix="/steam", tags=["Steam Integration"])

# ===============================================
# MODÈLES PYDANTIC
# ===============================================

class SteamProfileRequest(BaseModel):
    steam_id: str
    
class SteamLeaderboardRequest(BaseModel):
    stat_name: str = "total_kills"
    limit: int = 20

# ===============================================
# ENDPOINTS STEAM
# ===============================================

@router.post("/verify-profile")
async def verify_steam_profile(
    request: SteamProfileRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """🔍 Vérifie et lie un profil Steam à un utilisateur"""
    try:
        steam_id = request.steam_id.strip()
        
        # Validation du Steam ID
        if not _is_valid_steam_id(steam_id):
            raise HTTPException(
                status_code=400,
                detail="Steam ID invalide. Utilisez un Steam ID 64-bit."
            )
        
        # Vérifier si le Steam ID n'est pas déjà utilisé
        existing_profile = await db.steam_profiles.find_one({"steam_id": steam_id})
        if existing_profile and existing_profile.get('user_id') != current_user['id']:
            raise HTTPException(
                status_code=409,
                detail="Ce Steam ID est déjà lié à un autre compte."
            )
        
        # Lancer la vérification en arrière-plan
        background_tasks.add_task(
            _background_steam_verification,
            current_user['id'],
            steam_id
        )
        
        # Log de l'action
        log_user_action(current_user['id'], "steam_verification_requested", {
            "steam_id": steam_id,
            "timestamp": str(db.get_current_time())
        })
        
        app_logger.info(f"🎮 Vérification Steam lancée: {steam_id} pour user {current_user['id']}")
        
        return {
            "message": "Vérification Steam lancée avec succès",
            "steam_id": steam_id,
            "status": "processing",
            "estimated_time": "30-60 secondes"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"❌ Erreur vérification Steam: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la vérification Steam")

@router.get("/my-profile")
async def get_my_steam_profile(current_user: dict = Depends(get_current_user)):
    """📊 Récupère le profil Steam de l'utilisateur connecté"""
    try:
        steam_stats = await get_user_steam_stats(current_user['id'])
        
        if not steam_stats:
            return {
                "verified": False,
                "message": "Aucun profil Steam lié à ce compte"
            }
        
        # Enrichir avec des données utilisateur
        user_data = await db.users.find_one({"id": current_user['id']})
        
        return {
            "verified": True,
            "steam_data": steam_stats,
            "user_info": {
                "username": user_data.get('username'),
                "steam_verified": user_data.get('steam_verified', False),
                "verification_level": user_data.get('steam_verification_level', 'none')
            },
            "last_updated": steam_stats.get('verified_at')
        }
        
    except Exception as e:
        app_logger.error(f"❌ Erreur récupération profil Steam: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération du profil")

@router.get("/profile/{user_id}")
async def get_user_steam_profile(user_id: str):
    """👤 Récupère le profil Steam public d'un utilisateur"""
    try:
        steam_stats = await get_user_steam_stats(user_id)
        
        if not steam_stats or not steam_stats.get('verified'):
            raise HTTPException(
                status_code=404,
                detail="Profil Steam non trouvé ou non vérifié"
            )
        
        # Données publiques uniquement
        public_data = {
            "verified": steam_stats['verified'],
            "verification_level": steam_stats['verification_level'],
            "profile_summary": {
                "personaname": steam_stats['profile_data'].get('personaname', 'Joueur Anonyme'),
                "avatar": steam_stats['profile_data'].get('avatar', ''),
                "profileurl": steam_stats['profile_data'].get('profileurl', ''),
                "timecreated": steam_stats['profile_data'].get('timecreated')
            },
            "cs2_stats": {
                "total_kills": steam_stats['cs2_stats'].get('total_kills', 0),
                "total_wins": steam_stats['cs2_stats'].get('total_wins', 0),
                "kd_ratio": steam_stats['cs2_stats'].get('kd_ratio', 0),
                "headshot_percentage": steam_stats['cs2_stats'].get('headshot_percentage', 0),
                "accuracy": steam_stats['cs2_stats'].get('accuracy', 0)
            },
            "badges": steam_stats.get('badges', []),
            "security_status": steam_stats['security_status']
        }
        
        return public_data
        
    except HTTPException:
        raise  
    except Exception as e:
        app_logger.error(f"❌ Erreur récupération profil Steam public: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération du profil")

@router.get("/leaderboard")
async def get_steam_leaderboard(
    stat_name: str = "total_kills",
    limit: int = 20
):
    """🏆 Récupère le leaderboard basé sur les stats Steam"""
    try:
        if limit > 50:
            limit = 50
            
        # Stats autorisées
        allowed_stats = [
            'total_kills', 'total_wins', 'kd_ratio', 
            'headshot_percentage', 'accuracy', 'total_time_played'
        ]
        
        if stat_name not in allowed_stats:
            raise HTTPException(
                status_code=400,
                detail=f"Statistique non autorisée. Utilisez: {', '.join(allowed_stats)}"
            )
        
        leaderboard = await steam_stats_updater.get_steam_leaderboard(stat_name, limit)
        
        # Enrichir avec les données utilisateur
        enriched_leaderboard = []
        for entry in leaderboard:
            user_data = await db.users.find_one({"id": entry['user_id']})
            
            enriched_entry = {
                "rank": len(enriched_leaderboard) + 1,
                "username": user_data.get('username', 'Joueur Anonyme') if user_data else 'Joueur Anonyme',
                "steam_name": entry.get('username', 'Inconnu'),
                "stat_value": entry.get('stat_value', 0),
                "verification_level": entry.get('verification_level', 'none'),
                "steam_id": entry.get('steam_id', '')[:8] + "..." if entry.get('steam_id') else '',  # Partiel pour la sécurité
            }
            enriched_leaderboard.append(enriched_entry)
        
        return {
            "stat_name": stat_name,
            "total_players": len(enriched_leaderboard),
            "leaderboard": enriched_leaderboard,
            "last_updated": str(db.get_current_time())
        }
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"❌ Erreur leaderboard Steam: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération du leaderboard")

@router.post("/refresh-stats")
async def refresh_steam_stats(
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """🔄 Force la mise à jour des stats Steam de l'utilisateur"""
    try:
        # Vérifier si l'utilisateur a un profil Steam lié
        user_data = await db.users.find_one({"id": current_user['id']})
        if not user_data or not user_data.get('steam_verified'):
            raise HTTPException(
                status_code=400,
                detail="Aucun profil Steam lié. Veuillez d'abord vérifier votre profil."
            )
        
        steam_id = user_data.get('steam_id')
        if not steam_id:
            raise HTTPException(
                status_code=400,
                detail="Steam ID manquant dans le profil utilisateur."
            )
        
        # Lancer la mise à jour en arrière-plan
        background_tasks.add_task(
            _background_steam_verification,
            current_user['id'],
            steam_id
        )
        
        # Log de l'action
        log_user_action(current_user['id'], "steam_stats_refresh", {
            "steam_id": steam_id,
            "timestamp": str(db.get_current_time())
        })
        
        return {
            "message": "Mise à jour des stats Steam lancée",
            "status": "processing",
            "estimated_time": "30 secondes"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"❌ Erreur refresh Steam: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la mise à jour")

@router.get("/match-history/{user_id}")
async def get_steam_match_history(user_id: str):
    """📈 Récupère l'historique des matchs CS2 (simulé)"""
    try:
        # Vérifier que l'utilisateur a un profil Steam
        user_data = await db.users.find_one({"id": user_id})
        if not user_data or not user_data.get('steam_verified'):
            raise HTTPException(
                status_code=404,
                detail="Utilisateur sans profil Steam vérifié"
            )
        
        steam_id = user_data.get('steam_id')
        if not steam_id:
            raise HTTPException(
                status_code=400,
                detail="Steam ID manquant"
            )
        
        # Récupérer l'historique (simulé pour la démo)
        match_history = await steam_api_manager.get_cs2_match_history(steam_id)
        
        if not match_history:
            return {
                "user_id": user_id,
                "steam_id": steam_id[:8] + "...",
                "matches": [],
                "message": "Aucun historique de match disponible"
            }
        
        return {
            "user_id": user_id,
            "steam_id": steam_id[:8] + "...",
            "matches": match_history.get('matches', []),
            "total_matches": len(match_history.get('matches', [])),
            "last_updated": str(db.get_current_time())
        }
        
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"❌ Erreur historique matchs Steam: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération de l'historique")

@router.get("/stats/global")
async def get_global_steam_stats():
    """📊 Statistiques globales de l'intégration Steam"""
    try:
        # Compter les profils vérifiés par niveau
        pipeline = [
            {"$match": {"steam_verified": True}},
            {"$group": {
                "_id": "$steam_verification_level",
                "count": {"$sum": 1}
            }}
        ]
        
        verification_levels = await db.users.aggregate(pipeline).to_list(None)
        
        # Statistiques générales
        total_steam_users = await db.users.count_documents({"steam_verified": True})
        total_verified_profiles = await db.steam_profiles.count_documents({"verification_data.verified": True})
        
        # Top stats moyennes
        avg_stats = await db.steam_profiles.aggregate([
            {"$match": {"verification_data.verified": True}},
            {"$group": {
                "_id": None,
                "avg_kills": {"$avg": "$verification_data.cs2_stats.total_kills"},
                "avg_wins": {"$avg": "$verification_data.cs2_stats.total_wins"},
                "avg_kd": {"$avg": "$verification_data.cs2_stats.kd_ratio"},
                "avg_accuracy": {"$avg": "$verification_data.cs2_stats.accuracy"}
            }}
        ]).to_list(1)
        
        return {
            "total_steam_users": total_steam_users,
            "total_verified_profiles": total_verified_profiles,
            "verification_levels": {level['_id']: level['count'] for level in verification_levels},
            "average_stats": avg_stats[0] if avg_stats else {},
            "last_updated": str(db.get_current_time())
        }
        
    except Exception as e:
        app_logger.error(f"❌ Erreur stats globales Steam: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des statistiques")

# ===============================================
# FONCTIONS UTILITAIRES
# ===============================================

def _is_valid_steam_id(steam_id: str) -> bool:
    """Valide un Steam ID 64-bit"""
    try:
        # Steam ID 64-bit est un nombre de 17 chiffres commençant par 765611
        pattern = r'^765611\d{11}$'
        return bool(re.match(pattern, steam_id))
    except:
        return False

async def _background_steam_verification(user_id: str, steam_id: str):
    """Tâche de vérification Steam en arrière-plan"""
    try:
        app_logger.info(f"🔄 Démarrage vérification Steam background: {steam_id}")
        
        verification_result = await verify_user_steam_profile(user_id, steam_id)
        
        app_logger.info(f"✅ Vérification Steam terminée: {steam_id} -> {verification_result.get('verification_level', 'unknown')}")
        
        # Optionnel: Envoyer une notification à l'utilisateur
        # await send_notification(user_id, "steam_verification_complete", verification_result)
        
    except Exception as e:
        app_logger.error(f"❌ Erreur vérification Steam background: {e}")

app_logger.info("🎮 Routes Steam API chargées !")