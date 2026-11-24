from datetime import datetime, date
from typing import List, Optional
from sqlalchemy.orm import Session

try:
    from models import Medicine, DoseLog
    from schemas import MedicineCreate, MedicineUpdate, DoseLogCreate
except ImportError:
    from .models import Medicine, DoseLog
    from .schemas import MedicineCreate, MedicineUpdate, DoseLogCreate


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


# ==========================================
# Dose Tracking Business Logic (Part 5)
# ==========================================

def log_dose(
    db: Session,
    medicine_id: int,
    dose_data: DoseLogCreate,
    user_id: int,
) -> Optional[DoseLog]:
    """Record a medicine dose as taken, skipped, or missed."""
    medicine = get_medicine(db, medicine_id, user_id=user_id)
    if not medicine:
        return None

    dose_time = dose_data.dose_time
    if not dose_time:
        # Default to first reminder time or current clock time
        first_time = medicine.reminder_time.split(",")[0].strip() if medicine.reminder_time else ""
        dose_time = first_time or datetime.now().strftime("%I:%M %p")

    new_log = DoseLog(
        medicine_id=medicine_id,
        user_id=user_id,
        dose_time=dose_time,
        taken_at=datetime.utcnow(),
        status=dose_data.status,
        notes=dose_data.notes,
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log


def get_dose_logs(
    db: Session,
    user_id: int,
    medicine_id: Optional[int] = None,
    limit: int = 50,
) -> List[DoseLog]:
    """Retrieve history of recorded doses for the authenticated user."""
    query = db.query(DoseLog).filter(DoseLog.user_id == user_id)
    if medicine_id is not None:
        query = query.filter(DoseLog.medicine_id == medicine_id)
    return query.order_by(DoseLog.taken_at.desc()).limit(limit).all()


def get_today_schedule(db: Session, user_id: int) -> List[dict]:
    """
    Return all active medicines for the user with their scheduled reminder times
    and whether each dose was already logged/taken today.
    """
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    medicines = get_medicines(db, user_id=user_id, status=True)
    today_logs = (
        db.query(DoseLog)
        .filter(DoseLog.user_id == user_id, DoseLog.taken_at >= today_start)
        .all()
    )

    # Map medicine_id to list of taken dose_times today
    taken_map: dict[int, list[str]] = {}
    for log in today_logs:
        taken_map.setdefault(log.medicine_id, []).append(log.dose_time)

    schedule = []
    for med in medicines:
        times = [t.strip() for t in med.reminder_time.split(",") if t.strip()]
        taken_times = taken_map.get(med.id, [])
        is_fully_taken = len(times) > 0 and all(t in taken_times for t in times)

        schedule.append({
            "medicine_id": med.id,
            "medicine_name": med.medicine_name,
            "dosage": med.dosage,
            "frequency": med.frequency,
            "scheduled_times": times,
            "taken_times": taken_times,
            "is_fully_taken": is_fully_taken,
            "status": med.status,
        })

    return schedule
