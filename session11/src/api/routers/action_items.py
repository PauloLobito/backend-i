from fastapi import APIRouter, HTTPException, status

from src.api.schemas import (
    ActionItemCreate,
    ActionItemRead,
    ErrorResponse,
    ValidationErrorResponse,
)
from src.core.errors import NotFoundError, ValidationError
from src.repository import MeetingRepository
from src.services import MeetingService

router = APIRouter(prefix="/meetings", tags=["action-items"])

repository = MeetingRepository()
service = MeetingService(repository)


@router.post(
    "/{meeting_id}/action-items",
    response_model=ActionItemRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse},
    },
)
def create_action_item(meeting_id: str, payload: ActionItemCreate) -> ActionItemRead:
    try:
        item = service.add_action_item(
            meeting_id=meeting_id,
            description=payload.description,
            owner=payload.owner,
            due_date=payload.due_date,
        )
        return ActionItemRead(
            id=item.id,
            description=item.description,
            owner=item.owner,
            due_date=item.due_date.strftime("%Y-%m-%d"),
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc