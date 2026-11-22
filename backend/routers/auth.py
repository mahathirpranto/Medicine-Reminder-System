from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

try:
    from database import get_db
    from models import User, UserSession
    from schemas import (
        UserSignup,
        UserLogin,
        UserResponse,
        TokenResponse,
        RefreshRequest,
        RefreshTokenResponse,
        MessageResponse,
    )
    from auth import (
        hash_password,
        verify_password,
        create_access_token,
        generate_refresh_token,
        hash_token,
        get_current_user,
    )
except ImportError:
    from ..database import get_db
    from ..models import User, UserSession
    from ..schemas import (
        UserSignup,
        UserLogin,
        UserResponse,
        TokenResponse,
        RefreshRequest,
        RefreshTokenResponse,
        MessageResponse,
    )
    from ..auth import (
        hash_password,
        verify_password,
        create_access_token,
        generate_refresh_token,
        hash_token,
        get_current_user,
    )

auth_router = APIRouter(tags=["Authentication"])
users_router = APIRouter(tags=["Users"])


# ==========================================
# Authentication Endpoints
# ==========================================

@auth_router.post(
    "/signup",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def signup(payload: UserSignup, db: Session = Depends(get_db)):
    """
    Registers a new user, hashes their password with bcrypt,
    generates a 15-minute access token and a 7-day refresh token,
    and stores the SHA-256 token hash in the user_sessions table.
    """
    normalized_email = payload.email.lower().strip()
    existing_user = db.query(User).filter(User.email == normalized_email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists.",
        )

    # Hash password with bcrypt
    hashed_pwd = hash_password(payload.password)

    new_user = User(
        email=normalized_email,
        full_name=payload.full_name.strip(),
        hashed_password=hashed_pwd,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate tokens
    access_token = create_access_token(new_user.id, new_user.email)
    raw_refresh_token, token_hash, expires_at = generate_refresh_token()

    # Store refresh token hash in database session table
    user_session = UserSession(
        user_id=new_user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        is_revoked=False,
    )
    db.add(user_session)
    db.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=raw_refresh_token,
        token_type="bearer",
        user=UserResponse.model_validate(new_user),
    )


@auth_router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login and obtain access & refresh tokens",
)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """
    Verifies user credentials. On success, issues a short-lived access token
    and creates a new session in user_sessions with a hashed refresh token.
    """
    normalized_email = payload.email.lower().strip()
    user = db.query(User).filter(User.email == normalized_email).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate tokens
    access_token = create_access_token(user.id, user.email)
    raw_refresh_token, token_hash, expires_at = generate_refresh_token()

    # Save session
    user_session = UserSession(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        is_revoked=False,
    )
    db.add(user_session)
    db.commit()

    return TokenResponse(
        access_token=access_token,
        refresh_token=raw_refresh_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )


@auth_router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    summary="Renew access token using a refresh token",
)
def refresh_session(payload: RefreshRequest, db: Session = Depends(get_db)):
    """
    Validates the refresh token against the hashed token in user_sessions.
    Checks that the session has not been revoked and has not expired,
    then issues a fresh 15-minute access token.
    """
    token_hash = hash_token(payload.refresh_token)
    session_record = db.query(UserSession).filter(UserSession.token_hash == token_hash).first()

    if not session_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if session_record.is_revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This refresh token has been revoked. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if session_record.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Session is valid - issue fresh access token
    new_access_token = create_access_token(session_record.user.id, session_record.user.email)
    return RefreshTokenResponse(access_token=new_access_token, token_type="bearer")


@auth_router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Revoke active refresh token session",
)
def logout(payload: RefreshRequest, db: Session = Depends(get_db)):
    """
    Revokes the refresh token in the database, preventing it from being used
    to generate any further access tokens.
    """
    token_hash = hash_token(payload.refresh_token)
    session_record = db.query(UserSession).filter(UserSession.token_hash == token_hash).first()

    if session_record:
        session_record.is_revoked = True
        db.commit()

    return MessageResponse(message="Successfully logged out. Session has been revoked.")


# ==========================================
# User Profile Endpoints
# ==========================================

@users_router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current logged-in user profile",
)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Returns the public profile of the currently authenticated user.
    Requires valid Bearer access token in Authorization header.
    """
    return UserResponse.model_validate(current_user)


# Also expose /me on auth_router for client convenience
@auth_router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current logged-in user profile (alias)",
)
def get_auth_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)
