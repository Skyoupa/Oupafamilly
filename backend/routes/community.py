from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List, Optional
from models import User, News, NewsCreate, Team
from auth import get_current_active_user, is_admin, is_moderator_or_admin
from cache import cached, invalidate
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/community", tags=["Community"])

# Get database from database module
from database import db

@router.get("/stats")
@cached(ttl=600, key_prefix="community_stats")  # Cache for 10 minutes
async def get_community_stats():
    """Get overall community statistics."""
    try:
        # Count total users
        total_users = await db.users.count_documents({})
        
        # Count active users (logged in recently)
        from datetime import timedelta
        last_week = datetime.utcnow() - timedelta(days=7)
        active_users = await db.users.count_documents({
            "last_active": {"$gte": last_week}
        })
        
        # Count total teams
        total_teams = await db.teams.count_documents({})
        
        # Count total tournaments
        total_tournaments = await db.tournaments.count_documents({})
        completed_tournaments = await db.tournaments.count_documents({"status": "completed"})
        
        # Count matches played
        total_matches = await db.matches.count_documents({})
        completed_matches = await db.matches.count_documents({"status": "completed"})
        
        return {
            "users": {
                "total": total_users,
                "active_last_week": active_users
            },
            "teams": {
                "total": total_teams
            },
            "tournaments": {
                "total": total_tournaments,
                "completed": completed_tournaments,
                "ongoing": total_tournaments - completed_tournaments
            },
            "matches": {
                "total": total_matches,
                "completed": completed_matches
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting community stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching community statistics"
        )

@router.get("/posts", response_model=List[News])
async def get_community_posts(
    published_only: bool = True,
    limit: int = 20,
    skip: int = 0
):
    """Get community posts/news."""
    try:
        filter_dict = {}
        if published_only:
            filter_dict["is_published"] = True
        
        posts = await db.news.find(filter_dict).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
        
        # Enrich with author information
        enriched_posts = []
        for post_data in posts:
            post = News(**post_data)
            
            # Get author info
            author = await db.users.find_one({"id": post.author_id})
            if author:
                post_dict = post.dict()
                post_dict["author_name"] = author["username"]
                post_dict["author_role"] = author.get("role", "user")
                enriched_posts.append(post_dict)
            else:
                enriched_posts.append(post.dict())
        
        return enriched_posts
        
    except Exception as e:
        logger.error(f"Error getting community posts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching community posts"
        )

@router.post("/posts", response_model=News)
async def create_community_post(
    post_data: NewsCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new community post (admin/moderator only)."""
    try:
        if not is_moderator_or_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only moderators and admins can create community posts"
            )
        
        new_post = News(
            **post_data.dict(),
            author_id=current_user.id
        )
        
        await db.news.insert_one(new_post.dict())
        
        logger.info(f"Community post created: {post_data.title} by {current_user.username}")
        
        return new_post
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating community post: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating community post"
        )

@router.put("/posts/{post_id}")
async def update_community_post(
    post_id: str,
    post_data: NewsCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Update a community post."""
    try:
        # Get the post
        existing_post = await db.news.find_one({"id": post_id})
        if not existing_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        # Check permissions
        if existing_post["author_id"] != current_user.id and not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only edit your own posts"
            )
        
        # Update post
        await db.news.update_one(
            {"id": post_id},
            {
                "$set": {
                    **post_data.dict(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        logger.info(f"Community post updated: {post_id} by {current_user.username}")
        
        return {"message": "Post updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating community post: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating community post"
        )

@router.delete("/posts/{post_id}")
async def delete_community_post(
    post_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a community post."""
    try:
        # Get the post
        existing_post = await db.news.find_one({"id": post_id})
        if not existing_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        # Check permissions
        if existing_post["author_id"] != current_user.id and not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own posts"
            )
        
        # Delete post
        await db.news.delete_one({"id": post_id})
        
        logger.info(f"Community post deleted: {post_id} by {current_user.username}")
        
        return {"message": "Post deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting community post: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting community post"
        )

@router.get("/leaderboard")
async def get_community_leaderboard():
    """Get community leaderboard with trophies and rankings."""
    try:
        # Get all users with their tournament victories
        users = await db.users.find({}).to_list(100)
        
        leaderboard = []
        for user_data in users:
            user = User(**user_data)
            
            # Count tournament victories by type
            victories = await get_user_tournament_victories(user.id)
            
            # Calculate total points based on victories
            total_points = (
                victories["1v1"] * 100 +      # 100 points per 1v1 victory
                victories["2v2"] * 150 +      # 150 points per 2v2 victory  
                victories["5v5"] * 200        # 200 points per 5v5 victory
            )
            
            total_trophies = sum(victories.values())
            
            leaderboard.append({
                "user_id": user.id,
                "username": user.username,
                "total_points": total_points,
                "total_trophies": total_trophies,
                "victories_1v1": victories["1v1"],
                "victories_2v2": victories["2v2"],
                "victories_5v5": victories["5v5"],
                "role": user.role,
                "created_at": user.created_at
            })
        
        # Sort by total points descending
        leaderboard.sort(key=lambda x: x["total_points"], reverse=True)
        
        # Add ranks
        for i, player in enumerate(leaderboard):
            player["rank"] = i + 1
            
            # Add badge based on rank and achievements
            if player["rank"] == 1:
                player["badge"] = "Champion"
            elif player["rank"] <= 3:
                player["badge"] = "Elite"
            elif player["rank"] <= 10:
                player["badge"] = "Pro"
            elif player["total_trophies"] >= 5:
                player["badge"] = "Vétéran"
            elif player["total_trophies"] >= 3:
                player["badge"] = "Expert"
            else:
                player["badge"] = "Rising"
        
        return {"leaderboard": leaderboard[:50]}  # Top 50
        
    except Exception as e:
        logger.error(f"Error getting community leaderboard: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching community leaderboard"
        )

async def get_user_tournament_victories(user_id: str) -> dict:
    """Get tournament victories by type for a user."""
    try:
        # Find tournaments won by this user
        won_tournaments = await db.tournaments.find({
            "winner_id": user_id,
            "status": "completed"
        }).to_list(100)
        
        victories = {"1v1": 0, "2v2": 0, "5v5": 0}
        
        for tournament in won_tournaments:
            # Determine tournament type based on max_participants or tournament name
            max_participants = tournament.get("max_participants", 2)
            tournament_name = tournament.get("title", "").lower()
            
            if "1v1" in tournament_name or max_participants <= 2:
                victories["1v1"] += 1
            elif "2v2" in tournament_name or max_participants <= 4:
                victories["2v2"] += 1
            elif "5v5" in tournament_name or max_participants >= 5:
                victories["5v5"] += 1
            else:
                # Default based on participant count
                if max_participants <= 2:
                    victories["1v1"] += 1
                elif max_participants <= 4:
                    victories["2v2"] += 1
                else:
                    victories["5v5"] += 1
        
        return victories
        
    except Exception as e:
        logger.error(f"Error getting user victories: {str(e)}")
        return {"1v1": 0, "2v2": 0, "5v5": 0}

@router.get("/members")
@cached(ttl=300, key_prefix="community_members")  # Cache for 5 minutes
async def get_community_members():
    """Get community members with enhanced profiles."""
    try:
        users = await db.users.find({}).to_list(100)
        
        enriched_members = []
        for user_data in users:
            user = User(**user_data)
            
            # Get victory statistics
            victories = await get_user_tournament_victories(user.id)
            total_trophies = sum(victories.values())
            
            # Get user profile data if exists
            profile = await db.user_profiles.find_one({"user_id": user.id})
            
            member_info = {
                "id": user.id,
                "username": user.username,
                "role": user.role,
                "status": user.status,
                "created_at": user.created_at,
                "trophies": {
                    "total": total_trophies,
                    "1v1": victories["1v1"],
                    "2v2": victories["2v2"], 
                    "5v5": victories["5v5"]
                },
                "profile": {
                    "display_name": profile.get("display_name", user.username) if profile else user.username,
                    "bio": profile.get("bio", "") if profile else "",
                    "favorite_games": profile.get("favorite_games", []) if profile else [],
                    "avatar_url": profile.get("avatar_url", "") if profile else ""
                }
            }
            
            enriched_members.append(member_info)
        
        # Sort by total trophies descending
        enriched_members.sort(key=lambda x: x["trophies"]["total"], reverse=True)
        
        return {"members": enriched_members}
        
    except Exception as e:
        logger.error(f"Error getting community members: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching community members"
        )

@router.get("/teams")
@cached(ttl=300, key_prefix="community_teams")  # Cache for 5 minutes
async def get_community_teams():
    """Get community teams with rankings."""
    try:
        teams = await db.teams.find({}).to_list(100)
        
        enriched_teams = []
        for team_data in teams:
            team = Team(**team_data)
            
            # Calculate team statistics
            from routes.teams import calculate_team_statistics
            team_stats = await calculate_team_statistics(team.id)
            
            # Get team member names
            member_names = []
            for member_id in team.members:
                member = await db.users.find_one({"id": member_id})
                if member:
                    member_names.append(member["username"])
            
            # Get captain name
            captain = await db.users.find_one({"id": team.captain_id})
            captain_name = captain["username"] if captain else "Unknown"
            
            enriched_teams.append({
                "id": team.id,
                "name": team.name,
                "game": team.game,
                "captain": captain_name,
                "members": member_names,
                "member_count": len(team.members),
                "max_members": team.max_members,
                "is_open": team.is_open,
                "statistics": team_stats,
                "created_at": team.created_at
            })
        
        # Sort by total points descending
        enriched_teams.sort(key=lambda x: x["statistics"]["total_points"], reverse=True)
        
        # Add ranks
        for i, team in enumerate(enriched_teams):
            team["rank"] = i + 1
        
        return {"teams": enriched_teams}
        
    except Exception as e:
        logger.error(f"Error getting community teams: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching community teams"
        )

async def calculate_team_statistics(team_id: str) -> dict:
    """Calculate comprehensive statistics for a team."""
    try:
        # Find tournaments where this team participated
        tournaments_participated = await db.tournaments.find({
            "participants": {"$in": [team_id]}
        }).to_list(100)
        
        # Find tournaments won by this team
        tournaments_won = await db.tournaments.find({
            "winner_id": team_id,
            "status": "completed"
        }).to_list(100)
        
        # Calculate statistics
        total_tournaments = len(tournaments_participated)
        total_victories = len(tournaments_won)
        
        # Calculate points (similar to user system)
        total_points = 0
        victories_by_type = {"1v1": 0, "2v2": 0, "5v5": 0}
        
        for tournament in tournaments_won:
            max_participants = tournament.get("max_participants", 2)
            tournament_name = tournament.get("title", "").lower()
            
            if "1v1" in tournament_name or max_participants <= 2:
                victories_by_type["1v1"] += 1
                total_points += 100
            elif "2v2" in tournament_name or max_participants <= 4:
                victories_by_type["2v2"] += 1
                total_points += 150
            elif "5v5" in tournament_name or max_participants >= 5:
                victories_by_type["5v5"] += 1
                total_points += 200
        
        win_rate = (total_victories / total_tournaments * 100) if total_tournaments > 0 else 0
        
        return {
            "total_tournaments": total_tournaments,
            "tournaments_won": total_victories,
            "win_rate": round(win_rate, 1),
            "total_points": total_points,
            "victories_by_type": victories_by_type
        }
        
    except Exception as e:
        logger.error(f"Error calculating team statistics for {team_id}: {str(e)}")
        return {
            "total_tournaments": 0,
            "tournaments_won": 0,
            "win_rate": 0.0,
            "total_points": 0,
            "victories_by_type": {"1v1": 0, "2v2": 0, "5v5": 0}
        }

