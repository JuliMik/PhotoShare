"""
Utility module exposing internal helper functions to global application modules.
Provides string formatters, case converters, and layout normalizers.
"""

__all__ = ("camel_case_to_snake_case",)

# ==========================================
# Package Utilities Exports Matrix
# ==========================================

# Pulling down inner case conversion utilities into the root namespace
from .case_converter import camel_case_to_snake_case
