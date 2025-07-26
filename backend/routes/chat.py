from fastapi import APIRouter, Depends, HTTPException, status, Query, WebSocket, WebSocketDisconnect
from typing import List, Optional, Dict
from models import (
    User, ChatMessage, ChatMessageCreate, PrivateMessage, PrivateMessageCreate
)
from auth import get_current_active_user, get_user_from_websocket_token
from datetime import datetime, timedelta
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat & Messaging"])

# Get database from database module
from database import db

# Gestionnaire de connexions WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}  # user_id -> websocket
        self.channel_connections: Dict[str, List[str]] = {}  # channel -> [user_ids]
    
    async def connect(self, websocket: WebSocket, user_id: str, channel: str = "general"):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        
        if channel not in self.channel_connections:
            self.channel_connections[channel] = []
        if user_id not in self.channel_connections[channel]:
            self.channel_connections[channel].append(user_id)
        
        logger.info(f"User {user_id} connected to chat channel {channel}")
    
    def disconnect(self, user_id: str, channel: str = "general"):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        
        if channel in self.channel_connections and user_id in self.channel_connections[channel]:
            self.channel_connections[channel].remove(user_id)
        
        logger.info(f"User {user_id} disconnected from chat channel {channel}")
    
    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(message)
            except:
                # Connection fermée, nettoyer
                if user_id in self.active_connections:
                    del self.active_connections[user_id]
    
    async def broadcast_to_channel(self, message: str, channel: str):
        if channel in self.channel_connections:
            disconnected_users = []
            for user_id in self.channel_connections[channel]:
                if user_id in self.active_connections:
                    try:
                        await self.active_connections[user_id].send_text(message)
                    except:
                        disconnected_users.append(user_id)
            
            # Nettoyer les connexions fermées
            for user_id in disconnected_users:
                self.disconnect(user_id, channel)

manager = ConnectionManager()

# Routes REST pour l'historique des messages

@router.get("/messages/{channel}", response_model=List[ChatMessage])
async def get_chat_messages(
    channel: str,
    current_user: User = Depends(get_current_active_user),
    limit: int = Query(50, le=100),
    skip: int = Query(0, ge=0)
):
    """Obtenir l'historique des messages d'un channel."""
    try:
        # Valider le channel
        allowed_channels = ["general", "cs2", "lol", "wow", "sc2", "minecraft", "random"]
        if channel not in allowed_channels:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Channel invalide. Channels autorisés: {allowed_channels}"
            )
        
        messages = await db.chat_messages.find({
            "channel": channel,
            "is_deleted": False
        }).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
        
        # Inverser pour avoir les plus anciens en premier
        messages.reverse()
        
        return [ChatMessage(**message) for message in messages]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des messages: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des messages"
        )

@router.post("/messages", response_model=ChatMessage)
async def send_chat_message(
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Envoyer un message dans un channel (REST endpoint de fallback)."""
    try:
        # Valider le channel
        allowed_channels = ["general", "cs2", "lol", "wow", "sc2", "minecraft", "random"]
        if message_data.channel not in allowed_channels:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Channel invalide. Channels autorisés: {allowed_channels}"
            )
        
        # Vérifier le rate limiting (max 10 messages par minute)
        one_minute_ago = datetime.utcnow() - timedelta(minutes=1)
        recent_messages = await db.chat_messages.count_documents({
            "author_id": current_user.id,
            "created_at": {"$gte": one_minute_ago}
        })
        
        if recent_messages >= 10:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Trop de messages envoyés. Limite: 10 messages par minute."
            )
        
        # Créer le message
        new_message = ChatMessage(
            **message_data.dict(),
            author_id=current_user.id,
            author_name=current_user.username
        )
        
        await db.chat_messages.insert_one(new_message.dict())
        
        # Diffuser le message via WebSocket
        message_json = json.dumps({
            "type": "chat_message",
            "data": {
                "id": new_message.id,
                "channel": new_message.channel,
                "author_id": new_message.author_id,
                "author_name": new_message.author_name,
                "content": new_message.content,
                "message_type": new_message.message_type,
                "created_at": new_message.created_at.isoformat(),
                "reply_to": new_message.reply_to
            }
        })
        
        await manager.broadcast_to_channel(message_json, message_data.channel)
        
        # Récompenser l'activité (1 coin + 1 XP pour un message)
        await reward_user_for_chat_activity(current_user.id, current_user.username)
        
        logger.info(f"Message envoyé par {current_user.username} dans {message_data.channel}")
        
        return new_message
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de l'envoi du message"
        )

@router.delete("/messages/{message_id}")
async def delete_chat_message(
    message_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Supprimer un message de chat."""
    try:
        # Récupérer le message
        message_data = await db.chat_messages.find_one({"id": message_id})
        if not message_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message non trouvé"
            )
        
        # Vérifier les permissions (auteur ou admin)
        from auth import is_admin, is_moderator_or_admin
        if message_data["author_id"] != current_user.id and not is_moderator_or_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous ne pouvez supprimer que vos propres messages"
            )
        
        # Marquer comme supprimé (soft delete)
        await db.chat_messages.update_one(
            {"id": message_id},
            {
                "$set": {
                    "is_deleted": True,
                    "content": "[Message supprimé]",
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        # Notifier la suppression via WebSocket
        deletion_json = json.dumps({
            "type": "message_deleted",
            "data": {
                "message_id": message_id,
                "channel": message_data["channel"]
            }
        })
        
        await manager.broadcast_to_channel(deletion_json, message_data["channel"])
        
        logger.info(f"Message {message_id} supprimé par {current_user.username}")
        
        return {"message": "Message supprimé avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la suppression du message"
        )

# Messages privés

@router.get("/private", response_model=List[PrivateMessage])
async def get_private_messages(
    current_user: User = Depends(get_current_active_user),
    with_user_id: Optional[str] = None,
    limit: int = Query(50, le=100),
    skip: int = Query(0, ge=0)
):
    """Obtenir les messages privés de l'utilisateur."""
    try:
        filter_dict = {
            "$or": [
                {"sender_id": current_user.id},
                {"recipient_id": current_user.id}
            ]
        }
        
        if with_user_id:
            filter_dict = {
                "$or": [
                    {"sender_id": current_user.id, "recipient_id": with_user_id},
                    {"sender_id": with_user_id, "recipient_id": current_user.id}
                ]
            }
        
        messages = await db.private_messages.find(filter_dict).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
        
        # Marquer comme lu les messages reçus
        await db.private_messages.update_many(
            {"recipient_id": current_user.id, "is_read": False},
            {"$set": {"is_read": True}}
        )
        
        # Inverser pour avoir les plus anciens en premier
        messages.reverse()
        
        return [PrivateMessage(**message) for message in messages]
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des messages privés: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des messages privés"
        )

@router.post("/private", response_model=PrivateMessage)
async def send_private_message(
    message_data: PrivateMessageCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Envoyer un message privé."""
    try:
        # Vérifier que le destinataire existe
        recipient = await db.users.find_one({"id": message_data.recipient_id})
        if not recipient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Destinataire non trouvé"
            )
        
        # Empêcher l'auto-message
        if message_data.recipient_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vous ne pouvez pas vous envoyer un message à vous-même"
            )
        
        # Créer le message privé
        new_message = PrivateMessage(
            **message_data.dict(),
            sender_id=current_user.id
        )
        
        await db.private_messages.insert_one(new_message.dict())
        
        # Envoyer notification WebSocket au destinataire
        notification_json = json.dumps({
            "type": "private_message",
            "data": {
                "id": new_message.id,
                "sender_id": current_user.id,
                "sender_name": current_user.username,
                "content": new_message.content,
                "created_at": new_message.created_at.isoformat()
            }
        })
        
        await manager.send_personal_message(notification_json, message_data.recipient_id)
        
        logger.info(f"Message privé envoyé par {current_user.username} à {recipient['username']}")
        
        return new_message
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du message privé: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de l'envoi du message privé"
        )

@router.get("/private/unread-count")
async def get_unread_count(current_user: User = Depends(get_current_active_user)):
    """Obtenir le nombre de messages privés non lus."""
    try:
        unread_count = await db.private_messages.count_documents({
            "recipient_id": current_user.id,
            "is_read": False
        })
        
        return {"unread_count": unread_count}
        
    except Exception as e:
        logger.error(f"Erreur lors du comptage des messages non lus: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors du comptage des messages non lus"
        )

# Statistiques du chat

@router.get("/stats")
async def get_chat_stats():
    """Obtenir les statistiques générales du chat."""
    try:
        # Messages par channel dans les dernières 24h
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        stats = {}
        channels = ["general", "cs2", "lol", "wow", "sc2", "minecraft", "random"]
        
        total_messages_24h = 0
        
        for channel in channels:
            count = await db.chat_messages.count_documents({
                "channel": channel,
                "created_at": {"$gte": yesterday},
                "is_deleted": False
            })
            stats[f"{channel}_messages_24h"] = count
            total_messages_24h += count
        
        # Utilisateurs actifs dans le chat (dernières 24h)
        active_users = await db.chat_messages.distinct("author_id", {
            "created_at": {"$gte": yesterday},
            "is_deleted": False
        })
        
        # Messages privés dans les dernières 24h
        private_messages_24h = await db.private_messages.count_documents({
            "created_at": {"$gte": yesterday}
        })
        
        # Utilisateurs actuellement connectés
        online_users = len(manager.active_connections)
        
        return {
            "total_messages_24h": total_messages_24h,
            "private_messages_24h": private_messages_24h,
            "active_users_24h": len(active_users),
            "online_users": online_users,
            "channels": stats,
            "connections_by_channel": {
                channel: len(users) for channel, users in manager.channel_connections.items()
            }
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des stats de chat: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des statistiques"
        )

# WebSocket pour le chat en temps réel

@router.websocket("/ws/{channel}")
async def websocket_chat_endpoint(websocket: WebSocket, channel: str, token: str = Query(...)):
    """WebSocket endpoint pour le chat en temps réel."""
    
    # Authentifier l'utilisateur via le token
    user = await get_user_from_websocket_token(token)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    # Valider le channel
    allowed_channels = ["general", "cs2", "lol", "wow", "sc2", "minecraft", "random"]
    if channel not in allowed_channels:
        await websocket.close(code=status.WS_1003_UNSUPPORTED_DATA)
        return
    
    await manager.connect(websocket, user.id, channel)
    
    # Envoyer un message de bienvenue
    welcome_message = json.dumps({
        "type": "system",
        "data": {
            "message": f"Bienvenue dans le channel #{channel}, {user.username} !",
            "timestamp": datetime.utcnow().isoformat()
        }
    })
    await manager.send_personal_message(welcome_message, user.id)
    
    # Notifier les autres utilisateurs
    join_notification = json.dumps({
        "type": "user_joined",
        "data": {
            "username": user.username,
            "channel": channel,
            "timestamp": datetime.utcnow().isoformat()
        }
    })
    await manager.broadcast_to_channel(join_notification, channel)
    
    try:
        while True:
            # Recevoir les messages du client
            data = await websocket.receive_text()
            
            try:
                message_data = json.loads(data)
                
                if message_data.get("type") == "chat_message":
                    content = message_data.get("content", "").strip()
                    
                    if not content:
                        continue
                    
                    # Vérifier le rate limiting
                    one_minute_ago = datetime.utcnow() - timedelta(minutes=1)
                    recent_messages = await db.chat_messages.count_documents({
                        "author_id": user.id,
                        "created_at": {"$gte": one_minute_ago}
                    })
                    
                    if recent_messages >= 10:
                        error_message = json.dumps({
                            "type": "error",
                            "data": {
                                "message": "Trop de messages envoyés. Limite: 10 messages par minute."
                            }
                        })
                        await manager.send_personal_message(error_message, user.id)
                        continue
                    
                    # Créer et sauvegarder le message
                    new_message = ChatMessage(
                        channel=channel,
                        author_id=user.id,
                        author_name=user.username,
                        content=content[:500],  # Limiter à 500 caractères
                        message_type="text",
                        reply_to=message_data.get("reply_to")
                    )
                    
                    await db.chat_messages.insert_one(new_message.dict())
                    
                    # Diffuser le message à tous les utilisateurs du channel
                    broadcast_message = json.dumps({
                        "type": "chat_message",
                        "data": {
                            "id": new_message.id,
                            "channel": new_message.channel,
                            "author_id": new_message.author_id,
                            "author_name": new_message.author_name,
                            "content": new_message.content,
                            "message_type": new_message.message_type,
                            "created_at": new_message.created_at.isoformat(),
                            "reply_to": new_message.reply_to
                        }
                    })
                    
                    await manager.broadcast_to_channel(broadcast_message, channel)
                    
                    # Récompenser l'activité
                    await reward_user_for_chat_activity(user.id, user.username)
                
                elif message_data.get("type") == "typing":
                    # Diffuser l'indicateur de frappe
                    typing_message = json.dumps({
                        "type": "typing",
                        "data": {
                            "username": user.username,
                            "is_typing": message_data.get("is_typing", True)
                        }
                    })
                    await manager.broadcast_to_channel(typing_message, channel)
            
            except json.JSONDecodeError:
                # Message mal formé, ignorer
                continue
                
    except WebSocketDisconnect:
        manager.disconnect(user.id, channel)
        
        # Notifier les autres utilisateurs
        leave_notification = json.dumps({
            "type": "user_left",
            "data": {
                "username": user.username,
                "channel": channel,
                "timestamp": datetime.utcnow().isoformat()
            }
        })
        await manager.broadcast_to_channel(leave_notification, channel)
        
        logger.info(f"User {user.username} disconnected from {channel}")
    
    except Exception as e:
        logger.error(f"WebSocket error for user {user.username}: {str(e)}")
        manager.disconnect(user.id, channel)

# WebSocket pour les messages privés

@router.websocket("/ws/private")
async def websocket_private_endpoint(websocket: WebSocket, token: str = Query(...)):
    """WebSocket endpoint pour les messages privés en temps réel."""
    
    # Authentifier l'utilisateur via le token
    user = await get_user_from_websocket_token(token)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    await manager.connect(websocket, user.id, "private")
    
    try:
        while True:
            # Maintenir la connexion pour recevoir les notifications
            data = await websocket.receive_text()
            # Les messages privés sont gérés via l'API REST
            # Ce WebSocket sert uniquement aux notifications
            
    except WebSocketDisconnect:
        manager.disconnect(user.id, "private")
        logger.info(f"User {user.username} disconnected from private messages")
    
    except Exception as e:
        logger.error(f"Private WebSocket error for user {user.username}: {str(e)}")
        manager.disconnect(user.id, "private")

# Fonctions utilitaires

async def reward_user_for_chat_activity(user_id: str, username: str):
    """Récompenser un utilisateur pour son activité dans le chat."""
    try:
        # Limiter les récompenses : max 20 coins par jour via le chat
        today = datetime.utcnow().date()
        today_start = datetime.combine(today, datetime.min.time())
        
        today_chat_rewards = await db.coin_transactions.count_documents({
            "user_id": user_id,
            "transaction_type": "chat_activity",
            "created_at": {"$gte": today_start}
        })
        
        if today_chat_rewards >= 20:  # Max 20 récompenses par jour
            return
        
        # Donner 1 coin et 1 XP pour un message
        from models import CoinTransaction
        
        transaction = CoinTransaction(
            user_id=user_id,
            amount=1,
            transaction_type="chat_activity",
            description="Participation active au chat communautaire"
        )
        
        await db.coin_transactions.insert_one(transaction.dict())
        
        # Mettre à jour le profil
        await db.user_profiles.update_one(
            {"user_id": user_id},
            {
                "$inc": {
                    "coins": 1,
                    "total_coins_earned": 1,
                    "experience_points": 1
                },
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        # Vérifier montée de niveau
        from routes.currency import check_level_up
        await check_level_up(user_id, username)
        
    except Exception as e:
        logger.error(f"Erreur lors de la récompense pour activité chat: {str(e)}")