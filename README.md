# Backend I - Course Sessions

A comprehensive Django and FastAPI backend course covering APIs, testing, authentication, and deployment.

## Sessions Overview

| Session | Topic | Technology |
|---------|-------|------------|
| 1-4 | CLI Basics | Python/Typer |
| 5-14 | REST API | FastAPI |
| 15-17 | Django | Django ORM |

---

## Session 1 | CLI Basics

**Topic:** Meeting Note Assistant CLI

**Setup:**
```bash
cd session1
uv sync
```

**Test:**
```bash
uv run python session1/main.py --help
uv run python session1/main.py create-meeting --title "Planning" --date 2026-03-10 --owner Jorge
uv run python session1/main.py list-meetings
```

---

## Session 2 | Domain Models

**Topic:** In-memory data structures

**Setup:**
```bash
cd session2
uv sync
```

**Test:**
```bash
uv run python main.py
```

---

## Session 3 | CLI Refinement

**Topic:** Improved CLI with services

**Setup:**
```bash
cd session3
uv sync
```

**Test:**
```bash
uv run python -m app.cli
uv run python -m app.cli create-meeting --title "Sprint" --date 2026-03-15 --owner Ana
```

---

## Session 4 | File Persistence

**Topic:** JSON file storage

**Setup:**
```bash
cd session4
uv sync
```

**Test:**
```bash
uv run python main.py list
uv run python main.py add --title "Review" --date 2026-03-20 --owner Bruno
```

---

## Session 5 | FastAPI Setup

**Topic:** REST API introduction

**Setup:**
```bash
cd session5
uv sync
uv run pip install fastapi uvicorn
```

**Test:**
```bash
uv run uvicorn src.api.main:app --reload --port 8000
curl http://127.0.0.1:8000/
```

---

## Session 6 | CRUD Endpoints

**Topic:** Create, Read, Update, Delete

**Setup:**
```bash
cd session6
uv sync
uv run pip install fastapi uvicorn
```

**Test:**
```bash
uv run uvicorn src.api.main:app --reload --port 8000

# Create meeting
curl -X POST http://127.0.0.1:8000/meetings \
  -H "Content-Type: application/json" \
  -d '{"title":"Planning","date":"2026-03-10","owner":"Jorge"}'

# List meetings
curl http://127.0.0.1:8000/meetings

# Get meeting by ID
curl http://127.0.0.1:8000/meetings/{id}

# Update meeting
curl -X PUT http://127.0.0.1:8000/meetings/{id} \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Planning","date":"2026-03-10","owner":"Jorge"}'

# Delete meeting
curl -X DELETE http://127.0.0.1:8000/meetings/{id}
```

---

## Session 7 | Error Handling

**Topic:** HTTP exceptions and validation

**Setup:**
```bash
cd session7
uv sync
```

**Test:**
```bash
uv run uvicorn src.api.main:app --reload --port 8000

# Valid request
curl -X POST http://127.0.0.1:8000/meetings \
  -H "Content-Type: application/json" \
  -d '{"title":"Planning","date":"2026-03-10","owner":"Jorge"}'

# Invalid request (missing required field)
curl -X POST http://127.0.0.1:8000/meetings \
  -H "Content-Type: application/json" \
  -d '{"date":"2026-03-10"}'

# Not found
curl http://127.0.0.1:8000/meetings/nonexistent-id
```

---

## Session 8 | Report Service

**Topic:** Business logic separation

**Setup:**
```bash
cd session8
uv sync
```

**Test:**
```bash
uv run uvicorn src.api.main:app --reload --port 8000
curl http://127.0.0.1:8000/reports/summary
```

---

## Session 9 | Request Schemas

**Topic:** Pydantic validation

**Setup:**
```bash
cd session9
uv sync
```

**Test:**
```bash
uv run uvicorn src.api.main:app --reload --port 8000

# Valid payload
curl -X POST http://127.0.0.1:8000/meetings \
  -H "Content-Type: application/json" \
  -d '{"title":"Planning","date":"2026-03-10","owner":"Jorge","participants":["Ana"]}'

# Invalid date format
curl -X POST http://127.0.0.1:8000/meetings \
  -H "Content-Type: application/json" \
  -d '{"title":"Planning","date":"invalid","owner":"Jorge"}'
```

---

## Session 10 | Action Items

**Topic:** Nested resources

**Setup:**
```bash
cd session10
uv sync
```

**Test:**
```bash
uv run uvicorn src.api.main:app --reload --port 8000

# Create meeting
MEETING_ID=$(curl -s -X POST http://127.0.0.1:8000/meetings \
  -H "Content-Type: application/json" \
  -d '{"title":"Planning","date":"2026-03-10","owner":"Jorge"}' | jq -r '.id')

# Create action item
curl -X POST "http://127.0.0.1:8000/meetings/$MEETING_ID/action-items" \
  -H "Content-Type: application/json" \
  -d '{"description":"Review doc","owner":"Ana","due_date":"2026-03-15"}'

# List action items
curl http://127.0.0.1:8000/action-items
```

---

## Session 11 | Action Items Router

**Topic:** Separate routers for action items

**Setup:**
```bash
cd session11
uv sync
```

**Test:**
```bash
uv run uvicorn src.api.main:app --reload --port 8000

# Full CRUD for meetings and action items
curl http://127.0.0.1:8000/meetings
curl http://127.0.0.1:8000/action-items
```

---

## Session 12 | Filters, Sorting, and Pagination

**Topic:** Query parameters for search and navigation

**Setup:**
```bash
cd session12
uv sync
```

**Test:**
```bash
uv run uvicorn src.api.main:app --reload --port 8000

# Filter by owner
curl "http://127.0.0.1:8000/meetings?owner=Jorge"

# Pagination
curl "http://127.0.0.1:8000/meetings?limit=10&offset=0"

# Sorting
curl "http://127.0.0.1:8000/meetings?sort_by=date&order=desc"

# Combined filters
curl "http://127.0.0.1:8000/meetings?owner=Jorge&limit=5&offset=0&status=scheduled"

# Filter action items by owner
curl "http://127.0.0.1:8000/action-items?owner=Ana&limit=10"
```

---

## Session 13 | API Testing

**Topic:** pytest and TestClient

**Setup:**
```bash
cd session13
uv sync
uv pip install pytest httpx
```

**Test:**
```bash
# Run all tests
uv run pytest -q

# Run with verbose output
uv run pytest -v

# Run specific test
uv run pytest tests/test_meetings.py::test_health_ok -v
```

---

## Session 14 | API Checkpoint

**Topic:** OpenAPI metadata and dashboard

**Setup:**
```bash
cd session14
uv sync
uv pip install pytest httpx
```

**Test:**
```bash
uv run uvicorn src.api.main:app --reload --port 8000

# Check OpenAPI info
curl http://127.0.0.1:8000/openapi.json | jq '.info'

# Access docs
# http://127.0.0.1:8000/docs

# Dashboard summary
curl http://127.0.0.1:8000/dashboard/summary | jq

# Run tests
uv run pytest -q
```

---

## Session 15 | Django Setup + Models

**Topic:** Django ORM with Meeting and ActionItem models

**Setup:**
```bash
cd session15
uv pip install django
uv run python manage.py migrate
```

**Test:**
```bash
# Create superuser
uv run python manage.py createsuperuser

# Run server
uv run python manage.py runserver

# Django shell
uv run python manage.py shell
>>> from meetings.models import Meeting, ActionItem
>>> m = Meeting.objects.create(title="Planning", date="2026-03-10", owner="Jorge")
>>> Meeting.objects.all()
>>> m.delete()
```

---

## Session 16 | Django Admin

**Topic:** Admin interface with custom actions

**Setup:**
```bash
cd session16
uv pip install django
uv run python manage.py migrate
uv run python manage.py createsuperuser
```

**Test:**
```bash
# Run server
uv run python manage.py runserver

# Visit http://127.0.0.1:8000/admin

# Features:
# - List/filter/search meetings
# - List/filter action items
# - Custom action: "Mark selected tasks as completed"
```

---

## Session 17 | Authentication and Permissions

**Topic:** Users, groups, and ownership-based permissions

**Setup:**
```bash
cd session17
uv pip install django
uv run python manage.py migrate
uv run python manage.py createsuperuser
```

**Test:**
```bash
# Create groups and permissions
uv run python manage.py shell
>>> from permissions_setup import setup_permissions, setup_action_item_permissions
>>> setup_permissions()
>>> setup_action_item_permissions()
>>> exit()

# Run server
uv run python manage.py runserver

# Visit http://127.0.0.1:8000/admin
# Create users and assign to groups (admin, editor, viewer)
# Test that:
# - viewers can only view
# - editors can view and edit (not delete)
# - admins have full access
# - owners can edit their own items
```

---

## Quick Start - All Sessions

```bash
# Clone the repository
git clone https://github.com/PauloLobito/backend-i.git
cd backend-i

# Run tests for all FastAPI sessions (13-14)
for i in 13 14; do
  cd session$i
  uv sync
  uv run pytest -q
  cd ..
done

# Run Django migrations (15-17)
for i in 15 16 17; do
  cd session$i
  uv pip install django
  uv run python manage.py migrate
  cd ..
done
```

---

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Django (sessions 15-17)
- FastAPI (sessions 5-14)

---

## License

MIT
