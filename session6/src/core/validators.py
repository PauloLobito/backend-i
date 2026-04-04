from datetime import datetime

from core.errors import ValidationError


def validate_iso_date(value: str) -> None:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValidationError("Date must be YYYY-MM-DD") from exc