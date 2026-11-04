import os
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from sqlalchemy import create_engine
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
        return urlunsplit(parts._replace(query=urlencode(query)))
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

# Engine creation
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

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

    Base.metadata.create_all(bind=engine)

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
    except Exception as e:
        db.rollback()
        print(f"Database initialization note: {e}")
    finally:
        db.close()
