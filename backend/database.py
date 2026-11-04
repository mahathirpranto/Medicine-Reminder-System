import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Read DATABASE_URL or fall back to local SQLite database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./medicines.db")

# Handle Supabase / Heroku postgres URL format compatibility
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite requires specific connect args for multi-threaded FastAPI access
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
