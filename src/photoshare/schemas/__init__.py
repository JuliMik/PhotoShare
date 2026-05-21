"""
Explicitly exposes package components at the module root level.
Provides clean entry points for structural schemas and enumeration models.
"""

__all__ = (
    "UserRole",
)

# ==========================================
# Package Exports Matrix
# ==========================================

# Pulling down inner enumeration scopes into the namespace layer
from .enums import UserRole
