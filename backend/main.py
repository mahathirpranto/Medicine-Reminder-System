from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

try:
    from database import init_db
    from routers.medicines import router as medicines_router
except ImportError:
    from .database import init_db
    from .routers.medicines import router as medicines_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables and seed data if needed on startup
    init_db()
    yield


app = FastAPI(
    title="Medicine Reminder System API",
    description="REST API for CSE309 Mid Project MVP - Medicine Reminder System",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# Initialize database tables immediately on app load
init_db()

# Enable CORS for frontend development and external API testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Medicine CRUD Router (mounted at both /medicines and /api/medicines)
app.include_router(medicines_router)
app.include_router(medicines_router, prefix="/api")


# Support both /docs and /api/docs for Swagger UI
@app.get("/docs", include_in_schema=False)
def swagger_docs():
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="Medicine Reminder System API - Docs")


# Health check endpoints
@app.get("/health", tags=["Health"])
@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "app": "Medicine Reminder System",
        "version": "1.0.0"
    }


# Frontend static files serving (when built for production)
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")
