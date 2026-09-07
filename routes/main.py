from datetime import date, datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from extensions import db
from models import Member, Announcement, ContactMessage, ChatMessage, LibraryItem, WorshipSchedule, Leader, EventPost, Publication, ChoirMedia
from forms import ContactForm, ChatMessageForm
from bible_verses import get_daily_verse, get_daily_verse_index, VERSES

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def landing():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("landing.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    verse = get_daily_verse()
    verse_index = get_daily_verse_index()
    total_members = Member.query.count()
    upcoming_events = 3  # static placeholder count, shown on Matukio page
    recent_announcements = Announcement.query.order_by(Announcement.tarehe.desc()).limit(5).all()
    member_profile = Member.query.filter_by(user_id=current_user.id).first()
    today = date.today()
    birthday_today = bool(
        member_profile
        and member_profile.tarehe_ya_kuzaliwa
        and member_profile.tarehe_ya_kuzaliwa.month == today.month
        and member_profile.tarehe_ya_kuzaliwa.day == today.day
    )

    return render_template(
        "dashboard.html",
        verse=verse,
        verse_index=verse_index,
        all_verses=VERSES,
        total_members=total_members,
        upcoming_events=upcoming_events,
        recent_announcements=recent_announcements,
        member_profile=member_profile,
        birthday_today=birthday_today,
    )


@main_bp.route("/about")
@main_bp.route("/kuhusu")
@main_bp.route("/kuhusu-TUMH")
@login_required
def about():
    return render_template("pages/about.html")


@main_bp.route("/uongozi")
@login_required
def leadership():
    selected_year = request.args.get("year", type=int) or datetime.now().year
    years = [row[0] for row in db.session.query(Leader.year).distinct().order_by(Leader.year.desc()).all()]
    leaders = Leader.query.filter_by(year=selected_year).order_by(Leader.id).all()
    return render_template("pages/leadership.html", leaders=leaders, years=years, selected_year=selected_year)


@main_bp.route("/library")
@login_required
def library():
    category = request.args.get("category", "all")
    language = request.args.get("language", "all")
    query = LibraryItem.query
    if category != "all":
        query = query.filter_by(category=category)
    if language != "all":
        query = query.filter_by(language=language)
    documents = query.order_by(LibraryItem.category, LibraryItem.language, LibraryItem.title).all()
    return render_template("pages/library.html", documents=documents, selected_category=category, selected_language=language)


@main_bp.route("/kwaya")
@login_required
def kwaya():
    events_list = EventPost.query.order_by(EventPost.event_date.desc(), EventPost.created_at.desc()).all()
    publications_list = Publication.query.order_by(Publication.created_at.desc()).all()
    media_items = ChoirMedia.query.order_by(ChoirMedia.created_at.desc()).all()
    return render_template("pages/kwaya.html", events=events_list, publications=publications_list, media_items=media_items)


@main_bp.route("/matukio-na-picha")
@login_required
def events():
    events_list = EventPost.query.order_by(EventPost.event_date.desc(), EventPost.created_at.desc()).all()
    return render_template("pages/events.html", events=events_list)


@main_bp.route("/machapisho")
@login_required
def publications():
    publications_list = Publication.query.order_by(Publication.created_at.desc()).all()
    return render_template("pages/publications.html", publications=publications_list)


@main_bp.route("/matangazo")
@login_required
def announcements():
    all_announcements = Announcement.query.order_by(Announcement.tarehe.desc()).all()
    return render_template("pages/announcements.html", announcements=all_announcements)


@main_bp.route("/ratiba-za-ibada")
@login_required
def worship():
    selected_year = request.args.get("year", type=int) or datetime.now().year
    years = [row[0] for row in db.session.query(WorshipSchedule.year).distinct().order_by(WorshipSchedule.year.desc()).all()]
    schedule = WorshipSchedule.query.filter_by(year=selected_year).order_by(WorshipSchedule.id).all()
    return render_template("pages/worship.html", schedule=schedule, years=years, selected_year=selected_year)


@main_bp.route("/wasiliana-nasi", methods=["GET", "POST"])
@login_required
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = ContactMessage(
            jina=form.jina.data.strip(),
            email=form.email.data.lower().strip(),
            ujumbe=form.ujumbe.data.strip(),
        )
        db.session.add(message)
        db.session.commit()
        flash("Ujumbe wako umetumwa. Asante!", "success")
        return redirect(url_for("main.contact"))

    return render_template("pages/contact.html", form=form)


@main_bp.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    form = ChatMessageForm()
    if form.validate_on_submit():
        db.session.add(ChatMessage(sender_id=current_user.id, message=form.message.data.strip()))
        db.session.commit()
        return redirect(url_for("main.chat"))

    retention_cutoff = datetime.utcnow() - timedelta(days=2)
    ChatMessage.query.filter(ChatMessage.created_at < retention_cutoff).delete(
        synchronize_session=False
    )
    db.session.commit()

    page = max(request.args.get("page", 1, type=int), 1)
    pagination = ChatMessage.query.order_by(ChatMessage.created_at.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    messages = list(reversed(pagination.items))
    return render_template(
        "pages/chat.html", form=form, messages=messages, pagination=pagination
    )
