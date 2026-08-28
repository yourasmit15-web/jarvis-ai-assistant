# Setup

## Backend
1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r backend/requirements.txt`
3. `cp backend/.env.example .env`
4. `uvicorn backend.app:app --reload`

## Frontend
1. `cd frontend`
2. `npm install`
3. `cp .env.example .env`
4. `npm start`
