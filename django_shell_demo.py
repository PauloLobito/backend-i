#!/usr/bin/env python
import os
import sys
import django

sys.path.insert(0, "/workspaces/backend-i/session15")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend_i_django.settings")
django.setup()

from meetings.models import Meeting, ActionItem
from datetime import date

print("=== Session 15: Django Models ===\n")

print("1. Create a Meeting:")
meeting = Meeting.objects.create(
    title="Sprint Planning", date=date(2026, 4, 10), owner="Jorge"
)
print(f"   Created: {meeting}")

print("\n2. Create ActionItems linked to Meeting:")
item1 = ActionItem.objects.create(
    meeting=meeting,
    description="Review backlog items",
    owner="Ana",
    due_date=date(2026, 4, 12),
)
item2 = ActionItem.objects.create(
    meeting=meeting,
    description="Update project board",
    owner="Carlos",
    due_date=date(2026, 4, 15),
)
print(f"   Created: {item1}")
print(f"   Created: {item2}")

print("\n3. List all Meetings:")
for m in Meeting.objects.all():
    print(f"   - {m}")

print("\n4. List ActionItems for the meeting:")
for item in meeting.action_items.all():
    print(f"   - {item} (status: {item.status})")

print("\n5. ForeignKey cascade delete test:")
print(f"   Meeting has {meeting.action_items.count()} action items")
meeting.delete()
print(f"   After delete, ActionItems remaining: {ActionItem.objects.count()}")

print("\n=== Done! ===")
