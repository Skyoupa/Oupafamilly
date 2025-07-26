from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from typing import List, Optional
from models import (
    Tournament, TournamentCreate, User, TournamentStatus, 
    TournamentType, Game, Match
)
from auth import get_current_active_user, is_admin, is_moderator_or_admin
from datetime import datetime, timedelta
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tournaments", tags=["Tournaments"])

# Get database from database module
from database import db
from cache import cached, invalidate

@router.post("/", response_model=Tournament)
async def create_tournament(
    tournament_data: TournamentCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new tournament. For starting community, allow any member to create tournaments."""
    try:
        # For a growing community, be more permissive with tournament creation
        new_tournament = Tournament(
            **tournament_data.dict(),
            organizer_id=current_user.id,
            status=TournamentStatus.DRAFT
        )
        
        await db.tournaments.insert_one(new_tournament.dict())
        
        logger.info(f"Tournament created: {tournament_data.title} by {current_user.username}")
        
        return new_tournament
        
    except Exception as e:
        logger.error(f"Error creating tournament: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating tournament"
        )

@router.get("/", response_model=List[Tournament])
@cached(ttl=300, key_prefix="tournaments")  # Cache for 5 minutes
async def get_tournaments(
    tournament_status: Optional[TournamentStatus] = None,
    game: Optional[Game] = None,
    limit: int = Query(20, le=100),
    skip: int = Query(0, ge=0)
):
    """Get tournaments with optional filtering."""
    try:
        filter_dict = {}
        if tournament_status:
            filter_dict["status"] = tournament_status
        if game:
            filter_dict["game"] = game
        
        tournaments_data = await db.tournaments.find(filter_dict).skip(skip).limit(limit).to_list(limit)
        
        # Convert database format to model format
        tournaments = []
        for tournament_data in tournaments_data:
            try:
                # Map database fields to model fields
                mapped_tournament = {
                    "id": tournament_data.get("id", str(uuid.uuid4())),
                    "title": tournament_data.get("title", ""),
                    "description": tournament_data.get("description", ""),
                    "game": tournament_data.get("game", "cs2"),
                    "tournament_type": map_tournament_type(tournament_data.get("type", "elimination")),
                    "max_participants": tournament_data.get("max_participants", 16),
                    "entry_fee": tournament_data.get("entry_fee", 0.0),
                    "prize_pool": tournament_data.get("prize_pool", 0.0),
                    "status": map_tournament_status(tournament_data.get("status", "draft")),
                    "registration_start": tournament_data.get("registration_opens", datetime.utcnow()),
                    "registration_end": tournament_data.get("registration_closes", datetime.utcnow()),
                    "tournament_start": tournament_data.get("tournament_starts", datetime.utcnow()),
                    "tournament_end": tournament_data.get("tournament_ends"),
                    "rules": tournament_data.get("rules", "Standard tournament rules"),
                    "organizer_id": tournament_data.get("organizer_id", "system"),
                    "participants": tournament_data.get("participants", []),
                    "matches": tournament_data.get("matches", []),
                    "winner_id": tournament_data.get("winner_id"),
                    "created_at": tournament_data.get("created_at", datetime.utcnow()),
                    "updated_at": tournament_data.get("updated_at", datetime.utcnow())
                }
                
                tournament = Tournament(**mapped_tournament)
                tournaments.append(tournament)
                
            except Exception as e:
                logger.warning(f"Skipping invalid tournament data: {str(e)}")
                continue
        
        return tournaments
        
    except Exception as e:
        logger.error(f"Error getting tournaments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching tournaments"
        )

def map_tournament_status(db_status: str) -> TournamentStatus:
    """Map database status values to model enum values."""
    status_mapping = {
        "registration_open": TournamentStatus.OPEN,
        "ongoing": TournamentStatus.IN_PROGRESS,
        "completed": TournamentStatus.COMPLETED,
        "cancelled": TournamentStatus.CANCELLED,
        "draft": TournamentStatus.DRAFT
    }
    return status_mapping.get(db_status, TournamentStatus.DRAFT)

def map_tournament_type(db_type: str) -> TournamentType:
    """Map database type values to model enum values."""
    type_mapping = {
        "tournament": TournamentType.ELIMINATION,  # Default mapping
        "elimination": TournamentType.ELIMINATION,
        "bracket": TournamentType.BRACKET,
        "round_robin": TournamentType.ROUND_ROBIN
    }
    return type_mapping.get(db_type, TournamentType.ELIMINATION)

@router.get("/{tournament_id}", response_model=Tournament)
@cached(ttl=600, key_prefix="tournament")  # Cache for 10 minutes
async def get_tournament(tournament_id: str):
    """Get a specific tournament."""
    try:
        tournament_data = await db.tournaments.find_one({"id": tournament_id})
        if not tournament_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournament not found"
            )
        
        # Map database fields to model fields (same logic as in list endpoint)
        mapped_tournament = {
            "id": tournament_data.get("id", str(uuid.uuid4())),
            "title": tournament_data.get("title", ""),
            "description": tournament_data.get("description", ""),
            "game": tournament_data.get("game", "cs2"),
            "tournament_type": map_tournament_type(tournament_data.get("type", "elimination")),
            "max_participants": tournament_data.get("max_participants", 16),
            "entry_fee": tournament_data.get("entry_fee", 0.0),
            "prize_pool": tournament_data.get("prize_pool", 0.0),
            "status": map_tournament_status(tournament_data.get("status", "draft")),
            "registration_start": tournament_data.get("registration_opens", datetime.utcnow()),
            "registration_end": tournament_data.get("registration_closes", datetime.utcnow()),
            "tournament_start": tournament_data.get("tournament_starts", datetime.utcnow()),
            "tournament_end": tournament_data.get("tournament_ends"),
            "rules": tournament_data.get("rules", "Standard tournament rules"),
            "organizer_id": tournament_data.get("organizer_id", "system"),
            "participants": tournament_data.get("participants", []),
            "matches": tournament_data.get("matches", []),
            "winner_id": tournament_data.get("winner_id"),
            "created_at": tournament_data.get("created_at", datetime.utcnow()),
            "updated_at": tournament_data.get("updated_at", datetime.utcnow())
        }
        
        return Tournament(**mapped_tournament)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting tournament {tournament_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching tournament"
        )

@router.get("/{tournament_id}/participants-info")
@cached(ttl=180, key_prefix="tournament_participants")  # Cache for 3 minutes
async def get_tournament_participants_info(tournament_id: str):
    """Get detailed information about tournament participants."""
    try:
        tournament_data = await db.tournaments.find_one({"id": tournament_id})
        if not tournament_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournament not found"
            )
        
        participants_info = []
        participants = tournament_data.get("participants", [])
        
        # Get detailed info for each participant
        for participant_id in participants:
            # Try to get user info first
            user_data = await db.users.find_one({"id": participant_id})
            if user_data:
                # Get user profile for additional info
                profile_data = await db.user_profiles.find_one({"user_id": participant_id})
                
                participant_info = {
                    "id": participant_id,
                    "type": "user",
                    "name": user_data.get("username", "Utilisateur"),
                    "display_name": profile_data.get("display_name") if profile_data else user_data.get("username", "Utilisateur"),
                    "level": profile_data.get("level", 1) if profile_data else 1,
                    "game_info": profile_data.get("gaming_info", {}) if profile_data else {},
                    "avatar": profile_data.get("avatar_url") if profile_data else None,
                    "registered_at": datetime.utcnow()  # Could be tracked separately
                }
                participants_info.append(participant_info)
            else:
                # Try to get team info
                team_data = await db.teams.find_one({"id": participant_id})
                if team_data:
                    team_members = []
                    for member_id in team_data.get("members", []):
                        member_data = await db.users.find_one({"id": member_id})
                        if member_data:
                            team_members.append({
                                "id": member_id,
                                "username": member_data.get("username", "Membre"),
                                "role": "member"  # Could be expanded with roles
                            })
                    
                    participant_info = {
                        "id": participant_id,
                        "type": "team",
                        "name": team_data.get("name", "Équipe"),
                        "members": team_members,
                        "members_count": len(team_members),
                        "registered_at": team_data.get("created_at", datetime.utcnow())
                    }
                    participants_info.append(participant_info)
        
        # Calculate statistics
        stats = {
            "total_participants": len(participants_info),
            "user_participants": len([p for p in participants_info if p["type"] == "user"]),
            "team_participants": len([p for p in participants_info if p["type"] == "team"]),
            "max_participants": tournament_data.get("max_participants", 16),
            "spots_remaining": max(0, tournament_data.get("max_participants", 16) - len(participants_info)),
            "registration_full": len(participants_info) >= tournament_data.get("max_participants", 16)
        }
        
        return {
            "tournament_id": tournament_id,
            "participants": participants_info,
            "stats": stats,
            "registration_open": tournament_data.get("status") in ["registration", "open", "registration_open"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting participants info for tournament {tournament_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching tournament participants information"
        )

@router.post("/{tournament_id}/register")
async def register_for_tournament(
    tournament_id: str,
    team_id: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """Register current user (or their team) for a tournament."""
    try:
        # Get tournament
        tournament_data = await db.tournaments.find_one({"id": tournament_id})
        if not tournament_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournament not found"
            )
        
        tournament = Tournament(**tournament_data)
        
        # Check if tournament is open for registration
        if tournament.status != TournamentStatus.OPEN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tournament is not open for registration"
            )
        
        # Check if registration is still open
        if datetime.utcnow() > tournament.registration_end:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration period has ended"
            )
        
        # Determine tournament type based on max_participants and title
        tournament_requires_team = False
        tournament_name = tournament.title.lower()
        
        # Check tournament name patterns first (most reliable)
        if "1v1" in tournament_name or "1vs1" in tournament_name:
            tournament_requires_team = False
        elif "2v2" in tournament_name or "2vs2" in tournament_name:
            tournament_requires_team = True
            # Ensure max_participants is multiple of 2 for 2v2 tournaments
            if tournament.max_participants % 2 != 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="For 2v2 tournaments, max_participants must be a multiple of 2"
                )
        elif "5v5" in tournament_name or "5vs5" in tournament_name:
            tournament_requires_team = True
            # Ensure max_participants is multiple of 5 for 5v5 tournaments
            if tournament.max_participants % 5 != 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="For 5v5 tournaments, max_participants must be a multiple of 5"
                )
        else:
            # Fallback to max_participants logic
            # For individual tournaments: max_participants typically 8, 16, 32, etc.
            # For team tournaments: max_participants typically 4 (2v2), 10 (5v5), etc.
            # If max_participants is small (2-4), it's likely a team tournament
            # If max_participants is larger (8+), it's likely individual
            if tournament.max_participants <= 4:
                tournament_requires_team = True
                # For small numbers, assume 2v2 and validate multiple of 2
                if tournament.max_participants % 2 != 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="For team tournaments with few participants, max_participants must be a multiple of 2"
                    )
            else:
                tournament_requires_team = False
        
        participant_id = current_user.id
        
        # For team tournaments, team_id is required
        if tournament_requires_team:
            if not team_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Team is required for this tournament type. Please select a team."
                )
            
            # Verify the team exists and user is a member
            team_data = await db.teams.find_one({"id": team_id})
            if not team_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Team not found"
                )
            
            from models import Team
            team = Team(**team_data)
            
            # Check if user is captain or member
            if current_user.id not in team.members:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You must be a member of the team to register it"
                )
            
            # Check if team game matches tournament game
            if team.game != tournament.game:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Team game ({team.game}) doesn't match tournament game ({tournament.game})"
                )
            
            # Use team ID as participant
            participant_id = team_id
        
        # For individual tournaments, team_id should not be provided (optional check)
        elif team_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This is an individual tournament. Team registration is not allowed."
            )
        
        # Check if already registered (user or team)
        if participant_id in tournament.participants:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already registered for this tournament"
            )
        
        # Check if tournament is full
        if len(tournament.participants) >= tournament.max_participants:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tournament is full"
            )
        
        # Register participant (user or team)
        await db.tournaments.update_one(
            {"id": tournament_id},
            {"$push": {"participants": participant_id}}
        )
        
        # Update user profile tournament count
        await db.user_profiles.update_one(
            {"user_id": current_user.id},
            {"$inc": {"total_tournaments": 1}},
            upsert=True
        )
        
        registration_type = "team" if team_id else "individual"
        logger.info(f"User {current_user.username} registered for tournament {tournament.title} as {registration_type}")
        
        # Invalidate tournament cache
        invalidate.invalidate_tournament_cache(tournament_id)
        
        return {"message": "Successfully registered for tournament", "type": registration_type}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering for tournament {tournament_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error registering for tournament"
        )

@router.get("/{tournament_id}/user-teams")
async def get_user_teams_for_tournament(
    tournament_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get user's teams that are eligible for tournament registration."""
    try:
        # Get tournament to check game type
        tournament_data = await db.tournaments.find_one({"id": tournament_id})
        if not tournament_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournament not found"
            )
        
        tournament = Tournament(**tournament_data)
        
        # Get user's teams for the tournament game
        user_teams = await db.teams.find({
            "members": {"$in": [current_user.id]},
            "game": tournament.game
        }).to_list(50)
        
        # Format teams with member info
        eligible_teams = []
        for team_data in user_teams:
            from models import Team
            team = Team(**team_data)
            
            # Get member names
            member_names = []
            for member_id in team.members:
                member = await db.users.find_one({"id": member_id})
                if member:
                    member_names.append({
                        "id": member["id"],
                        "username": member["username"]
                    })
            
            # Get captain name
            captain = await db.users.find_one({"id": team.captain_id})
            captain_name = captain["username"] if captain else "Unknown"
            
            eligible_teams.append({
                "id": team.id,
                "name": team.name,
                "game": team.game,
                "captain": captain_name,
                "is_captain": team.captain_id == current_user.id,
                "members": member_names,
                "member_count": len(team.members),
                "max_members": team.max_members,
                "description": team.description
            })
        
        # Determine if tournament requires team
        tournament_requires_team = False
        tournament_name = tournament.title.lower()
        
        # Check tournament name patterns first (most reliable)
        if "1v1" in tournament_name or "1vs1" in tournament_name:
            tournament_requires_team = False
        elif "2v2" in tournament_name or "2vs2" in tournament_name:
            tournament_requires_team = True
            # Validate max_participants is multiple of 2 for 2v2 tournaments
            if tournament.max_participants % 2 != 0:
                logger.warning(f"Tournament {tournament.title} has invalid max_participants ({tournament.max_participants}) for 2v2 tournament")
        elif "5v5" in tournament_name or "5vs5" in tournament_name:
            tournament_requires_team = True
            # Validate max_participants is multiple of 5 for 5v5 tournaments
            if tournament.max_participants % 5 != 0:
                logger.warning(f"Tournament {tournament.title} has invalid max_participants ({tournament.max_participants}) for 5v5 tournament")
        else:
            # Fallback to max_participants logic
            if tournament.max_participants <= 4:
                tournament_requires_team = True
            else:
                tournament_requires_team = False
        
        return {
            "tournament_id": tournament_id,
            "tournament_name": tournament.title, 
            "tournament_game": tournament.game,
            "requires_team": tournament_requires_team,
            "eligible_teams": eligible_teams,
            "can_register_individual": not tournament_requires_team
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user teams for tournament {tournament_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting user teams for tournament"
        )

@router.delete("/{tournament_id}")
async def delete_tournament(
    tournament_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a tournament (admin only). Cannot delete if tournament is in progress or completed."""
    try:
        # Check admin permissions
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can delete tournaments"
            )
        
        # Get tournament
        tournament_data = await db.tournaments.find_one({"id": tournament_id})
        if not tournament_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournament not found"
            )
        
        tournament = Tournament(**tournament_data)
        
        # Check if tournament can be deleted (prevent deletion of in-progress tournaments)
        if tournament.status == TournamentStatus.IN_PROGRESS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete tournament that is currently in progress"
            )
        
        # Clean up participant registrations first
        for participant_id in tournament.participants:
            # Update user profile tournament count
            await db.user_profiles.update_one(
                {"user_id": participant_id},
                {"$inc": {"total_tournaments": -1}},
                upsert=True
            )
        
        # Delete associated matches
        await db.matches.delete_many({"tournament_id": tournament_id})
        
        # Delete the tournament
        result = await db.tournaments.delete_one({"id": tournament_id})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournament not found"
            )
        
        logger.info(f"Tournament {tournament.title} deleted by admin {current_user.username}")
        
        return {"message": f"Tournament '{tournament.title}' has been successfully deleted"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting tournament {tournament_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting tournament"
        )

@router.delete("/{tournament_id}/register")
async def unregister_from_tournament(
    tournament_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Unregister current user from a tournament."""
    try:
        # Get tournament
        tournament_data = await db.tournaments.find_one({"id": tournament_id})
        if not tournament_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournament not found"
            )
        
        tournament = Tournament(**tournament_data)
        
        # Check if user is registered
        if current_user.id not in tournament.participants:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not registered for this tournament"
            )
        
        # Check if tournament hasn't started yet
        if tournament.status == TournamentStatus.IN_PROGRESS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot unregister from ongoing tournament"
            )
        
        # Unregister user
        await db.tournaments.update_one(
            {"id": tournament_id},
            {"$pull": {"participants": current_user.id}}
        )
        
        # Update user profile tournament count
        await db.user_profiles.update_one(
            {"user_id": current_user.id},
            {"$inc": {"total_tournaments": -1}}
        )
        
        logger.info(f"User {current_user.username} unregistered from tournament {tournament.title}")
        
        return {"message": "Successfully unregistered from tournament"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error unregistering from tournament {tournament_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error unregistering from tournament"
        )

@router.get("/{tournament_id}/participants-info")
async def get_tournament_participants_info(tournament_id: str):
    """Get detailed information about tournament participants (users and teams)."""
    try:
        # Get tournament
        tournament_data = await db.tournaments.find_one({"id": tournament_id})
        if not tournament_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournament not found"
            )

        tournament = Tournament(**tournament_data)
        participants_info = []

        for participant_id in tournament.participants:
            # Try to find as user first
            user_data = await db.users.find_one({"id": participant_id})
            if user_data:
                participants_info.append({
                    "id": participant_id,
                    "type": "user",
                    "name": user_data["username"],
                    "display_name": user_data["username"]
                })
                continue
            
            # Try to find as team
            team_data = await db.teams.find_one({"id": participant_id})
            if team_data:
                participants_info.append({
                    "id": participant_id,
                    "type": "team", 
                    "name": team_data["name"],
                    "display_name": f"{team_data['name']} ({len(team_data['members'])}/{team_data['max_members']})",
                    "members_count": len(team_data["members"]),
                    "max_members": team_data["max_members"]
                })
                continue
            
            # Fallback for unknown participants
            participants_info.append({
                "id": participant_id,
                "type": "unknown",
                "name": f"Participant {participant_id[:8]}",
                "display_name": f"Participant {participant_id[:8]}"
            })

        return {
            "tournament_id": tournament_id,
            "tournament_type": tournament.tournament_type,
            "participants": participants_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting tournament participants info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching participants information"
        )

@router.put("/{tournament_id}/status")
async def update_tournament_status(
    tournament_id: str,
    new_status: TournamentStatus,
    current_user: User = Depends(get_current_active_user)
):
    """Update tournament status. Only organizer or admin can do this."""
    try:
        # Get tournament
        tournament_data = await db.tournaments.find_one({"id": tournament_id})
        if not tournament_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournament not found"
            )
        
        tournament = Tournament(**tournament_data)
        
        # Check permissions
        if tournament.organizer_id != current_user.id and not is_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only tournament organizer or admin can update status"
            )
        
        # Update status
        await db.tournaments.update_one(
            {"id": tournament_id},
            {"$set": {"status": new_status, "updated_at": datetime.utcnow()}}
        )
        
        logger.info(f"Tournament {tournament.title} status updated to {new_status} by {current_user.username}")
        
        return {"message": f"Tournament status updated to {new_status}"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating tournament status {tournament_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating tournament status"
        )

@router.get("/stats/community")
async def get_tournament_stats():
    """Get tournament statistics for the community."""
    try:
        total_tournaments = await db.tournaments.count_documents({})
        active_tournaments = await db.tournaments.count_documents({"status": "in_progress"})
        upcoming_tournaments = await db.tournaments.count_documents({"status": "open"})
        completed_tournaments = await db.tournaments.count_documents({"status": "completed"})
        
        # Get tournaments by game
        pipeline = [
            {"$group": {"_id": "$game", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        games_stats = await db.tournaments.aggregate(pipeline).to_list(None)
        
        # Get recent tournament activity (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_tournaments = await db.tournaments.count_documents({
            "created_at": {"$gte": thirty_days_ago}
        })
        
        return {
            "total_tournaments": total_tournaments,
            "active_tournaments": active_tournaments,
            "upcoming_tournaments": upcoming_tournaments,
            "completed_tournaments": completed_tournaments,
            "games_popularity": [{"game": stat["_id"], "count": stat["count"]} for stat in games_stats],
            "recent_activity": recent_tournaments,
            "community_engagement": {
                "tournaments_per_month": recent_tournaments,
                "completion_rate": round((completed_tournaments / total_tournaments * 100) if total_tournaments > 0 else 0, 2)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting tournament stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching tournament statistics"
        )

@router.get("/templates/popular")
async def get_popular_tournament_templates():
    """Get popular CS2 tournament templates for Oupafamilly community."""
    templates = [
        {
            "name": "CS2 Quick Match 1v1",
            "description": "Duels rapides Counter-Strike 2 en 1v1",
            "game": "cs2",
            "tournament_type": "elimination",
            "max_participants": 16,
            "suggested_duration_hours": 3,
            "rules": """🎯 FORMAT: Élimination directe 1v1
🗺️ MAPS: aim_botz, aim_map (maps d'aim officielles)
⏱️ DURÉE: First to 16 frags par match
🔫 ARMES: AK47/M4A4 uniquement, pas d'AWP
💰 ÉCONOMIE: Argent illimité pour achats
📋 RÈGLES SPÉCIALES:
- Pas de camping (max 10 secondes statique)
- Restart possible si problème technique
- Screenshot obligatoire du score final"""
        },
        {
            "name": "CS2 Team Deathmatch 5v5",
            "description": "Affrontement classique 5v5 en mode Team Deathmatch",
            "game": "cs2",
            "tournament_type": "elimination",
            "max_participants": 32,
            "suggested_duration_hours": 5,
            "rules": """🎯 FORMAT: Élimination directe 5v5 Teams
🗺️ MAPS: Mirage, Inferno, Dust2, Cache (vote par équipe)
⏱️ DURÉE: First to 75 frags par équipe
🔫 ARMES: Toutes armes autorisées
💰 ÉCONOMIE: Argent illimité
📋 RÈGLES D'ÉQUIPE:
- Équipes fixes de 5 joueurs + 1 remplaçant
- Communication Discord obligatoire
- Capitaine d'équipe désigné
- Timeout autorisé (2 par équipe max)
🏆 FINALE: BO3 sur maps différentes"""
        },
        {
            "name": "CS2 Championship 5v5",
            "description": "Tournoi compétitif officiel format Major avec maps Active Duty 2025",
            "game": "cs2",
            "tournament_type": "bracket",
            "max_participants": 20,  # Multiple de 5 pour 5v5
            "suggested_duration_hours": 8,
            "rules": """🎯 FORMAT: Double élimination bracket 5v5
🗺️ MAPS Active Duty 2025: Ancient, Dust2, Inferno, Mirage, Nuke, Overpass, Train
⏱️ DURÉE: MR12 (Premier à 13 rounds)
🔫 ARMES: Règles compétitives officielles CS2 2025
💰 ÉCONOMIE: Système d'économie standard CS2
📋 RÈGLES COMPÉTITIVES:
- Ban/Pick de maps système Veto (Ban-Ban-Pick-Pick-Ban-Ban-Decider)
- Équipes fixes de 5 joueurs + 2 remplaçants maximum
- Overtime en MR3 (premier à 4 rounds) avec switch sides
- Time-out: 4 par équipe (30 secondes chacun)
- Anti-cheat requis + enregistrement démo obligatoire
🎮 NOUVEAUTÉS 2025:
- Overpass de retour (remplace Anubis)
- Train ajouté au pool officiel
🏆 STRUCTURE: Phases de groupe puis playoffs BO3"""
        },
        {
            "name": "CS2 Retake Masters",
            "description": "Spécialité mode Retake sur les sites des maps Active Duty 2025",
            "game": "cs2",
            "tournament_type": "round_robin",
            "max_participants": 16,
            "suggested_duration_hours": 4,
            "rules": """🎯 FORMAT: Round Robin mode Retake
🗺️ MAPS 2025: Sites A/B de Ancient, Dust2, Inferno, Mirage, Nuke, Overpass, Train
⏱️ DURÉE: 20 rounds retake par adversaire (10 par site)
🔫 ARMES: Kit retake prédéfini (AK/M4 + utility selon site)
💰 ÉCONOMIE: Équipement standardisé par map/site
📋 RÈGLES RETAKE:
- Terrorists spawn déjà sur site avec bombe plantée (35s timer)
- Counter-Terrorists doivent reprendre le site ou défuser
- Rotation automatique toutes les 5 rounds
- Points: +3 défuse, +2 site retake, +1 frag
🎮 SPÉCIFICITÉS 2025:
- Sites Overpass et Train: setups spéciaux
- Ancient sites: focus utility usage
🏆 CLASSEMENT: Cumul points + coefficient de difficulté par site"""
        },
        {
            "name": "CS2 Competitive 2v2",
            "description": "Format compétitif 2v2 sur les maps officielles Active Duty 2025",
            "game": "cs2",
            "tournament_type": "elimination",
            "max_participants": 8,  # Multiple de 2 pour 2v2
            "suggested_duration_hours": 4,
            "rules": """🎯 FORMAT: Élimination directe 2v2
🗺️ MAPS Active Duty 2025: Ancient, Dust2, Inferno, Mirage, Nuke, Overpass, Train
⏱️ DURÉE: MR12 (premier à 13 rounds)
🔫 ARMES: Toutes armes autorisées selon les règles compétitives
💰 ÉCONOMIE: Standard CS2 ($800 départ)
📋 RÈGLES ÉQUIPE:
- Équipes fixes de 2 joueurs exactement
- Substitution interdite en cours de match
- Pause technique: 2 minutes maximum par équipe
- Ban/Pick maps: Ban-Ban-Pick par équipe
🎮 CONFIGURATION 2025:
- Friendly fire: ON
- Buy time: 20 secondes
- Round time: 1:55 minutes
- Overtime: MR3 si égalité 12-12
🏆 AVANTAGE 2v2: Communication simplifiée, stratégies duo"""
        },
        {
            "name": "CS2 Pistol Masters",
            "description": "Tournoi exclusivement aux armes de poing - Maps Active Duty 2025",
            "game": "cs2",
            "tournament_type": "elimination",
            "max_participants": 16,
            "suggested_duration_hours": 3,
            "rules": """🎯 FORMAT: Élimination directe individuelle
🗺️ MAPS 2025: Sites sélectionnés d'Ancient, Dust2, Inferno, Mirage (zones mid/close)
⏱️ DURÉE: Premier à 16 frags par match
🔫 ARMES: Pistolets uniquement (Glock-18, USP-S, P2000, P250, Five-SeveN, Tec-9, CZ-75, Desert Eagle)
💰 ÉCONOMIE: 1000$ par round (round economy)
📋 RÈGLES PISTOLET:
- Kevlar + casque autorisé (round 3+)
- Grenades: 1 HE ou 1 Flash maximum
- Kit défusal interdit
- Zones de combat restreintes (no long angles)
🎮 ROUNDS SPÉCIAUX:
- Rounds 5,10,15: Deagle Only
- Rounds 7,14: No Kevlar challenge
- Round final: Classic pistols only (Glock/USP)
🏆 TECHNIQUE: Focus sur movement, crosshair placement et game sense"""
        }
    ]
    
    return {"templates": templates}