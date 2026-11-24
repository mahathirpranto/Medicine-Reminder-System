from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr


# ==========================================
# Auth & User Schemas
# ==========================================

class UserSignup(BaseModel):
    """Payload for user registration."""
    email: EmailStr = Field(..., description="User's valid email address")
    password: str = Field(..., min_length=6, description="Password (at least 6 characters)")
    full_name: str = Field(..., min_length=1, description="User's display or full name")
    role: Optional[str] = Field(default="patient", description="User role: patient (default) or admin")


class UserLogin(BaseModel):
    """Payload for user authentication."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=1, description="User's password")


class UserResponse(BaseModel):
    """Public profile of an authenticated user."""
    id: int
    email: str
    full_name: str
    role: str = "patient"
    is_main_admin: bool = False
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


# ==========================================
# Dose Tracking Schemas (Part 5)
# ==========================================

class DoseLogCreate(BaseModel):
    """Payload to record a taken or skipped medicine dose."""
    dose_time: Optional[str] = Field(default=None, description="Scheduled time string, e.g. 08:00 AM")
    status: str = Field(default="taken", description="Dose status: taken, skipped, or missed")
    notes: Optional[str] = Field(default=None, description="Optional patient notes")


class DoseLogResponse(BaseModel):
    """Returned when a dose record is inspected."""
    id: int
    medicine_id: int
    user_id: int
    dose_time: str
    taken_at: datetime
    status: str
    notes: Optional[str] = None
    medicine_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class TodayScheduleItem(BaseModel):
    """Scheduled medication item for today with dose completion status."""
    medicine_id: int
    medicine_name: str
    dosage: str
    frequency: str
    scheduled_times: List[str]
    taken_times: List[str]
    is_fully_taken: bool
    status: bool

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Admin & RBAC Schemas
# ==========================================

class AdminStatsResponse(BaseModel):
    """System-wide summary metrics for administrators."""
    total_users: int
    total_patients: int
    total_admins: int
    total_medicines: int
    active_medicines: int
    total_doses_logged: int
    doses_taken_today: int


class AdminUserSummary(BaseModel):
    """Summary of a user for admin listing."""
    id: int
    email: str
    full_name: str
    role: str
    is_main_admin: bool = False
    created_at: datetime
    medicines_count: int
    active_medicines_count: int

    model_config = ConfigDict(from_attributes=True)


class UserRoleUpdate(BaseModel):
    """Payload to update a user's role."""
    role: str = Field(..., pattern="^(patient|admin|super_admin)$", description="Role: patient, admin, or super_admin")
