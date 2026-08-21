# AI Job Matcher

AI Job Matcher is a full-stack application that analyzes a user's resume and matches them with relevant job opportunities using AI. It's split into a React frontend (`client`) and a FastAPI backend (`server`).

> 🚧 **Status:** Early development — Phase 1 (Authentication).

## Features

- **Authentication** — register/login with JWT access tokens and an httpOnly refresh-token cookie
- **Resume upload** — upload a PDF resume for parsing
- **AI resume analysis** — extracts skills, experience, and preferred roles using the Groq API
- **Job search** — scrapes/searches jobs based on the analyzed resume
- **AI recommendations** — generates job recommendations tailored to the resume

## Tech Stack

**Backend** (`server/`)
- FastAPI + Uvicorn
- SQLAlchemy + Alembic (PostgreSQL)
- PyJWT + bcrypt (authentication)
- Groq API (AI resume analysis & recommendations)

**Frontend** (`client/`)
- React 19 + Vite
- React Router
- Tailwind CSS
- Axios

## Project Structure

```
AI_Job_Matcher/
├── client/                 # React frontend
│   └── src/
│       ├── components/     # UI components (dashboard, protected routes, etc.)
│       ├── context/        # Auth context
│       ├── pages/          # Login / Register pages
│       └── services/       # API clients (auth, jobs, etc.)
└── server/                 # FastAPI backend
    ├── app/
    │   ├── core/            # Config, security, dependencies
    │   ├── database/        # DB session setup
    │   ├── models/          # SQLAlchemy models
    │   ├── prompts/         # AI prompt templates
    │   ├── routers/         # /auth, /resumes, /analysis, /jobsRouter, /recommendation
    │   ├── schemas/         # Pydantic schemas
    │   └── services/        # Business logic (parsing, scraping, AI calls)
    ├── alembic/             # Database migrations
    └── main.py              # App entry point
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL

### Backend Setup

```bash
cd server
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Create a `server/.env` file (never commit this file — it's already gitignored) based on `server/.env.example`:

```env
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/AI_Job_Matcher_db
GROQ_API_KEY=your-groq-api-key

JWT_SECRET_KEY=generate-your-own-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Generate a strong `JWT_SECRET_KEY` with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Run database migrations:

```bash
alembic upgrade head
```

Start the API:

```bash
uvicorn main:app --reload
```

API available at `http://127.0.0.1:8000`, docs at `http://127.0.0.1:8000/docs`.

### Frontend Setup

```bash
cd client
npm install
npm run dev
```

Frontend available at `http://localhost:5173`.

## API Overview

| Prefix               | Purpose                                 |
|----------------------|------------------------------------------|
| `/auth`              | Register, login, token refresh          |
| `/resumes`           | Upload resume PDFs                      |
| `/analysis`          | AI analysis of an uploaded resume       |
| `/jobsRouter`        | Search jobs based on resume analysis    |
| `/recommendation`    | Get AI-generated job recommendations    |

## Roadmap

- [x] Project scaffolding (client + server)
- [x] Authentication (Phase 1)
- [x] Resume upload & AI analysis
- [x] Job search & AI recommendations
- [ ] User dashboard polish
- [ ] Deployment setup
