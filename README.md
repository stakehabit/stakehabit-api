# StakeHabit API

StakeHabit API is a FastAPI backend for habit tracking, streak management, and shared-stake pools. It supports user authentication, private habit CRUD, daily check-ins, streak calculations, and multi-user pool creation and participation.

## What the backend provides

- JWT-based authentication with bcrypt password hashing
- Habit creation, updates, deletion, and per-habit check-ins
- Streak calculation for daily consistency
- Pool creation, joining, participant tracking, and pool check-ins
- OpenAPI documentation at `/docs` for interactive exploration

## Quick start

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -e ".[dev]"
```

3. Create a `.env` file with the required settings:

```env
DATABASE_URL="postgresql://user:password@host:port/database"
JWT_SECRET_KEY="replace-with-a-long-random-secret"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="60"
```

4. Run database migrations:

```bash
alembic upgrade head
```

5. Start the development server:

```bash
.venv/bin/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` and the interactive docs at `http://localhost:8000/docs`.

## Main API surface

### Authentication
- `POST /register`
- `POST /login`
- `GET /me`

### Habits
- `GET /habits`
- `POST /habits`
- `GET /habits/{id}`
- `PATCH /habits/{id}`
- `DELETE /habits/{id}`
- `POST /habits/{id}/checkins`
- `GET /habits/{id}/streak`

### Pools
- `GET /pools`
- `POST /pools`
- `GET /pools/{pool_id}`
- `POST /pools/{pool_id}/join`
- `GET /pools/{pool_id}/participants`
- `POST /pools/{pool_id}/checkin`
- `GET /pools/{pool_id}/checkins/{wallet_address}`

Protected endpoints expect an `Authorization: Bearer <token>` header.

## Documentation

- [DEVELOPMENT.md](DEVELOPMENT.md) for local setup and contributor workflows
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for a feature overview and architecture summary
- [contributions.md](contributions.md) for contribution rules and PR expectations
- [FRONTEND_INTEGRATION_GUIDE.md](FRONTEND_INTEGRATION_GUIDE.md) for frontend and agent handoff details

## Testing

```bash
.venv/bin/python -m pytest tests/ -q
```
