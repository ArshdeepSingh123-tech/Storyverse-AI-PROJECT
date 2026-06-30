# StoryVerse AI 📚✨

> **Emotion-Aware Multilingual AI Storytelling Platform**  
> Built with Next.js · FastAPI · PostgreSQL · Ollama (Local LLM)

---

## Overview

StoryVerse AI is a production-ready, full-stack AI storytelling platform that generates personalized, emotion-aware narratives in multiple languages — running entirely on your local machine using **Ollama** with no cloud API dependency.

### Key Highlights

- **100% Local AI** — Powered by Ollama (Llama 3.1), no OpenAI/Gemini key required
- **Emotion-Aware** — Stories adapt tone based on your selected mood (7 emotions)
- **Multilingual** — English, Hindi (हिंदी), Punjabi (ਪੰਜਾਬੀ)
- **Personalized** — You become the story's protagonist
- **Export** — PDF, DOCX, TXT download support
- **Narration** — Text-to-speech for all languages (gTTS)
- **Analytics** — Rich charts tracking your storytelling journey
- **Premium UI** — Glassmorphism, Framer Motion animations, dark mode

---

## Tech Stack

| Layer      | Technology                                                    |
|------------|---------------------------------------------------------------|
| Frontend   | Next.js 14, React 18, TypeScript, Tailwind CSS, Framer Motion |
| Backend    | FastAPI, Python 3.11, SQLAlchemy ORM, Pydantic v2             |
| Database   | PostgreSQL 16                                                 |
| AI Engine  | Ollama (llama3.1:8b default — swappable)                     |
| Auth       | JWT (python-jose), bcrypt                                     |
| Export     | ReportLab (PDF), python-docx (DOCX)                           |
| Narration  | gTTS (Google Text-to-Speech — offline-capable)               |
| Deployment | Docker + Docker Compose                                       |

---

## Project Structure

```
storyverse/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/
│   │   │   ├── auth.py          # JWT auth endpoints
│   │   │   ├── stories.py       # Story CRUD + export + narration
│   │   │   └── analytics.py     # Analytics + AI health
│   │   ├── core/
│   │   │   ├── config.py        # Settings (env-based)
│   │   │   ├── database.py      # SQLAlchemy session
│   │   │   └── security.py      # JWT + bcrypt utilities
│   │   ├── models/
│   │   │   └── models.py        # SQLAlchemy ORM models
│   │   ├── schemas/
│   │   │   └── schemas.py       # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── ai_service.py    # Ollama provider + story generator
│   │   │   ├── story_service.py # Business logic + export
│   │   │   └── narration_service.py  # TTS narration
│   │   └── main.py              # FastAPI app
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   └── src/
│       ├── app/
│       │   ├── page.tsx                        # Landing page
│       │   ├── layout.tsx                      # Root layout + fonts
│       │   ├── globals.css                     # Tailwind + custom styles
│       │   ├── auth/
│       │   │   ├── login/page.tsx
│       │   │   └── register/page.tsx
│       │   └── dashboard/
│       │       ├── layout.tsx                  # Sidebar layout
│       │       ├── page.tsx                    # Dashboard home
│       │       ├── story/
│       │       │   ├── page.tsx                # Story generator (multi-step)
│       │       │   └── [id]/page.tsx           # Story reader
│       │       ├── library/page.tsx            # Story library + search
│       │       ├── analytics/page.tsx          # Charts dashboard
│       │       └── profile/page.tsx            # User profile
│       ├── lib/
│       │   ├── api.ts           # Axios client + all API functions
│       │   ├── store.ts         # Zustand auth store
│       │   └── utils.ts         # Helpers, genre/emotion metadata
│       └── types/
│           └── index.ts         # TypeScript type definitions
│
├── docker-compose.yml
└── README.md
```

---

## Prerequisites

1. **Node.js** 20+
2. **Python** 3.11+
3. **PostgreSQL** 16+
4. **Ollama** installed and running

---

## Quick Start (Local Development)

### Step 1 — Install & Start Ollama

```bash
# Install Ollama from https://ollama.com
# Then pull the model:
ollama pull llama3.1:8b

# Start Ollama server (usually auto-starts, or run manually):
ollama serve
```

### Step 2 — PostgreSQL Database

```bash
# Create DB (macOS/Linux with psql):
psql -U postgres -c "CREATE USER storyverse WITH PASSWORD 'storyverse123';"
psql -U postgres -c "CREATE DATABASE storyverse_db OWNER storyverse;"

# On Windows (PowerShell):
# Use pgAdmin or psql equivalent
```

### Step 3 — Backend Setup

```bash
cd storyverse/backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env if needed (DB URL, model name, etc.)

# Start the backend
uvicorn app.main:app --reload --port 8000
```

Backend runs at: `http://localhost:8000`  
API Docs: `http://localhost:8000/docs`

### Step 4 — Frontend Setup

```bash
cd storyverse/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs at: `http://localhost:3000`

---

## Docker Deployment

```bash
cd storyverse

# Build and start all services
docker compose up --build -d

# Check logs
docker compose logs -f backend

# Stop all services
docker compose down
```

**Important:** Ollama must be running on the host machine. The Docker backend connects via `host.docker.internal:11434`.

---

## Environment Variables

### Backend (`backend/.env`)

| Variable                   | Default                                                  | Description                        |
|----------------------------|----------------------------------------------------------|------------------------------------|
| `DATABASE_URL`             | `postgresql://storyverse:storyverse123@localhost:5432/storyverse_db` | PostgreSQL connection URL |
| `SECRET_KEY`               | *(change this)*                                          | JWT signing secret (32+ chars)     |
| `ALGORITHM`                | `HS256`                                                  | JWT algorithm                      |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `10080`                                               | Token TTL (7 days)                 |
| `OLLAMA_BASE_URL`          | `http://localhost:11434`                                 | Ollama API endpoint                |
| `OLLAMA_MODEL`             | `llama3.1:8b`                                           | Model to use for generation        |
| `CORS_ORIGINS`             | `["http://localhost:3000"]`                             | Allowed frontend origins           |

### Frontend (`frontend/.env.local`)

| Variable                | Default                     | Description               |
|-------------------------|-----------------------------|---------------------------|
| `NEXT_PUBLIC_API_URL`   | `http://localhost:8000`     | Backend API base URL      |

---

## API Reference

### Authentication

| Method | Endpoint              | Description          |
|--------|-----------------------|----------------------|
| POST   | `/api/v1/auth/register` | Create account     |
| POST   | `/api/v1/auth/login`    | Sign in, get JWT   |
| GET    | `/api/v1/auth/me`       | Get current user   |
| PUT    | `/api/v1/auth/me`       | Update profile     |

### Stories

| Method | Endpoint                              | Description                  |
|--------|---------------------------------------|------------------------------|
| POST   | `/api/v1/stories`                     | Generate new story           |
| GET    | `/api/v1/stories`                     | List stories (paginated)     |
| GET    | `/api/v1/stories/{id}`                | Get story with chapters      |
| POST   | `/api/v1/stories/{id}/favorite`       | Toggle favourite             |
| DELETE | `/api/v1/stories/{id}`                | Delete story                 |
| GET    | `/api/v1/stories/{id}/download/{fmt}` | Download (txt/pdf/docx)      |
| GET    | `/api/v1/stories/{id}/narrate`        | TTS audio stream (mp3)       |

### Analytics & AI

| Method | Endpoint          | Description              |
|--------|-------------------|--------------------------|
| GET    | `/api/v1/analytics` | User analytics data    |
| GET    | `/api/v1/ai/health` | Ollama connectivity    |
| GET    | `/api/v1/ai/models` | Available Ollama models|

Full interactive docs available at `http://localhost:8000/docs` when backend is running.

---

## Story Generation Flow

```
User selects:
  Genre → Emotion → Language & Length → Personalization
        ↓
  FastAPI receives StoryCreate payload
        ↓
  OllamaProvider.generate(prompt, system)
        ↓
  llama3.1:8b generates structured JSON
        ↓
  StoryGenerator._parse_story_response()
        ↓
  Story + Chapters saved to PostgreSQL
        ↓
  StoryResponse returned to frontend
```

### Supported Configurations

**Genres:** Adventure, Fantasy, Horror, Mystery, Sci-Fi, Comedy, Historical, Educational, Motivational

**Emotions:** Happy 😊, Sad 😢, Angry 😠, Fear 😨, Excited 🤩, Motivated 💪, Neutral 😐

**Languages:** English 🇬🇧, Hindi 🇮🇳, Punjabi 🏳️

**Lengths:**
- Short: 600–900 words, 2 chapters
- Medium: 1,200–1,800 words, 3 chapters  
- Long: 2,500–3,500 words, 5 chapters

---

## Switching AI Models

StoryVerse AI uses a **modular AI provider** architecture. To switch models:

1. Pull the new model in Ollama:
   ```bash
   ollama pull mistral:7b
   # or
   ollama pull llama3.2:3b
   # or
   ollama pull gemma2:9b
   ```

2. Update `backend/.env`:
   ```env
   OLLAMA_MODEL=mistral:7b
   ```

3. Restart the backend. No code changes needed.

---

## Database Schema

### `users` table
```sql
id, email (unique), username (unique), hashed_password,
full_name, age, gender, interests, avatar_url,
is_active, is_verified, created_at, updated_at
```

### `stories` table
```sql
id, user_id (FK), title, content, moral,
language, genre, emotion, story_length,
protagonist_name, protagonist_age, protagonist_gender, protagonist_interests,
is_favorite, is_public, word_count, read_time_minutes,
model_used, generation_time_seconds, created_at, updated_at
```

### `chapters` table
```sql
id, story_id (FK), chapter_number, title, content,
image_url, image_prompt, created_at
```

---

## Features Roadmap

- [x] Multilingual story generation (EN/HI/PA)
- [x] Emotion-aware narrative tone
- [x] Personalized protagonist
- [x] Chapter-based story structure
- [x] PDF / DOCX / TXT export
- [x] AI narration (gTTS)
- [x] Story library with search & filters
- [x] Analytics dashboard with charts
- [x] JWT authentication
- [x] Docker deployment
- [ ] AI image generation per chapter (Stable Diffusion via ComfyUI)
- [ ] AI video generation (story slideshow with narration)
- [ ] Story sharing (public URLs)
- [ ] Custom model fine-tuning support
- [ ] Story collaboration (multi-user)

---

## Troubleshooting

**"Cannot connect to Ollama"**
```bash
# Make sure Ollama is running
ollama serve

# Check if model is downloaded
ollama list

# Pull if missing
ollama pull llama3.1:8b
```

**"relation 'users' does not exist"**
```bash
# Tables are auto-created on startup, but check DB URL:
# Make sure PostgreSQL is running and DB exists
psql -U storyverse -d storyverse_db -c "\dt"
```

**"CORS error in browser"**
```bash
# Check CORS_ORIGINS in backend/.env includes your frontend URL:
CORS_ORIGINS=["http://localhost:3000"]
```

**"Story generation is slow"**
- Use a smaller model: `ollama pull llama3.2:3b`
- Choose "Short" story length
- Ensure no other GPU-heavy processes are running

---

## License

MIT — Free to use, modify and distribute.

---

*Built with ❤️ using Next.js, FastAPI, and Ollama.*
