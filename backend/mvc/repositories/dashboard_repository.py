from collections import Counter

from backend.models.database import Conversation, Note


class DashboardRepository:
    """Read-only persistence operations required by the dashboard."""

    def all_conversations(self, user_id):
        """Return the complete conversation history for one learner."""
        return (
            Conversation.query.filter_by(user_id=user_id)
            .order_by(Conversation.timestamp.desc())
            .all()
        )

    def recent_conversations(self, user_id, limit=100):
        return (
            Conversation.query.filter_by(user_id=user_id)
            .order_by(Conversation.timestamp.desc())
            .limit(limit)
            .all()
        )

    def note_count(self, user_id):
        return Note.query.filter_by(user_id=user_id).count()

    def conversation_count(self, user_id):
        return Conversation.query.filter_by(user_id=user_id).count()

    def note_topic_counts(self, user_id):
        """Return note activity grouped by topic for one learner."""
        topics = Note.query.with_entities(Note.topic).filter_by(user_id=user_id).all()
        return Counter((topic or "").strip().lower() for topic, in topics if topic)
