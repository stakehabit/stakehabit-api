# StakeHabit API

FastAPI backend for habit tracking with JWT authentication, PostgreSQL, and Alembic migrations.

## Run

1. Install dependencies:

```bash
python -m pip install -e .
```

2. Set environment variables in `.env`:

```env
DATABASE_URL="postgresql://user:password@host:port/database"
JWT_SECRET_KEY="your-secret-key"
```

3. Run migrations:

```bash
alembic upgrade head
```

4. Start the app:

```bash
python -m uvicorn app.main:app --reload
```

## API

- `POST /register`
- `POST /login`
- `GET /me`
- `GET /habits`
- `POST /habits`
- `GET /habits/{id}`
- `PATCH /habits/{id}`
- `DELETE /habits/{id}`
- `POST /habits/{id}/checkins`
- `GET /habits/{id}/streak`
