import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "development").lower()
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        if ENVIRONMENT == "production":
            raise RuntimeError("SECRET_KEY must be configured in production.")
        SECRET_KEY = "tucasa-mabibo-dev-secret-key-change-me"

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'tucasa.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Maximum total request size (16 MB)
    MAX_UPLOAD_FILE_SIZE = 12 * 1024 * 1024  # Maximum individual upload (12 MB)

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = ENVIRONMENT == "production"

    WHATSAPP_GROUP_LINK = os.environ.get(
        "WHATSAPP_GROUP_LINK", "https://chat.whatsapp.com/YOUR_INVITE_CODE_HERE"
    )

    UPLOAD_FOLDER = os.path.join(basedir, "static", "uploads", "logo")
    RESOURCE_UPLOAD_FOLDER = os.path.join(basedir, "static", "uploads", "resources")
    MEDIA_UPLOAD_FOLDER = os.path.join(basedir, "static", "uploads", "media")
    ALLOWED_LOGO_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    DEFAULT_ADMIN_EMAIL = os.environ.get("DEFAULT_ADMIN_EMAIL", "admin@tucasa.ac.tz")
    DEFAULT_ADMIN_PASSWORD = os.environ.get("DEFAULT_ADMIN_PASSWORD", "TUMH122")
    DEFAULT_ADMIN_NAME = os.environ.get("DEFAULT_ADMIN_NAME", "TUMH")
