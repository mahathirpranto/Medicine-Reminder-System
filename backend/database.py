import os
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Query parameters that Supabase and Vercel add but libpq/psycopg rejects
_UNSUPPORTED_QUERY_KEYS = {"supa", "pgbouncer"}


def _normalize_database_url(url: str) -> str:
    """Normalize postgres URL and strip unsupported query parameters."""
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    
    if url.startswith(("postgresql://", "postgresql+psycopg://", "postgresql+psycopg2://")):
        parts = urlsplit(url)
        query = [(k, v) for k, v in parse_qsl(parts.query) if k not in _UNSUPPORTED_QUERY_KEYS]
        normalized = urlunsplit(parts._replace(query=urlencode(query)))
        if normalized.startswith("postgresql://"):
            try:
                import psycopg  # noqa: F401
            except ImportError:
                try:
                    import psycopg2  # noqa: F401
                    normalized = normalized.replace("postgresql://", "postgresql+psycopg2://", 1)
                except ImportError:
                    pass
        return normalized
    return url


# Resolve DATABASE_URL from environment or fall back to SQLite
raw_db_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")

if raw_db_url:
    DATABASE_URL = _normalize_database_url(raw_db_url)
else:
    # On Vercel, the filesystem is read-only except /tmp
    if os.getenv("VERCEL"):
        db_path = Path("/tmp") / "medicines.db"
    else:
        db_path = Path(__file__).resolve().parent / "medicines.db"
    DATABASE_URL = f"sqlite:///{db_path.as_posix()}"

# Engine creation with connection pooling optimized for serverless deployments (Supabase/Vercel)
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,      # Test connections before giving them to the app
        pool_size=5,             # Keep up to 5 connections per serverless container
        max_overflow=10,         # Allow burst of up to 10 extra connections
        pool_recycle=300,        # Refresh stale connections after 5 minutes
        pool_timeout=30,         # Max seconds to wait for a connection
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency to provide a database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables and seed initial demo data if empty."""
    try:
        import models
    except ImportError:
        from . import models

    # Create all tables (users, user_sessions, medicines, dose_logs)
    Base.metadata.create_all(bind=engine)

    # Safe migration: ensure user_id column exists on medicines table if upgrading from older schema
    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE medicines ADD COLUMN user_id INTEGER REFERENCES users(id)"))
            conn.commit()
    except Exception:
        pass  # Column already exists

    # Safe migration: ensure role column exists on users table if upgrading from older schema
    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR DEFAULT 'patient'"))
            conn.commit()
    except Exception:
        pass  # Column already exists

    # Safe migration: ensure is_main_admin column exists on users table
    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN is_main_admin BOOLEAN DEFAULT FALSE"))
            conn.commit()
    except Exception:
        pass  # Column already exists

    # Seed initial medicines if table is empty
    db = SessionLocal()
    try:
        count = db.query(models.Medicine).count()
        if count == 0:
            sample_medicines = [
                models.Medicine(
                    medicine_name="Paracetamol",
                    dosage="500 mg",
                    frequency="Twice daily",
                    reminder_time="08:00 AM, 08:00 PM",
                    start_date="2026-11-01",
                    end_date="2026-11-10",
                    status=True,
                ),
                models.Medicine(
                    medicine_name="Vitamin D3",
                    dosage="1000 IU",
                    frequency="Once daily",
                    reminder_time="09:00 AM",
                    start_date="2026-11-01",
                    end_date="2026-12-01",
                    status=True,
                ),
                models.Medicine(
                    medicine_name="Amoxicillin",
                    dosage="250 mg",
                    frequency="Three times daily",
                    reminder_time="08:00 AM, 02:00 PM, 08:00 PM",
                    start_date="2026-11-02",
                    end_date="2026-11-09",
                    status=False,
                ),
            ]
            db.add_all(sample_medicines)
            db.commit()

        # Seed or upgrade Main System Administrator account
        try:
            from auth import hash_password
        except ImportError:
            from .auth import hash_password

        admin_user = db.query(models.User).filter(models.User.email == "admin@example.com").first()
        if not admin_user:
            new_admin = models.User(
                email="admin@example.com",
                full_name="System Administrator",
                hashed_password=hash_password("AdminPassword123!"),
                role="super_admin",
                is_main_admin=True,
            )
            db.add(new_admin)
            db.commit()
        else:
            # Ensure proper Main Admin flags
            admin_user.is_main_admin = True
            admin_user.role = "super_admin"
            admin_user.full_name = "System Administrator"
            db.commit()

        # Seed Vatista (Secondary Administrator) account
        vatista_user = db.query(models.User).filter(models.User.email == "vatista@example.com").first()
        if not vatista_user:
            new_vatista = models.User(
                email="vatista@example.com",
                full_name="Vatista (Admin)",
                hashed_password=hash_password("VatistaPassword123!"),
                role="admin",
                is_main_admin=False,
            )
            db.add(new_vatista)
            db.commit()
        else:
            vatista_user.role = "admin"
            vatista_user.is_main_admin = False
            db.commit()
    except Exception as e:
        db.rollback()
        print(f"Database initialization note: {e}")
    finally:
        db.close()
