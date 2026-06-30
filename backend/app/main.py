from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import os

from app.core.config import settings
from app.core.database import create_tables
from app.api.v1 import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_tables()
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    print("✅ StoryVerse AI Backend started")
    print(f"📚 Ollama endpoint: {settings.OLLAMA_BASE_URL}")
    print(f"🤖 Model: {settings.OLLAMA_MODEL}")
    yield
    # Shutdown
    print("👋 StoryVerse AI Backend stopped")


app = FastAPI(
    title="StoryVerse AI API",
    description="Emotion-Aware Multilingual AI Storytelling Platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(api_router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "StoryVerse AI",
        "version": "1.0.0",
    }
