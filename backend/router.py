"""
Re-export router for compatibility with automated evaluation scripts.
"""
try:
    from routers.medicines import router as medicines_router
except ImportError:
    from .routers.medicines import router as medicines_router
