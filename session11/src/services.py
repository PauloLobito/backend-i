import logging
from datetime import datetime
from uuid import uuid4

from src.api.models import ActionItem, Meeting, MeetingResponse
from src.core.errors import NotFoundError, ValidationError
from src.core.validators import validate_iso_date
from src.repository import MeetingRepository

logger = logging.getLogger(__name__)


class MeetingService:
    def __init__(self, repository: MeetingRepository):
        self.repository = repository

    def create_meeting(
        self,
        title: str,
        owner: str,
        due_date: str,
        participants: list[str] | None = None,
    ) -> MeetingResponse:
        logger.info(
            "Creating meeting title=%s owner=%s due_date=%s",
            title,
            owner,
            due_date,
        )

        if not title.strip():
            raise ValidationError("Title is required")
        if len(title.strip()) < 3:
            raise ValidationError("Title must have at least 3 characters")

        if not owner.strip():
            raise ValidationError("Owner is required")
        if len(owner.strip()) < 2:
            raise ValidationError("Owner must have at least 2 characters")

        if not due_date.strip():
            raise ValidationError("Due date is required")

        validate_iso_date(due_date)

        if participants is None or not participants:
            participants = [owner]

        cleaned_participants = [p.strip() for p in participants if p.strip()]
        if not cleaned_participants:
            raise ValidationError("Participants must not be empty")

        meeting_id = str(uuid4())
        meeting_date = datetime.strptime(due_date, "%Y-%m-%d")

        meeting = Meeting(
            title=title.strip(),
            owner=owner.strip(),
            participants=cleaned_participants,
            date=meeting_date,
            status="scheduled",
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
            raise NotFoundError("Meeting not found")

        return meeting

    def update_meeting(
        self,
        meeting_id: str,
        title: str,
        owner: str,
        due_date: str,
        participants: list[str],
        content: str = "",
        action_items: list[ActionItem] | None = None,
    ) -> Meeting:
        logger.info("Updating meeting id=%s", meeting_id)

        existing = self.repository.get(meeting_id)
        if existing is None:
            raise NotFoundError("Meeting not found")

        if not title.strip():
            raise ValidationError("Title is required")
        if len(title.strip()) < 3:
            raise ValidationError("Title must have at least 3 characters")

        if not owner.strip():
            raise ValidationError("Owner is required")
        if len(owner.strip()) < 2:
            raise ValidationError("Owner must have at least 2 characters")

        if not due_date.strip():
            raise ValidationError("Due date is required")

        validate_iso_date(due_date)

        cleaned_participants = [p.strip() for p in participants if p.strip()]
        if not cleaned_participants:
            raise ValidationError("Participants must not be empty")

        meeting = Meeting(
            title=title.strip(),
            owner=owner.strip(),
            participants=cleaned_participants,
            date=datetime.strptime(due_date, "%Y-%m-%d"),
            status=existing.status,
            content=content,
            action_items=action_items if action_items is not None else existing.action_items,
        )

        self.repository.save(meeting_id, meeting)
        logger.info("Meeting updated id=%s", meeting_id)
        return meeting

    def add_action_item(
        self,
        meeting_id: str,
        description: str,
        owner: str,
        due_date: str,
    ) -> ActionItem:
        logger.info("Adding action item to meeting id=%s", meeting_id)

        meeting = self.repository.get(meeting_id)
        if meeting is None:
            raise NotFoundError("Meeting not found")

        if not description.strip():
            raise ValidationError("Description is required")
        if len(description.strip()) < 3:
            raise ValidationError("Description must have at least 3 characters")

        if not owner.strip():
            raise ValidationError("Action item owner is required")
        if len(owner.strip()) < 2:
            raise ValidationError("Action item owner must have at least 2 characters")

        if not due_date.strip():
            raise ValidationError("Action item due date is required")

        validate_iso_date(due_date)

        item = ActionItem(
            id=str(uuid4()),
            description=description.strip(),
            owner=owner.strip(),
            due_date=datetime.strptime(due_date, "%Y-%m-%d"),
        )

        updated = Meeting(
            title=meeting.title,
            owner=meeting.owner,
            participants=meeting.participants,
            date=meeting.date,
            status=meeting.status,
            content=meeting.content,
            action_items=[*meeting.action_items, item],
        )

        self.repository.save(meeting_id, updated)
        logger.info("Action item added to meeting id=%s action_item_id=%s", meeting_id, item.id)
        return item

    def update_status(self, meeting_id: str, new_status: str) -> Meeting:
        logger.info("Updating status for meeting id=%s to %s", meeting_id, new_status)

        existing = self.repository.get(meeting_id)
        if existing is None:
            raise NotFoundError("Meeting not found")

        allowed_statuses = {"scheduled", "in_progress", "completed", "cancelled"}
        if new_status not in allowed_statuses:
            raise ValidationError("Invalid status")

        transitions = {
            "scheduled": {"in_progress", "cancelled"},
            "in_progress": {"completed", "cancelled"},
            "completed": set(),
            "cancelled": set(),
        }

        if new_status == existing.status:
            return existing

        if new_status not in transitions[existing.status]:
            raise ValidationError(
                f"Invalid status transition from {existing.status} to {new_status}"
            )

        updated = Meeting(
            title=existing.title,
            owner=existing.owner,
            participants=existing.participants,
            date=existing.date,
            status=new_status,
            content=existing.content,
            action_items=existing.action_items,
        )

        self.repository.save(meeting_id, updated)
        logger.info("Meeting status updated id=%s", meeting_id)
        return updated

    def delete_meeting(self, meeting_id: str) -> None:
        logger.info("Deleting meeting id=%s", meeting_id)

        deleted = self.repository.delete(meeting_id)
        if not deleted:
            raise NotFoundError("Meeting not found")

        logger.info("Meeting deleted id=%s", meeting_id)