from django.test import TestCase
from django.utils import timezone
from .models import Meeting, ActionItem


class MeetingModelTest(TestCase):
    def test_create_meeting(self):
        meeting = Meeting.objects.create(
            title="Test Meeting",
            date=timezone.now().date(),
            owner="John"
        )
        self.assertEqual(meeting.title, "Test Meeting")
        self.assertEqual(meeting.owner, "John")

    def test_create_action_item(self):
        meeting = Meeting.objects.create(
            title="Test Meeting",
            date=timezone.now().date(),
            owner="John"
        )
        item = ActionItem.objects.create(
            meeting=meeting,
            description="Test item",
            owner="Alice",
            due_date=timezone.now().date()
        )
        self.assertEqual(item.meeting, meeting)
        self.assertEqual(item.status, "open")

    def test_cascade_delete(self):
        meeting = Meeting.objects.create(
            title="Test Meeting",
            date=timezone.now().date(),
            owner="John"
        )
        ActionItem.objects.create(
            meeting=meeting,
            description="Test item",
            owner="Alice",
            due_date=timezone.now().date()
        )
        meeting_id = meeting.id
        meeting.delete()
        self.assertFalse(ActionItem.objects.filter(meeting_id=meeting_id).exists())
