from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

try:
    from database import Base
except ImportError:
    from .database import Base


class User(Base):
    """
    SQLAlchemy model representing a registered user account.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="patient", nullable=False)
    is_main_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    medicines = relationship("Medicine", back_populates="user", cascade="all, delete-orphan")
    dose_logs = relationship("DoseLog", back_populates="user", cascade="all, delete-orphan")


class UserSession(Base):
    """
    SQLAlchemy model storing hashed refresh tokens to manage user sessions,
    token expiration, and revocation (logout).
    """
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(String, unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    user = relationship("User", back_populates="sessions")


class Medicine(Base):
    """
    SQLAlchemy model representing a medicine record in the database.
    Associated with a user_id for multi-user privacy.
    """
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    medicine_name = Column(String, nullable=False, index=True)
    dosage = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    reminder_time = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    status = Column(Boolean, default=True, nullable=False)

    # Relationships
    user = relationship("User", back_populates="medicines")
    dose_logs = relationship("DoseLog", back_populates="medicine", cascade="all, delete-orphan")


class DoseLog(Base):
    """
    SQLAlchemy model representing a recorded medicine dose event.
    Tracks whether a scheduled dose was taken, skipped, or missed.
    """
    __tablename__ = "dose_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    medicine_id = Column(Integer, ForeignKey("medicines.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    dose_time = Column(String, nullable=False)  # Scheduled time, e.g. "08:00 AM" or date string
    taken_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String, default="taken", nullable=False)  # "taken", "skipped", "missed"
    notes = Column(Text, nullable=True)

    # Relationships
    medicine = relationship("Medicine", back_populates="dose_logs")
    user = relationship("User", back_populates="dose_logs")
