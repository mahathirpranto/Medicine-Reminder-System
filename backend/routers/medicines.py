from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

try:
    from database import get_db
    from schemas import MedicineCreate, MedicineUpdate, MedicineResponse
    from models import User
    from auth import get_current_user
    import crud
except ImportError:
    from ..database import get_db
    from ..schemas import MedicineCreate, MedicineUpdate, MedicineResponse
    from ..models import User
    from ..auth import get_current_user
    from .. import crud

medicines_router = APIRouter(prefix="/medicines", tags=["Medicines"])
router = medicines_router  # Alias for compatibility


# 1. CREATE: Add a new medicine
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


# 2. READ LIST: Get all medicines
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


# 3. READ SINGLE: Get one medicine by ID
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


# 4. UPDATE: Edit medicine by ID
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


# 5. DELETE: Remove medicine by ID
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
