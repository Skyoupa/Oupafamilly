from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import Optional
from models import User
from auth import get_current_active_user
from datetime import datetime
import logging
import uuid
import os
import shutil

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/profiles", tags=["Profiles"])

# Get database from database module
from database import db

@router.get("/{user_id}")
async def get_user_profile(user_id: str):
    """Get user profile with trophies and statistics."""
    try:
        # Get user basic info
        user_data = await db.users.find_one({"id": user_id})
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user = User(**user_data)
        
        # Get extended profile
        profile = await db.user_profiles.find_one({"user_id": user_id})
        
        # Get tournament statistics
        tournament_stats = await get_user_tournament_stats(user_id)
        
        # Get team memberships
        teams = await db.teams.find({"members": {"$in": [user_id]}}).to_list(10)
        
        # Get recent matches
        recent_matches = await db.matches.find({
            "$or": [
                {"player1_id": user_id},
                {"player2_id": user_id}
            ],
            "status": "completed"
        }).sort("completed_at", -1).limit(10).to_list(10)
        
        profile_data = {
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role,
                "status": user.status,
                "created_at": user.created_at,
                "is_verified": user.is_verified
            },
            "profile": {
                "display_name": profile.get("display_name", user.username) if profile else user.username,
                "bio": profile.get("bio", "") if profile else "",
                "avatar_url": profile.get("avatar_url", "") if profile else "",
                "discord_username": profile.get("discord_username", "") if profile else "",
                "twitch_username": profile.get("twitch_username", "") if profile else "",
                "steam_profile": profile.get("steam_profile", "") if profile else "",
                "favorite_games": profile.get("favorite_games", []) if profile else [],
                "gaming_experience": profile.get("gaming_experience", {}) if profile else {},
                "location": profile.get("location", "") if profile else "",
                "banner_url": profile.get("banner_url", "") if profile else ""
            },
            "statistics": tournament_stats,
            "teams": [
                {
                    "id": team["id"],
                    "name": team["name"],
                    "game": team["game"],
                    "is_captain": team["captain_id"] == user_id
                }
                for team in teams
            ],
            "recent_matches": [
                {
                    "id": match["id"],
                    "tournament_id": match["tournament_id"],
                    "opponent_id": match["player2_id"] if match["player1_id"] == user_id else match["player1_id"],
                    "won": match["winner_id"] == user_id,
                    "score": f"{match['player1_score']}-{match['player2_score']}" if match["player1_id"] == user_id else f"{match['player2_score']}-{match['player1_score']}",
                    "completed_at": match["completed_at"]
                }
                for match in recent_matches
            ]
        }
        
        return profile_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user profile {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching user profile"
        )

@router.put("/my-profile")
async def update_my_profile(
    display_name: Optional[str] = None,
    bio: Optional[str] = None,
    discord_username: Optional[str] = None,
    twitch_username: Optional[str] = None,
    steam_profile: Optional[str] = None,
    location: Optional[str] = None,
    favorite_games: Optional[list] = None,
    gaming_experience: Optional[dict] = None,
    current_user: User = Depends(get_current_active_user)
):
    """Update user's own profile."""
    try:
        update_data = {"updated_at": datetime.utcnow()}
        
        if display_name is not None:
            update_data["display_name"] = display_name[:50]  # Limit length
        if bio is not None:
            update_data["bio"] = bio[:500]  # Limit length
        if discord_username is not None:
            update_data["discord_username"] = discord_username[:50]
        if twitch_username is not None:
            update_data["twitch_username"] = twitch_username[:50]
        if steam_profile is not None:
            update_data["steam_profile"] = steam_profile
        if location is not None:
            update_data["location"] = location[:100]
        if favorite_games is not None:
            update_data["favorite_games"] = favorite_games[:10]  # Max 10 games
        if gaming_experience is not None:
            update_data["gaming_experience"] = gaming_experience
        
        # Upsert profile
        await db.user_profiles.update_one(
            {"user_id": current_user.id},
            {"$set": update_data},
            upsert=True
        )
        
        logger.info(f"Profile updated for user {current_user.username}")
        
        return {"message": "Profile updated successfully"}
        
    except Exception as e:
        logger.error(f"Error updating profile for {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating profile"
        )

@router.post("/upload-avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """Upload user avatar."""
    try:
        # Validate file type
        allowed_types = ["image/jpeg", "image/png", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only JPEG, PNG, and WebP images are allowed"
            )
        
        # Validate file size (max 5MB)
        file_size = 0
        chunk_size = 1024
        for chunk in iter(lambda: file.file.read(chunk_size), b""):
            file_size += len(chunk)
            if file_size > 5 * 1024 * 1024:  # 5MB
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="File size must be less than 5MB"
                )
        
        # Reset file pointer
        file.file.seek(0)
        
        # Create uploads directory if it doesn't exist
        upload_dir = "/app/uploads/avatars"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        filename = f"{current_user.id}_{uuid.uuid4().hex[:8]}.{file_extension}"
        file_path = os.path.join(upload_dir, filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Update profile with avatar URL
        avatar_url = f"/uploads/avatars/{filename}"
        await db.user_profiles.update_one(
            {"user_id": current_user.id},
            {
                "$set": {
                    "avatar_url": avatar_url,
                    "updated_at": datetime.utcnow()
                }
            },
            upsert=True
        )
        
        logger.info(f"Avatar uploaded for user {current_user.username}: {filename}")
        
        return {
            "message": "Avatar uploaded successfully",
            "avatar_url": avatar_url
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading avatar for {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error uploading avatar"
        )

@router.post("/upload-avatar-base64")
async def upload_avatar_base64(
    avatar_data: str,  # Base64 encoded image data
    current_user: User = Depends(get_current_active_user)
):
    """Upload user avatar from base64 encoded image data."""
    try:
        import base64
        import io
        from PIL import Image
        
        # Extract the actual base64 data (remove data:image/...;base64, prefix if present)
        if avatar_data.startswith('data:image'):
            header, encoded = avatar_data.split(',', 1)
            # Validate image type from header
            if 'jpeg' not in header and 'jpg' not in header and 'png' not in header and 'webp' not in header:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only JPEG, PNG, and WebP images are allowed"
                )
        else:
            encoded = avatar_data
        
        # Decode base64
        try:
            image_data = base64.b64decode(encoded)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid base64 image data"
            )
        
        # Validate image and check size
        try:
            image = Image.open(io.BytesIO(image_data))
            
            # Check file size (max 5MB)
            if len(image_data) > 5 * 1024 * 1024:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Image size must be less than 5MB"
                )
            
            # Resize image if too large (max 800x800)
            if image.width > 800 or image.height > 800:
                image.thumbnail((800, 800), Image.Resampling.LANCZOS)
                
                # Save resized image to bytes
                output = io.BytesIO()
                image.save(output, format='PNG', optimize=True)
                image_data = output.getvalue()
                
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image data"
            )
        
        # Convert to base64 and store directly in database (for simplicity)
        avatar_base64 = base64.b64encode(image_data).decode('utf-8')
        avatar_url = f"data:image/png;base64,{avatar_base64}"
        
        # Update profile with avatar base64 data
        await db.user_profiles.update_one(
            {"user_id": current_user.id},
            {
                "$set": {
                    "avatar_url": avatar_url,
                    "updated_at": datetime.utcnow()
                }
            },
            upsert=True
        )
        
        logger.info(f"Base64 avatar uploaded for user {current_user.username}")
        
        return {
            "message": "Avatar uploaded successfully",
            "avatar_url": avatar_url
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading base64 avatar for {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error uploading avatar"
        )

async def get_user_tournament_stats(user_id: str) -> dict:
    """Get comprehensive tournament statistics for a user."""
    try:
        # Get all tournaments where user participated
        tournaments_participated = await db.tournaments.find({
            "participants": {"$in": [user_id]}
        }).to_list(100)
        
        # Get tournaments won
        tournaments_won = await db.tournaments.find({
            "winner_id": user_id,
            "status": "completed"
        }).to_list(100)
        
        # Get all matches played
        matches_played = await db.matches.find({
            "$or": [
                {"player1_id": user_id},
                {"player2_id": user_id}
            ],
            "status": "completed"
        }).to_list(200)
        
        # Calculate statistics
        total_tournaments = len(tournaments_participated)
        total_victories = len(tournaments_won)
        total_matches = len(matches_played)
        
        # Count victories by tournament type
        victories_by_type = {"1v1": 0, "2v2": 0, "5v5": 0}
        for tournament in tournaments_won:
            max_participants = tournament.get("max_participants", 2)
            tournament_name = tournament.get("title", "").lower()
            
            if "1v1" in tournament_name or max_participants <= 2:
                victories_by_type["1v1"] += 1
            elif "2v2" in tournament_name or max_participants <= 4:
                victories_by_type["2v2"] += 1
            elif "5v5" in tournament_name or max_participants >= 5:
                victories_by_type["5v5"] += 1
        
        # Calculate match win rate
        matches_won = sum(1 for match in matches_played if match["winner_id"] == user_id)
        win_rate = (matches_won / total_matches * 100) if total_matches > 0 else 0
        
        # Calculate points
        total_points = (
            victories_by_type["1v1"] * 100 +
            victories_by_type["2v2"] * 150 +
            victories_by_type["5v5"] * 200
        )
        
        return {
            "tournaments": {
                "total": total_tournaments,
                "victories": total_victories,
                "win_rate": (total_victories / total_tournaments * 100) if total_tournaments > 0 else 0
            },
            "matches": {
                "total": total_matches,
                "victories": matches_won,
                "defeats": total_matches - matches_won,
                "win_rate": round(win_rate, 1)
            },
            "trophies": {
                "total": sum(victories_by_type.values()),
                "1v1": victories_by_type["1v1"],
                "2v2": victories_by_type["2v2"],
                "5v5": victories_by_type["5v5"]
            },
            "ranking": {
                "total_points": total_points,
                "level": get_user_level(total_points),
                "next_level_points": get_next_level_points(total_points)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting tournament stats for {user_id}: {str(e)}")
        return {
            "tournaments": {"total": 0, "victories": 0, "win_rate": 0},
            "matches": {"total": 0, "victories": 0, "defeats": 0, "win_rate": 0},
            "trophies": {"total": 0, "1v1": 0, "2v2": 0, "5v5": 0},
            "ranking": {"total_points": 0, "level": "Novice", "next_level_points": 100}
        }

def get_user_level(points: int) -> str:
    """Get user level based on points."""
    if points >= 2000:
        return "Legend"
    elif points >= 1500:
        return "Master"
    elif points >= 1000:
        return "Expert"
    elif points >= 500:
        return "Advanced"
    elif points >= 200:
        return "Intermediate"
    elif points >= 50:
        return "Beginner"
    else:
        return "Novice"

def get_next_level_points(points: int) -> int:
    """Get points needed for next level."""
    levels = [50, 200, 500, 1000, 1500, 2000]
    for level_points in levels:
        if points < level_points:
            return level_points - points
    return 0  # Already at max level