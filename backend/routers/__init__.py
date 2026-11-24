from .medicines import medicines_router
from .auth import auth_router, users_router
from .admin import admin_router

__all__ = ["medicines_router", "auth_router", "users_router", "admin_router"]
