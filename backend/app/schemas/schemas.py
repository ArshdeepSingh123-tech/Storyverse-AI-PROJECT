from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
from app.models.models import Language, Genre, Emotion, StoryLength, Gender
import re


# Auth Schemas
class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None

    @field_validator("username")
    @classmethod
    def username_valid(cls, v):
        if not re.match(r"^[a-zA-Z0-9_]{3,30}$", v):
            raise ValueError("Username must be 3-30 chars, alphanumeric + underscore")
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: Optional[str]
    age: Optional[int]
    gender: Optional[Gender]
    interests: Optional[str]
    avatar_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Gender] = None
    interests: Optional[str] = None


# Story Schemas
class StoryCreate(BaseModel):
    language: Language = Language.ENGLISH
    genre: Genre
    emotion: Emotion = Emotion.NEUTRAL
    story_length: StoryLength = StoryLength.MEDIUM
    protagonist_name: Optional[str] = None
    protagonist_age: Optional[int] = None
    protagonist_gender: Optional[Gender] = None
    protagonist_interests: Optional[str] = None
    custom_topic: Optional[str] = None


class ChapterResponse(BaseModel):
    id: str
    chapter_number: int
    title: Optional[str]
    content: str
    image_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class StoryResponse(BaseModel):
    id: str
    title: str
    content: str
    moral: Optional[str]
    language: Language
    genre: Genre
    emotion: Emotion
    story_length: StoryLength
    protagonist_name: Optional[str]
    protagonist_age: Optional[int]
    protagonist_gender: Optional[Gender]
    protagonist_interests: Optional[str]
    is_favorite: bool
    word_count: int
    read_time_minutes: float
    model_used: Optional[str]
    generation_time_seconds: Optional[float]
    created_at: datetime
    chapters: List[ChapterResponse] = []

    class Config:
        from_attributes = True


class StoryListResponse(BaseModel):
    id: str
    title: str
    language: Language
    genre: Genre
    emotion: Emotion
    story_length: StoryLength
    protagonist_name: Optional[str]
    is_favorite: bool
    word_count: int
    read_time_minutes: float
    created_at: datetime

    class Config:
        from_attributes = True


class StoriesPageResponse(BaseModel):
    stories: List[StoryListResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class AnalyticsResponse(BaseModel):
    total_stories: int
    total_words: int
    favorite_stories: int
    favorite_genre: Optional[str]
    favorite_language: Optional[str]
    genre_distribution: dict
    language_distribution: dict
    emotion_distribution: dict
    monthly_stories: List[dict]
    avg_word_count: float
    total_read_time_hours: float


TokenResponse.model_rebuild()
