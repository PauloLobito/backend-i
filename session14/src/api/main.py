from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.api.routers.meetings import router as meetings_router
from src.api.routers.action_items import router as action_items_router
from src.repository import MeetingRepository
from src.services import MeetingService

app = FastAPI(
    title="Meeting Note Assistant API",
    version="0.2.0",
    description="Meetings, notes, and action items management",
)


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


@app.get("/dashboard/summary")
def dashboard_summary() -> dict:
    repository = MeetingRepository()
    service = MeetingService(repository)
    result = service.list_meetings(limit=10000, offset=0)

    total_meetings = result["total"]
    total_action_items = 0
    meetings_by_status = {}
    action_items_by_owner = {}

    for meeting_id, meeting in result["items"]:
        status = meeting.status or "unknown"
        meetings_by_status[status] = meetings_by_status.get(status, 0) + 1

        for item in meeting.action_items:
            total_action_items += 1
            owner = item.owner or "unassigned"
            action_items_by_owner[owner] = action_items_by_owner.get(owner, 0) + 1

    return {
        "total_meetings": total_meetings,
        "total_action_items": total_action_items,
        "meetings_by_status": meetings_by_status,
        "action_items_by_owner": action_items_by_owner,
    }


app.include_router(meetings_router)
app.include_router(action_items_router)
