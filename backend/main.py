import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

try:
    from database import get_db, init_db
    from models import Medicine
    from schemas import MedicineCreate, MedicineUpdate, MedicineResponse
except ImportError:
    from .database import get_db, init_db
    from .models import Medicine
    from .schemas import MedicineCreate, MedicineUpdate, MedicineResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables and seed data if needed on startup
    init_db()
    yield


app = FastAPI(
    title="Medicine Reminder System API",
    description="REST API for CSE309 Mid Project MVP - Medicine Reminder System",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# Initialize database tables immediately on app load
init_db()

# Support both /docs and /api/docs
@app.get("/docs", include_in_schema=False)
def swagger_docs():
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="Medicine Reminder System API - Docs")


# Enable CORS for frontend development and external API testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoints
@app.get("/health", tags=["Health"])
@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "app": "Medicine Reminder System",
        "version": "1.0.0"
    }


# ==========================================
# CRUD Operations for Medicines
# ==========================================

# 1. CREATE: Add a new medicine
@app.post(
    "/medicines",
    response_model=MedicineResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Medicines"],
    summary="Add a new medicine"
)
@app.post(
    "/api/medicines",
    response_model=MedicineResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False
)
def create_medicine(medicine: MedicineCreate, db: Session = Depends(get_db)):
    """
    Create a new medicine record in the system.
    """
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


# 2. READ LIST: Get all medicines (with optional search and status filter)
@app.get(
    "/medicines",
    response_model=List[MedicineResponse],
    tags=["Medicines"],
    summary="Get all medicines"
)
@app.get(
    "/api/medicines",
    response_model=List[MedicineResponse],
    include_in_schema=False
)
def get_medicines(
    search: Optional[str] = Query(None, description="Search by medicine name or dosage"),
    status: Optional[bool] = Query(None, description="Filter by active status (true/false)"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all medicines from the database with optional filtering.
    """
    query = db.query(Medicine)

    if status is not None:
        query = query.filter(Medicine.status == status)

    if search:
        search_filter = f"%{search.strip()}%"
        query = query.filter(
            (Medicine.medicine_name.ilike(search_filter)) |
            (Medicine.dosage.ilike(search_filter))
        )

    # Order by status (active first), then id descending
    return query.order_by(Medicine.status.desc(), Medicine.id.desc()).all()


# 3. READ SINGLE: Get one medicine by ID
@app.get(
    "/medicines/{medicine_id}",
    response_model=MedicineResponse,
    tags=["Medicines"],
    summary="Get one medicine by ID"
)
@app.get(
    "/api/medicines/{medicine_id}",
    response_model=MedicineResponse,
    include_in_schema=False
)
def get_medicine(medicine_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific medicine record by its unique ID.
    """
    db_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not db_medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medicine with ID {medicine_id} not found"
        )
    return db_medicine


# 4. UPDATE: Edit medicine by ID
@app.put(
    "/medicines/{medicine_id}",
    response_model=MedicineResponse,
    tags=["Medicines"],
    summary="Update medicine by ID"
)
@app.put(
    "/api/medicines/{medicine_id}",
    response_model=MedicineResponse,
    include_in_schema=False
)
def update_medicine(
    medicine_id: int,
    medicine_data: MedicineUpdate,
    db: Session = Depends(get_db)
):
    """
    Update details of an existing medicine by ID.
    """
    db_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not db_medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medicine with ID {medicine_id} not found"
        )

    # Update only fields provided
    update_dict = medicine_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        if isinstance(value, str):
            setattr(db_medicine, key, value.strip())
        else:
            setattr(db_medicine, key, value)

    db.commit()
    db.refresh(db_medicine)
    return db_medicine


# 5. DELETE: Remove medicine by ID
@app.delete(
    "/medicines/{medicine_id}",
    tags=["Medicines"],
    summary="Delete medicine by ID"
)
@app.delete(
    "/api/medicines/{medicine_id}",
    include_in_schema=False
)
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
    """
    Delete a medicine record by ID.
    """
    db_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not db_medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medicine with ID {medicine_id} not found"
        )

    deleted_id = db_medicine.id
    deleted_name = db_medicine.medicine_name
    db.delete(db_medicine)
    db.commit()
    return {
        "message": f"Medicine '{deleted_name}' (ID: {deleted_id}) deleted successfully",
        "id": deleted_id
    }


# Frontend static files serving (when built for production)
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")
