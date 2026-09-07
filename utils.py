import os
import uuid
from functools import wraps

from flask import abort, current_app
from flask_login import current_user


def admin_required(f):
    """Decorator: only allow access to logged-in admin users."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def allowed_logo_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_LOGO_EXTENSIONS"]
    )


def save_logo_file(file_storage, previous_relative_path=None):
    """Save an uploaded logo image with a unique filename. Returns relative path or None."""
    if not file_storage or file_storage.filename == "":
        return None
    if not allowed_logo_file(file_storage.filename):
        return None

    ext = file_storage.filename.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)

    if previous_relative_path:
        previous_file = os.path.join(current_app.static_folder, previous_relative_path)
        try:
            if os.path.exists(previous_file):
                os.remove(previous_file)
        except OSError:
            pass

    filepath = os.path.join(upload_folder, unique_name)
    file_storage.save(filepath)

    # Path relative to /static for use in templates via url_for('static', filename=...)
    return f"uploads/logo/{unique_name}"


def save_resource_file(file_storage):
    if not file_storage or not file_storage.filename:
        return None
    extension = file_storage.filename.rsplit(".", 1)[-1].lower()
    if extension not in {"pdf", "doc", "docx"}:
        return None
    os.makedirs(current_app.config["RESOURCE_UPLOAD_FOLDER"], exist_ok=True)
    filename = f"{uuid.uuid4().hex}.{extension}"
    file_storage.save(os.path.join(current_app.config["RESOURCE_UPLOAD_FOLDER"], filename))
    return f"uploads/resources/{filename}"


def save_event_image(file_storage):
    if not file_storage or not file_storage.filename:
        return None
    extension = file_storage.filename.rsplit(".", 1)[-1].lower()
    if extension not in {"png", "jpg", "jpeg", "gif", "webp"}:
        return None
    os.makedirs(current_app.config["RESOURCE_UPLOAD_FOLDER"], exist_ok=True)
    filename = f"{uuid.uuid4().hex}.{extension}"
    file_storage.save(os.path.join(current_app.config["RESOURCE_UPLOAD_FOLDER"], filename))
    return f"uploads/resources/{filename}"


def save_media_file(file_storage):
    if not file_storage or not file_storage.filename:
        return None
    allowed = {"mp3", "wav", "m4a", "mp4", "mov", "avi", "pdf", "doc", "docx", "png", "jpg", "jpeg", "webp"}
    extension = file_storage.filename.rsplit(".", 1)[-1].lower()
    if extension not in allowed:
        return None
    os.makedirs(current_app.config["MEDIA_UPLOAD_FOLDER"], exist_ok=True)
    filename = f"{uuid.uuid4().hex}.{extension}"
    file_storage.save(os.path.join(current_app.config["MEDIA_UPLOAD_FOLDER"], filename))
    return f"uploads/media/{filename}"


def save_leader_photo(file_storage):
    if not file_storage or not file_storage.filename:
        return None
    extension = file_storage.filename.rsplit(".", 1)[-1].lower()
    if extension not in {"png", "jpg", "jpeg", "webp"}:
        return None
    os.makedirs(current_app.config["RESOURCE_UPLOAD_FOLDER"], exist_ok=True)
    filename = f"{uuid.uuid4().hex}.{extension}"
    file_storage.save(os.path.join(current_app.config["RESOURCE_UPLOAD_FOLDER"], filename))
    return f"uploads/resources/{filename}"
