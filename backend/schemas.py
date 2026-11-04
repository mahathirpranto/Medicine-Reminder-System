from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


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

    model_config = ConfigDict(from_attributes=True)
