# Project Summary

StakeHabit API is a modular FastAPI backend for a habit-tracking product that now also supports shared pools for friend or community challenges. The backend is designed to be easy to consume from a frontend app or from another coding agent.

## Current capabilities

### Authentication and user accounts
- Registration and login with email and password
- JWT token issuance and validation
- Password hashing with bcrypt
- Protected routes that resolve the current user from the token

### Habit tracking
- Create, read, update, and delete habits
- Track habits per authenticated user
- Add daily check-ins and retrieve streak information
- Keep habit data isolated by user

### Shared pools
- Create active pools with metadata such as duration, stake amount, currency, and participant limits
- Join pools with a wallet address
- Track participant progress and leaderboard-style participant data
- Record pool check-ins by wallet address for each participant

## API shape

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

## Architecture

The project follows a simple layered structure:
- `app/api` for route handlers
- `app/services` for business logic
- `app/schemas` for request and response validation
- `app/models` for SQLAlchemy ORM models
- `app/core` for settings and security helpers
- `alembic` for schema migrations

## Development notes

- The app is served through FastAPI and can be explored locally via `/docs`.
- The default development server is started with Uvicorn.
- Database migrations are managed through Alembic.
- Tests are implemented with pytest and use a lightweight database fixture for local validation.

## Suggested next steps

- Add richer pool outcomes and winner selection logic
- Expose pool analytics and rewards metadata
- Add frontend-friendly pagination and filtering for habits and pools
- Harden production deployment configuration for environment-specific secrets and database settings
