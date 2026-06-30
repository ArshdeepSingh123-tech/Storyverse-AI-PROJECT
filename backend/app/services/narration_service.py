import io
from gtts import gTTS
from app.models.models import Language


LANG_MAP = {
    Language.ENGLISH: "en",
    Language.HINDI: "hi",
    Language.PUNJABI: "pa",
}


async def generate_narration(text: str, language: Language) -> bytes:
    """Generate text-to-speech audio for story narration."""
    lang_code = LANG_MAP.get(language, "en")
    # Truncate for narration (gTTS has limits)
    max_chars = 3000
    narration_text = text[:max_chars] + ("..." if len(text) > max_chars else "")
    
    tts = gTTS(text=narration_text, lang=lang_code, slow=False)
    buffer = io.BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    return buffer.read()
