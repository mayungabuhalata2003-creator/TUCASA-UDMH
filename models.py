from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    jina = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="member")  # member | admin
    tarehe = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == "admin"

    def __repr__(self):
        return f"<User {self.email}>"


class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    jina = db.Column(db.String(150), nullable=False)
    jinsia = db.Column(db.String(10), nullable=False)  # Me / Ke
    mwaka = db.Column(db.String(20), nullable=False)  # Year of study
    kozi = db.Column(db.String(150), nullable=False)  # Course
    simu = db.Column(db.String(20), nullable=False)  # Phone
    email = db.Column(db.String(150), nullable=False)
    hostel = db.Column(db.String(100), nullable=False)
    vipaji = db.Column(db.String(255), nullable=True)  # Talents
    tarehe_ya_kuzaliwa = db.Column(db.Date, nullable=True)
    kukubali_whatsapp = db.Column(db.Boolean, default=False)
    tarehe = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="member_profile")

    def __repr__(self):
        return f"<Member {self.jina}>"


class Announcement(db.Model):
    __tablename__ = "announcements"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tarehe = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Announcement {self.title}>"


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    jina = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    ujumbe = db.Column(db.Text, nullable=False)
    tarehe = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ContactMessage from {self.jina}>"


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    sender = db.relationship("User", backref="chat_messages")


class EventPost(db.Model):
    __tablename__ = "event_posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.Date, nullable=True)
    image_path = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Publication(db.Model):
    __tablename__ = "publications"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=True)
    summary = db.Column(db.Text, nullable=True)
    resource_url = db.Column(db.String(500), nullable=True)
    file_path = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ChoirMedia(db.Model):
    __tablename__ = "choir_media"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    media_type = db.Column(db.String(50), nullable=False, default="song")
    description = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(500), nullable=True)
    external_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Setting(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.String(500), nullable=True)

    @staticmethod
    def get(key, default=None):
        setting = Setting.query.filter_by(key=key).first()
        return setting.value if setting else default

    @staticmethod
    def set(key, value):
        setting = Setting.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = Setting(key=key, value=value)
            db.session.add(setting)
        db.session.commit()
        return setting


class LibraryItem(db.Model):
    __tablename__ = "library_items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    language = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(150), nullable=True)
    resource_url = db.Column(db.String(500), nullable=True)
    file_path = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class WorshipSchedule(db.Model):
    __tablename__ = "worship_schedules"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False, index=True)
    day = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    activity = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Leader(db.Model):
    __tablename__ = "leaders"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False, index=True)
    name = db.Column(db.String(150), nullable=False)
    position = db.Column(db.String(150), nullable=False)
    photo_path = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
