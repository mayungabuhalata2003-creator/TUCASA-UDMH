import os

from flask import Flask, jsonify, send_from_directory
from flask_login import current_user
from flask_wtf.csrf import generate_csrf
from sqlalchemy import inspect, text

from config import Config
from extensions import db, login_manager, csrf
from models import User, Setting, LibraryItem, WorshipSchedule, Leader
from datetime import datetime


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if app.config.get("ENVIRONMENT") == "production":
        secret_key = app.config.get("SECRET_KEY")
        if not secret_key or secret_key == "tucasa-mabibo-dev-secret-key-change-me":
            raise RuntimeError("Set a strong, unique SECRET_KEY before production deployment.")
        if app.config.get("DEFAULT_ADMIN_PASSWORD") == "TUMH122":
            raise RuntimeError("Set a unique DEFAULT_ADMIN_PASSWORD before production deployment.")

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.member import member_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(member_bp)
    app.register_blueprint(admin_bp)

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except (TypeError, ValueError):
            return None

    @app.route("/sw.js")
    def service_worker():
        return send_from_directory(app.static_folder, "sw.js", mimetype="application/javascript")

    @app.route("/csrf-token")
    def csrf_token():
        return jsonify(csrf_token=generate_csrf())

    @app.context_processor
    def inject_globals():
        logo_path = None
        try:
            logo_path = Setting.get("logo_path")
        except Exception:
            pass
        assoc_name = Setting.get("assoc_name", "TUCASA UDSM MABIBO HOSTEL")
        hostel_name = Setting.get("hostel_name", "Mabibo Hostel")
        contact_email = Setting.get("contact_email", "info@tucasa.ac.tz")
        return {
            "site_logo": logo_path,
            "current_year": datetime.now().year,
            "assoc_name": assoc_name,
            "hostel_name": hostel_name,
            "contact_email": contact_email,
        }

    @app.errorhandler(403)
    def forbidden(e):
        return "<h3>403 - Huna ruhusa ya kufikia ukurasa huu.</h3>", 403

    @app.errorhandler(404)
    def not_found(e):
        return "<h3>404 - Ukurasa haukupatikana.</h3>", 404

    @app.errorhandler(413)
    def file_too_large(e):
        return "<h3>Faili ni kubwa mno. Kikomo cha ombi ni 16 MB.</h3>", 413

    with app.app_context():
        db.create_all()
        _upgrade_existing_schema()
        _create_default_admin(app)
        _create_default_content()

    return app


def _create_default_admin(app):
    """Create default admin only when no admin exists yet."""
    if User.query.filter_by(role="admin").first():
        return
    admin = User(
        jina=app.config["DEFAULT_ADMIN_NAME"],
        email=app.config["DEFAULT_ADMIN_EMAIL"],
        role="admin",
    )
    admin.set_password(app.config["DEFAULT_ADMIN_PASSWORD"])
    db.session.add(admin)
    db.session.commit()
    print("Default admin account created; change its password after first login.")


def _upgrade_existing_schema():
    if db.engine.dialect.name != "sqlite":
        return
    member_columns = {column["name"] for column in inspect(db.engine).get_columns("members")}
    new_columns = {
        "status": "ALTER TABLE members ADD COLUMN status VARCHAR(30) DEFAULT 'pending'",
        "is_active": "ALTER TABLE members ADD COLUMN is_active BOOLEAN DEFAULT 1",
        "photo_path": "ALTER TABLE members ADD COLUMN photo_path VARCHAR(500)",
        "updated_at": "ALTER TABLE members ADD COLUMN updated_at DATETIME",
    }
    for name, sql in new_columns.items():
        if name not in member_columns:
            db.session.execute(text(sql))
    db.session.commit()

    if "tarehe_ya_kuzaliwa" not in member_columns:
        db.session.execute(text("ALTER TABLE members ADD COLUMN tarehe_ya_kuzaliwa DATE"))
        db.session.commit()


def _create_default_content():
    if LibraryItem.query.count() == 0:
        db.session.add_all([
            LibraryItem(title="Ellen G. White Writings", category="Ellen G. White", language="English", author="Ellen G. White", resource_url="https://egwwritings.org/"),
            LibraryItem(title="Maandiko ya Ellen G. White", category="Ellen G. White", language="Kiswahili", author="Ellen G. White", resource_url="https://egwwritings.org/"),
            LibraryItem(title="King James Bible", category="Bible", language="English", resource_url="https://www.biblegateway.com/versions/King-James-Version-KJV-Bible/"),
            LibraryItem(title="Biblia ya Kiswahili", category="Bible", language="Kiswahili", resource_url="https://www.biblegateway.com/"),
            LibraryItem(title="SDA Hymnal", category="SDA Hymns", language="English", resource_url="https://hymnary.org/hymnal/SDAH"),
            LibraryItem(title="Nyimbo za Waadventista kwa Kiswahili", category="SDA Hymns", language="Kiswahili", resource_url="https://hymnary.org/"),
        ])
    if WorshipSchedule.query.count() == 0:
        db.session.add_all([
            WorshipSchedule(year=datetime.now().year, day="Ijumaa", time="18:00 - 19:30", activity="Maandalio ya Sabato"),
            WorshipSchedule(year=datetime.now().year, day="Jumamosi Asubuhi", time="08:00 - 12:00", activity="Ibada Kuu ya Sabato"),
            WorshipSchedule(year=datetime.now().year, day="Jumamosi Mchana", time="15:00 - 17:00", activity="AY / Vijana"),
            WorshipSchedule(year=datetime.now().year, day="Jumatano", time="18:30 - 19:30", activity="Maombi ya Kati ya Wiki"),
        ])
    if Leader.query.count() == 0:
        db.session.add_all([
            Leader(year=datetime.now().year, name="JOHN JOHN", position="Mwenyekiti"),
            Leader(year=datetime.now().year, name="SALAM SALAM", position="Makamu Mwenyekiti"),
            Leader(year=datetime.now().year, name="MANASE YOKERA", position="KATIBU"),
            Leader(year=datetime.now().year, name="MKATE JUMA", position="KATIBU"),
            Leader(year=datetime.now().year, name="AMINA DAVID", position="Mweka Hazina"),
            Leader(year=datetime.now().year, name="HAMIS CYPRIAN", position="Mhazini msaidizi"),
            Leader(year=datetime.now().year, name="ERIC MAJOGORO", position="Mambo ya kiroho"),
        ])
    db.session.commit()


app = create_app()

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)

