from datetime import datetime
from uuid import uuid4

from fastapi import FastAPI, HTTPException

from api.models import Meeting, MeetingRequest, MeetingResponse
from core.errors import NotFoundError, ValidationError
from core.validators import validate_iso_date

api = FastAPI()

MEETINGS: dict[str, Meeting] = {}


@api.get("/", response_model=list[Meeting])
def list_meetings(
    title: str = "",
    owner: str = "",
    date: datetime | None = None,
) -> list[Meeting]:
    results = list(MEETINGS.values())

    if title:
        results = [m for m in results if m.title == title]

    if owner:
        results = [m for m in results if m.owner == owner]

    if date is not None:
        results = [m for m in results if m.date == date]

    return results


@api.post("/", response_model=MeetingResponse)
def create_meetings(meeting: MeetingRequest) -> MeetingResponse:
    try:
        if not meeting.owner.strip():
            raise ValidationError("Owner is required")

        if not meeting.due_date.strip():
            raise ValidationError("Due date is required")

        validate_iso_date(meeting.due_date)

        meeting_id = str(uuid4())
        meeting_date = datetime.strptime(meeting.due_date, "%Y-%m-%d")

        MEETINGS[meeting_id] = Meeting(
            title=meeting.title,
            owner=meeting.owner,
            date=meeting_date,
            content="",
        )

        return MeetingResponse(id=meeting_id)

    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@api.get("/{meeting_id}", response_model=Meeting)
def get_meeting(meeting_id: str) -> Meeting:
    try:
        if meeting_id not in MEETINGS:
            raise NotFoundError("Meeting not found")

        return MEETINGS[meeting_id]

    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc