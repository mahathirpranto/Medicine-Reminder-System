from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

try:
    from database import get_db
    from schemas import MedicineCreate, MedicineUpdate, MedicineResponse
    import crud
except ImportError:
    from ..database import get_db
    from ..schemas import MedicineCreate, MedicineUpdate, MedicineResponse
    from .. import crud

router = APIRouter(prefix="/medicines", tags=["Medicines"])


# 1. CREATE: Add a new medicine
@router.post(
    "",
    response_model=MedicineResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new medicine"
)
def create_medicine(medicine: MedicineCreate, db: Session = Depends(get_db)):
    """Create a new medicine schedule in the database."""
    return crud.create_medicine(db=db, medicine=medicine)


# 2. READ LIST: Get all medicines
@router.get(
    "",
    response_model=List[MedicineResponse],
    summary="Get all medicines"
)
def get_medicines(
    search: Optional[str] = Query(None, description="Search by medicine name or dosage"),
    status: Optional[bool] = Query(None, description="Filter by active status (true/false)"),
    db: Session = Depends(get_db)
):
    """Retrieve all medicines from the database with optional filtering."""
    return crud.get_medicines(db=db, search=search, status=status)


# 3. READ SINGLE: Get one medicine by ID
@router.get(
    "/{medicine_id}",
    response_model=MedicineResponse,
    summary="Get one medicine by ID"
)
def get_medicine(medicine_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific medicine record by its unique ID."""
    db_medicine = crud.get_medicine(db=db, medicine_id=medicine_id)
    if not db_medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medicine with ID {medicine_id} not found"
        )
    return db_medicine


# 4. UPDATE: Edit medicine by ID
@router.put(
    "/{medicine_id}",
    response_model=MedicineResponse,
    summary="Update medicine by ID"
)
def update_medicine(
    medicine_id: int,
    medicine_data: MedicineUpdate,
    db: Session = Depends(get_db)
):
    """Update details of an existing medicine by ID."""
    db_medicine = crud.update_medicine(
        db=db,
        medicine_id=medicine_id,
        medicine_data=medicine_data
    )
    if not db_medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medicine with ID {medicine_id} not found"
        )
    return db_medicine


# 5. DELETE: Remove medicine by ID
@router.delete(
    "/{medicine_id}",
    summary="Delete medicine by ID"
)
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
    """Delete a medicine record by ID."""
    db_medicine = crud.delete_medicine(db=db, medicine_id=medicine_id)
    if not db_medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medicine with ID {medicine_id} not found"
        )
    return {
        "message": f"Medicine '{db_medicine.medicine_name}' (ID: {db_medicine.id}) deleted successfully",
        "id": db_medicine.id
    }
