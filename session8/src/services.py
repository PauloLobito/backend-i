import logging
from datetime import datetime
from uuid import uuid4

from src.api.models import Meeting, MeetingResponse
from src.core.errors import NotFoundError, ValidationError
from src.core.validators import validate_iso_date
from src.repository import MeetingRepository

logger = logging.getLogger(__name__)


class MeetingService:
    def __init__(self, repository: MeetingRepository):
        self.repository = repository

    def create_meeting(self, title: str, owner: str, due_date: str) -> MeetingResponse:
        logger.info(
            "Creating meeting title=%s owner=%s due_date=%s",
            title,
            owner,
            due_date,
        )

        if not title.strip():
            logger.warning("Invalid input: title is empty")
            raise ValidationError("Title is required")

        if not owner.strip():
            logger.warning("Invalid input: owner is empty")
            raise ValidationError("Owner is required")

        if not due_date.strip():
            logger.warning("Invalid input: due_date is empty")
            raise ValidationError("Due date is required")

        validate_iso_date(due_date)

        meeting_id = str(uuid4())
        meeting_date = datetime.strptime(due_date, "%Y-%m-%d")

        meeting = Meeting(
            title=title,
            owner=owner,
            date=meeting_date,
            content="",
            action_items=[],
        )

        self.repository.save(meeting_id, meeting)
        logger.info("Meeting created successfully id=%s", meeting_id)

        return MeetingResponse(id=meeting_id)

    def list_meetings(self) -> dict[str, Meeting]:
        logger.info("Listing meetings")
        meetings = self.repository.list_all()
        logger.info("Found %s meetings", len(meetings))
        return meetings

    def show_meeting(self, meeting_id: str) -> Meeting:
        logger.info("Fetching meeting id=%s", meeting_id)

        meeting = self.repository.get(meeting_id)
        if meeting is None:
            logger.warning("Meeting not found id=%s", meeting_id)
            raise NotFoundError("Meeting not found")

        logger.info("Meeting retrieved id=%s", meeting_id)
        return meeting

    def delete_meeting(self, meeting_id: str) -> None:
        logger.info("Deleting meeting id=%s", meeting_id)

        deleted = self.repository.delete(meeting_id)
        if not deleted:
            logger.warning("Meeting not found id=%s", meeting_id)
            raise NotFoundError("Meeting not found")

        logger.info("Meeting deleted id=%s", meeting_id)