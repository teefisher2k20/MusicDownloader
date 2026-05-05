from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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


@app.get("/", response_class=HTMLResponse, tags=["ui"])
async def index() -> HTMLResponse:
    html = """
        <!doctype html>
        <html lang=\"en\">
            <head>
                <meta charset=\"utf-8\" />
                <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
                <title>Video Orchestration Platform</title>
                <style>
                    body {
                        margin: 0;
                        font-family: Segoe UI, Tahoma, Geneva, Verdana, sans-serif;
                        background: linear-gradient(130deg, #0f172a, #1e293b);
                        color: #e2e8f0;
                        min-height: 100vh;
                        display: grid;
                        place-items: center;
                    }
                    .card {
                        width: min(720px, calc(100vw - 32px));
                        background: rgba(15, 23, 42, 0.7);
                        border: 1px solid rgba(148, 163, 184, 0.3);
                        border-radius: 14px;
                        padding: 20px;
                    }
                    .links a {
                        display: inline-block;
                        margin-right: 10px;
                        margin-top: 10px;
                        text-decoration: none;
                        padding: 9px 12px;
                        border-radius: 8px;
                        background: #334155;
                        color: #f8fafc;
                    }
                    .links a:hover { background: #475569; }
                </style>
            </head>
            <body>
                <main class=\"card\">
                    <h1>Video Orchestration Platform</h1>
                    <p>API-first render orchestration with queue workers, storage adapters, and Remotion planning docs.</p>
                    <div class=\"links\">
                        <a href=\"/docs\">OpenAPI UI</a>
                        <a href=\"/v1/remotion/ideas\">Remotion Feature Lab</a>
                    </div>
                </main>
            </body>
        </html>
        """
    return HTMLResponse(content=html)
