# RAGHUVIR - Personal AI Assistant

RAGHUVIR is a security-first personal AI assistant foundation (Phase 1) with chat, intent understanding, memory, tool orchestration, permissions, confirmations, audit logs, and a futuristic dashboard UI.

## Quick start

### Backend
1. `cd /home/runner/work/jarvis-ai-assistant/jarvis-ai-assistant`
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r backend/requirements.txt`
4. `cp backend/.env.example backend/.env`
5. `uvicorn backend.app:app --reload --port 8000`

### Frontend
1. `cd frontend`
2. `npm install`
3. `cp .env.example .env`
4. `npm start`

### Docker
- `docker compose up --build`

Default greeting: **"I'm RAGHUVIR, your personal AI assistant. How can I help?"**
