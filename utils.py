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


def _extension(filename):
    return filename.rsplit(".", 1)[1].lower() if "." in filename else ""


def _valid_upload(file_storage, allowed_extensions):
    """Validate extension and size before persisting a randomly named upload."""
    if not file_storage or not file_storage.filename:
        return False
    if _extension(file_storage.filename) not in allowed_extensions:
        return False

    stream = file_storage.stream
    try:
        stream.seek(0, os.SEEK_END)
        size = stream.tell()
        stream.seek(0)
    except (AttributeError, OSError):
        return False
    return size <= current_app.config.get("MAX_UPLOAD_FILE_SIZE", 12 * 1024 * 1024)


def _save_upload(file_storage, folder, relative_folder, allowed_extensions):
    if not _valid_upload(file_storage, allowed_extensions):
        return None
    extension = _extension(file_storage.filename)
    os.makedirs(folder, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.{extension}"
    file_storage.save(os.path.join(folder, filename))
    return f"{relative_folder}/{filename}"


def allowed_logo_file(filename):
    return _extension(filename) in current_app.config["ALLOWED_LOGO_EXTENSIONS"]


def save_logo_file(file_storage, previous_relative_path=None):
    """Save a size-limited logo upload and return its static-relative path."""
    if not file_storage or not file_storage.filename:
        return None
    if not _valid_upload(file_storage, current_app.config["ALLOWED_LOGO_EXTENSIONS"]):
        return None

    # Verify common image signatures instead of trusting the filename extension.
    stream = file_storage.stream
    header = stream.read(12)
    stream.seek(0)
    ext = _extension(file_storage.filename)
    signatures = {
        "png": header.startswith(b"\x89PNG\r\n\x1a\n"),
        "jpg": header.startswith(b"\xff\xd8\xff"),
        "jpeg": header.startswith(b"\xff\xd8\xff"),
        "gif": header.startswith((b"GIF87a", b"GIF89a")),
        "webp": header.startswith(b"RIFF") and header[8:12] == b"WEBP",
    }
    if not signatures.get(ext, False):
        return None

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(upload_folder, unique_name)
    file_storage.save(filepath)

    if previous_relative_path:
        previous_file = os.path.join(current_app.static_folder, previous_relative_path)
        try:
            if os.path.exists(previous_file):
                os.remove(previous_file)
        except OSError:
            pass

    return f"uploads/logo/{unique_name}"


def save_resource_file(file_storage):
    return _save_upload(
        file_storage,
        current_app.config["RESOURCE_UPLOAD_FOLDER"],
        "uploads/resources",
        {"pdf", "doc", "docx"},
    )


def save_event_image(file_storage):
    return _save_upload(
        file_storage,
        current_app.config["RESOURCE_UPLOAD_FOLDER"],
        "uploads/resources",
        {"png", "jpg", "jpeg", "gif", "webp"},
    )


def save_media_file(file_storage):
    allowed = {
        "mp3", "wav", "m4a", "mp4", "mov", "avi", "pdf", "doc", "docx",
        "png", "jpg", "jpeg", "webp",
    }
    return _save_upload(
        file_storage,
        current_app.config["MEDIA_UPLOAD_FOLDER"],
        "uploads/media",
        allowed,
    )


def save_leader_photo(file_storage):
    return _save_upload(
        file_storage,
        current_app.config["RESOURCE_UPLOAD_FOLDER"],
        "uploads/resources",
        {"png", "jpg", "jpeg", "webp"},
    )
