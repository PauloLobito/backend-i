"""
Demo script for Django shell operations with Meeting and ActionItem models.

Run this in the Django shell with:
    python manage.py shell < django_shell_demo.py

Or import and use the functions directly.
"""

from datetime import date
from meetings.models import Meeting, ActionItem


def create_meeting():
    meeting = Meeting.objects.create(
        title="Q2 Planning Meeting",
        date=date(2026, 4, 15),
        owner="John Doe"
    )
    print(f"Created meeting: {meeting.title} (id={meeting.id})")
    return meeting


def create_action_items_for_meeting(meeting):
    items = [
        ActionItem.objects.create(
            meeting=meeting,
            description="Review quarterly targets",
            owner="Alice Smith",
            due_date=date(2026, 4, 20)
        ),
        ActionItem.objects.create(
            meeting=meeting,
            description="Prepare budget proposal",
            owner="Bob Johnson",
            due_date=date(2026, 4, 25)
        ),
        ActionItem.objects.create(
            meeting=meeting,
            description="Schedule follow-up meeting",
            owner="John Doe",
            due_date=date(2026, 4, 30)
        ),
    ]
    print(f"Created {len(items)} action items for meeting: {meeting.title}")
    return items


def list_meetings():
    meetings = Meeting.objects.all()
    print("\n--- All Meetings ---")
    for m in meetings:
        print(f"  [{m.id}] {m.title} on {m.date} (owner: {m.owner})")
        for item in m.action_items.all():
            print(f"      - {item.description} | {item.owner} | {item.status}")
    return meetings


if __name__ == "__main__":
    meeting = create_meeting()
    create_action_items_for_meeting(meeting)
    list_meetings()
