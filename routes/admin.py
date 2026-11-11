from urllib.parse import quote

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app,
)
from datetime import datetime
from flask_login import login_required

from extensions import db
from models import Member, Announcement, ContactMessage, Setting, LibraryItem, WorshipSchedule, Leader, EventPost, Publication, ChoirMedia
from forms import AnnouncementForm, LogoUploadForm, WhatsAppBroadcastForm, SettingsForm, LibraryItemForm, WorshipScheduleForm, LeaderForm, EventPostForm, PublicationForm, ChoirMediaForm
from utils import admin_required, save_logo_file, save_resource_file, save_leader_photo, save_event_image, save_media_file

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    total_members = Member.query.count()
    recent_members = Member.query.order_by(Member.tarehe.desc()).limit(5).all()
    total_announcements = Announcement.query.count()
    total_messages = ContactMessage.query.count()
    return render_template(
        "admin/dashboard.html",
        total_members=total_members,
        recent_members=recent_members,
        total_announcements=total_announcements,
        total_messages=total_messages,
    )


# ---------- Members management ----------
@admin_bp.route("/wanachama")
@login_required
@admin_required
def members():
    search = request.args.get("q", "").strip()
    query = Member.query
    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(
                Member.jina.ilike(like),
                Member.email.ilike(like),
                Member.hostel.ilike(like),
                Member.kozi.ilike(like),
            )
        )
    all_members = query.order_by(Member.tarehe.desc()).all()
    return render_template("admin/members.html", members=all_members, search=search)


@admin_bp.route("/wanachama/<int:member_id>/approve", methods=["POST"])
@login_required
@admin_required
def approve_member(member_id):
    member = Member.query.get_or_404(member_id)
    member.status = "approved"
    member.is_active = True
    db.session.commit()
    flash(f"Mwanachama {member.jina} amethibitishwa.", "success")
    return redirect(url_for("admin.members"))


@admin_bp.route("/wanachama/<int:member_id>/futa", methods=["POST"])
@login_required
@admin_required
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    db.session.delete(member)
    db.session.commit()
    flash(f"Mwanachama {member.jina} amefutwa.", "info")
    return redirect(url_for("admin.members"))


# ---------- Announcements management ----------
@admin_bp.route("/matangazo", methods=["GET", "POST"])
@login_required
@admin_required
def announcements():
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(title=form.title.data.strip(), content=form.content.data.strip())
        db.session.add(announcement)
        db.session.commit()
        flash("Tangazo limeongezwa.", "success")
        return redirect(url_for("admin.announcements"))

    all_announcements = Announcement.query.order_by(Announcement.tarehe.desc()).all()
    return render_template("admin/announcements.html", form=form, announcements=all_announcements)


@admin_bp.route("/matangazo/<int:announcement_id>/futa", methods=["POST"])
@login_required
@admin_required
def delete_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    db.session.delete(announcement)
    db.session.commit()
    flash("Tangazo limefutwa.", "info")
    return redirect(url_for("admin.announcements"))


# ---------- Logo upload ----------
@admin_bp.route("/nembo", methods=["GET", "POST"])
@login_required
@admin_required
def logo():
    form = LogoUploadForm()
    current_logo = Setting.get("logo_path")

    if request.method == "POST":
        uploaded_file = form.logo.data or request.files.get("logo")
        if uploaded_file and getattr(uploaded_file, "filename", ""):
            if form.validate_on_submit():
                relative_path = save_logo_file(uploaded_file, current_logo)
                if relative_path:
                    Setting.set("logo_path", relative_path)
                    flash("Nembo (logo) imepakiwa kwa mafanikio.", "success")
                else:
                    flash("Faili haikubaliki. Tumia PNG, JPG, JPEG, GIF au WEBP pekee.", "danger")
                return redirect(url_for("admin.logo"))

            for error in form.logo.errors:
                flash(error, "danger")
            return render_template("admin/logo.html", form=form, current_logo=current_logo)

    if request.method == "POST" and not request.files.get("logo"):
        flash("Tafadhali chagua picha ya nembo kwanza.", "warning")

    return render_template("admin/logo.html", form=form, current_logo=current_logo)


# ---------- WhatsApp broadcast ----------
@admin_bp.route("/whatsapp", methods=["GET", "POST"])
@login_required
@admin_required
def whatsapp():
    form = WhatsAppBroadcastForm()
    links = []

    if form.validate_on_submit():
        message_text = form.message.data.strip()
        eligible_members = Member.query.filter(
            Member.kukubali_whatsapp.is_(True), Member.simu.isnot(None), Member.simu != ""
        ).all()

        for m in eligible_members:
            phone = "".join(ch for ch in m.simu if ch.isdigit() or ch == "+")
            if phone.startswith("0"):
                phone = "255" + phone[1:]
            elif phone.startswith("+"):
                phone = phone[1:]
            encoded_message = quote(message_text)
            wa_link = f"https://wa.me/{phone}?text={encoded_message}"
            links.append({"jina": m.jina, "simu": m.simu, "link": wa_link})

        if not links:
            flash("Hakuna wanachama waliokubali kupokea ujumbe wa WhatsApp.", "warning")

    return render_template("admin/whatsapp.html", form=form, links=links)


# ---------- Contact messages ----------
@admin_bp.route("/ujumbe")
@login_required
@admin_required
def messages():
    all_messages = ContactMessage.query.order_by(ContactMessage.tarehe.desc()).all()
    return render_template("admin/messages.html", messages=all_messages)


# ---------- General settings ----------
@admin_bp.route("/mipangilio", methods=["GET", "POST"])
@login_required
@admin_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        association_name = (form.association_name.data or "").strip() or "TUCASA UDSM MABIBO HOSTEL"
        hostel_name = (form.hostel_name.data or "").strip() or "Mabibo Hostel"
        whatsapp_link = (form.whatsapp_link.data or "").strip() or current_app.config["WHATSAPP_GROUP_LINK"]
        contact_email = (form.contact_email.data or "").strip() or "info@tucasa.ac.tz"

        Setting.set("assoc_name", association_name)
        Setting.set("hostel_name", hostel_name)
        Setting.set("whatsapp_link", whatsapp_link)
        Setting.set("contact_email", contact_email)
        flash("Mipangilio imehifadhiwa kwa mafanikio.", "success")
        return redirect(url_for("admin.settings"))

    form.association_name.data = Setting.get("assoc_name", "TUCASA UDSM MABIBO HOSTEL")
    form.hostel_name.data = Setting.get("hostel_name", "Mabibo Hostel")
    form.whatsapp_link.data = Setting.get("whatsapp_link", current_app.config["WHATSAPP_GROUP_LINK"])
    form.contact_email.data = Setting.get("contact_email", "info@tucasa.ac.tz")
    return render_template("admin/settings.html", form=form)


@admin_bp.route("/kwaya")
@login_required
@admin_required
def choir_dashboard():
    total_events = EventPost.query.count()
    total_publications = Publication.query.count()
    total_media = ChoirMedia.query.count()
    recent_events = EventPost.query.order_by(EventPost.event_date.desc(), EventPost.created_at.desc()).limit(5).all()
    recent_publications = Publication.query.order_by(Publication.created_at.desc()).limit(5).all()
    recent_media = ChoirMedia.query.order_by(ChoirMedia.created_at.desc()).limit(5).all()
    return render_template(
        "admin/choir.html",
        total_events=total_events,
        total_publications=total_publications,
        total_media=total_media,
        recent_events=recent_events,
        recent_publications=recent_publications,
        recent_media=recent_media,
    )


@admin_bp.route("/kwaya-media", methods=["GET", "POST"])
@login_required
@admin_required
def choir_media():
    form = ChoirMediaForm()
    if form.validate_on_submit():
        file_path = save_media_file(form.file.data)
        if form.file.data and not file_path:
            flash("Faili la media si halali. Tumia mp3, wav, m4a, mp4, pdf, docx, png, jpg, jpeg au webp.", "danger")
            return render_template("admin/choir_media.html", form=form, media_items=ChoirMedia.query.order_by(ChoirMedia.created_at.desc()).all())
        db.session.add(ChoirMedia(
            title=form.title.data.strip(),
            media_type=form.media_type.data,
            description=(form.description.data or "").strip(),
            external_url=(form.external_url.data or "").strip(),
            file_path=file_path,
        ))
        db.session.commit()
        flash("Media ya kwaya imehifadhiwa kwa mafanikio.", "success")
        return redirect(url_for("admin.choir_media"))
    media_items = ChoirMedia.query.order_by(ChoirMedia.created_at.desc()).all()
    return render_template("admin/choir_media.html", form=form, media_items=media_items)


@admin_bp.route("/kwaya-media/<int:media_id>/futa", methods=["POST"])
@login_required
@admin_required
def delete_choir_media(media_id):
    item = ChoirMedia.query.get_or_404(media_id)
    db.session.delete(item)
    db.session.commit()
    flash("Media ya kwaya imefutwa.", "info")
    return redirect(url_for("admin.choir_media"))


@admin_bp.route("/matukio", methods=["GET", "POST"])
@login_required
@admin_required
def event_posts():
    form = EventPostForm()
    if form.validate_on_submit():
        image_path = save_event_image(form.image.data)
        if form.image.data and not image_path:
            flash("Picha ya tukio haikubaliki. Tumia PNG, JPG, JPEG, GIF au WEBP.", "danger")
            return render_template("admin/events.html", form=form, events=EventPost.query.order_by(EventPost.event_date.desc(), EventPost.id.desc()).all())
        db.session.add(EventPost(
            title=form.title.data.strip(),
            description=form.description.data.strip(),
            event_date=form.event_date.data,
            image_path=image_path,
        ))
        db.session.commit()
        flash("Tukio limehifadhiwa kwenye sehemu ya picha na matukio.", "success")
        return redirect(url_for("admin.event_posts"))
    events = EventPost.query.order_by(EventPost.event_date.desc(), EventPost.id.desc()).all()
    return render_template("admin/events.html", form=form, events=events)


@admin_bp.route("/matukio/<int:event_id>/futa", methods=["POST"])
@login_required
@admin_required
def delete_event_post(event_id):
    event = EventPost.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash("Tukio limefutwa.", "info")
    return redirect(url_for("admin.event_posts"))


@admin_bp.route("/machapisho-admin", methods=["GET", "POST"])
@login_required
@admin_required
def manage_publications():
    form = PublicationForm()
    if form.validate_on_submit():
        file_path = save_resource_file(form.file.data)
        if form.file.data and not file_path:
            flash("Faili la machapisho halali. Tumia PDF, DOC, au DOCX.", "danger")
            return render_template("admin/publications.html", form=form, publications=Publication.query.order_by(Publication.created_at.desc()).all())
        db.session.add(Publication(
            title=form.title.data.strip(),
            author=(form.author.data or "").strip(),
            summary=(form.summary.data or "").strip(),
            resource_url=(form.resource_url.data or "").strip(),
            file_path=file_path,
        ))
        db.session.commit()
        flash("Machapisho yamehifadhiwa kwa mafanikio.", "success")
        return redirect(url_for("admin.manage_publications"))
    publications = Publication.query.order_by(Publication.created_at.desc()).all()
    return render_template("admin/publications.html", form=form, publications=publications)


@admin_bp.route("/machapisho-admin/<int:publication_id>/futa", methods=["POST"])
@login_required
@admin_required
def delete_publication(publication_id):
    publication = Publication.query.get_or_404(publication_id)
    db.session.delete(publication)
    db.session.commit()
    flash("Machapisho yamefutwa.", "info")
    return redirect(url_for("admin.manage_publications"))


@admin_bp.route("/library", methods=["GET", "POST"])
@login_required
@admin_required
def library():
    form = LibraryItemForm()
    if form.validate_on_submit():
        file_path = save_resource_file(form.file.data)
        if form.file.data and not file_path:
            flash("Tafadhali pakia PDF halali.", "danger")
            return render_template("admin/library.html", form=form, items=LibraryItem.query.order_by(LibraryItem.category, LibraryItem.title).all())
        db.session.add(LibraryItem(
            title=form.title.data.strip(), category=form.category.data, language=form.language.data,
            author=(form.author.data or "").strip(), resource_url=(form.resource_url.data or "").strip(), file_path=file_path,
        ))
        db.session.commit()
        flash("Rasilimali imeongezwa kwenye library.", "success")
        return redirect(url_for("admin.library"))
    items = LibraryItem.query.order_by(LibraryItem.category, LibraryItem.language, LibraryItem.title).all()
    return render_template("admin/library.html", form=form, items=items)


@admin_bp.route("/library/<int:item_id>/futa", methods=["POST"])
@login_required
@admin_required
def delete_library_item(item_id):
    item = LibraryItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("Rasilimali imefutwa.", "info")
    return redirect(url_for("admin.library"))


@admin_bp.route("/ratiba", methods=["GET", "POST"])
@login_required
@admin_required
def worship_schedule():
    form = WorshipScheduleForm()
    if form.validate_on_submit():
        try:
            year = int(form.year.data)
        except (TypeError, ValueError):
            form.year.errors.append("Mwaka lazima uwe namba yenye tarakimu 4.")
        else:
            db.session.add(WorshipSchedule(year=year, day=form.day.data.strip(), time=form.time.data.strip(), activity=form.activity.data.strip()))
            db.session.commit()
            flash("Ratiba ya ibada imehifadhiwa.", "success")
            return redirect(url_for("admin.worship_schedule"))
    schedules = WorshipSchedule.query.order_by(WorshipSchedule.year.desc(), WorshipSchedule.id).all()
    return render_template("admin/worship.html", form=form, schedules=schedules)


@admin_bp.route("/ratiba/<int:schedule_id>/futa", methods=["POST"])
@login_required
@admin_required
def delete_worship_schedule(schedule_id):
    schedule = WorshipSchedule.query.get_or_404(schedule_id)
    db.session.delete(schedule)
    db.session.commit()
    flash("Ratiba imefutwa.", "info")
    return redirect(url_for("admin.worship_schedule"))


@admin_bp.route("/ratiba/<int:schedule_id>/hariri", methods=["GET", "POST"])
@login_required
@admin_required
def edit_worship_schedule(schedule_id):
    schedule = WorshipSchedule.query.get_or_404(schedule_id)
    form = WorshipScheduleForm(obj=schedule)
    if form.validate_on_submit():
        try:
            schedule.year = int(form.year.data)
        except (TypeError, ValueError):
            form.year.errors.append("Mwaka lazima uwe namba yenye tarakimu 4.")
        else:
            schedule.day = form.day.data.strip()
            schedule.time = form.time.data.strip()
            schedule.activity = form.activity.data.strip()
            db.session.commit()
            flash("Ratiba imebadilishwa.", "success")
            return redirect(url_for("admin.worship_schedule"))
    return render_template("admin/edit_worship.html", form=form, schedule=schedule)


@admin_bp.route("/viongozi", methods=["GET", "POST"])
@login_required
@admin_required
def leaders():
    form = LeaderForm()
    if form.validate_on_submit():
        try:
            year = int(form.year.data)
        except (TypeError, ValueError):
            form.year.errors.append("Mwaka lazima uwe namba yenye tarakimu 4.")
        else:
            photo_path = save_leader_photo(form.photo.data)
            if form.photo.data and not photo_path:
                flash("Picha haikubaliki.", "danger")
                return render_template("admin/leaders.html", form=form, leaders=Leader.query.order_by(Leader.year.desc(), Leader.id).all())
            db.session.add(Leader(year=year, name=form.name.data.strip(), position=form.position.data.strip(), photo_path=photo_path))
            db.session.commit()
            flash("Kiongozi ameongezwa kwa mwaka husika.", "success")
            return redirect(url_for("admin.leaders"))
    leaders_list = Leader.query.order_by(Leader.year.desc(), Leader.id).all()
    return render_template("admin/leaders.html", form=form, leaders=leaders_list)


@admin_bp.route("/viongozi/<int:leader_id>/futa", methods=["POST"])
@login_required
@admin_required
def delete_leader(leader_id):
    leader = Leader.query.get_or_404(leader_id)
    db.session.delete(leader)
    db.session.commit()
    flash("Kiongozi amefutwa.", "info")
    return redirect(url_for("admin.leaders"))


@admin_bp.route("/viongozi/<int:leader_id>/hariri", methods=["GET", "POST"])
@login_required
@admin_required
def edit_leader(leader_id):
    leader = Leader.query.get_or_404(leader_id)
    form = LeaderForm(obj=leader)
    if form.validate_on_submit():
        try:
            leader.year = int(form.year.data)
        except (TypeError, ValueError):
            form.year.errors.append("Mwaka lazima uwe namba yenye tarakimu 4.")
        else:
            leader.name = form.name.data.strip()
            leader.position = form.position.data.strip()
            if form.photo.data:
                leader.photo_path = save_leader_photo(form.photo.data)
            db.session.commit()
            flash("Taarifa za kiongozi zimebadilishwa.", "success")
            return redirect(url_for("admin.leaders"))
    return render_template("admin/edit_leader.html", form=form, leader=leader)

