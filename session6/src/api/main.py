from datetime import datetime
from uuid import uuid4
import logging

from fastapi import FastAPI, HTTPException

from api.models import Meeting, MeetingRequest, MeetingResponse
from core.errors import NotFoundError, ValidationError
from core.validators import validate_iso_date

logger = logging.getLogger(__name__)

api = FastAPI()

MEETINGS: dict[str, Meeting] = {}


@api.get("/", response_model=list[Meeting])
def list_meetings(
    title: str = "",
    owner: str = "",
    date: datetime | None = None,
) -> list[Meeting]:
    logger.info(
        "Listing meetings with filters title=%s owner=%s date=%s",
        title,
        owner,
        date,
    )

    results = list(MEETINGS.values())

    if title:
        results = [m for m in results if m.title == title]

    if owner:
        results = [m for m in results if m.owner == owner]

    if date is not None:
        results = [m for m in results if m.date == date]

    logger.info("Found %s meetings", len(results))
    return results


@api.post("/", response_model=MeetingResponse)
def create_meetings(meeting: MeetingRequest) -> MeetingResponse:
    logger.info(
        "Creating meeting title=%s owner=%s due_date=%s",
        meeting.title,
        meeting.owner,
        meeting.due_date,
    )

    try:
        if not meeting.owner.strip():
            logger.warning("Invalid input: owner is empty")
            raise ValidationError("Owner is required")

        if not meeting.due_date.strip():
            logger.warning("Invalid input: due_date is empty")
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

        logger.info("Meeting created successfully id=%s", meeting_id)
        return MeetingResponse(id=meeting_id)

    except ValidationError as exc:
        logger.warning("Validation error while creating meeting: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.error("Unexpected error while creating meeting: %s", exc)
        raise


@api.get("/{meeting_id}", response_model=Meeting)
def get_meeting(meeting_id: str) -> Meeting:
    logger.info("Fetching meeting id=%s", meeting_id)

    try:
        if meeting_id not in MEETINGS:
            logger.warning("Meeting not found id=%s", meeting_id)
            raise NotFoundError("Meeting not found")

        logger.info("Meeting retrieved id=%s", meeting_id)
        return MEETINGS[meeting_id]

    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc