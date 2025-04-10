A MonoRepo for a toy-project

# Real-Time Inventory Tracker.

# Backend

- FastAPI

backend/
├── app/
│ ├── api/ # Route definitions
│ │ └── v1/ # Versioned API (v1)
│ │ ├── orgs.py # Organization endpoints
│ │ ├── users.py # User profile endpoints
│ │ ├── inventory.py # Inventory endpoints
│ │ └── websocket.py # WebSocket handlers
│ ├── core/ # App config, startup, CORS, security
│ │ ├── config.py
│ │ ├── database.py
│ │ └── security.py
│ ├── crud/ # Direct DB access logic
│ │ ├── orgs.py
│ │ ├── users.py
│ │ └── inventory.py
│ ├── models/ # (Optional) SQLAlchemy models if used
│ ├── schemas/ # Pydantic request/response models
│ │ ├── orgs.py
│ │ ├── users.py
│ │ └── inventory.py
│ ├── services/ # Business logic & orchestration
│ │ ├── org_service.py
│ │ └── inventory_sync.py
│ ├── dependencies.py # FastAPI dependencies (e.g. current user/org)
│ └── main.py # FastAPI app entry point
├── .env # Local dev environment
├── requirements.txt # Python dependencies

---

## 📌 Conventions

### General

- Use **PEP8** + format with `black` or `ruff`
- Use **async/await** for all I/O: DB, WebSocket, HTTP
- Keep route handlers thin; push logic into `crud/` and `services/`

---

### API Layer (`api/`)

- Each domain (e.g. orgs, users) gets its own file
- All routes are versioned under `api/v1/`
- Use prefixes and tags when registering routers in `main.py`

---

### Schema Layer (`schemas/`)

- Define all input/output using **Pydantic** models
- One file per domain for clarity and reuse

---

### CRUD Layer (`crud/`)

- Only handles DB reads/writes (via Supabase or ORM)
- No logic or side-effects (pure access layer)

---

### Services Layer (`services/`)

- Put non-trivial logic here (multi-step flows, validations, side-effects)
- Example: assigning items, streaming updates, syncing logs

---

### Dependencies (`dependencies.py`)

- Central place for shared `Depends()` logic
- Common examples:
  - `get_current_user`
  - `get_user_org`

---

## 🧪 Local Development

```bash
# From backend/
uvicorn app.main:app --reload

```
