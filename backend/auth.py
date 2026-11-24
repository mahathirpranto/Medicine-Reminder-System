import os
import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

try:
    from database import get_db
    from models import User
except ImportError:
    from .database import get_db
    from .models import User


# Secret settings
JWT_SECRET = os.getenv("JWT_SECRET", "medicine-reminder-super-secret-key-cse309-2026")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

# HTTP Bearer scheme for Swagger UI and Authorization headers
bearer_scheme = HTTPBearer(auto_error=False)


# ==========================================
# Password Hashing (bcrypt)
# ==========================================

def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against stored bcrypt hash."""
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False


# ==========================================
# Token Generation & Hashing
# ==========================================

def create_access_token(user_id: int, email: str, role: str = "patient", is_main_admin: bool = False) -> str:
    """
    Generate a stateless 15-minute JWT access token.
    Verified without database query.
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "is_main_admin": is_main_admin,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "type": "access",
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a signed JWT access token.
    Raises HTTPException(401) on expiration or invalid signature.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired. Please refresh your session.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def hash_token(raw_token: str) -> str:
    """Compute SHA-256 hash of a raw token string."""
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def generate_refresh_token() -> tuple[str, str, datetime]:
    """
    Generate an opaque cryptographically secure refresh token.
    Returns: (raw_token_for_client, sha256_hash_for_database, expires_at_datetime)
    """
    raw_token = secrets.token_urlsafe(48)
    token_hash = hash_token(raw_token)
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return raw_token, token_hash, expires_at


# ==========================================
# Current User Dependency
# ==========================================

def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Dependency to authenticate and return the current user from Bearer JWT.
    Enforces that the request is authenticated.
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid Bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(credentials.credentials)
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user identifier")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account not found or deactivated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """
    Optional user dependency for routes that can function with or without auth.
    """
    if not credentials or not credentials.credentials:
        return None
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload.get("sub"))
        return db.query(User).filter(User.id == user_id).first()
    except Exception:
        return None


# ==========================================
# Role-Based Access Control (RBAC) Dependencies
# ==========================================

def require_role(allowed_roles: list[str]):
    """
    Factory for role-based authorization dependencies.
    Verifies that the authenticated user's role is within allowed_roles.
    Raises HTTP 403 Forbidden if unauthorized.
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        user_role = getattr(current_user, "role", "patient") or "patient"
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: This action requires one of the following roles: {', '.join(allowed_roles)}. Your current role is '{user_role}'.",
            )
        return current_user

    return role_checker


def is_main_admin_user(user: User) -> bool:
    """Check whether a user is the primary System Administrator."""
    if not user:
        return False
    return bool(
        getattr(user, "is_main_admin", False)
        or getattr(user, "role", "") == "super_admin"
        or getattr(user, "email", "").lower() == "admin@example.com"
    )


# Convenient pre-configured role dependencies
require_admin = require_role(["admin", "super_admin"])
require_super_admin = require_role(["super_admin"])
require_patient = require_role(["patient"])
require_patient_or_admin = require_role(["patient", "admin", "super_admin"])
