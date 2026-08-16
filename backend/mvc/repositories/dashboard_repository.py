from backend.models.database import Conversation, Note


class DashboardRepository:
    """Read-only persistence operations required by the dashboard."""

    def recent_conversations(self, user_id, limit=100):
        return (
            Conversation.query.filter_by(user_id=user_id)
            .order_by(Conversation.timestamp.desc())
            .limit(limit)
            .all()
        )

    def note_count(self, user_id):
        return Note.query.filter_by(user_id=user_id).count()
