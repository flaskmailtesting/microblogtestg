from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user
from flask_babel import _
from werkzeug.urls import url_parse
from megatutApp import db
from megatutApp.models import User
from megatutApp.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from megatutApp.auth.email import send_password_reset_email
from megatutApp.auth import bp

@bp.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("main.index"))
	lform = LoginForm()
	if lform.validate_on_submit():
		user = User.query.filter_by(username=lform.username.data).first()
		if user is None or not user.check_password(lform.password.data):
			flash(_("Invalid username or password."))
			return redirect(url_for("auth.login"))
		login_user(user, remember=lform.remember_me.data)
		next_page = request.args.get("next")
		if not next_page or url_parse(next_page).netloc != "":
			next_page = url_for("main.index")
		return redirect(next_page)
	return render_template("auth/login.html", title=_("Sign In"), form=lform)

@bp.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("main.index"))

@bp.route("/register", methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("main.index"))
	rform = RegistrationForm()
	if rform.validate_on_submit():
		user = User(username=rform.username.data, email=rform.email.data)
		user.set_password(rform.password.data)
		db.session.add(user)
		db.session.commit()
		flash(_("Congratulations, you are now a registered user!"))
		return redirect(url_for("auth.login"))
	return render_template("auth/register.html", title=_("Register"), form=rform)

@bp.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for("main.index"))
	rprform = ResetPasswordRequestForm()
	if rprform.validate_on_submit():
		user = User.query.filter_by(email=rprform.email.data).first()
		if user:
			send_password_reset_email(user)
		flash(_("Check your email for the instructions to reset your password"))
		return redirect(url_for("main.index"))
	return render_template("auth/reset_password_request.html", title=_("Reset Password"), form=rprform)

@bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for("main.index"))
	user = User.verify_reset_password(token)
	if not user:
		return redirect(url_for("main.index"))
	rpform = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(rpform.password.data)
		db.session.commit()
		flash(_("Your password has been reset."))
		return redirect(url_for("auth.login"))
	render_template("auth/reset_password.html", form=rpform)

