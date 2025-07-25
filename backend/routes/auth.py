from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta, datetime
from models import (
    User, UserCreate, UserLogin, UserResponse, UserProfile, 
    UserProfileResponse, UserUpdate, Token, UserRole, UserStatus
)
from auth import (
    authenticate_user, create_access_token, get_password_hash,
    get_current_active_user, get_user_by_email, ACCESS_TOKEN_EXPIRE_MINUTES,
    pwd_context
)
from motor.motor_asyncio import AsyncIOMotorClient
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Get database from database module
from database import db

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    """Register a new user."""
    try:
        # Check if user already exists
        existing_user = await get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if username already exists
        existing_username = await db.users.find_one({"username": user_data.username})
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            role=UserRole.MEMBER,
            status=UserStatus.ACTIVE  # For a starting community, auto-activate users
        )
        
        # Insert user into database
        await db.users.insert_one(new_user.dict())
        
        # Create user profile
        user_profile = UserProfile(
            user_id=new_user.id,
            display_name=user_data.display_name
        )
        await db.user_profiles.insert_one(user_profile.dict())
        
        logger.info(f"New user registered: {user_data.email}")
        
        return UserResponse(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            role=new_user.role,
            status=new_user.status,
            created_at=new_user.created_at,
            is_verified=new_user.is_verified
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )

@router.post("/login", response_model=Token)
async def login_user(user_credentials: UserLogin):
    """Login user and return access token."""
    try:
        user = await authenticate_user(db, user_credentials.email, user_credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Update last login
        await db.users.update_one(
            {"id": user.id},
            {"$set": {"last_login": user.updated_at}}
        )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        logger.info(f"User logged in: {user_credentials.email}")
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error logging in user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error logging in"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information."""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
        status=current_user.status,
        created_at=current_user.created_at,
        is_verified=current_user.is_verified
    )

@router.get("/profile", response_model=UserProfileResponse)
async def get_user_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user profile."""
    try:
        profile_data = await db.user_profiles.find_one({"user_id": current_user.id})
        if not profile_data:
            # Create default profile if doesn't exist
            profile = UserProfile(
                user_id=current_user.id,
                display_name=current_user.username
            )
            await db.user_profiles.insert_one(profile.dict())
            profile_data = profile.dict()
        
        return UserProfileResponse(**profile_data)
        
    except Exception as e:
        logger.error(f"Error getting user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting profile"
        )

@router.put("/profile", response_model=UserProfileResponse)
async def update_user_profile(
    profile_update: UserUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update current user profile."""
    try:
        update_data = {k: v for k, v in profile_update.dict().items() if v is not None}
        update_data["updated_at"] = current_user.updated_at
        
        result = await db.user_profiles.update_one(
            {"user_id": current_user.id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found"
            )
        
        # Get updated profile
        updated_profile = await db.user_profiles.find_one({"user_id": current_user.id})
        return UserProfileResponse(**updated_profile)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating profile"
        )

@router.get("/stats")
async def get_auth_stats(current_user: User = Depends(get_current_active_user)):
    """Get authentication statistics - useful for a growing community."""
    try:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        total_users = await db.users.count_documents({})
        active_users = await db.users.count_documents({"status": "active"})
        pending_users = await db.users.count_documents({"status": "pending"})
        
        # Get recent registrations (last 7 days)
        from datetime import datetime, timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_registrations = await db.users.count_documents({
            "created_at": {"$gte": week_ago}
        })
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "pending_users": pending_users,
            "recent_registrations": recent_registrations,
            "community_growth": {
                "week": recent_registrations,
                "active_percentage": round((active_users / total_users * 100) if total_users > 0 else 0, 2)
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting auth stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting statistics"
        )

@router.delete("/delete-account")
async def delete_user_account(
    current_user: User = Depends(get_current_active_user)
):
    """Delete the current user's account and all associated data."""
    try:
        # Check if user is admin (prevent admin deletion)
        if current_user.role == "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin accounts cannot be deleted. Please contact support."
            )
        
        user_id = current_user.id
        username = current_user.username
        
        # Clean up user data from various collections
        
        # Remove user from all teams
        await db.teams.update_many(
            {"members": {"$in": [user_id]}},
            {"$pull": {"members": user_id}}
        )
        
        # Transfer team captaincy or delete teams if user is captain
        captain_teams = await db.teams.find({"captain_id": user_id}).to_list(100)
        for team_data in captain_teams:
            from models import Team
            team = Team(**team_data)
            if len(team.members) > 1:
                # Transfer captaincy to first available member
                new_captain = team.members[0] if team.members[0] != user_id else team.members[1]
                await db.teams.update_one(
                    {"id": team.id},
                    {
                        "$set": {"captain_id": new_captain},
                        "$pull": {"members": user_id}
                    }
                )
            else:
                # Delete team if user is the only member
                await db.teams.delete_one({"id": team.id})
        
        # Remove user from tournament participants
        await db.tournaments.update_many(
            {"participants": {"$in": [user_id]}},
            {"$pull": {"participants": user_id}}
        )
        
        # Delete user profile
        await db.user_profiles.delete_one({"user_id": user_id})
        
        # Delete user's content (news, tutorials where they are author)
        await db.news.delete_many({"author_id": user_id})
        await db.tutorials.delete_many({"author_id": user_id})
        
        # Finally, delete the user account
        result = await db.users.delete_one({"id": user_id})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User account not found"
            )
        
        logger.info(f"User account {username} ({user_id}) deleted successfully with all associated data")
        
        return {
            "message": f"Account '{username}' has been permanently deleted along with all associated data",
            "deleted_data": {
                "teams_updated": len(captain_teams),
                "profile_deleted": True,
                "content_deleted": True
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user account {current_user.id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user account"
        )

@router.post("/request-password-reset")
async def request_password_reset(email: str):
    """Request a password reset email."""
    try:
        # Find user by email
        user_data = await db.users.find_one({"email": email.lower()})
        if not user_data:
            # Don't reveal if email exists or not for security
            return {"message": "If this email is registered, you will receive a password reset link"}
        
        user = User(**user_data)
        
        # Generate reset token (in real app, use secure random token and store with expiry)
        import secrets
        import time
        
        reset_token = secrets.token_urlsafe(32)
        reset_expires = int(time.time()) + 3600  # 1 hour from now
        
        # Store reset token in database (you might want a separate collection for this)
        await db.password_resets.insert_one({
            "user_id": user.id,
            "email": user.email,
            "token": reset_token,
            "expires_at": reset_expires,
            "used": False,
            "created_at": datetime.utcnow()
        })
        
        # In a real application, you would send an email here
        # For now, we'll just log the reset link
        reset_link = f"http://localhost:3000/reset-password?token={reset_token}"
        logger.info(f"Password reset requested for {email}. Reset link: {reset_link}")
        
        # Return success message (same for existing and non-existing emails)
        return {
            "message": "If this email is registered, you will receive a password reset link",
            "reset_link": reset_link  # Remove this in production
        }
        
    except Exception as e:
        logger.error(f"Error requesting password reset for {email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing password reset request"
        )

@router.post("/reset-password")
async def reset_password(
    token: str,
    new_password: str
):
    """Reset password using reset token."""
    try:
        import time
        
        # Find valid reset token
        reset_data = await db.password_resets.find_one({
            "token": token,
            "used": False,
            "expires_at": {"$gt": int(time.time())}
        })
        
        if not reset_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        
        # Validate new password
        if len(new_password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 6 characters"
            )
        
        # Hash new password
        hashed_password = pwd_context.hash(new_password)
        
        # Update user password
        result = await db.users.update_one(
            {"id": reset_data["user_id"]},
            {"$set": {
                "hashed_password": hashed_password,
                "updated_at": datetime.utcnow()
            }}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Mark reset token as used
        await db.password_resets.update_one(
            {"token": token},
            {"$set": {"used": True, "used_at": datetime.utcnow()}}
        )
        
        logger.info(f"Password reset completed for user {reset_data['user_id']}")
        
        return {"message": "Password has been successfully reset"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resetting password with token {token}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error resetting password"
        )