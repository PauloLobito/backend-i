from datetime import datetime

from src.api.models import Meeting
from src.core.errors import ValidationError
from src.core.validators import validate_iso_date


def summary(meetings: list[Meeting]) -> dict:
    return {
        "meetings": len(meetings),
        "action_items": sum(len(m.action_items) for m in meetings),
    }


def period_summary(meetings: list[Meeting], from_date: str, to_date: str) -> dict:
    validate_iso_date(from_date)
    validate_iso_date(to_date)

    from_dt = datetime.strptime(from_date, "%Y-%m-%d")
    to_dt = datetime.strptime(to_date, "%Y-%m-%d")

    if from_dt > to_dt:
        raise ValidationError("from_date must be less than or equal to to_date")

    filtered = [meeting for meeting in meetings if from_dt <= meeting.date <= to_dt]

    return {
        "from_date": from_date,
        "to_date": to_date,
        "meetings": len(filtered),
        "action_items": sum(len(m.action_items) for m in filtered),
    }