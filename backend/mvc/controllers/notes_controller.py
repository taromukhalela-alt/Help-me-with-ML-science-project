from flask import Blueprint, current_app, jsonify, request
from flask_login import current_user, login_required


notes_bp = Blueprint("notes", __name__)


def _validation_error(error):
    status = 413 if "too long" in str(error).lower() else 400
    return jsonify({"success": False, "message": str(error)}), status


@notes_bp.get("/api/notes")
@login_required
def get_notes():
    notes = current_app.extensions["note_service"].list_notes(current_user.id)
    return jsonify({"success": True, "notes": notes})


@notes_bp.post("/api/notes")
@login_required
def create_note():
    try:
        note = current_app.extensions["note_service"].create(
            current_user.id, request.get_json(silent=True) or {}
        )
    except ValueError as error:
        return _validation_error(error)
    return jsonify({"success": True, "note": note})


@notes_bp.put("/api/notes/<note_id>")
@login_required
def update_note(note_id):
    try:
        note = current_app.extensions["note_service"].update(
            current_user.id, note_id, request.get_json(silent=True) or {}
        )
    except ValueError as error:
        return _validation_error(error)
    if note is None:
        return jsonify({"success": False, "message": "Note not found"}), 404
    return jsonify({"success": True, "note": note})


@notes_bp.delete("/api/notes/<note_id>")
@login_required
def delete_note(note_id):
    if not current_app.extensions["note_service"].delete(current_user.id, note_id):
        return jsonify({"success": False, "message": "Note not found"}), 404
    return jsonify({"success": True, "message": "Note deleted"})
