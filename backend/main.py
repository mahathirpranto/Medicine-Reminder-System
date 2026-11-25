from contextlib import asynccontextmanager
import os
from pathlib import Path
import traceback

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

try:
    from database import init_db, SessionLocal, engine
    from routers.medicines import medicines_router
    from routers.auth import auth_router, users_router
    from routers.admin import admin_router
except ImportError:
    from .database import init_db, SessionLocal, engine
    from .routers.medicines import medicines_router
    from .routers.auth import auth_router, users_router
    from .routers.admin import admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables and seed data if needed on startup
    try:
        init_db()
    except Exception as e:
        print(f"Startup DB initialization note: {e}")
    yield


app = FastAPI(
    title="Medicine Reminder System API",
    description="REST API with JWT Authentication, Refresh Token Sessions, and Medicine Reminder Management",
    version="2.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
    debug=True,
)

# Initialize database tables immediately on app load with safe error catching
try:
    init_db()
except Exception as e:
    print(f"Initial DB sync note: {e}")

# Enable CORS for frontend development and external API testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Authentication Routers (mounted at both /auth and /api/auth)
app.include_router(auth_router, prefix="/api/auth")
app.include_router(auth_router, prefix="/auth")

# Register Users Router (mounted at /api/users and /users)
app.include_router(users_router, prefix="/api/users")
app.include_router(users_router, prefix="/users")

# Register Admin RBAC Router (mounted at /api/admin and /admin)
app.include_router(admin_router, prefix="/api/admin")
app.include_router(admin_router, prefix="/admin")

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
        "version": "2.0.0"
    }


@app.get("/debug-check", tags=["Health"])
@app.get("/api/debug-check", tags=["Health"])
def debug_check():
    results = {}
    
    # 1. Check environment variables
    raw = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or ""
    results["db_url_set"] = bool(raw)
    results["db_url_prefix"] = (raw[:25] + "...") if raw else "none"
    results["engine_url"] = str(engine.url).split("@")[-1] if "@" in str(engine.url) else str(engine.url)
    results["jwt_secret_set"] = bool(os.getenv("JWT_SECRET"))

    # 2. Check bcrypt
    try:
        try:
            from auth import hash_password, verify_password
        except ImportError:
            from .auth import hash_password, verify_password
        h = hash_password("test1234")
        v = verify_password("test1234", h)
        results["bcrypt_ok"] = v
    except Exception as e:
        results["bcrypt_error"] = str(e)

    # 3. Check JWT
    try:
        try:
            from auth import create_access_token
        except ImportError:
            from .auth import create_access_token
        t = create_access_token(1, "test@example.com")
        results["jwt_ok"] = bool(t)
    except Exception as e:
        results["jwt_error"] = str(e)

    # 4. Check DB Connection & Query
    try:
        db = SessionLocal()
        try:
            try:
                from models import User
            except ImportError:
                from .models import User
            users_count = db.query(User).count()
            admin = db.query(User).filter(User.email == "admin@example.com").first()
            results["db_connected"] = True
            results["users_count"] = users_count
            results["admin_exists"] = bool(admin)
            if admin:
                results["admin_role"] = admin.role
                results["admin_is_main"] = admin.is_main_admin
        finally:
            db.close()
    except Exception as e:
        results["db_error"] = str(e)
        results["db_traceback"] = traceback.format_exc()

    return results


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "traceback": traceback.format_exc()},
    )


# Frontend static files serving (when built for production)
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")
