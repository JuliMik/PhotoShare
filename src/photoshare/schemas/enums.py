from enum import Enum


# ==========================================
# System Access Control Enumerations
# ==========================================

class UserRole(str, Enum):
    """
    Enumeration mapping out the system security roles for Role-Based Access Control (RBAC).
    Inherits from 'str' to enforce clean serialization natively within Pydantic and SQLAlchemy fields.
    """
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
