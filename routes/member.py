from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

from extensions import db
from models import Member, Setting
from forms import MemberRegistrationForm

member_bp = Blueprint("member", __name__)


@member_bp.route("/usajili-wa-wanachama", methods=["GET", "POST"])
@login_required
def register():
    # Kila akaunti inaruhusiwa kuwa na usajili mmoja tu.
    existing_member = Member.query.filter_by(user_id=current_user.id).first()
    if existing_member:
        flash("Tayari umesajiliwa kama mwanachama.", "info")
        return redirect(url_for("member.success"))

    form = MemberRegistrationForm()

    # Pre-fill email and name for a new form.
    if not form.is_submitted():
        form.email.data = current_user.email
        form.jina.data = current_user.jina

    if form.validate_on_submit():
        member = Member(
            user_id=current_user.id,
            jina=form.jina.data.strip(),
            jinsia=form.jinsia.data,
            mwaka=form.mwaka.data,
            kozi=form.kozi.data.strip(),
            simu=form.simu.data.strip(),
            email=form.email.data.lower().strip(),
            hostel=form.hostel.data.strip(),
            tarehe_ya_kuzaliwa=form.tarehe_ya_kuzaliwa.data,
            vipaji=form.vipaji.data.strip() if form.vipaji.data else "",
            kukubali_whatsapp=form.kukubali_whatsapp.data,
        )
        db.session.add(member)
        db.session.commit()
        flash("Umefanikiwa kujisajili kama mwanachama wa TUCASA UDSM MABIBO HOSTEL!", "success")
        return redirect(url_for("member.success"))

    return render_template("member_register.html", form=form)


@member_bp.route("/usajili/imefanikiwa")
@login_required
def success():
    whatsapp_link = Setting.get("whatsapp_link", current_app.config["WHATSAPP_GROUP_LINK"])
    return render_template("member_success.html", whatsapp_link=whatsapp_link)
