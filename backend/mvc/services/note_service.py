import secrets

from backend.models.database import Note, utc_now
from backend.mvc.repositories.note_repository import NoteRepository


class NoteService:
    """Note CRUD use cases, independent of Flask request objects."""

    def __init__(self, validate_payload, list_limit, repository=None):
        self._validate_payload = validate_payload
        self._list_limit = list_limit
        self._repository = repository or NoteRepository()

    def list_notes(self, user_id):
        return [note.to_dict() for note in self._repository.list_for_user(user_id, self._list_limit)]

    def create(self, user_id, payload):
        title, topic, content, tags = self._validate_payload(payload)
        note = Note(
            id=f"note_{secrets.token_urlsafe(12)}",
            user_id=user_id,
            title=title or "Untitled Note",
            content=(content or "").strip(),
            topic=topic or "General",
            tags=tags,
            source="ai" if bool(payload.get("ai_generated", False)) else "user",
        )
        self._repository.add(note)
        self._repository.commit()
        return note.to_dict()

    def update(self, user_id, note_id, payload):
        note = self._repository.get_for_user(note_id, user_id)
        if not note:
            return None
        title, topic, content, tags = self._validate_payload(payload)
        if title is not None:
            note.title = title.strip()
        if content is not None:
            note.content = content.strip()
        if topic is not None:
            note.topic = topic.strip()
        if tags is not None:
            note.tags = tags
        note.updated_at = utc_now()
        self._repository.commit()
        return note.to_dict()

    def delete(self, user_id, note_id):
        note = self._repository.get_for_user(note_id, user_id)
        if not note:
            return False
        self._repository.delete(note)
        self._repository.commit()
        return True
