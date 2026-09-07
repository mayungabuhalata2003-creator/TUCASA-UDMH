# TUCASA - Mabibo Hostel Membership System

A complete Flask web application for **TUCASA** (Tanzania Union Christian Adventist Students Association), University of Dar es Salaam - Mabibo Hostel. It handles member signup/login, member registration, a daily Bible verse, announcements, a WhatsApp click-to-chat broadcast tool, logo upload, and a full admin panel.

## Tech Stack
- Flask (Python)
- SQLite + Flask-SQLAlchemy
- Flask-Login (authentication/sessions)
- Flask-WTF (forms + CSRF protection)
- Bootstrap 5 + Bootstrap Icons
- Vanilla JavaScript

## Project Structure
```
tucasa/
├── app.py                 # App factory + entry point
├── config.py               # Configuration (secret key, DB URI, WhatsApp link, uploads)
├── extensions.py            # db, login_manager, csrf instances
├── models.py                # User, Member, Announcement, ContactMessage, Setting
├── forms.py                 # All Flask-WTF forms
├── bible_verses.py           # Swahili Bible verses + daily rotation logic
├── utils.py                  # admin_required decorator, logo upload helper
├── requirements.txt
├── routes/
│   ├── auth.py               # signup, login, logout
│   ├── main.py                # dashboard + content pages
│   ├── member.py               # member registration + success page
│   └── admin.py                # admin panel (members, announcements, logo, WhatsApp, settings)
├── templates/
│   ├── base.html               # Sidebar layout shell
│   ├── landing.html             # Public landing page (dark gradient hero)
│   ├── auth/ (login, signup)
│   ├── pages/ (about, leadership, library, events, publications, announcements, worship, contact)
│   └── admin/ (dashboard, members, announcements, logo, whatsapp, messages, settings)
└── static/
    ├── css/style.css
    ├── js/main.js
    └── uploads/logo/           # Uploaded logo images land here
```

## Setup Instructions

### 1. Create a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Configure environment variables
Copy the example file and edit values as needed:
```bash
cp .env.example .env
```
Set `SECRET_KEY`, `WHATSAPP_GROUP_LINK`, `DEFAULT_ADMIN_EMAIL`, and `DEFAULT_ADMIN_PASSWORD` as desired. If you skip this step, sensible defaults are used automatically.

### 4. Run the application
```bash
python app.py
```
The app will:
- Automatically create the SQLite database (`tucasa.db`) and all tables on first run.
- Automatically create a **default admin account** if no admin exists yet:
  - Email: `admin@tucasa.ac.tz`
  - Password: `Admin@123`
  - **Change this password after your first login** (or set your own via `.env`).

Visit **http://127.0.0.1:5000** in your browser.

## Key Features

- **Signup/Login** — students self-register with full name, email, and password (Werkzeug-hashed). Clear messaging if a user tries to log in without an account.
- **Sidebar dashboard** — after login, all navigation happens through a sidebar (collapsible on mobile) with the daily Bible verse, quick stats, and recent announcements.
- **Daily Bible verse** — cycles automatically based on day-of-year through a list of 12 Swahili verses, with a fade-in-up CSS animation.
- **Member registration** — a dedicated form (separate from signup) capturing full member details; on success, shows a WhatsApp group join button.
- **WhatsApp broadcast (admin)** — admin writes a message once; the system generates a `wa.me` click-to-chat link for every member who opted in, normalizing Tanzanian phone numbers (leading `0` → `255`).
- **Logo upload (admin)** — validated image upload (2MB max), stored with a unique filename, injected into every page via a context processor.
- **Content pages** — About, Leadership, Library, Events & Photos, Publications, Announcements, Worship Schedule, Contact Us (saves to DB).
- **Admin panel** — dashboard stats, member management with search + delete, announcements CRUD, logo upload, WhatsApp broadcast tool, contact message viewer, and WhatsApp link settings.
- **Security** — CSRF protection site-wide (Flask-WTF), hashed passwords, `@admin_required` decorator guarding all `/admin/*` routes, validated file uploads.

## Notes
- This starter uses SQLite for simplicity. For production, point `DATABASE_URL` at PostgreSQL/MySQL and set a strong, unique `SECRET_KEY`.
- Static "for now" pages (Events, Publications) use placeholder data in `routes/main.py` — replace with database-backed content whenever you're ready to make them admin-editable too.
- Run `flask run` for Flask's built-in reloader/debugger, or `python app.py` directly (both work with this setup).
