from fastapi import APIRouter, HTTPException, Query, status

from src.api.schemas import (
    ActionItemCreate,
    ActionItemRead,
    ErrorResponse,
    ValidationErrorResponse,
)
from src.core.errors import NotFoundError, ValidationError
from src.repository import MeetingRepository
from src.services import MeetingService

router = APIRouter(tags=["action-items"])

repository = MeetingRepository()
service = MeetingService(repository)


@router.post(
    "/meetings/{meeting_id}/action-items",
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


@router.get("/action-items")
def list_action_items(
    owner: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> dict:
    result = service.list_meetings(limit=100000, offset=0)
    meetings = result["items"]

    items = []
    for meeting_id, meeting in meetings:
        for item in meeting.action_items:
            if owner and item.owner != owner:
                continue
            items.append(
                {
                    "id": item.id,
                    "description": item.description,
                    "owner": item.owner,
                    "due_date": item.due_date.strftime("%Y-%m-%d"),
                    "meeting_id": meeting_id,
                    "meeting_title": meeting.title,
                }
            )

    items = sorted(items, key=lambda x: (x["due_date"], x["id"]))
    total = len(items)

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items[offset : offset + limit],
    }