from uuid import uuid4

from app.domain.models import Meeting
from app.services.memory_store import meetings


def create_meeting(title: str, date: str, owner: str) -> Meeting:
    meeting = Meeting(
        id=str(uuid4()),
        title=title,
        date=date,
        owner=owner,
    )

    meetings.append(meeting)
    return meeting


def list_meetings() -> list[Meeting]:
    return meetings


def get_meeting_by_id(meeting_id: str) -> Meeting | None:
    for m in meetings:
        if m.id == meeting_id:
            return m
    return None