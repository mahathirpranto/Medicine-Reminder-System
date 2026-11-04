from sqlalchemy import Column, Integer, String, Boolean

try:
    from database import Base
except ImportError:
    from .database import Base


class Medicine(Base):
    """
    SQLAlchemy model representing a medicine record in the database.
    Corresponds to the required 'medicines' table design.
    """
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    medicine_name = Column(String, nullable=False, index=True)
    dosage = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    reminder_time = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    status = Column(Boolean, default=True, nullable=False)
