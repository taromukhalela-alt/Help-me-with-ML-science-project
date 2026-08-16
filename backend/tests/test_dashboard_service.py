from datetime import datetime, timezone
from types import SimpleNamespace

from backend.mvc.services.dashboard_service import DashboardService


class FakeDashboardRepository:
    def note_count(self, user_id):
        assert user_id == "learner-1"
        return 2

    def recent_conversations(self, user_id, limit=100):
        assert user_id == "learner-1"
        assert limit == 100
        return [
            FakeConversation("forces", 80.0),
            FakeConversation("forces", 60.0),
            FakeConversation("waves", None),
        ]


class FakeConversation(SimpleNamespace):
    def __init__(self, intent, confidence):
        super().__init__(
            intent=intent,
            confidence=confidence,
            message="A learner question",
            timestamp=datetime.now(timezone.utc),
            chat_id="chat-1",
        )

    def to_dict(self):
        return {"chat_id": self.chat_id, "message": self.message, "reply": "A tutor response"}


def test_dashboard_service_builds_a_view_model_from_repository_data():
    service = DashboardService(
        latency_reader=lambda user_id: 12.0,
        animation_intents={"forces"},
        repository=FakeDashboardRepository(),
    )

    dashboard = service.build("learner-1")

    assert dashboard["success"] is True
    assert dashboard["stats"]["questions_asked"] == 3
    assert dashboard["metrics"][0]["value"] == 70.2
    assert dashboard["metrics"][1]["value"] == 12.0
    forces = next(item for item in dashboard["syllabus"] if item["title"] == "Newton's Laws & Forces")
    assert forces["progress"] == 29
