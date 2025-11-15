"""
Date utilities.

Helper functions for working with dates, e.g.:
  - calculating days until the next occurrence of a date (birthday)
"""

from datetime import date, datetime
from typing import Optional


def _to_date(value: datetime | date) -> date:
    """Normalize datetime/date to a date instance."""
    if isinstance(value, datetime):
        return value.date()
    return value
