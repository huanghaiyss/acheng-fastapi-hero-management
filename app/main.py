from contextlib import asynccontextmanager
from fastapi import FastAPI,HTTPException,Depends
from app.database.db import create_db_and_tables
from app.routes.heroes import router as heroes_router
from app.routes.teams import router as teams_router
from app.routes.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(heroes_router, prefix="/heroes", tags=["heroes"])
app.include_router(teams_router, prefix="/teams", tags=["teams"])
app.include_router(users_router, prefix="/users", tags=["users"])

