from backend.mvc.controllers.dashboard_controller import dashboard_bp
from backend.mvc.controllers.notes_controller import notes_bp


def register_feature_routes(app):
    """Register MVC controllers while legacy features are migrated gradually."""
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(notes_bp)
