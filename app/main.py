from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.habits import router as habit_router
from app.api.v1.pools import router as pool_router


def create_app() -> FastAPI:
    app = FastAPI(title="StakeHabit API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router, prefix="", tags=["auth"])
    app.include_router(habit_router, prefix="", tags=["habits"])
    app.include_router(pool_router, prefix="", tags=["pools"])

    return app


app = create_app()
