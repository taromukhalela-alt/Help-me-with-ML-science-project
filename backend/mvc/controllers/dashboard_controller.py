from flask import Blueprint, current_app, jsonify
from flask_login import current_user, login_required


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/api/dashboard")
@login_required
def get_dashboard():
    """Return the dashboard view model for the current learner."""
    try:
        return jsonify(current_app.extensions["dashboard_service"].build(current_user.id))
    except Exception:
        current_app.logger.exception("Dashboard data error")
        return jsonify({"success": False, "error": "Unable to load dashboard data"}), 500
