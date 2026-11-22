from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
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
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    medicines = relationship("Medicine", back_populates="user", cascade="all, delete-orphan")


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
    Now associated with an optional/required user_id for multi-user privacy.
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

    # Relationship
    user = relationship("User", back_populates="medicines")
