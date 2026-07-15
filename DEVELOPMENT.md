# Development Guide

This guide covers the day-to-day workflow for working on the StakeHabit API locally.

## Prerequisites

- Python 3.11+
- PostgreSQL (local install or Supabase)
- Git
- A terminal with access to your virtual environment

## Setup

1. Clone the repository:

```bash
cd /home/devmaro/stakehabit-api
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install app dependencies:

```bash
pip install -e ".[dev]"
```

4. Create a local `.env` file:

```env
DATABASE_URL="postgresql://user:password@localhost:5432/stakehabit"
JWT_SECRET_KEY="replace-with-a-long-random-secret"
JWT_ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="60"
```

## Run the API

### Development server

```bash
.venv/bin/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The app is available at:
- `http://localhost:8000`
- `http://localhost:8000/docs` for the Swagger UI
- `http://localhost:8000/redoc` for ReDoc

### Production-style start

```bash
.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Database workflow

### Create a new migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations

```bash
alembic upgrade head
```

### Roll back one revision

```bash
alembic downgrade -1
```

### Inspect migration history

```bash
alembic current
alembic history
```

## Testing

### Run the full suite

```bash
.venv/bin/python -m pytest tests/ -q
```

### Run a single file

```bash
.venv/bin/python -m pytest tests/test_pools.py -q
```

### Run a single test

```bash
.venv/bin/python -m pytest tests/test_pools.py::test_pool_flow -q
```

## Example API requests

### Register a user

```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
```

### Log in

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
```

### Create a habit

```bash
curl -X POST http://localhost:8000/habits \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Exercise",
    "frequency": "daily",
    "target_days_per_week": 5,
    "is_active": true
  }'
```

### Create a pool

```bash
curl -X POST http://localhost:8000/pools \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Streak Pool",
    "description": "Daily goals with shared stakes",
    "duration": 14,
    "stake_amount": "10.0000000",
    "currency": "USD",
    "max_participants": 5,
    "winner_split": 80,
    "charity": "help",
    "creator_address": "GABCDEF1234567890"
  }'
```

## Project structure

```text
app/
├── api/
│   └── v1/
│       ├── auth.py
│       ├── habits.py
│       └── pools.py
├── core/
│   ├── config.py
│   └── security.py
├── db/
│   ├── base.py
│   └── session.py
├── models/
│   ├── habit.py
│   ├── pool.py
│   ├── pool_checkin.py
│   ├── pool_participant.py
│   ├── user.py
│   └── checkin.py
├── schemas/
├── services/
└── main.py

tests/
alembic/
```

## Notes for collaborators

- Keep route handlers thin and move business logic into service modules.
- Prefer updating schemas and tests when adding or changing API behavior.
- Use the shared docs in [README.md](README.md), [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md), and [FRONTEND_INTEGRATION_GUIDE.md](FRONTEND_INTEGRATION_GUIDE.md) as the source of truth for integration expectations.


### Add a New Endpoint

1. **Create schema** in `app/schemas/`:
   ```python
   from pydantic import BaseModel
   
   class NewResourceCreate(BaseModel):
       field: str
   ```

2. **Create model** in `app/models/`:
   ```python
   from sqlalchemy import Column, String
   from app.db.base import Base
   
   class NewResource(Base):
       __tablename__ = "new_resources"
       id = Column(Integer, primary_key=True)
       field = Column(String)
   ```

3. **Create service** in `app/services/`:
   ```python
   def create_new_resource(db, data):
       resource = NewResource(**data.model_dump())
       db.add(resource)
       db.commit()
       db.refresh(resource)
       return resource
   ```

4. **Add route** in `app/api/v1/`:
   ```python
   @router.post("/new-resources")
   def create(data: NewResourceCreate, current_user=Depends(get_current_user)):
       return create_new_resource(db, data)
   ```

5. **Create migration**:
   ```bash
   alembic revision --autogenerate -m "feat: add new_resources table"
   alembic upgrade head
   ```

6. **Write tests** in `tests/`:
   ```python
   def test_create_new_resource(client):
       response = client.post("/new-resources", json={"field": "value"})
       assert response.status_code == 201
   ```

### Add a New Field to Habit

1. Update `Habit` model in `app/models/habit.py`
2. Update `HabitRead` and `HabitUpdate` schemas
3. Create migration: `alembic revision --autogenerate -m "feat: add field to habits"`
4. Update service layer if needed
5. Update tests
6. Add route changes if needed

## Troubleshooting

### Database Connection Issues
- Verify `.env` `DATABASE_URL` is correct
- Check PostgreSQL is running
- Verify network connectivity to database host
- Check database credentials

### JWT Token Expired
- Tokens expire after 60 minutes (configurable in `settings.access_token_expire_minutes`)
- User must login again to get new token
- Implement refresh token endpoint for long sessions

### Migration Conflicts
```bash
# If migration is corrupted
alembic current           # See current version
alembic history           # See all versions
alembic stamp [version]   # Force update to version
```

### Test Failures
- Run with `-v -s` flags to see verbose output
- Check `.venv` is activated
- Ensure dependencies installed: `pip install -e .[dev]`
- Delete `.venv` and reinstall if issues persist

## Performance Tips

1. **Add database indexes** for frequently queried fields
2. **Implement pagination** for list endpoints (future)
3. **Use connection pooling** (SQLAlchemy handles this)
4. **Cache streak calculations** for read-heavy operations
5. **Batch inserts** for bulk operations
6. **Use async endpoints** with FastAPI async support (future)

## Security Checklist

- [ ] Change `JWT_SECRET_KEY` to a secure random value
- [ ] Use HTTPS in production
- [ ] Set database password to strong value
- [ ] Enable CORS only for trusted domains
- [ ] Implement rate limiting on auth endpoints
- [ ] Add CSRF protection if using cookies
- [ ] Regularly rotate JWT secrets
- [ ] Validate all user inputs
- [ ] Log security events
- [ ] Run security linters regularly

## Git Workflow

### Commit Messages (Semantic)
```
feat: add new feature
fix: fix a bug
docs: documentation changes
style: formatting/style changes
refactor: code refactoring
perf: performance improvements
test: test additions/changes
chore: dependency/config changes
```

### Example Commits
```bash
git add app/services/new_service.py
git commit -m "feat(services): add new service for processing"

git add app/api/v1/new_routes.py
git commit -m "feat(api): add endpoints for new feature"

git add tests/
git commit -m "test: add tests for new feature"

git add pyproject.toml
git commit -m "chore: add new dependency"
```

## Useful Commands

```bash
# Virtual environment
source .venv/bin/activate      # Activate (Linux/macOS)
.venv\Scripts\activate         # Activate (Windows)
deactivate                     # Deactivate

# Dependencies
pip list                       # Show installed packages
pip show <package>             # Show package info
pip install --upgrade <package> # Upgrade package

# Database
alembic upgrade head           # Apply all migrations
alembic downgrade -1           # Rollback one
psql -U user -d database       # Connect to PostgreSQL

# Testing
pytest tests/ -v               # Run all tests
pytest tests/ -k "test_name"   # Run specific test
pytest --collect-only          # List all tests

# Code quality
python -m py_compile app/      # Check syntax
```

## Next Steps

1. Test all endpoints locally
2. Deploy to staging environment
3. Run load tests
4. Configure monitoring and logging
5. Set up CI/CD pipeline
6. Plan stake integration feature
7. Plan charity integration feature
8. Implement notification system
