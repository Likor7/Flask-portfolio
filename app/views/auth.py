from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from flask_mail import Message
from sqlalchemy import func

from app import mail
from app.models import User
from app.forms import (
    LoginForm,
    RegistrationForm,
    ProfileForm,
    ForgotPasswordForm,
    PasswordResetForm,
)

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.authenticate(form.user_identifier.data, form.password.data)
        if user:
            login_user(user)
            flash("Login successful.", "success")
            return redirect(url_for("main.index"))
        flash("Wrong username or password.", "danger")
    return render_template("auth/login.html", form=form)


@auth_blueprint.route("/logout", methods=["GET"])
def logout():
    logout_user()
    flash("Logout successful.", "success")
    return redirect(url_for("main.index"))


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        user.save()
        login_user(user)
        flash("Registration successful. You are logged in.", "success")
        return redirect(url_for("main.index"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("auth/register.html", form=form)


@auth_blueprint.route("/profile", methods=["GET", "POST"])
def profile():
    user: User = User.query.get(current_user.id)
    form = ProfileForm()
    if form.validate_on_submit():
        user.first_name = (form.first_name.data,)
        user.last_name = (form.last_name.data,)
        user.username = (form.username.data,)
        user.email = (form.email.data,)
        user.save()

        flash("Profile has been successfully updated", "info")
        return redirect(url_for("main.index"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    elif request.method == "GET":
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.username.data = user.username
        form.email.data = user.email
    return render_template("auth/profile.html", form=form)


@auth_blueprint.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user: User = User.query.filter(
            func.lower(User.email) == func.lower(form.email.data)
        ).first()
        if user:
            user.reset_password()
            message = Message('Hello, Dear User', sender='helper@mail.com', recipients=[str(form.email.data)])
            message.body = "To change your password follow the link below:\n\n" + str(
                url_for("auth.forgot_password",
                        reset_password_uuid=user.reset_password_uuid,
                        _external=True)
                        ) + "\n\nIf you don't want to change your password, just ignore this message!"
            mail.send(message)
            flash("Link to reset password sent successfully.", "success")
            return redirect(url_for("main.index"))
        flash("User not found.", "danger")
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template("auth/forgot_password.html", form=form)


@auth_blueprint.route("/reset_password/<reset_password_uuid>", methods=["GET", "POST"])
def reset_password(reset_password_uuid: str):
    user: User = User.query.filter(
        User.reset_password_uuid == reset_password_uuid
    ).first()
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("main.index"))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.password = form.password.data
        user.reset_password_uuid = ""
        user.save()
        login_user(user)
        flash("Login successful.", "success")
        return redirect(url_for("main.index"))
    elif form.is_submitted():
        flash("The given data was invalid.", "danger")
    return render_template(
        "auth/password_reset.html", form=form, reset_password_uuid=reset_password_uuid
    )
