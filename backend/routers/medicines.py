from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

try:
    from database import get_db
    from schemas import (
        MedicineCreate,
        MedicineUpdate,
        MedicineResponse,
        DoseLogCreate,
        DoseLogResponse,
        TodayScheduleItem,
    )
    from models import User
    from auth import get_current_user
    import crud
except ImportError:
    from ..database import get_db
    from ..schemas import (
        MedicineCreate,
        MedicineUpdate,
        MedicineResponse,
        DoseLogCreate,
        DoseLogResponse,
        TodayScheduleItem,
    )
    from ..models import User
    from ..auth import get_current_user
    from .. import crud

medicines_router = APIRouter(prefix="/medicines", tags=["Medicines"])
router = medicines_router  # Alias for compatibility


# ==========================================
# 1. TODAY'S SCHEDULE & REMINDERS (Part 5)
# (Must be defined before /{medicine_id} path)
# ==========================================

@medicines_router.get(
    "/schedule/today",
    response_model=List[TodayScheduleItem],
    summary="Get today's medication schedule and dose status",
)
def get_today_medication_schedule(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Returns all active medicines for today with their scheduled reminder times
    and whether each dose has already been taken today.
    """
    return crud.get_today_schedule(db=db, user_id=current_user.id)


@medicines_router.get(
    "/doses/history",
    response_model=List[DoseLogResponse],
    summary="Get user's recent dose history",
)
def get_user_dose_history(
    limit: int = Query(50, ge=1, le=100, description="Max logs to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve history of all doses recorded by the authenticated user."""
    logs = crud.get_dose_logs(db=db, user_id=current_user.id, limit=limit)
    # Populate medicine_name for convenience
    result = []
    for log in logs:
        item = DoseLogResponse.model_validate(log)
        if log.medicine:
            item.medicine_name = log.medicine.medicine_name
        result.append(item)
    return result


# ==========================================
# 2. MEDICINE CRUD OPERATIONS
# ==========================================

# CREATE: Add a new medicine
@medicines_router.post(
    "",
    response_model=MedicineResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new medicine",
)
def create_medicine(
    medicine: MedicineCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new medicine schedule in the database linked to the authenticated user."""
    return crud.create_medicine(db=db, medicine=medicine, user_id=current_user.id)


# READ LIST: Get all medicines
@medicines_router.get(
    "",
    response_model=List[MedicineResponse],
    summary="Get all medicines",
)
def get_medicines(
    search: Optional[str] = Query(None, description="Search by medicine name or dosage"),
    status: Optional[bool] = Query(None, description="Filter by active status (true/false)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve all medicines for the authenticated user with optional filtering."""
    return crud.get_medicines(db=db, user_id=current_user.id, search=search, status=status)


# READ SINGLE: Get one medicine by ID
@medicines_router.get(
    "/{medicine_id}",
    response_model=MedicineResponse,
    summary="Get one medicine by ID",
)
def get_medicine(
    medicine_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve a specific medicine record owned by the authenticated user."""
    db_medicine = crud.get_medicine(db=db, medicine_id=medicine_id, user_id=current_user.id)
    if not db_medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medicine with ID {medicine_id} not found",
        )
    return db_medicine


# UPDATE: Edit medicine by ID
@medicines_router.put(
    "/{medicine_id}",
    response_model=MedicineResponse,
    summary="Update medicine by ID",
)
def update_medicine(
    medicine_id: int,
    medicine_data: MedicineUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update details of an existing medicine owned by the authenticated user."""
    db_medicine = crud.update_medicine(
        db=db,
        medicine_id=medicine_id,
        medicine_data=medicine_data,
        user_id=current_user.id,
    )
    if not db_medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medicine with ID {medicine_id} not found",
        )
    return db_medicine


# DELETE: Remove medicine by ID
@medicines_router.delete(
    "/{medicine_id}",
    summary="Delete medicine by ID",
)
def delete_medicine(
    medicine_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a medicine record owned by the authenticated user."""
    db_medicine = crud.delete_medicine(
        db=db, medicine_id=medicine_id, user_id=current_user.id
    )
    if not db_medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medicine with ID {medicine_id} not found",
        )
    return {
        "message": f"Medicine '{db_medicine.medicine_name}' (ID: {db_medicine.id}) deleted successfully",
        "id": db_medicine.id,
    }


# ==========================================
# 3. DOSE TRACKING OPERATIONS (Part 5)
# ==========================================

@medicines_router.post(
    "/{medicine_id}/doses",
    response_model=DoseLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record a dose as taken or skipped",
)
def record_dose(
    medicine_id: int,
    dose_data: DoseLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Record an intake of medicine (mark as taken) for patient compliance tracking."""
    log = crud.log_dose(
        db=db,
        medicine_id=medicine_id,
        dose_data=dose_data,
        user_id=current_user.id,
    )
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medicine with ID {medicine_id} not found",
        )
    response = DoseLogResponse.model_validate(log)
    if log.medicine:
        response.medicine_name = log.medicine.medicine_name
    return response


@medicines_router.get(
    "/{medicine_id}/doses",
    response_model=List[DoseLogResponse],
    summary="Get dose history for a specific medicine",
)
def get_medicine_dose_history(
    medicine_id: int,
    limit: int = Query(30, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve history of recorded doses for this specific medicine."""
    medicine = crud.get_medicine(db, medicine_id=medicine_id, user_id=current_user.id)
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medicine with ID {medicine_id} not found",
        )
    logs = crud.get_dose_logs(db=db, user_id=current_user.id, medicine_id=medicine_id, limit=limit)
    result = []
    for log in logs:
        item = DoseLogResponse.model_validate(log)
        item.medicine_name = medicine.medicine_name
        result.append(item)
    return result
