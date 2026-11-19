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
    search: Optional[str] = None,
    status: Optional[bool] = None
) -> List[Medicine]:
    """Retrieve all medicines with optional search and status filtering."""
    query = db.query(Medicine)

    if status is not None:
        query = query.filter(Medicine.status == status)

    if search:
        search_filter = f"%{search.strip()}%"
        query = query.filter(
            (Medicine.medicine_name.ilike(search_filter)) |
            (Medicine.dosage.ilike(search_filter))
        )

    return query.order_by(Medicine.status.desc(), Medicine.id.desc()).all()


def get_medicine(db: Session, medicine_id: int) -> Optional[Medicine]:
    """Retrieve a single medicine record by ID."""
    return db.query(Medicine).filter(Medicine.id == medicine_id).first()


def create_medicine(db: Session, medicine: MedicineCreate) -> Medicine:
    """Create and persist a new medicine record."""
    db_medicine = Medicine(
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
    medicine_data: MedicineUpdate
) -> Optional[Medicine]:
    """Update existing medicine fields."""
    db_medicine = get_medicine(db, medicine_id)
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


def delete_medicine(db: Session, medicine_id: int) -> Optional[Medicine]:
    """Delete a medicine record by ID."""
    db_medicine = get_medicine(db, medicine_id)
    if not db_medicine:
        return None

    db.delete(db_medicine)
    db.commit()
    return db_medicine
