from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
from models import User, UserResponse, CommunityStats, UserRole, UserStatus
from auth import get_current_active_user, get_admin_user, is_admin
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["Administration"])

# Get database from database module
from database import db

@router.get("/dashboard")
async def get_admin_dashboard(current_user: User = Depends(get_admin_user)):
    """Get comprehensive admin dashboard data for community management."""
    try:
        # User statistics
        total_users = await db.users.count_documents({})
        active_users = await db.users.count_documents({"status": "active"})
        pending_users = await db.users.count_documents({"status": "pending"})
        
        # Recent activity (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        new_users_week = await db.users.count_documents({"created_at": {"$gte": week_ago}})
        
        # Tournament statistics
        total_tournaments = await db.tournaments.count_documents({})
        active_tournaments = await db.tournaments.count_documents({"status": "in_progress"})
        upcoming_tournaments = await db.tournaments.count_documents({"status": "open"})
        
        # Content statistics
        total_news = await db.news.count_documents({"is_published": True})
        total_tutorials = await db.tutorials.count_documents({"is_published": True})
        
        # Recent user registrations (last 5)
        recent_users = await db.users.find({}).sort("created_at", -1).limit(5).to_list(5)
        
        # Most active users (by tournament participation)
        pipeline = [
            {"$group": {"_id": "$user_id", "tournament_count": {"$sum": "$total_tournaments"}}},
            {"$sort": {"tournament_count": -1}},
            {"$limit": 5}
        ]
        active_users_data = await db.user_profiles.aggregate(pipeline).to_list(5)
        
        return {
            "community_overview": {
                "total_members": total_users,
                "active_members": active_users,
                "pending_members": pending_users,
                "growth_this_week": new_users_week,
                "activity_rate": round((active_users / total_users * 100) if total_users > 0 else 0, 2)
            },
            "tournaments": {
                "total": total_tournaments,
                "active": active_tournaments,
                "upcoming": upcoming_tournaments
            },
            "content": {
                "news_articles": total_news,
                "tutorials": total_tutorials
            },
            "recent_members": [
                {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"],
                    "status": user["status"],
                    "created_at": user["created_at"]
                } for user in recent_users
            ],
            "community_health": {
                "engagement_score": min(100, (active_tournaments + total_tutorials + new_users_week) * 10),
                "needs_attention": pending_users > 0 or active_users < (total_users * 0.5)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting admin dashboard: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching dashboard data"
        )

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    current_user: User = Depends(get_admin_user),
    status: Optional[UserStatus] = None,
    role: Optional[UserRole] = None,
    limit: int = Query(50, le=200),
    skip: int = Query(0, ge=0)
):
    """Get all users with filtering options."""
    try:
        filter_dict = {}
        if status:
            filter_dict["status"] = status
        if role:
            filter_dict["role"] = role
        
        users = await db.users.find(filter_dict).skip(skip).limit(limit).to_list(limit)
        
        return [
            UserResponse(
                id=user["id"],
                username=user["username"],
                email=user["email"],
                role=user["role"],
                status=user["status"],
                created_at=user["created_at"],
                is_verified=user["is_verified"]
            ) for user in users
        ]
        
    except Exception as e:
        logger.error(f"Error getting users: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching users"
        )

@router.put("/users/{user_id}/status")
async def update_user_status(
    user_id: str,
    new_status: UserStatus,
    current_user: User = Depends(get_admin_user)
):
    """Update user status."""
    try:
        result = await db.users.update_one(
            {"id": user_id},
            {"$set": {"status": new_status, "updated_at": datetime.utcnow()}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"User {user_id} status updated to {new_status} by admin {current_user.username}")
        
        return {"message": f"User status updated to {new_status}"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user status"
        )

@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: str,
    new_role: UserRole,
    current_user: User = Depends(get_admin_user)
):
    """Update user role."""
    try:
        # Prevent admin from demoting themselves
        if user_id == current_user.id and new_role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot change your own admin role"
            )
        
        result = await db.users.update_one(
            {"id": user_id},
            {"$set": {"role": new_role, "updated_at": datetime.utcnow()}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"User {user_id} role updated to {new_role} by admin {current_user.username}")
        
        return {"message": f"User role updated to {new_role}"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user role: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user role"
        )

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_admin_user)
):
    """Delete a user (use with caution in growing community)."""
    try:
        # Prevent admin from deleting themselves
        if user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete your own account"
            )
        
        # Delete user profile first
        await db.user_profiles.delete_one({"user_id": user_id})
        
        # Delete user
        result = await db.users.delete_one({"id": user_id})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"User {user_id} deleted by admin {current_user.username}")
        
        return {"message": "User deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user"
        )

@router.get("/community-growth")
async def get_community_growth_stats(
    current_user: User = Depends(get_admin_user),
    days: int = Query(30, ge=7, le=365)
):
    """Get community growth statistics over time."""
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Daily user registrations
        pipeline = [
            {"$match": {"created_at": {"$gte": start_date}}},
            {
                "$group": {
                    "_id": {
                        "year": {"$year": "$created_at"},
                        "month": {"$month": "$created_at"},
                        "day": {"$dayOfMonth": "$created_at"}
                    },
                    "registrations": {"$sum": 1}
                }
            },
            {"$sort": {"_id.year": 1, "_id.month": 1, "_id.day": 1}}
        ]
        daily_registrations = await db.users.aggregate(pipeline).to_list(None)
        
        # Tournament participation over time
        tournament_pipeline = [
            {"$match": {"created_at": {"$gte": start_date}}},
            {
                "$group": {
                    "_id": {
                        "year": {"$year": "$created_at"},
                        "month": {"$month": "$created_at"},
                        "day": {"$dayOfMonth": "$created_at"}
                    },
                    "tournaments": {"$sum": 1}
                }
            },
            {"$sort": {"_id.year": 1, "_id.month": 1, "_id.day": 1}}
        ]
        daily_tournaments = await db.tournaments.aggregate(tournament_pipeline).to_list(None)
        
        # User retention (users still active after registration)
        total_users = await db.users.count_documents({"created_at": {"$gte": start_date}})
        active_new_users = await db.users.count_documents({
            "created_at": {"$gte": start_date},
            "status": "active"
        })
        
        retention_rate = round((active_new_users / total_users * 100) if total_users > 0 else 0, 2)
        
        return {
            "period_days": days,
            "daily_registrations": [
                {
                    "date": f"{item['_id']['year']}-{item['_id']['month']:02d}-{item['_id']['day']:02d}",
                    "count": item["registrations"]
                } for item in daily_registrations
            ],
            "daily_tournaments": [
                {
                    "date": f"{item['_id']['year']}-{item['_id']['month']:02d}-{item['_id']['day']:02d}",
                    "count": item["tournaments"]
                } for item in daily_tournaments
            ],
            "summary": {
                "total_new_users": total_users,
                "active_new_users": active_new_users,
                "retention_rate": retention_rate,
                "average_daily_registrations": round(total_users / days, 2) if days > 0 else 0
            },
            "growth_trend": "growing" if total_users > 0 else "starting"
        }
        
    except Exception as e:
        logger.error(f"Error getting community growth stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching growth statistics"
        )

@router.post("/announcements/broadcast")
async def broadcast_announcement(
    message: str,
    title: str,
    current_user: User = Depends(get_admin_user)
):
    """Broadcast an important announcement to all community members."""
    try:
        from models import News, NewsCreate
        
        # Create a pinned news article for the announcement
        announcement = News(
            title=f"📢 {title}",
            content=message,
            summary=message[:200] + "..." if len(message) > 200 else message,
            author_id=current_user.id,
            is_published=True,
            is_pinned=True,
            tags=["announcement", "important"]
        )
        
        await db.news.insert_one(announcement.dict())
        
        logger.info(f"Announcement broadcasted: {title} by admin {current_user.username}")
        
        return {
            "message": "Announcement broadcasted successfully",
            "announcement_id": announcement.id,
            "title": title,
            "content": message
        }
        
    except Exception as e:
        logger.error(f"Error broadcasting announcement: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error broadcasting announcement"
        )

@router.get("/moderation/reports")
async def get_moderation_reports(current_user: User = Depends(get_admin_user)):
    """Get items that might need moderation attention."""
    try:
        # For a growing community, focus on key metrics that need attention
        
        # Users with pending status
        pending_users = await db.users.find({"status": "pending"}).to_list(None)
        
        # Recently created content that might need review
        recent_tutorials = await db.tutorials.find({
            "created_at": {"$gte": datetime.utcnow() - timedelta(days=7)},
            "is_published": True
        }).to_list(None)
        
        # Tournaments with no participants (might be poorly configured)
        empty_tournaments = await db.tournaments.find({
            "status": "open",
            "participants": {"$size": 0},
            "registration_end": {"$gte": datetime.utcnow()}
        }).to_list(None)
        
        return {
            "pending_users": [
                {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"],
                    "created_at": user["created_at"]
                } for user in pending_users
            ],
            "recent_tutorials": [
                {
                    "id": tutorial["id"],
                    "title": tutorial["title"],
                    "game": tutorial["game"],
                    "author_id": tutorial["author_id"],
                    "created_at": tutorial["created_at"]
                } for tutorial in recent_tutorials
            ],
            "empty_tournaments": [
                {
                    "id": tournament["id"],
                    "title": tournament["title"],
                    "game": tournament["game"],
                    "organizer_id": tournament["organizer_id"],
                    "registration_end": tournament["registration_end"]
                } for tournament in empty_tournaments
            ],
            "attention_needed": len(pending_users) > 0 or len(empty_tournaments) > 0
        }
        
    except Exception as e:
        logger.error(f"Error getting moderation reports: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching moderation reports"
        )