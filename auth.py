from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

# Create blueprint for authentication routes
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration route."""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Validation
        if not username or not email or not password:
            flash("All fields are required.", "error")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return render_template("register.html")

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "error")
            return render_template("register.html")

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return render_template("register.html")

        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("auth.login"))
        except Exception:
            db.session.rollback()
            flash("An error occurred during registration.", "error")
            return render_template("register.html")

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """User login route."""
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please enter both username and password.", "error")
            return render_template("login.html")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome back, {user.username}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Invalid username or password.", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    """User logout route."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))
