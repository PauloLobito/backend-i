# Backend I - Course Sessions

A comprehensive Django and FastAPI backend course covering APIs, testing, authentication, and deployment.

## Repository

**GitHub:** https://github.com/PauloLobito/backend-i

## Sessions Overview

| Session | Topic | Technology | Web Testing |
|---------|-------|------------|-------------|
| 1-4 | CLI Basics | Python/Typer | Terminal only |
| 5-14 | REST API | FastAPI | ✅ Browser |
| 15-17 | Django | Django ORM | ✅ Browser |

---

## FastAPI Web Interface (Sessions 5-14)

All FastAPI sessions include an **interactive web interface** for testing:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc
- **OpenAPI JSON:** http://127.0.0.1:8000/openapi.json

### How to Access

```bash
# 1. Go to any session folder (5-14)
cd session5  # or session6, session7, etc.

# 2. Install dependencies
uv sync

# 3. Start the server
uv run uvicorn src.api.main:app --reload --port 8000

# 4. Open in browser:
#    - http://127.0.0.1:8000/docs
#    - http://127.0.0.1:8000/redoc
```

---

## Session 1 | CLI Basics

**Topic:** Meeting Note Assistant CLI

**Setup:**
```bash
cd session1
uv sync
```

**Test (Terminal):**
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
```

**Web Testing:**
- Open: http://127.0.0.1:8000/docs
- Click "GET /" → "Try it out" → "Execute"

---

## Session 6 | CRUD Endpoints

**Topic:** Create, Read, Update, Delete

**Setup:**
```bash
cd session6
uv sync
uv run pip install fastapi uvicorn
```

**Start Server:**
```bash
uv run uvicorn src.api.main:app --reload --port 8000
```

**Web Testing (http://127.0.0.1:8000/docs):**

| Operation | Endpoint | Method |
|-----------|----------|--------|
| Create meeting | /meetings | POST |
| List meetings | /meetings | GET |
| Get meeting | /meetings/{id} | GET |
| Update meeting | /meetings/{id} | PUT |
| Delete meeting | /meetings/{id} | DELETE |

**Terminal Testing:**
```bash
# Create meeting
curl -X POST http://127.0.0.1:8000/meetings \
  -H "Content-Type: application/json" \
  -d '{"title":"Planning","date":"2026-03-10","owner":"Jorge"}'

# List meetings
curl http://127.0.0.1:8000/meetings
```

---

## Session 7 | Error Handling

**Topic:** HTTP exceptions and validation

**Setup:**
```bash
cd session7
uv sync
```

**Start Server:**
```bash
uv run uvicorn src.api.main:app --reload --port 8000
```

**Web Testing (http://127.0.0.1:8000/docs):**

1. Try "POST /meetings" with missing required field → 422 error
2. Try "GET /meetings/{id}" with invalid ID → 404 error

**Terminal Testing:**
```bash
# Valid request
curl -X POST http://127.0.0.1:8000/meetings \
  -H "Content-Type: application/json" \
  -d '{"title":"Planning","date":"2026-03-10","owner":"Jorge"}'

# Invalid request (missing required field)
curl -X POST http://127.0.0.1:8000/meetings \
  -H "Content-Type: application/json" \
  -d '{"date":"2026-03-10"}'
```

---

## Session 8 | Report Service

**Topic:** Business logic separation

**Setup:**
```bash
cd session8
uv sync
```

**Start Server:**
```bash
uv run uvicorn src.api.main:app --reload --port 8000
```

**Web Testing:**
- http://127.0.0.1:8000/docs → "GET /reports/summary" → "Try it out" → "Execute"

**Terminal Testing:**
```bash
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

**Start Server:**
```bash
uv run uvicorn src.api.main:app --reload --port 8000
```

**Web Testing (http://127.0.0.1:8000/docs):**

1. "POST /meetings" with valid data → 201 Created
2. "POST /meetings" with invalid date → 422 Validation Error
3. "POST /meetings" with empty title → 422 Validation Error

---

## Session 10 | Action Items

**Topic:** Nested resources

**Setup:**
```bash
cd session10
uv sync
```

**Start Server:**
```bash
uv run uvicorn src.api.main:app --reload --port 8000
```

**Web Testing (http://127.0.0.1:8000/docs):**

| Operation | Endpoint | Method |
|-----------|----------|--------|
| Create meeting | /meetings | POST |
| Create action item | /meetings/{id}/action-items | POST |
| List action items | /action-items | GET |

**Terminal Testing:**
```bash
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

**Start Server:**
```bash
uv run uvicorn src.api.main:app --reload --port 8000
```

**Web Testing (http://127.0.0.1:8000/docs):**

Test all CRUD operations for both meetings and action items.

---

## Session 12 | Filters, Sorting, and Pagination

**Topic:** Query parameters for search and navigation

**Setup:**
```bash
cd session12
uv sync
```

**Start Server:**
```bash
uv run uvicorn src.api.main:app --reload --port 8000
```

**Web Testing (http://127.0.0.1:8000/docs):**

| Filter | Query Param | Example |
|--------|-------------|---------|
| By owner | owner=Jorge | /meetings?owner=Jorge |
| By status | status=scheduled | /meetings?status=scheduled |
| Limit | limit=10 | /meetings?limit=10 |
| Offset | offset=0 | /meetings?offset=0 |
| Sort by | sort_by=date | /meetings?sort_by=date |
| Order | order=desc | /meetings?order=desc |
| Combined | all filters | /meetings?owner=Jorge&limit=5&offset=0 |

**Try in Swagger UI:**
1. "GET /meetings" → "Try it out"
2. Add query: `owner=Jorge&limit=10&offset=0&sort_by=date&order=asc`
3. "Execute"

**Terminal Testing:**
```bash
# Filter by owner
curl "http://127.0.0.1:8000/meetings?owner=Jorge"

# Pagination
curl "http://127.0.0.1:8000/meetings?limit=10&offset=0"

# Sorting
curl "http://127.0.0.1:8000/meetings?sort_by=date&order=desc"

# Combined filters
curl "http://127.0.0.1:8000/meetings?owner=Jorge&limit=5&offset=0&status=scheduled"
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

**Web Testing:**
```bash
uv run uvicorn src.api.main:app --reload --port 8000
# Then open http://127.0.0.1:8000/docs
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

**Start Server:**
```bash
uv run uvicorn src.api.main:app --reload --port 8000
```

**Web Testing:**

| Page | URL | Description |
|------|-----|-------------|
| Swagger UI | http://127.0.0.1:8000/docs | Interactive API docs |
| ReDoc | http://127.0.0.1:8000/redoc | Alternative docs view |
| Dashboard | http://127.0.0.1:8000/dashboard/summary | API metrics |
| Health | http://127.0.0.1:8000/health | Health check |

**OpenAPI Info:**
```bash
curl http://127.0.0.1:8000/openapi.json | jq '.info'
```

**Expected Output:**
```json
{
  "title": "Meeting Note Assistant API",
  "version": "0.2.0",
  "description": "Meetings, notes, and action items management"
}
```

**Run Tests:**
```bash
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

**Start Server:**
```bash
uv run python manage.py runserver
```

**Web Testing:**
- Open: http://127.0.0.1:8000/admin

**Django Shell Testing:**
```bash
uv run python manage.py shell
>>> from meetings.models import Meeting, ActionItem
>>> m = Meeting.objects.create(title="Planning", date="2026-03-10", owner="Jorge")
>>> Meeting.objects.all()
>>> ActionItem.objects.create(meeting=m, description="Review doc", owner="Ana", due_date="2026-03-15")
>>> m.action_items.all()
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

**Start Server:**
```bash
uv run python manage.py runserver
```

**Web Testing:**

1. Open: http://127.0.0.1:8000/admin
2. Login with superuser credentials
3. Test **Meetings**:
   - List all meetings
   - Filter by date/owner
   - Search by title/owner
   - Create new meeting
   - Edit existing meeting
4. Test **Action Items**:
   - List all action items
   - Filter by status
   - Search by description/owner
   - Create new action item
5. Test **Custom Action**:
   - Select action items
   - Choose "Mark selected tasks as completed"
   - Click "Go"

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

**Setup Permissions:**
```bash
uv run python manage.py shell
>>> from permissions_setup import setup_permissions, setup_action_item_permissions
>>> setup_permissions()
>>> setup_action_item_permissions()
>>> exit()
```

**Start Server:**
```bash
uv run python manage.py runserver
```

**Web Testing:**

1. Open: http://127.0.0.1:8000/admin
2. Login as superuser
3. Create users and assign to groups:
   - **admin** - Full access (add, change, delete, view)
   - **editor** - Add, change, view (no delete)
   - **viewer** - View only (no add, change, delete)
4. Logout and login as different users to test permissions

---

## Quick Start - All Sessions

### FastAPI Sessions (5-14)
```bash
for i in 5 6 7 8 9 10 11 12 13 14; do
  cd session$i
  uv sync
  uv run uvicorn src.api.main:app --reload --port 8000 &
  echo "Testing session$i..."
  sleep 2
  curl http://127.0.0.1:8000/docs
  kill %1 2>/dev/null
  cd ..
done
```

### Django Sessions (15-17)
```bash
for i in 15 16 17; do
  cd session$i
  uv pip install django
  uv run python manage.py migrate
  uv run python manage.py runserver &
  echo "Testing session$i at http://127.0.0.1:8000/admin"
  sleep 2
  kill %1 2>/dev/null
  cd ..
done
```

---

## Requirements

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10+ | Runtime |
| uv | Latest | Package manager |
| Django | Latest | Sessions 15-17 |
| FastAPI | Latest | Sessions 5-14 |
| pytest | Latest | Sessions 13-14 |

### Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Browser Testing Tips

### Swagger UI (/docs)
1. Lists all endpoints with descriptions
2. Click any endpoint to expand
3. Click "Try it out"
4. Fill parameters/body
5. Click "Execute"
6. See response with status code

### ReDoc (/redoc)
1. Clean, readable documentation
2. Click endpoint to see details
3. Copy request examples

### Django Admin (/admin)
1. Login required
2. CRUD operations via forms
3. Filter sidebar
4. Search boxes
5. Custom actions dropdown


