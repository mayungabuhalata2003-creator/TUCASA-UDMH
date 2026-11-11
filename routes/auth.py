from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db
from models import User
from forms import SignupForm, LoginForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Barua pepe hii tayari imesajiliwa. Tafadhali ingia (login).", "warning")
            return redirect(url_for("auth.login"))
        user = User(jina=form.jina.data.strip(), email=email, role="member")
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Umefanikiwa kujisajili! Sasa ingia (login) na taarifa zako.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/signup.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.email.data.strip()
        user = User.query.filter(db.func.lower(User.email) == username.lower()).first()
        if not user:
            flash("Huna akaunti. Tafadhali jisajili (signup) kwanza.", "danger")
            return redirect(url_for("auth.signup"))
        if not user.check_password(form.password.data):
            flash("Nywila si sahihi. Jaribu tena.", "danger")
            return render_template("auth/login.html", form=form)
        login_user(user)
        flash(f"Karibu tena, {user.jina}!", "success")
        next_page = request.args.get("next", "")
        if next_page.startswith("/") and not next_page.startswith("//") and "\\" not in next_page:
            return redirect(next_page)
        return redirect(url_for("main.dashboard"))
    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Umetoka (logged out) kwa mafanikio.", "info")
    return redirect(url_for("main.landing"))
