import logging

from fastapi import FastAPI, HTTPException

from src.api.models import Meeting
from src.core.errors import NotFoundError
from src.repository import MeetingRepository
from src.services import MeetingService

logger = logging.getLogger(__name__)

app = FastAPI(title="Meeting Note Assistant API")

repository = MeetingRepository()
service = MeetingService(repository)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/meetings", response_model=list[Meeting])
def list_meetings() -> list[Meeting]:
    logger.info("Listing meetings via API")
    meetings = service.list_meetings()
    return list(meetings.values())


@app.get("/meetings/{meeting_id}", response_model=Meeting)
def get_meeting(meeting_id: str) -> Meeting:
    logger.info("Fetching meeting via API id=%s", meeting_id)

    try:
        return service.show_meeting(meeting_id)
    except NotFoundError as exc:
        logger.warning("Meeting not found via API id=%s", meeting_id)
        raise HTTPException(status_code=404, detail=str(exc)) from exc