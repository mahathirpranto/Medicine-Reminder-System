"""
Admin Router (RBAC: Main System Administrator vs Secondary Admins)
Provides administrative endpoints accessible to users with 'admin' or 'super_admin' roles.
Enforces hierarchical protection:
- System Administrator (Main Admin) has supreme access.
- Secondary Admins (e.g., Vatista) can perform administrative operations but
  CANNOT modify, demote, or delete the Main System Administrator.
"""

from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

try:
    from database import get_db
    from models import User, Medicine, DoseLog
    from schemas import AdminStatsResponse, AdminUserSummary, UserRoleUpdate, MessageResponse
    from auth import require_admin, is_main_admin_user
except ImportError:
    from ..database import get_db
    from ..models import User, Medicine, DoseLog
    from ..schemas import AdminStatsResponse, AdminUserSummary, UserRoleUpdate, MessageResponse
    from ..auth import require_admin, is_main_admin_user


admin_router = APIRouter(tags=["Admin"])


@admin_router.get(
    "/stats",
    response_model=AdminStatsResponse,
    summary="Get system-wide health and usage statistics (Admin Only)",
)
def get_system_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """
    Returns aggregated system metrics across all patients and medications.
    Accessible to both Main System Administrator and secondary admins (e.g. Vatista).
    """
    total_users = db.query(User).count()
    total_patients = db.query(User).filter(User.role == "patient").count()
    total_admins = db.query(User).filter(User.role.in_(["admin", "super_admin"])).count()

    total_medicines = db.query(Medicine).count()
    active_medicines = db.query(Medicine).filter(Medicine.status == True).count()

    total_doses = db.query(DoseLog).count()
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    doses_today = (
        db.query(DoseLog)
        .filter(DoseLog.taken_at >= today_start, DoseLog.status == "taken")
        .count()
    )

    return AdminStatsResponse(
        total_users=total_users,
        total_patients=total_patients,
        total_admins=total_admins,
        total_medicines=total_medicines,
        active_medicines=active_medicines,
        total_doses_logged=total_doses,
        doses_taken_today=doses_today,
    )


@admin_router.get(
    "/users",
    response_model=List[AdminUserSummary],
    summary="List all registered users and their medication metrics (Admin Only)",
)
def list_all_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """
    Returns all registered users with their roles, main-admin status, and medication counts.
    Accessible to both Main System Administrator and secondary admins (e.g. Vatista).
    """
    users = db.query(User).order_by(User.created_at.desc()).all()
    results = []

    for u in users:
        med_count = db.query(Medicine).filter(Medicine.user_id == u.id).count()
        active_med_count = (
            db.query(Medicine)
            .filter(Medicine.user_id == u.id, Medicine.status == True)
            .count()
        )
        is_main = is_main_admin_user(u)
        results.append(
            AdminUserSummary(
                id=u.id,
                email=u.email,
                full_name=u.full_name,
                role=getattr(u, "role", "patient") or "patient",
                is_main_admin=is_main,
                created_at=u.created_at,
                medicines_count=med_count,
                active_medicines_count=active_med_count,
            )
        )

    return results


@admin_router.put(
    "/users/{user_id}/role",
    response_model=MessageResponse,
    summary="Update a user's role (Admin Only with Hierarchical Protection)",
)
def update_user_role(
    user_id: int,
    payload: UserRoleUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """
    Allows an administrator to modify user roles.
    HIERARCHICAL CONSTRAINTS:
    1. Secondary admins (like Vatista) CANNOT modify, demote, or alter the Main System Administrator.
    2. Only the Main System Administrator can designate a 'super_admin' or demote other admins.
    """
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    caller_is_main_admin = is_main_admin_user(admin)
    target_is_main_admin = is_main_admin_user(target_user)

    # 1. Protection for Main System Administrator
    if target_is_main_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied: You cannot modify, demote, or alter the role of the Main System Administrator.",
        )

    # 2. Only Main System Administrator can promote to super_admin
    if payload.role == "super_admin" and not caller_is_main_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied: Only the Main System Administrator can grant Super Admin privileges.",
        )

    # 3. Secondary admins cannot demote fellow administrators
    if target_user.role in ("admin", "super_admin") and not caller_is_main_admin and payload.role == "patient":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied: Secondary administrators cannot demote administrator accounts. Only the Main System Administrator can demote admins.",
        )

    target_user.role = payload.role
    db.commit()

    return MessageResponse(
        message=f"User '{target_user.email}' role successfully updated to '{payload.role}'."
    )


@admin_router.delete(
    "/users/{user_id}",
    response_model=MessageResponse,
    summary="Delete a user account (Main System Administrator Only)",
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """
    Allows the Main System Administrator to delete a user account and associated medicines/logs.
    HIERARCHICAL CONSTRAINTS:
    1. EXCLUSIVE PRIVILEGE: Only the Main System Administrator has authority to delete user accounts.
    2. The Main System Administrator can NEVER be deleted.
    3. Self-deletion via admin portal is prevented.
    """
    caller_is_main_admin = is_main_admin_user(admin)

    # 1. Only Main System Administrator can delete users
    if not caller_is_main_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied: Only the Main System Administrator has authority to delete user accounts.",
        )

    # 2. Prevent self-deletion
    if user_id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Administrators cannot delete their own account from the admin portal.",
        )

    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    target_is_main_admin = is_main_admin_user(target_user)

    # 3. Main System Administrator can never be deleted
    if target_is_main_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied: The Main System Administrator cannot be deleted.",
        )

    deleted_email = target_user.email
    db.delete(target_user)
    db.commit()

    return MessageResponse(
        message=f"User '{deleted_email}' and all associated records deleted successfully."
    )
