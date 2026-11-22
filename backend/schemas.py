from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr


# ==========================================
# Auth & User Schemas
# ==========================================

class UserSignup(BaseModel):
    """Payload for user registration."""
    email: EmailStr = Field(..., description="User's valid email address")
    password: str = Field(..., min_length=6, description="Password (at least 6 characters)")
    full_name: str = Field(..., min_length=1, description="User's display or full name")


class UserLogin(BaseModel):
    """Payload for user authentication."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=1, description="User's password")


class UserResponse(BaseModel):
    """Public profile of an authenticated user."""
    id: int
    email: str
    full_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """Returned on successful login or registration."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshRequest(BaseModel):
    """Payload to request a new access token using a refresh token."""
    refresh_token: str = Field(..., min_length=1, description="The opaque refresh token string")


class RefreshTokenResponse(BaseModel):
    """Returned when an access token is renewed."""
    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    """Generic status/message response."""
    message: str


# ==========================================
# Medicine Schemas
# ==========================================

class MedicineBase(BaseModel):
    """Base schema with common medicine attributes."""
    medicine_name: str = Field(..., description="Name of the medicine, e.g. Paracetamol", min_length=1)
    dosage: str = Field(..., description="Dosage information, e.g. 500 mg, 1 tablet", min_length=1)
    frequency: str = Field(..., description="Frequency of intake, e.g. Twice daily", min_length=1)
    reminder_time: str = Field(..., description="Reminder time, e.g. 08:00 AM, 08:00 PM", min_length=1)
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)", min_length=1)
    end_date: str = Field(..., description="End date (YYYY-MM-DD)", min_length=1)
    status: bool = Field(default=True, description="Active status: True for active, False for inactive")


class MedicineCreate(MedicineBase):
    """Schema for creating a new medicine."""
    pass


class MedicineUpdate(BaseModel):
    """Schema for updating an existing medicine. All fields optional."""
    medicine_name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    reminder_time: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[bool] = None


class MedicineResponse(MedicineBase):
    """Schema for returning medicine data."""
    id: int
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
