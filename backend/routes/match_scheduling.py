from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from models import User, Match, MatchStatus, Tournament
from auth import get_current_active_user, is_admin
from datetime import datetime, timedelta
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/match-scheduling", tags=["Match Scheduling"])

# Get database from database module
from database import db

# Modèles pour la planification des matchs

class MatchScheduleCreate(BaseModel):
    match_id: str
    scheduled_time: datetime
    notes: Optional[str] = None

class MatchScheduleUpdate(BaseModel):
    scheduled_time: Optional[datetime] = None
    notes: Optional[str] = None

class ScheduledMatch(BaseModel):
    id: str
    tournament_id: str
    tournament_name: str
    round_number: int
    match_number: int
    player1_name: Optional[str] = None
    player2_name: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    status: MatchStatus
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class TournamentSchedule(BaseModel):
    tournament_id: str
    tournament_name: str
    matches: List[ScheduledMatch]
    total_matches: int
    scheduled_matches: int
    pending_matches: int

# Fonctions utilitaires

async def get_participant_name(participant_id: str) -> str:
    """Récupérer le nom d'un participant (équipe ou joueur)."""
    try:
        # Chercher d'abord dans les équipes
        team = await db.teams.find_one({"id": participant_id})
        if team:
            return team.get("name", f"Équipe {participant_id[:8]}")
        
        # Sinon chercher dans les utilisateurs
        user = await db.users.find_one({"id": participant_id})
        if user:
            profile = await db.user_profiles.find_one({"user_id": participant_id})
            if profile:
                return profile.get("display_name", user.get("username", f"Joueur {participant_id[:8]}"))
            return user.get("username", f"Joueur {participant_id[:8]}")
        
        return f"Participant {participant_id[:8]}"
        
    except:
        return f"Participant {participant_id[:8]}"

async def enrich_match_with_names(match_data: Dict) -> ScheduledMatch:
    """Enrichir les données de match avec les noms des participants."""
    # Récupérer le nom du tournoi
    tournament = await db.tournaments.find_one({"id": match_data.get("tournament_id")})
    tournament_name = tournament.get("title", "Tournoi") if tournament else "Tournoi"
    
    # Récupérer les noms des participants
    player1_name = None
    player2_name = None
    
    if match_data.get("player1_id"):
        player1_name = await get_participant_name(match_data["player1_id"])
    
    if match_data.get("player2_id"):
        player2_name = await get_participant_name(match_data["player2_id"])
    
    return ScheduledMatch(
        id=match_data["id"],
        tournament_id=match_data["tournament_id"],
        tournament_name=tournament_name,
        round_number=match_data.get("round_number", 1),
        match_number=match_data.get("match_number", 1),
        player1_name=player1_name,
        player2_name=player2_name,
        scheduled_time=match_data.get("scheduled_time"),
        status=MatchStatus(match_data.get("status", "scheduled")),
        notes=match_data.get("notes"),
        created_at=match_data.get("created_at", datetime.utcnow()),
        updated_at=match_data.get("updated_at", datetime.utcnow())
    )

# Endpoints

@router.get("/tournament/{tournament_id}/matches", response_model=TournamentSchedule)
async def get_tournament_matches(
    tournament_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Obtenir tous les matchs d'un tournoi avec leur planification."""
    try:
        # Vérifier que le tournoi existe
        tournament = await db.tournaments.find_one({"id": tournament_id})
        if not tournament:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournoi non trouvé"
            )
        
        # Récupérer tous les matchs du tournoi
        matches_data = await db.matches.find({"tournament_id": tournament_id}).sort("round_number", 1).sort("match_number", 1).to_list(1000)
        
        # Enrichir les matchs avec les noms
        enriched_matches = []
        for match_data in matches_data:
            enriched_match = await enrich_match_with_names(match_data)
            enriched_matches.append(enriched_match)
        
        # Calculer les statistiques
        total_matches = len(enriched_matches)
        scheduled_matches = sum(1 for match in enriched_matches if match.scheduled_time is not None)
        pending_matches = total_matches - scheduled_matches
        
        return TournamentSchedule(
            tournament_id=tournament_id,
            tournament_name=tournament.get("title", "Tournoi"),
            matches=enriched_matches,
            total_matches=total_matches,
            scheduled_matches=scheduled_matches,
            pending_matches=pending_matches
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des matchs du tournoi: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des matchs"
        )

@router.post("/schedule-match", response_model=ScheduledMatch)
async def schedule_match(
    schedule_data: MatchScheduleCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Programmer un match (admin/organisateur seulement)."""
    try:
        # Vérifier que le match existe
        match_data = await db.matches.find_one({"id": schedule_data.match_id})
        if not match_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Match non trouvé"
            )
        
        # Vérifier les permissions (admin ou organisateur du tournoi)
        tournament = await db.tournaments.find_one({"id": match_data["tournament_id"]})
        if not tournament:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournoi non trouvé"
            )
        
        if not (is_admin(current_user) or tournament.get("organizer_id") == current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Seuls les administrateurs ou l'organisateur du tournoi peuvent programmer les matchs"
            )
        
        # Vérifier que la date n'est pas dans le passé
        if schedule_data.scheduled_time < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Impossible de programmer un match dans le passé"
            )
        
        # Vérifier que la date est dans la période du tournoi
        tournament_start = tournament.get("tournament_start")
        tournament_end = tournament.get("tournament_end")
        
        if tournament_start and schedule_data.scheduled_time < tournament_start:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le match ne peut pas être programmé avant le début du tournoi"
            )
        
        if tournament_end and schedule_data.scheduled_time > tournament_end:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le match ne peut pas être programmé après la fin du tournoi"
            )
        
        # Mettre à jour le match
        update_data = {
            "scheduled_time": schedule_data.scheduled_time,
            "updated_at": datetime.utcnow()
        }
        
        if schedule_data.notes:
            update_data["notes"] = schedule_data.notes
        
        await db.matches.update_one(
            {"id": schedule_data.match_id},
            {"$set": update_data}
        )
        
        # Récupérer le match mis à jour
        updated_match_data = await db.matches.find_one({"id": schedule_data.match_id})
        enriched_match = await enrich_match_with_names(updated_match_data)
        
        # Créer une activité
        from routes.activity import create_automatic_activity
        await create_automatic_activity(
            user_id=current_user.id,
            user_name=current_user.username,
            activity_type="match_scheduled",
            title="📅 Match programmé",
            description=f"A programmé le match {enriched_match.player1_name or 'TBD'} vs {enriched_match.player2_name or 'TBD'} pour le {schedule_data.scheduled_time.strftime('%d/%m/%Y à %H:%M')}",
            reference_id=schedule_data.match_id
        )
        
        logger.info(f"Match {schedule_data.match_id} programmé par {current_user.username} pour {schedule_data.scheduled_time}")
        
        return enriched_match
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la programmation du match: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la programmation du match"
        )

@router.put("/match/{match_id}/schedule", response_model=ScheduledMatch)
async def update_match_schedule(
    match_id: str,
    schedule_data: MatchScheduleUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Mettre à jour la programmation d'un match (admin/organisateur seulement)."""
    try:
        # Vérifier que le match existe
        match_data = await db.matches.find_one({"id": match_id})
        if not match_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Match non trouvé"
            )
        
        # Vérifier les permissions
        tournament = await db.tournaments.find_one({"id": match_data["tournament_id"]})
        if not tournament:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournoi non trouvé"
            )
        
        if not (is_admin(current_user) or tournament.get("organizer_id") == current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Seuls les administrateurs ou l'organisateur du tournoi peuvent modifier la programmation"
            )
        
        # Préparer les données de mise à jour
        update_data = {"updated_at": datetime.utcnow()}
        
        if schedule_data.scheduled_time is not None:
            # Vérifier que la nouvelle date n'est pas dans le passé
            if schedule_data.scheduled_time < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Impossible de programmer un match dans le passé"
                )
            update_data["scheduled_time"] = schedule_data.scheduled_time
        
        if schedule_data.notes is not None:
            update_data["notes"] = schedule_data.notes
        
        # Mettre à jour le match
        await db.matches.update_one(
            {"id": match_id},
            {"$set": update_data}
        )
        
        # Récupérer le match mis à jour
        updated_match_data = await db.matches.find_one({"id": match_id})
        enriched_match = await enrich_match_with_names(updated_match_data)
        
        logger.info(f"Programmation du match {match_id} mise à jour par {current_user.username}")
        
        return enriched_match
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour de la programmation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la mise à jour de la programmation"
        )

@router.delete("/match/{match_id}/schedule")
async def remove_match_schedule(
    match_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Supprimer la programmation d'un match (admin/organisateur seulement)."""
    try:
        # Vérifier que le match existe
        match_data = await db.matches.find_one({"id": match_id})
        if not match_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Match non trouvé"
            )
        
        # Vérifier les permissions
        tournament = await db.tournaments.find_one({"id": match_data["tournament_id"]})
        if not tournament:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournoi non trouvé"
            )
        
        if not (is_admin(current_user) or tournament.get("organizer_id") == current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Seuls les administrateurs ou l'organisateur du tournoi peuvent supprimer la programmation"
            )
        
        # Supprimer la programmation
        await db.matches.update_one(
            {"id": match_id},
            {
                "$unset": {"scheduled_time": "", "notes": ""},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        logger.info(f"Programmation du match {match_id} supprimée par {current_user.username}")
        
        return {"message": "Programmation supprimée avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la suppression de la programmation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la suppression de la programmation"
        )

@router.get("/upcoming-matches", response_model=List[ScheduledMatch])
async def get_upcoming_matches(
    days: int = Query(7, ge=1, le=30),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user)
):
    """Obtenir les matchs programmés dans les prochains jours."""
    try:
        # Calculer la plage de dates
        now = datetime.utcnow()
        future_date = now + timedelta(days=days)
        
        # Récupérer les matchs programmés
        matches_data = await db.matches.find({
            "scheduled_time": {
                "$gte": now,
                "$lte": future_date
            },
            "status": {"$in": ["scheduled", "in_progress"]}
        }).sort("scheduled_time", 1).limit(limit).to_list(limit)
        
        # Enrichir les matchs avec les noms
        enriched_matches = []
        for match_data in matches_data:
            enriched_match = await enrich_match_with_names(match_data)
            enriched_matches.append(enriched_match)
        
        return enriched_matches
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des matchs à venir: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la récupération des matchs à venir"
        )

@router.get("/schedule-conflicts/{tournament_id}")
async def check_schedule_conflicts(
    tournament_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Vérifier les conflits de programmation pour un tournoi."""
    try:
        # Récupérer tous les matchs programmés du tournoi
        matches_data = await db.matches.find({
            "tournament_id": tournament_id,
            "scheduled_time": {"$exists": True, "$ne": None}
        }).sort("scheduled_time", 1).to_list(1000)
        
        conflicts = []
        
        # Vérifier les conflits (matches à moins de 2 heures d'intervalle)
        for i, match1 in enumerate(matches_data):
            for match2 in matches_data[i+1:]:
                time1 = match1["scheduled_time"]
                time2 = match2["scheduled_time"]
                
                time_diff = abs((time2 - time1).total_seconds() / 3600)  # Différence en heures
                
                if time_diff < 2:  # Conflit si moins de 2 heures d'écart
                    conflicts.append({
                        "match1_id": match1["id"],
                        "match2_id": match2["id"],
                        "time_diff_hours": round(time_diff, 2),
                        "time1": time1,
                        "time2": time2
                    })
        
        return {
            "tournament_id": tournament_id,
            "total_scheduled_matches": len(matches_data),
            "conflicts": conflicts,
            "has_conflicts": len(conflicts) > 0
        }
        
    except Exception as e:
        logger.error(f"Erreur lors de la vérification des conflits: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la vérification des conflits"
        )