import httpx
import json
import time
import re
from typing import Optional
from app.core.config import settings
from app.models.models import Language, Genre, Emotion, StoryLength, Gender


class OllamaProvider:
    """Dedicated AI provider using Ollama for local LLM execution."""

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL
        self.timeout = 300.0

    async def generate(self, prompt: str, system: str = "") -> str:
        """Generate text using Ollama API."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.85,
                    "top_p": 0.9,
                    "num_predict": 4096,
                },
            }
            if system:
                payload["system"] = system

            try:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                return data.get("response", "")
            except httpx.ConnectError:
                raise RuntimeError(
                    "Cannot connect to Ollama. Please ensure Ollama is running: `ollama serve`"
                )
            except httpx.TimeoutException:
                raise RuntimeError("Ollama request timed out. Try a shorter story or faster model.")

    async def check_health(self) -> dict:
        """Check if Ollama is running and model is available."""
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                resp = await client.get(f"{self.base_url}/api/tags")
                resp.raise_for_status()
                models = resp.json().get("models", [])
                model_names = [m["name"] for m in models]
                return {
                    "status": "healthy",
                    "available_models": model_names,
                    "current_model": self.model,
                    "model_ready": any(self.model in m for m in model_names),
                }
            except Exception as e:
                return {"status": "unavailable", "error": str(e)}

    async def list_models(self) -> list:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{self.base_url}/api/tags")
            resp.raise_for_status()
            return resp.json().get("models", [])


class StoryGenerator:
    """Generates emotion-aware, multilingual, personalized stories using Ollama."""

    LANGUAGE_INSTRUCTIONS = {
        Language.ENGLISH: "Write the entire story in English.",
        Language.HINDI: "पूरी कहानी हिंदी में लिखें। Use Devanagari script throughout.",
        Language.PUNJABI: "ਪੂਰੀ ਕਹਾਣੀ ਪੰਜਾਬੀ ਵਿੱਚ ਲਿਖੋ। Use Gurmukhi script throughout.",
    }

    EMOTION_GUIDANCE = {
        Emotion.HAPPY: "joyful, uplifting, cheerful, with a warm and positive tone",
        Emotion.SAD: "melancholic, touching, emotionally deep, with bittersweet undertones",
        Emotion.ANGRY: "intense, passionate, driven by conflict and resolution",
        Emotion.FEAR: "suspenseful, tense, with mounting dread and atmospheric darkness",
        Emotion.EXCITED: "fast-paced, energetic, thrilling, with high momentum",
        Emotion.MOTIVATED: "inspiring, empowering, with a strong growth arc and triumph",
        Emotion.NEUTRAL: "balanced, thoughtful, with a steady narrative pace",
    }

    LENGTH_CONFIG = {
        StoryLength.SHORT: {"words": "600-900", "chapters": 2},
        StoryLength.MEDIUM: {"words": "1200-1800", "chapters": 3},
        StoryLength.LONG: {"words": "2500-3500", "chapters": 5},
    }

    def __init__(self):
        self.provider = OllamaProvider()

    def _build_protagonist_desc(
        self,
        name: Optional[str],
        age: Optional[int],
        gender: Optional[Gender],
        interests: Optional[str],
    ) -> str:
        if not name:
            return ""
        parts = [f"The main character is {name}"]
        if age:
            parts.append(f"aged {age}")
        if gender and gender != Gender.PREFER_NOT:
            parts.append(f"({gender.value})")
        desc = ", ".join(parts) + "."
        if interests:
            desc += f" Their interests include: {interests}."
        desc += " Make this character the hero of the story."
        return desc

    def _build_system_prompt(self, language: Language) -> str:
        lang_instruction = self.LANGUAGE_INSTRUCTIONS.get(language, "")
        return f"""You are StoryVerse AI, a master storyteller who creates immersive, emotionally resonant stories.
{lang_instruction}
Always produce well-structured, engaging narratives with vivid descriptions and compelling characters.
Format your response EXACTLY as valid JSON with no markdown, no code blocks, no extra text.
The JSON must follow the exact schema provided."""

    def _build_story_prompt(
        self,
        genre: Genre,
        emotion: Emotion,
        story_length: StoryLength,
        language: Language,
        protagonist_name: Optional[str] = None,
        protagonist_age: Optional[int] = None,
        protagonist_gender: Optional[Gender] = None,
        protagonist_interests: Optional[str] = None,
        custom_topic: Optional[str] = None,
    ) -> str:
        config = self.LENGTH_CONFIG[story_length]
        emotion_tone = self.EMOTION_GUIDANCE.get(emotion, "balanced")
        protagonist = self._build_protagonist_desc(
            protagonist_name, protagonist_age, protagonist_gender, protagonist_interests
        )

        topic_line = f"Topic/Theme: {custom_topic}" if custom_topic else ""
        num_chapters = config["chapters"]

        return f"""Create a complete {genre.value} story with these specifications:
- Emotion/Tone: {emotion_tone}
- Target length: {config['words']} words total
- Number of chapters: {num_chapters}
{f'- {protagonist}' if protagonist else ''}
{topic_line}

Return ONLY this JSON (no markdown, no backticks):
{{
  "title": "Compelling story title",
  "chapters": [
    {{
      "chapter_number": 1,
      "title": "Chapter title",
      "content": "Chapter content (detailed paragraphs)",
      "image_prompt": "Detailed visual scene description for AI image generation"
    }}
  ],
  "moral": "The moral or lesson of the story",
  "character_descriptions": "Brief descriptions of main characters"
}}

Make sure chapters array has exactly {num_chapters} chapters with rich, immersive content."""

    async def generate_story(
        self,
        genre: Genre,
        emotion: Emotion,
        story_length: StoryLength,
        language: Language,
        protagonist_name: Optional[str] = None,
        protagonist_age: Optional[int] = None,
        protagonist_gender: Optional[Gender] = None,
        protagonist_interests: Optional[str] = None,
        custom_topic: Optional[str] = None,
    ) -> dict:
        start_time = time.time()

        system = self._build_system_prompt(language)
        prompt = self._build_story_prompt(
            genre, emotion, story_length, language,
            protagonist_name, protagonist_age, protagonist_gender,
            protagonist_interests, custom_topic
        )

        raw_response = await self.provider.generate(prompt, system)

        # Parse JSON response robustly
        story_data = self._parse_story_response(raw_response)
        story_data["model_used"] = self.provider.model
        story_data["generation_time_seconds"] = round(time.time() - start_time, 2)

        return story_data

    def _parse_story_response(self, raw: str) -> dict:
        """Robustly parse story JSON from LLM response."""
        # Try direct parse
        try:
            return json.loads(raw.strip())
        except json.JSONDecodeError:
            pass

        # Extract JSON block from markdown
        json_patterns = [
            r'```json\s*([\s\S]+?)\s*```',
            r'```\s*([\s\S]+?)\s*```',
            r'\{[\s\S]+\}',
        ]
        for pattern in json_patterns:
            match = re.search(pattern, raw, re.DOTALL)
            if match:
                candidate = match.group(1) if '```' in pattern else match.group(0)
                try:
                    return json.loads(candidate.strip())
                except json.JSONDecodeError:
                    continue

        # Fallback: construct story from raw text
        return {
            "title": "An Untitled Story",
            "chapters": [{"chapter_number": 1, "title": "Chapter 1", "content": raw, "image_prompt": "A dramatic story scene"}],
            "moral": "Every story has a lesson to teach.",
            "character_descriptions": "",
        }


# Singleton instances
ollama_provider = OllamaProvider()
story_generator = StoryGenerator()
