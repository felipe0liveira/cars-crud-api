from fastapi import FastAPI
from contextlib import asynccontextmanager
from api import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    from core.database import engine
    from app.models.cars import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield  # Done

app = FastAPI(lifespan=lifespan)

app.include_router(router)