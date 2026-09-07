import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "tucasa-mabibo-dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'tucasa.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # WhatsApp group invite link (can be changed by admin via Settings table too)
    WHATSAPP_GROUP_LINK = os.environ.get(
        "WHATSAPP_GROUP_LINK", "https://chat.whatsapp.com/YOUR_INVITE_CODE_HERE"
    )

    # Uploads
    UPLOAD_FOLDER = os.path.join(basedir, "static", "uploads", "logo")
    RESOURCE_UPLOAD_FOLDER = os.path.join(basedir, "static", "uploads", "resources")
    MEDIA_UPLOAD_FOLDER = os.path.join(basedir, "static", "uploads", "media")
    ALLOWED_LOGO_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
    # Default admin (created automatically on first run if no admin exists)
    DEFAULT_ADMIN_EMAIL = os.environ.get("DEFAULT_ADMIN_EMAIL", "admin@tucasa.ac.tz")
    DEFAULT_ADMIN_PASSWORD = os.environ.get("DEFAULT_ADMIN_PASSWORD", "TUMH122")
    DEFAULT_ADMIN_NAME = os.environ.get("DEFAULT_ADMIN_NAME", "TUMH")
