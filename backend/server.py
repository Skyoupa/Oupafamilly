from fastapi import FastAPI, APIRouter, Request
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List
import uuid
from datetime import datetime

# Import database
from database import db, client

# Import route modules
from routes import auth, tournaments, teams, matches, content, admin, community, profiles, currency, comments, chat, activity, betting, admin_economy, match_scheduling, monitoring, achievements, elo, steam, analytics, premium

# Configure structured logging and monitoring
from monitoring import configure_structured_logging, app_logger, RequestLoggingMiddleware
configure_structured_logging()

# Create rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create the main app without a prefix
app = FastAPI(
    title="Oupafamilly API",
    description="API pour la communauté multigaming Oupafamilly",
    version="1.0.0"
)

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Add rate limiting state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models (keeping original status check models)
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {
        "message": "Bienvenue sur l'API Oupafamilly",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "auth": "/api/auth",
            "tournaments": "/api/tournaments", 
            "teams": "/api/teams",
            "matches": "/api/matches",
            "content": "/api/content",
            "admin": "/api/admin",
            "community": "/api/community",
            "profiles": "/api/profiles",
            "currency": "/api/currency",
            "comments": "/api/comments",
            "chat": "/api/chat",
            "activity": "/api/activity",
            "betting": "/api/betting",
            "admin_economy": "/api/admin/economy",
            "match_scheduling": "/api/match-scheduling",
            "achievements": "/api/achievements",
            "elo": "/api/elo"
        }
    }

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Health check endpoint
@api_router.get("/health")
async def health_check():
    try:
        # Test database connection
        await db.command("ping")
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        return {
            "status": "unhealthy", 
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow()
        }

# Include route modules
api_router.include_router(auth.router)
api_router.include_router(tournaments.router)
api_router.include_router(teams.router)
api_router.include_router(matches.router)
api_router.include_router(content.router)
api_router.include_router(admin.router)
api_router.include_router(community.router)
api_router.include_router(profiles.router)
api_router.include_router(currency.router)
api_router.include_router(comments.router)
api_router.include_router(chat.router)
api_router.include_router(activity.router)
api_router.include_router(betting.router)
api_router.include_router(admin_economy.router)
api_router.include_router(match_scheduling.router)
api_router.include_router(monitoring.router)
api_router.include_router(achievements.router)
api_router.include_router(elo.router)
api_router.include_router(steam.router)
api_router.include_router(analytics.router)
api_router.include_router(premium.router)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[
        "http://localhost:3000",  # Développement local
        "http://127.0.0.1:3000",  # Développement local alternative
        # Ajoutez vos domaines de production ici :
        # "https://votre-domaine.com",
        # "https://www.votre-domaine.com"
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin", "User-Agent"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
