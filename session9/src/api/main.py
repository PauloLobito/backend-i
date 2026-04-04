import logging

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.api.schemas import (
    ErrorResponse,
    MeetingCreate,
    MeetingRead,
    ValidationErrorResponse,
)
from src.core.errors import NotFoundError, ValidationError
from src.repository import MeetingRepository
from src.services import MeetingService

logger = logging.getLogger(__name__)

app = FastAPI(title="Meeting Note Assistant API")

repository = MeetingRepository()
service = MeetingService(repository)


@app.exception_handler(RequestValidationError)
def request_validation_exception_handler(_, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
        },
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get(
    "/meetings",
    response_model=list[MeetingRead],
)
def list_meetings() -> list[MeetingRead]:
    logger.info("Listing meetings via API")
    meetings = service.list_meetings()

    return [
        MeetingRead(
            id=meeting_id,
            title=meeting.title,
            date=meeting.date.strftime("%Y-%m-%d"),
            owner=meeting.owner,
            participants=meeting.participants,
            content=meeting.content,
            action_items=meeting.action_items,
        )
        for meeting_id, meeting in meetings.items()
    ]


@app.get(
    "/meetings/{meeting_id}",
    response_model=MeetingRead,
    responses={
        404: {"model": ErrorResponse},
    },
)
def get_meeting(meeting_id: str) -> MeetingRead:
    logger.info("Fetching meeting via API id=%s", meeting_id)

    try:
        meeting = service.show_meeting(meeting_id)
        return MeetingRead(
            id=meeting_id,
            title=meeting.title,
            date=meeting.date.strftime("%Y-%m-%d"),
            owner=meeting.owner,
            participants=meeting.participants,
            content=meeting.content,
            action_items=meeting.action_items,
        )
    except NotFoundError as exc:
        logger.warning("Meeting not found via API id=%s", meeting_id)
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post(
    "/meetings",
    response_model=MeetingRead,
    status_code=201,
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
    },
)
def create_meeting(payload: MeetingCreate) -> MeetingRead:
    logger.info(
        "Creating meeting via API title=%s owner=%s date=%s",
        payload.title,
        payload.owner,
        payload.date,
    )

    try:
        result = service.create_meeting(
            title=payload.title,
            owner=payload.owner,
            due_date=payload.date,
            participants=payload.participants,
        )

        meeting = service.show_meeting(result.id)

        return MeetingRead(
            id=result.id,
            title=meeting.title,
            date=meeting.date.strftime("%Y-%m-%d"),
            owner=meeting.owner,
            participants=meeting.participants,
            content=meeting.content,
            action_items=meeting.action_items,
        )
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc