from datetime import datetime

from src.core.errors import ValidationError


def validate_iso_date(value: str) -> None:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValidationError("Date must be in YYYY-MM-DD format") from exc