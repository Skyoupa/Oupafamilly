from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

# Enums
class UserRole(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator" 
    MEMBER = "member"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class TournamentStatus(str, Enum):
    DRAFT = "draft"
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TournamentType(str, Enum):
    ELIMINATION = "elimination"
    BRACKET = "bracket"
    ROUND_ROBIN = "round_robin"

class MatchStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Game(str, Enum):
    CS2 = "cs2"
    WOW = "wow"
    LOL = "lol"
    SC2 = "sc2"
    MINECRAFT = "minecraft"

# User Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: EmailStr
    hashed_password: str
    role: UserRole = UserRole.MEMBER
    status: UserStatus = UserStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    is_verified: bool = False

class UserProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    display_name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None  # Support for base64 encoded images
    banner_url: Optional[str] = None
    location: Optional[str] = None
    favorite_games: List[Game] = []
    gaming_experience: Dict[Game, str] = {}  # game -> level (beginner, intermediate, expert)
    discord_username: Optional[str] = None
    twitch_username: Optional[str] = None
    steam_profile: Optional[str] = None
    total_tournaments: int = 0
    tournaments_won: int = 0
    # Trophy tracking by game mode
    trophies_1v1: int = 0
    trophies_2v2: int = 0
    trophies_5v5: int = 0
    total_points: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    display_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    favorite_games: Optional[List[Game]] = None
    gaming_experience: Optional[Dict[Game, str]] = None
    discord_username: Optional[str] = None
    twitch_username: Optional[str] = None
    steam_profile: Optional[str] = None

# Team Models
class Team(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    captain_id: str
    members: List[str] = []  # user_ids
    game: Game
    max_members: int = 6  # Maximum 6 members as requested
    is_open: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TeamCreate(BaseModel):
    name: str
    description: Optional[str] = None
    game: Game
    max_members: int = 6  # Maximum 6 members as requested

# Tournament Models
class Tournament(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    game: Game
    tournament_type: TournamentType
    max_participants: int
    entry_fee: float = 0.0
    prize_pool: float = 0.0
    status: TournamentStatus = TournamentStatus.DRAFT
    registration_start: datetime
    registration_end: datetime
    tournament_start: datetime
    tournament_end: Optional[datetime] = None
    rules: str
    organizer_id: str
    participants: List[str] = []  # user_ids or team_ids
    matches: List[str] = []  # match_ids
    winner_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TournamentCreate(BaseModel):
    title: str
    description: str
    game: Game
    tournament_type: TournamentType
    max_participants: int
    entry_fee: float = 0.0
    prize_pool: float = 0.0
    registration_start: datetime
    registration_end: datetime
    tournament_start: datetime
    rules: str

# Match Models
class Match(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tournament_id: str
    round_number: int
    match_number: int
    player1_id: Optional[str] = None
    player2_id: Optional[str] = None
    winner_id: Optional[str] = None
    player1_score: int = 0
    player2_score: int = 0
    status: MatchStatus = MatchStatus.SCHEDULED
    scheduled_time: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class MatchCreate(BaseModel):
    tournament_id: str
    round_number: int
    match_number: int
    player1_id: Optional[str] = None
    player2_id: Optional[str] = None
    scheduled_time: Optional[datetime] = None

# Tutorial Models
class Tutorial(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    game: Game
    level: str  # beginner, intermediate, expert
    content: str
    video_url: Optional[str] = None
    author_id: str
    tags: List[str] = []
    views: int = 0
    likes: int = 0
    is_published: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TutorialCreate(BaseModel):
    title: str
    description: str
    game: Game
    level: str
    content: str
    video_url: Optional[str] = None
    tags: List[str] = []

# Community Models
class CommunityPost(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    author_id: str
    author_name: Optional[str] = None  # Will be populated from user
    is_published: bool = False
    is_pinned: bool = False
    tags: List[str] = []
    likes: List[str] = []  # user_ids who liked
    views: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CommunityPostCreate(BaseModel):
    title: str
    content: str
    tags: List[str] = []
    is_pinned: bool = False

# Team Statistics for ranking
class TeamStats(BaseModel):
    team_id: str
    total_tournaments: int = 0
    tournaments_won: int = 0
    total_matches: int = 0
    matches_won: int = 0
    win_rate: float = 0.0
    points: int = 0
    rank: Optional[int] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# News/Announcements Models
class News(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    summary: Optional[str] = None
    author_id: str
    is_published: bool = False
    is_pinned: bool = False
    tags: List[str] = []
    views: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class NewsCreate(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    tags: List[str] = []
    is_pinned: bool = False

# Community Stats Models (for a growing community)
class CommunityStats(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    total_members: int = 0
    active_members_today: int = 0
    active_members_week: int = 0
    total_tournaments: int = 0
    active_tournaments: int = 0
    total_teams: int = 0
    games_played: Dict[Game, int] = {}
    date: datetime = Field(default_factory=datetime.utcnow)

# Response Models
class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: UserRole
    status: UserStatus
    created_at: datetime
    is_verified: bool

class UserProfileResponse(BaseModel):
    id: str
    user_id: str
    display_name: str
    bio: Optional[str]
    avatar_url: Optional[str]
    favorite_games: List[Game]
    gaming_experience: Dict[Game, str]
    discord_username: Optional[str]
    twitch_username: Optional[str]
    steam_profile: Optional[str]
    total_tournaments: int
    tournaments_won: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None