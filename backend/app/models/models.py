from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import enum
import uuid

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class Language(str, enum.Enum):
    ENGLISH = "english"
    HINDI = "hindi"
    PUNJABI = "punjabi"


class Genre(str, enum.Enum):
    ADVENTURE = "adventure"
    FANTASY = "fantasy"
    HORROR = "horror"
    MYSTERY = "mystery"
    SCIFI = "scifi"
    COMEDY = "comedy"
    HISTORICAL = "historical"
    EDUCATIONAL = "educational"
    MOTIVATIONAL = "motivational"


class Emotion(str, enum.Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    FEAR = "fear"
    EXCITED = "excited"
    MOTIVATED = "motivated"
    NEUTRAL = "neutral"


class StoryLength(str, enum.Enum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT = "prefer_not_to_say"


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    age = Column(Integer)
    gender = Column(Enum(Gender))
    interests = Column(Text)
    avatar_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    stories = relationship("Story", back_populates="author", cascade="all, delete-orphan")


class Story(Base):
    __tablename__ = "stories"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    moral = Column(Text)
    language = Column(Enum(Language), nullable=False, default=Language.ENGLISH)
    genre = Column(Enum(Genre), nullable=False)
    emotion = Column(Enum(Emotion), nullable=False, default=Emotion.NEUTRAL)
    story_length = Column(Enum(StoryLength), nullable=False, default=StoryLength.MEDIUM)
    protagonist_name = Column(String(100))
    protagonist_age = Column(Integer)
    protagonist_gender = Column(Enum(Gender))
    protagonist_interests = Column(Text)
    is_favorite = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)
    word_count = Column(Integer, default=0)
    read_time_minutes = Column(Float, default=0)
    model_used = Column(String(100))
    generation_time_seconds = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    author = relationship("User", back_populates="stories")
    chapters = relationship("Chapter", back_populates="story", cascade="all, delete-orphan", order_by="Chapter.chapter_number")


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    story_id = Column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    chapter_number = Column(Integer, nullable=False)
    title = Column(String(500))
    content = Column(Text, nullable=False)
    image_url = Column(String(500))
    image_prompt = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    story = relationship("Story", back_populates="chapters")
