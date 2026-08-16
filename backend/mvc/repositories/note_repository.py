from backend.models.database import Note, db


class NoteRepository:
    """Persistence operations for learner notes."""

    def list_for_user(self, user_id, limit):
        return (
            Note.query.filter_by(user_id=user_id)
            .order_by(Note.updated_at.desc())
            .limit(limit)
            .all()
        )

    def get_for_user(self, note_id, user_id):
        return Note.query.filter_by(id=note_id, user_id=user_id).first()

    def add(self, note):
        db.session.add(note)

    def delete(self, note):
        db.session.delete(note)

    def commit(self):
        db.session.commit()
