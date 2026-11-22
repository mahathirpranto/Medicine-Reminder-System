from typing import List, Optional
from sqlalchemy.orm import Session

try:
    from models import Medicine
    from schemas import MedicineCreate, MedicineUpdate
except ImportError:
    from .models import Medicine
    from .schemas import MedicineCreate, MedicineUpdate


def get_medicines(
    db: Session,
    user_id: Optional[int] = None,
    search: Optional[str] = None,
    status: Optional[bool] = None,
) -> List[Medicine]:
    """
    Retrieve medicines for a specific user (or all if user_id is None).
    Supports search and status filtering.
    """
    query = db.query(Medicine)

    if user_id is not None:
        query = query.filter((Medicine.user_id == user_id) | (Medicine.user_id.is_(None)))

    if status is not None:
        query = query.filter(Medicine.status == status)

    if search:
        search_filter = f"%{search.strip()}%"
        query = query.filter(
            (Medicine.medicine_name.ilike(search_filter))
            | (Medicine.dosage.ilike(search_filter))
        )

    return query.order_by(Medicine.status.desc(), Medicine.id.desc()).all()


def get_medicine(
    db: Session, medicine_id: int, user_id: Optional[int] = None
) -> Optional[Medicine]:
    """Retrieve a single medicine record by ID, verifying user ownership if user_id provided."""
    query = db.query(Medicine).filter(Medicine.id == medicine_id)
    if user_id is not None:
        query = query.filter((Medicine.user_id == user_id) | (Medicine.user_id.is_(None)))
    return query.first()


def create_medicine(
    db: Session, medicine: MedicineCreate, user_id: Optional[int] = None
) -> Medicine:
    """Create and persist a new medicine record associated with the user."""
    db_medicine = Medicine(
        user_id=user_id,
        medicine_name=medicine.medicine_name.strip(),
        dosage=medicine.dosage.strip(),
        frequency=medicine.frequency.strip(),
        reminder_time=medicine.reminder_time.strip(),
        start_date=medicine.start_date.strip(),
        end_date=medicine.end_date.strip(),
        status=medicine.status,
    )
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    return db_medicine


def update_medicine(
    db: Session,
    medicine_id: int,
    medicine_data: MedicineUpdate,
    user_id: Optional[int] = None,
) -> Optional[Medicine]:
    """Update existing medicine fields, ensuring the user owns the record."""
    db_medicine = get_medicine(db, medicine_id, user_id=user_id)
    if not db_medicine:
        return None

    update_dict = medicine_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        if isinstance(value, str):
            setattr(db_medicine, key, value.strip())
        else:
            setattr(db_medicine, key, value)

    db.commit()
    db.refresh(db_medicine)
    return db_medicine


def delete_medicine(
    db: Session, medicine_id: int, user_id: Optional[int] = None
) -> Optional[Medicine]:
    """Delete a medicine record by ID, ensuring the user owns the record."""
    db_medicine = get_medicine(db, medicine_id, user_id=user_id)
    if not db_medicine:
        return None

    db.delete(db_medicine)
    db.commit()
    return db_medicine
