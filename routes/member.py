from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

from extensions import db
from models import Member, Setting
from forms import MemberRegistrationForm, MemberProfileForm

member_bp = Blueprint("member", __name__)


@member_bp.route("/usajili-wa-wanachama", methods=["GET", "POST"])
@login_required
def register():
    existing_member = Member.query.filter_by(user_id=current_user.id).first()
    if existing_member:
        flash("Tayari umesajiliwa kama mwanachama.", "info")
        return redirect(url_for("member.success"))

    form = MemberRegistrationForm()
    if not form.is_submitted():
        form.email.data = current_user.email
        form.jina.data = current_user.jina

    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        if Member.query.filter(db.func.lower(Member.email) == email).first():
            flash("Barua pepe hii tayari imesajiliwa na mwanachama mwingine.", "danger")
            return render_template("member_register.html", form=form)

        member = Member(
            user_id=current_user.id,
            jina=form.jina.data.strip(),
            jinsia=form.jinsia.data,
            mwaka=form.mwaka.data,
            kozi=form.kozi.data.strip(),
            simu=form.simu.data.strip(),
            email=email,
            hostel=form.hostel.data.strip(),
            tarehe_ya_kuzaliwa=form.tarehe_ya_kuzaliwa.data,
            vipaji=form.vipaji.data.strip() if form.vipaji.data else "",
            kukubali_whatsapp=form.kukubali_whatsapp.data,
            status="pending",
            is_active=True,
        )
        db.session.add(member)
        db.session.commit()
        flash("Umefanikiwa kujisajili kama mwanachama wa TUCASA UDSM MABIBO HOSTEL!", "success")
        return redirect(url_for("member.success"))

    return render_template("member_register.html", form=form)


@member_bp.route("/member/profile")
@login_required
def profile():
    member = Member.query.filter_by(user_id=current_user.id).first()
    if not member:
        flash("Huna taarifa za mwanachama bado. Tafadhali jisajili kwanza.", "warning")
        return redirect(url_for("member.register"))

    # The profile template contains the editable form, so always provide it,
    # including on the GET request to /member/profile.
    form = MemberProfileForm(obj=member)
    return render_template("member_profile.html", form=form, member=member)


@member_bp.route("/member/profile/edit", methods=["GET", "POST"])
@member_bp.route("/member/update", methods=["GET", "POST"])
@login_required
def edit_profile():
    member = Member.query.filter_by(user_id=current_user.id).first()
    if not member:
        flash("Huna taarifa za mwanachama bado. Tafadhali jisajili kwanza.", "warning")
        return redirect(url_for("member.register"))

    form = MemberProfileForm(obj=member)
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        duplicate_email = Member.query.filter(
            db.func.lower(Member.email) == email,
            Member.id != member.id,
        ).first()
        if duplicate_email:
            flash("Barua pepe hii tayari imesajiliwa na mwanachama mwingine.", "danger")
            return render_template("member_profile.html", form=form, member=member)

        member.jina = form.jina.data.strip()
        member.jinsia = form.jinsia.data
        member.mwaka = form.mwaka.data
        member.kozi = form.kozi.data.strip()
        member.simu = form.simu.data.strip()
        member.email = email
        member.hostel = form.hostel.data.strip()
        member.tarehe_ya_kuzaliwa = form.tarehe_ya_kuzaliwa.data
        member.vipaji = form.vipaji.data.strip() if form.vipaji.data else ""
        member.kukubali_whatsapp = form.kukubali_whatsapp.data
        # Member.updated_at is refreshed automatically by its SQLAlchemy onupdate handler.

        db.session.commit()
        flash("Taarifa zako zimebadilishwa.", "success")
        return redirect(url_for("member.profile"))

    return render_template("member_profile.html", form=form, member=member)


@member_bp.route("/usajili/imefanikiwa")
@login_required
def success():
    member = Member.query.filter_by(user_id=current_user.id).first()
    whatsapp_link = Setting.get("whatsapp_link", current_app.config["WHATSAPP_GROUP_LINK"])
    return render_template("member_success.html", whatsapp_link=whatsapp_link, member=member)

