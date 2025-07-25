from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from models import Team, TeamCreate, User, Game
from auth import get_current_active_user, is_admin, is_moderator_or_admin
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/teams", tags=["Teams"])

# Get database from database module
from database import db

@router.post("/", response_model=Team)
async def create_team(
    team_data: TeamCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new team with current user as captain."""
    try:
        # Check if team name already exists for this game
        existing_team = await db.teams.find_one({
            "name": team_data.name,
            "game": team_data.game
        })
        
        if existing_team:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A team named '{team_data.name}' already exists for {team_data.game}"
            )
        
        new_team = Team(
            **team_data.dict(),
            captain_id=current_user.id,
            members=[current_user.id]  # Captain is automatically a member
        )
        
        await db.teams.insert_one(new_team.dict())
        
        # Update user profile team count
        await db.user_profiles.update_one(
            {"user_id": current_user.id},
            {"$inc": {"total_teams": 1}}
        )
        
        logger.info(f"Team created: {team_data.name} by {current_user.username}")
        
        return new_team
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating team: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating team"
        )

@router.get("/", response_model=List[Team])
async def get_teams(
    game: Optional[Game] = None,
    is_open: Optional[bool] = None,
    limit: int = Query(20, le=100),
    skip: int = Query(0, ge=0)
):
    """Get teams with optional filtering."""
    try:
        filter_dict = {}
        if game:
            filter_dict["game"] = game
        if is_open is not None:
            filter_dict["is_open"] = is_open
        
        teams = await db.teams.find(filter_dict).skip(skip).limit(limit).to_list(limit)
        return [Team(**team) for team in teams]
        
    except Exception as e:
        logger.error(f"Error getting teams: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching teams"
        )

@router.get("/my-teams", response_model=List[Team])
async def get_my_teams(
    current_user: User = Depends(get_current_active_user)
):
    """Get teams where current user is captain or member."""
    try:
        teams = await db.teams.find({
            "$or": [
                {"captain_id": current_user.id},
                {"members": {"$in": [current_user.id]}}
            ]
        }).to_list(100)
        
        return [Team(**team) for team in teams]
        
    except Exception as e:
        logger.error(f"Error getting user teams: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching user teams"
        )

@router.get("/{team_id}", response_model=Team)
async def get_team(team_id: str):
    """Get a specific team."""
    try:
        team_data = await db.teams.find_one({"id": team_id})
        if not team_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        return Team(**team_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting team {team_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching team"
        )

@router.post("/{team_id}/join")
async def join_team(
    team_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Join a team as a member."""
    try:
        # Get team
        team_data = await db.teams.find_one({"id": team_id})
        if not team_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        team = Team(**team_data)
        
        # Check if team is open for new members
        if not team.is_open:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Team is not accepting new members"
            )
        
        # Check if user is already a member
        if current_user.id in team.members:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already a member of this team"
            )
        
        # Check if team is full
        if len(team.members) >= team.max_members:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Team is full"
            )
        
        # Add user to team
        await db.teams.update_one(
            {"id": team_id},
            {
                "$push": {"members": current_user.id},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        logger.info(f"User {current_user.username} joined team {team.name}")
        
        return {"message": f"Successfully joined team {team.name}"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error joining team {team_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error joining team"
        )

@router.delete("/{team_id}/leave")
async def leave_team(
    team_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Leave a team."""
    try:
        # Get team
        team_data = await db.teams.find_one({"id": team_id})
        if not team_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        team = Team(**team_data)
        
        # Check if user is a member
        if current_user.id not in team.members:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not a member of this team"
            )
        
        # Captain cannot leave unless transferring captaincy or disbanding team
        if team.captain_id == current_user.id:
            if len(team.members) > 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Captain must transfer captaincy or disband team before leaving"
                )
            else:
                # If captain is the only member, disband the team
                await db.teams.delete_one({"id": team_id})
                logger.info(f"Team {team.name} disbanded by captain {current_user.username}")
                return {"message": f"Team {team.name} disbanded"}
        
        # Remove user from team
        await db.teams.update_one(
            {"id": team_id},
            {
                "$pull": {"members": current_user.id},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        logger.info(f"User {current_user.username} left team {team.name}")
        
        return {"message": f"Successfully left team {team.name}"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error leaving team {team_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error leaving team"
        )

@router.put("/{team_id}/captain")
async def transfer_captaincy(
    team_id: str,
    new_captain_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Transfer team captaincy to another member."""
    try:
        # Get team
        team_data = await db.teams.find_one({"id": team_id})
        if not team_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        team = Team(**team_data)
        
        # Check if current user is captain
        if team.captain_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only team captain can transfer captaincy"
            )
        
        # Check if new captain is a member
        if new_captain_id not in team.members:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New captain must be a team member"
            )
        
        # Transfer captaincy
        await db.teams.update_one(
            {"id": team_id},
            {
                "$set": {
                    "captain_id": new_captain_id,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        logger.info(f"Team {team.name} captaincy transferred to {new_captain_id} by {current_user.username}")
        
        return {"message": "Captaincy transferred successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error transferring captaincy {team_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error transferring captaincy"
        )

@router.delete("/{team_id}")
async def delete_team(
    team_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a team. Only captain or admin can do this."""
    try:
        # Get team
        team_data = await db.teams.find_one({"id": team_id})
        if not team_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        team = Team(**team_data)
        
        # Check permissions
        if team.captain_id != current_user.id and not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only team captain or admin can delete team"
            )
        
        # Delete the team
        delete_result = await db.teams.delete_one({"id": team_id})
        
        if delete_result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete team"
            )
        
        logger.info(f"Team {team.name} deleted by {current_user.username}")
        
        return {"message": f"Team '{team.name}' deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting team {team_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting team"
        )

@router.put("/{team_id}")
async def update_team(
    team_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    is_open: Optional[bool] = None,
    max_members: Optional[int] = None,
    current_user: User = Depends(get_current_active_user)
):
    """Update team details. Only captain can do this."""
    try:
        # Get team
        team_data = await db.teams.find_one({"id": team_id})
        if not team_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        team = Team(**team_data)
        
        # Check permissions
        if team.captain_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only team captain can update team"
            )
        
        # Prepare update fields
        update_fields = {"updated_at": datetime.utcnow()}
        
        if name is not None:
            # Check if new name already exists for this game
            existing_team = await db.teams.find_one({
                "name": name,
                "game": team.game,
                "id": {"$ne": team_id}
            })
            if existing_team:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"A team named '{name}' already exists for {team.game}"
                )
            update_fields["name"] = name
        
        if description is not None:
            update_fields["description"] = description
        
        if is_open is not None:
            update_fields["is_open"] = is_open
        
        if max_members is not None:
            if max_members < len(team.members):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot set max_members to {max_members}, team currently has {len(team.members)} members"
                )
            update_fields["max_members"] = max_members
        
        # Update team
        await db.teams.update_one(
            {"id": team_id},
            {"$set": update_fields}
        )
        
        logger.info(f"Team {team.name} updated by {current_user.username}")
        
        return {"message": "Team updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating team {team_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating team"
        )

@router.post("/{team_id}/add-member")
async def add_member_to_team(
    team_id: str,
    user_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Add a member to team (captain only)."""
    try:
        # Get team
        team_data = await db.teams.find_one({"id": team_id})
        if not team_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        team = Team(**team_data)
        
        # Check permissions - only captain can add members
        if team.captain_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only team captain can add members"
            )
        
        # Check if user exists
        user_to_add = await db.users.find_one({"id": user_id})
        if not user_to_add:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if user is already a member
        if user_id in team.members:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a member of this team"
            )
        
        # Check if team is full
        if len(team.members) >= team.max_members:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Team is full"
            )
        
        # Add user to team
        await db.teams.update_one(
            {"id": team_id},
            {
                "$push": {"members": user_id},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        logger.info(f"User {user_to_add['username']} added to team {team.name} by {current_user.username}")
        
        return {"message": f"User {user_to_add['username']} added to team successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding member to team {team_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error adding member to team"
        )

@router.delete("/{team_id}/remove-member/{user_id}")
async def remove_member_from_team(
    team_id: str,
    user_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Remove a member from team (captain only, cannot remove captain)."""
    try:
        # Get team
        team_data = await db.teams.find_one({"id": team_id})
        if not team_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        team = Team(**team_data)
        
        # Check permissions - only captain can remove members
        if team.captain_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only team captain can remove members"
            )
        
        # Cannot remove captain
        if user_id == team.captain_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove team captain. Transfer captaincy first."
            )
        
        # Check if user is a member
        if user_id not in team.members:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not a member of this team"
            )
        
        # Get user info for logging
        user_to_remove = await db.users.find_one({"id": user_id})
        
        # Remove user from team
        await db.teams.update_one(
            {"id": team_id},
            {
                "$pull": {"members": user_id},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        logger.info(f"User {user_to_remove['username'] if user_to_remove else user_id} removed from team {team.name} by {current_user.username}")
        
        return {"message": f"User removed from team successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing member from team {team_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error removing member from team"
        )

@router.get("/{team_id}/available-users")
async def get_available_users_for_team(
    team_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get users that can be added to the team (captain only)."""
    try:
        # Get team
        team_data = await db.teams.find_one({"id": team_id})
        if not team_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        team = Team(**team_data)
        
        # Check permissions - only captain can see available users
        if team.captain_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only team captain can view available users"
            )
        
        # Get all users except current team members
        all_users = await db.users.find({
            "id": {"$nin": team.members},
            "status": "active"
        }).to_list(100)
        
        available_users = [
            {
                "id": user["id"],
                "username": user["username"],
                "role": user.get("role", "member"),
                "created_at": user["created_at"]
            }
            for user in all_users
        ]
        
        return {"available_users": available_users}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting available users for team {team_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting available users"
        )

@router.get("/stats/community")
async def get_team_stats():
    """Get team statistics for the community."""
    try:
        total_teams = await db.teams.count_documents({})
        open_teams = await db.teams.count_documents({"is_open": True})
        
        # Get teams by game
        pipeline = [
            {"$group": {"_id": "$game", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        games_stats = await db.teams.aggregate(pipeline).to_list(None)
        
        # Get average team size
        size_pipeline = [
            {"$group": {"_id": None, "avg_size": {"$avg": {"$size": "$members"}}}}
        ]
        size_result = await db.teams.aggregate(size_pipeline).to_list(1)
        avg_team_size = round(size_result[0]["avg_size"] if size_result else 0, 1)
        
        return {
            "total_teams": total_teams,
            "open_teams": open_teams,
            "games_popularity": [{"game": stat["_id"], "count": stat["count"]} for stat in games_stats],
            "average_team_size": avg_team_size,
            "community_engagement": {
                "teams_looking_for_members": open_teams,
                "team_formation_rate": round((open_teams / total_teams * 100) if total_teams > 0 else 0, 2)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting team stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching team statistics"
        )

@router.get("/leaderboard")
async def get_team_leaderboard(
    game: Optional[Game] = None,
    limit: int = Query(50, le=100)
):
    """Get team leaderboard with rankings based on tournament victories."""
    try:
        # Build filter for teams
        filter_dict = {}
        if game:
            filter_dict["game"] = game
        
        teams = await db.teams.find(filter_dict).to_list(500)
        
        team_rankings = []
        for team_data in teams:
            team = Team(**team_data)
            
            # Calculate team statistics
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
            
            team_rankings.append({
                "team_id": team.id,
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
        team_rankings.sort(key=lambda x: x["statistics"]["total_points"], reverse=True)
        
        # Add ranks
        for i, team in enumerate(team_rankings[:limit]):
            team["rank"] = i + 1
            
            # Add performance badge
            stats = team["statistics"]
            if stats["tournaments_won"] >= 5:
                team["badge"] = "Champions"
            elif stats["tournaments_won"] >= 3:
                team["badge"] = "Elite"
            elif stats["tournaments_won"] >= 1:
                team["badge"] = "Champions"
            elif stats["total_tournaments"] >= 3:
                team["badge"] = "Competitors"
            else:
                team["badge"] = "Rising"
        
        return {"leaderboard": team_rankings[:limit]}
        
    except Exception as e:
        logger.error(f"Error getting team leaderboard: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching team leaderboard"
        )

@router.delete("/{team_id}/delete")
async def delete_team(
    team_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a team (captain only). Cannot delete if team is registered in active tournaments."""
    try:
        # Get team
        team_data = await db.teams.find_one({"id": team_id})
        if not team_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        team = Team(**team_data)
        
        # Check permissions - only captain can delete team
        if team.captain_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only team captain can delete the team"
            )
        
        # Check if team is registered in any active tournaments
        active_tournaments = await db.tournaments.find({
            "participants": {"$in": [team_id]},
            "status": {"$in": ["open", "in_progress"]}
        }).to_list(100)
        
        if active_tournaments:
            tournament_names = [t["title"] for t in active_tournaments]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete team. Team is registered in active tournaments: {', '.join(tournament_names)}"
            )
        
        # Remove team from all completed tournaments (cleanup)
        await db.tournaments.update_many(
            {"participants": {"$in": [team_id]}},
            {"$pull": {"participants": team_id}}
        )
        
        # Delete the team
        await db.teams.delete_one({"id": team_id})
        
        logger.info(f"Team {team.name} deleted by captain {current_user.username}")
        
        return {"message": f"Team '{team.name}' has been successfully deleted"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting team {team_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting team"
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