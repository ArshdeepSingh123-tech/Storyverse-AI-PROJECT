from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User
from app.schemas.schemas import AnalyticsResponse
from app.services.story_service import get_analytics
from app.services.ai_service import ollama_provider

router = APIRouter(tags=["Analytics & AI"])


@router.get("/analytics", response_model=AnalyticsResponse)
async def get_user_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_analytics(db, current_user.id)


@router.get("/ai/health")
async def ai_health():
    """Check Ollama connectivity and available models."""
    return await ollama_provider.check_health()


@router.get("/ai/models")
async def list_models():
    """List available Ollama models."""
    try:
        models = await ollama_provider.list_models()
        return {"models": models}
    except Exception as e:
        return {"models": [], "error": str(e)}
