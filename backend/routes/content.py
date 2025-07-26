from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from models import News, NewsCreate, User, Tutorial, TutorialCreate, Game, Tournament
from auth import get_current_active_user, is_moderator_or_admin
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/content", tags=["Content"])

# Get database from database module
from database import db

# News/Announcements Routes
@router.post("/news", response_model=News)
async def create_news(
    news_data: NewsCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a news article. For growing community, allow moderators and admins."""
    try:
        if not is_moderator_or_admin(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only moderators and admins can create news"
            )
        
        new_news = News(
            **news_data.dict(),
            author_id=current_user.id,
            is_published=True  # For small community, auto-publish
        )
        
        await db.news.insert_one(new_news.dict())
        
        logger.info(f"News created: {news_data.title} by {current_user.username}")
        
        return new_news
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating news: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating news article"
        )

@router.get("/news", response_model=List[News])
async def get_news(
    limit: int = Query(10, le=50),
    skip: int = Query(0, ge=0),
    pinned_only: bool = False
):
    """Get news articles."""
    try:
        filter_dict = {"is_published": True}
        if pinned_only:
            filter_dict["is_pinned"] = True
        
        # Sort by pinned first, then by creation date
        sort_criteria = [("is_pinned", -1), ("created_at", -1)]
        
        news_list = await db.news.find(filter_dict).sort(sort_criteria).skip(skip).limit(limit).to_list(limit)
        return [News(**news_item) for news_item in news_list]
        
    except Exception as e:
        logger.error(f"Error getting news: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching news"
        )

@router.get("/news/{news_id}", response_model=News)
async def get_news_article(news_id: str):
    """Get a specific news article and increment view count."""
    try:
        # Increment view count
        await db.news.update_one(
            {"id": news_id},
            {"$inc": {"views": 1}}
        )
        
        news_data = await db.news.find_one({"id": news_id, "is_published": True})
        if not news_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="News article not found"
            )
        
        return News(**news_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting news article {news_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching news article"
        )

# Tutorial Routes
@router.post("/tutorials", response_model=Tutorial)
async def create_tutorial(
    tutorial_data: TutorialCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a tutorial. Allow any member to contribute tutorials."""
    try:
        new_tutorial = Tutorial(
            **tutorial_data.dict(),
            author_id=current_user.id,
            is_published=True  # For growing community, auto-publish with community moderation
        )
        
        await db.tutorials.insert_one(new_tutorial.dict())
        
        logger.info(f"Tutorial created: {tutorial_data.title} by {current_user.username}")
        
        return new_tutorial
        
    except Exception as e:
        logger.error(f"Error creating tutorial: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating tutorial"
        )

@router.get("/tutorials", response_model=List[Tutorial])
async def get_tutorials(
    game: Optional[Game] = None,
    level: Optional[str] = None,
    limit: int = Query(100, le=100),
    skip: int = Query(0, ge=0)
):
    """Get tutorials with optional filtering."""
    try:
        filter_dict = {"is_published": True}
        if game:
            filter_dict["game"] = game
        if level:
            filter_dict["level"] = level
        
        tutorials = await db.tutorials.find(filter_dict).sort([("sort_order", 1), ("created_at", -1)]).skip(skip).limit(limit).to_list(limit)
        return [Tutorial(**tutorial) for tutorial in tutorials]
        
    except Exception as e:
        logger.error(f"Error getting tutorials: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching tutorials"
        )

@router.get("/tutorials/{tutorial_id}", response_model=Tutorial)
async def get_tutorial(tutorial_id: str):
    """Get a specific tutorial and increment view count."""
    try:
        # Increment view count
        await db.tutorials.update_one(
            {"id": tutorial_id},
            {"$inc": {"views": 1}}
        )
        
        tutorial_data = await db.tutorials.find_one({"id": tutorial_id, "is_published": True})
        if not tutorial_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tutorial not found"
            )
        
        return Tutorial(**tutorial_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting tutorial {tutorial_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching tutorial"
        )

@router.post("/tutorials/{tutorial_id}/like")
async def like_tutorial(
    tutorial_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Like a tutorial."""
    try:
        # Check if tutorial exists
        tutorial_data = await db.tutorials.find_one({"id": tutorial_id})
        if not tutorial_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tutorial not found"
            )
        
        # For simplicity in a growing community, allow multiple likes for now
        # In a more mature system, you'd track individual likes
        await db.tutorials.update_one(
            {"id": tutorial_id},
            {"$inc": {"likes": 1}}
        )
        
        return {"message": "Tutorial liked successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error liking tutorial {tutorial_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error liking tutorial"
        )

@router.get("/tutorials/by-game/{game}")
async def get_tutorials_by_game(game: Game):
    """Get tutorials organized by skill level for a specific game."""
    try:
        levels = ["beginner", "intermediate", "expert"]
        result = {}
        
        for level in levels:
            tutorials = await db.tutorials.find({
                "game": game,
                "level": level,
                "is_published": True
            }).sort([("sort_order", 1), ("created_at", -1)]).to_list(None)
            
            result[level] = [Tutorial(**tutorial) for tutorial in tutorials]
        
        return {
            "game": game,
            "tutorials_by_level": result,
            "total_tutorials": sum(len(result[level]) for level in levels)
        }
        
    except Exception as e:
        logger.error(f"Error getting tutorials for game {game}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching tutorials by game"
        )

@router.get("/stats/content")
async def get_content_stats(current_user: User = Depends(get_current_active_user)):
    """Get content statistics - useful for community growth tracking."""
    try:
        # News stats
        total_news = await db.news.count_documents({"is_published": True})
        pinned_news = await db.news.count_documents({"is_published": True, "is_pinned": True})
        
        # Tutorial stats
        total_tutorials = await db.tutorials.count_documents({"is_published": True})
        
        # Tutorials by game
        pipeline = [
            {"$match": {"is_published": True}},
            {"$group": {"_id": "$game", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        tutorials_by_game = await db.tutorials.aggregate(pipeline).to_list(None)
        
        # Recent content (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_news = await db.news.count_documents({
            "created_at": {"$gte": thirty_days_ago},
            "is_published": True
        })
        recent_tutorials = await db.tutorials.count_documents({
            "created_at": {"$gte": thirty_days_ago},
            "is_published": True
        })
        
        # Top viewed content
        top_news = await db.news.find(
            {"is_published": True}
        ).sort("views", -1).limit(5).to_list(5)
        
        top_tutorials = await db.tutorials.find(
            {"is_published": True}
        ).sort("views", -1).limit(5).to_list(5)
        
        return {
            "news": {
                "total": total_news,
                "pinned": pinned_news,
                "recent": recent_news,
                "top_viewed": [{"id": item["id"], "title": item["title"], "views": item["views"]} for item in top_news]
            },
            "tutorials": {
                "total": total_tutorials,
                "recent": recent_tutorials,
                "by_game": [{"game": stat["_id"], "count": stat["count"]} for stat in tutorials_by_game],
                "top_viewed": [{"id": item["id"], "title": item["title"], "views": item["views"]} for item in top_tutorials]
            },
            "community_engagement": {
                "content_per_month": recent_news + recent_tutorials,
                "tutorials_per_game": dict((stat["_id"], stat["count"]) for stat in tutorials_by_game)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting content stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching content statistics"
        )

@router.get("/welcome/new-member")
async def get_welcome_content():
    """Get welcome content for new community members."""
    try:
        # Get pinned announcements
        welcome_news = await db.news.find({
            "is_published": True,
            "is_pinned": True
        }).sort("created_at", -1).limit(3).to_list(3)
        
        # Get beginner tutorials across all games
        beginner_tutorials = await db.tutorials.find({
            "is_published": True,
            "level": "beginner"
        }).sort("views", -1).limit(10).to_list(10)
        
        # Get upcoming tournaments
        upcoming_tournaments = await db.tournaments.find({
            "status": "open",
            "registration_end": {"$gte": datetime.utcnow()}
        }).sort("tournament_start", 1).limit(5).to_list(5)
        
        return {
            "welcome_message": "Bienvenue dans la communauté Oupafamilly ! 🎮",
            "important_announcements": [News(**news) for news in welcome_news],
            "getting_started_tutorials": [Tutorial(**tutorial) for tutorial in beginner_tutorials],
            "upcoming_events": [Tournament(**tournament) for tournament in upcoming_tournaments],
            "community_tips": [
                "Complète ton profil avec tes jeux favoris",
                "Consulte les tutoriels pour améliorer tes compétences",
                "Participe aux tournois pour rencontrer d'autres joueurs",
                "N'hésite pas à poser des questions sur Discord"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting welcome content: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching welcome content"
        )

@router.delete("/news/{news_id}")
async def delete_news(
    news_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a news article. Only moderators, admins, or the author can delete."""
    try:
        # Get the news article
        news_data = await db.news.find_one({"id": news_id})
        if not news_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="News article not found"
            )
        
        news = News(**news_data)
        
        # Check permissions: admin, moderator, or author
        if (current_user.role not in ["admin", "moderator"] and 
            current_user.id != news.author_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators, moderators, or the author can delete this news article"
            )
        
        # Delete the news article
        result = await db.news.delete_one({"id": news_id})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="News article not found"
            )
        
        logger.info(f"News article '{news.title}' deleted by {current_user.username}")
        
        return {"message": f"News article '{news.title}' has been successfully deleted"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting news {news_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting news article"
        )

@router.delete("/tutorials/{tutorial_id}")
async def delete_tutorial(
    tutorial_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a tutorial. Only moderators, admins, or the author can delete."""
    try:
        # Get the tutorial
        tutorial_data = await db.tutorials.find_one({"id": tutorial_id})
        if not tutorial_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tutorial not found"
            )
        
        tutorial = Tutorial(**tutorial_data)
        
        # Check permissions: admin, moderator, or author
        if (current_user.role not in ["admin", "moderator"] and 
            current_user.id != tutorial.author_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators, moderators, or the author can delete this tutorial"
            )
        
        # Delete the tutorial
        result = await db.tutorials.delete_one({"id": tutorial_id})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tutorial not found"
            )
        
        logger.info(f"Tutorial '{tutorial.title}' deleted by {current_user.username}")
        
        return {"message": f"Tutorial '{tutorial.title}' has been successfully deleted"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting tutorial {tutorial_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting tutorial"
        )