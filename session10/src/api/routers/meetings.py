import logging

from fastapi import APIRouter, HTTPException, status

from src.api.schemas import (
    ErrorResponse,
    MeetingCreate,
    MeetingRead,
    MeetingStatusUpdate,
    MeetingUpdate,
    ValidationErrorResponse,
)
from src.core.errors import NotFoundError, ValidationError
from src.repository import MeetingRepository
from src.services import MeetingService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/meetings", tags=["meetings"])

repository = MeetingRepository()
service = MeetingService(repository)


def to_meeting_read(meeting_id: str, meeting) -> MeetingRead:
    return MeetingRead(
        id=meeting_id,
        title=meeting.title,
        date=meeting.date.strftime("%Y-%m-%d"),
        owner=meeting.owner,
        participants=meeting.participants,
        status=meeting.status,
        content=meeting.content,
        action_items=meeting.action_items,
    )


@router.post(
    "",
    response_model=MeetingRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
    },
)
def create_meeting(payload: MeetingCreate) -> MeetingRead:
    try:
        result = service.create_meeting(
            title=payload.title,
            owner=payload.owner,
            due_date=payload.date,
            participants=payload.participants,
        )
        meeting = service.show_meeting(result.id)
        return to_meeting_read(result.id, meeting)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("", response_model=list[MeetingRead])
def list_meetings() -> list[MeetingRead]:
    meetings = service.list_meetings()
    return [
        to_meeting_read(meeting_id, meeting)
        for meeting_id, meeting in meetings.items()
    ]


@router.get(
    "/{meeting_id}",
    response_model=MeetingRead,
    responses={404: {"model": ErrorResponse}},
)
def get_meeting(meeting_id: str) -> MeetingRead:
    try:
        meeting = service.show_meeting(meeting_id)
        return to_meeting_read(meeting_id, meeting)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.put(
    "/{meeting_id}",
    response_model=MeetingRead,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
    },
)
def update_meeting(meeting_id: str, payload: MeetingUpdate) -> MeetingRead:
    try:
        meeting = service.update_meeting(
            meeting_id=meeting_id,
            title=payload.title,
            owner=payload.owner,
            due_date=payload.date,
            participants=payload.participants,
            content=payload.content,
            action_items=payload.action_items,
        )
        return to_meeting_read(meeting_id, meeting)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.patch(
    "/{meeting_id}/status",
    response_model=MeetingRead,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
def patch_meeting_status(
    meeting_id: str,
    payload: MeetingStatusUpdate,
) -> MeetingRead:
    try:
        meeting = service.update_status(meeting_id, payload.status)
        return to_meeting_read(meeting_id, meeting)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete(
    "/{meeting_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse}},
)
def delete_meeting(meeting_id: str) -> None:
    try:
        service.delete_meeting(meeting_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc