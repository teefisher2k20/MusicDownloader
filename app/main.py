from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.database import init_db
from app.logging_config import configure_logging
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await init_db()
    yield


app = FastAPI(
    title="Video Orchestration Platform",
    description=(
        "Programmatic video rendering orchestration service. "
        "Submit render jobs, poll status, and retrieve signed artifact URLs."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(router, prefix="/v1")


@app.get("/health", tags=["ops"])
async def health() -> dict:
    return {"status": "ok", "environment": settings.environment}
