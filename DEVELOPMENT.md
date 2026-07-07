# Development Guide

## Environment Setup

### Prerequisites
- Python 3.11+
- PostgreSQL (via Supabase or local)
- Git

### Installation

1. Clone the repository:
   ```bash
   cd /home/devmaro/stakehabit-api
   ```

2. Create virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -e .[dev]
   ```

4. Configure `.env`:
   ```env
   DATABASE_URL=postgresql://user:password@host:port/database
   JWT_SECRET_KEY=your-secure-random-key-min-32-chars
   ```

## Running the Application

### Development Server
```bash
.venv/bin/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will automatically reload on file changes.

### Production Server (Manual)
```bash
.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Database Management

### Create Migrations
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
alembic upgrade head      # All pending migrations
alembic upgrade +1        # Next migration only
```

### Rollback Migrations
```bash
alembic downgrade -1      # Rollback one migration
alembic downgrade base    # Rollback all migrations
```

### Check Migration Status
```bash
alembic current           # Current schema version
alembic history           # All migrations history
```

## Testing

### Run All Tests
```bash
.venv/bin/python -m pytest tests/ -v
```

### Run Specific Test File
```bash
.venv/bin/python -m pytest tests/test_auth.py -v
```

### Run Specific Test
```bash
.venv/bin/python -m pytest tests/test_auth.py::test_register_and_login -v
```

### Run with Coverage
```bash
.venv/bin/python -m pytest tests/ --cov=app --cov-report=html
```

### Run Tests with Output
```bash
.venv/bin/python -m pytest tests/ -v -s
```

## Code Quality

### Type Checking (Optional - requires mypy)
```bash
pip install mypy
mypy app/
```

### Format Code (Optional - requires black)
```bash
pip install black
black app/ tests/
```

### Lint Code (Optional - requires ruff)
```bash
pip install ruff
ruff check app/ tests/
```

## API Testing

### Using cURL

#### Register
```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
```

#### Get Profile
```bash
curl -X GET http://localhost:8000/me \
  -H "Authorization: Bearer <token>"
```

#### Create Habit
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

#### List Habits
```bash
curl -X GET http://localhost:8000/habits \
  -H "Authorization: Bearer <token>"
```

#### Add Check-in
```bash
curl -X POST http://localhost:8000/habits/1/checkins \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2024-07-07"
  }'
```

#### Get Streak
```bash
curl -X GET http://localhost:8000/habits/1/streak \
  -H "Authorization: Bearer <token>"
```

### Using HTTPie
```bash
# Register
http POST localhost:8000/register email=user@example.com password=securepass123

# Login
http POST localhost:8000/login email=user@example.com password=securepass123

# Get Profile
http GET localhost:8000/me Authorization:"Bearer <token>"
```

### Using Postman
1. Import the API endpoints
2. Set base URL: `http://localhost:8000`
3. Add token to Authorization header after login
4. Test endpoints in order

## Project Structure Explained

```
app/
├── main.py              # FastAPI app creation and routes registration
├── api/                 # API routes
│   ├── deps.py          # Shared dependencies (get_current_user, get_db)
│   └── v1/              # API version 1
│       ├── auth.py      # Authentication endpoints
│       └── habits.py    # Habit endpoints
├── models/              # SQLAlchemy ORM models
│   ├── user.py
│   ├── habit.py
│   └── checkin.py
├── schemas/             # Pydantic validation schemas
│   ├── user.py
│   ├── auth.py
│   ├── habit.py
│   ├── checkin.py
│   ├── streak.py
│   └── token.py
├── services/            # Business logic (isolated from API)
│   ├── auth_service.py
│   ├── user_service.py
│   ├── habit_service.py
│   ├── checkin_service.py
│   └── streak_service.py
├── db/                  # Database configuration
│   ├── base.py          # SQLAlchemy declarative base
│   └── session.py       # Database engine and session management
└── core/                # Core configurations
    ├── config.py        # Settings from environment
    └── security.py      # JWT and password utilities

tests/
├── conftest.py          # Pytest fixtures
├── test_auth.py         # Auth tests
├── test_habits.py       # Habit CRUD tests
├── test_checkin.py      # Check-in tests
└── test_streak.py       # Streak calculation tests

alembic/
├── env.py               # Alembic environment setup
├── script.py.mako       # Migration template
└── versions/
    └── 0001_initial.py  # Initial schema migration

.env                     # Environment variables (git ignored)
.gitignore              # Git ignore patterns
pyproject.toml          # Project metadata and dependencies
alembic.ini             # Alembic configuration
README.md               # Quick start guide
PROJECT_SUMMARY.md      # Detailed feature summary
```

## Common Tasks

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
