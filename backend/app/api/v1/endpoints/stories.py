from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Genre, Language, Emotion
from app.schemas.schemas import StoryCreate, StoryResponse, StoryListResponse, StoriesPageResponse
from app.services import story_service, narration_service

router = APIRouter(prefix="/stories", tags=["Stories"])


@router.post("", response_model=StoryResponse, status_code=201)
async def generate_story(
    payload: StoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate a new AI story."""
    try:
        story = await story_service.create_story(db, current_user, payload)
        return story
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Story generation failed: {str(e)}")


@router.get("", response_model=StoriesPageResponse)
async def list_stories(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    search: Optional[str] = Query(None),
    genre: Optional[Genre] = Query(None),
    language: Optional[Language] = Query(None),
    emotion: Optional[Emotion] = Query(None),
    favorites_only: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return story_service.get_user_stories(
        db, current_user.id, page, page_size, search, genre, language, emotion, favorites_only
    )


@router.get("/{story_id}", response_model=StoryResponse)
async def get_story(
    story_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    story = story_service.get_story_by_id(db, story_id, current_user.id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@router.post("/{story_id}/favorite")
async def toggle_favorite(
    story_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        story = story_service.toggle_favorite(db, story_id, current_user.id)
        return {"is_favorite": story.is_favorite, "message": "Updated"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Story not found")


@router.delete("/{story_id}", status_code=204)
async def delete_story(
    story_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = story_service.delete_story(db, story_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Story not found")


@router.get("/{story_id}/download/{format}")
async def download_story(
    story_id: str,
    format: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    story = story_service.get_story_by_id(db, story_id, current_user.id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in story.title)[:50]

    if format == "txt":
        content = story_service.export_story_txt(story)
        return Response(
            content=content,
            media_type="text/plain",
            headers={"Content-Disposition": f'attachment; filename="{safe_title}.txt"'},
        )
    elif format == "pdf":
        content = story_service.export_story_pdf(story)
        return Response(
            content=content,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{safe_title}.pdf"'},
        )
    elif format == "docx":
        content = story_service.export_story_docx(story)
        return Response(
            content=content,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f'attachment; filename="{safe_title}.docx"'},
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid format. Use: txt, pdf, docx")


@router.get("/{story_id}/narrate")
async def narrate_story(
    story_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    story = story_service.get_story_by_id(db, story_id, current_user.id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    try:
        audio = await narration_service.generate_narration(story.content, story.language)
        return Response(
            content=audio,
            media_type="audio/mpeg",
            headers={"Content-Disposition": f'inline; filename="narration.mp3"'},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Narration failed: {str(e)}")
