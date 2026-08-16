# MVC migration

The application is being migrated feature by feature without changing its
existing HTTP API or React client.

## Current boundary

The dashboard and note CRUD features are the reference implementations:

```
React Dashboard view
        |
GET /api/dashboard
        |
DashboardController
        |
DashboardService
        |
DashboardRepository -> SQLAlchemy models
```

Notes follow the same path through `NotesController`, `NoteService`, and
`NoteRepository`. Advanced note AI, search, sync, and export endpoints are
still in the legacy module and will move as the next notes slice.

`app.py` remains the temporary composition root. It configures Flask and
registers feature controllers through `mvc.routes.register_feature_routes`.
This avoids a high-risk rewrite while keeping new business logic out of the
legacy module.

## Backend layout

Most backend implementation files now live under `backend/`:

- `controllers/` — authentication and Flask-facing controllers
- `models/` — SQLAlchemy entities and database setup
- `domain/` — CAPS knowledge and deterministic physics simulation
- `services/` — AI prompt and generation utilities
- `ml/` — classifier training and artifact loading
- `scripts/` — migration and dataset-generation utilities

The short modules at the repository root are backwards-compatible import and
command shims. New backend code should import from `backend.*` directly.

## Next feature migrations

1. Extract `ChatService`, then make the chat route only validate a request,
   call the service, and return its response.
2. Split notes, learner memory, and adaptive-practice operations into their
   own controllers, services, repositories, and request schemas.
3. Move the Flask setup from `app.py` into an application factory once all
   controllers are registered through `mvc.routes`.
4. Replace direct frontend `fetch` calls with feature API clients and custom
   controller hooks (`useChatController`, `useNotesController`).

## Rules for new work

- Controllers only translate HTTP requests and responses.
- Services own use-case and AI orchestration logic.
- Repositories own SQLAlchemy queries and commits.
- SQLAlchemy entities remain persistence models; deterministic curriculum and
  physics modules remain domain services.
