from datetime import date


def check_date_range(start_date: date | None, end_date: date | None) -> None:
    """Raise ValueError if end_date is before start_date; skip the check if either is missing."""
    if start_date is not None and end_date is not None and end_date < start_date:
        raise ValueError("end_date cannot be before start_date")
