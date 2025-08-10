from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Image
from datetime import datetime
import os

# Create blueprint for main routes
main_bp = Blueprint("main", __name__)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


@main_bp.route("/")
def home():
    """Home page showing image gallery."""
    if current_user.is_authenticated:
        # Show all images but indicate ownership
        images = Image.query.order_by(Image.uploaded_at.desc()).all()
    else:
        # Show public gallery or redirect to login
        images = []
    return render_template("index.html", images=images)


@main_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    """Image upload route."""
    if request.method == "POST":
        if "image" not in request.files:
            flash("No file selected.", "error")
            return redirect(request.url)

        file = request.files["image"]

        if file.filename == "":
            flash("No file selected.", "error")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            original_filename = file.filename
            # Create a unique filename to avoid conflicts
            filename = secure_filename(f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{original_filename}")
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

            try:
                file.save(file_path)

                # Save to database
                image = Image(filename=filename, original_filename=original_filename, user_id=current_user.id)
                db.session.add(image)
                db.session.commit()

                flash("Image uploaded successfully!", "success")
                return redirect(url_for("main.home"))
            except Exception:
                db.session.rollback()
                flash("An error occurred while uploading the image.", "error")
        else:
            flash("Invalid file type. Please upload PNG, JPG, JPEG, or GIF files.", "error")

    return render_template("upload.html")


@main_bp.route("/my-images")
@login_required
def my_images():
    """Display user's uploaded images."""
    images = Image.query.filter_by(user_id=current_user.id).order_by(Image.uploaded_at.desc()).all()
    return render_template("my_images.html", images=images)


@main_bp.route("/delete-image/<int:image_id>")
@login_required
def delete_image(image_id):
    """Delete an image (only by owner)."""
    image = Image.query.get_or_404(image_id)

    # Check if the current user owns this image
    if image.user_id != current_user.id:
        flash("You can only delete your own images.", "error")
        return redirect(url_for("main.home"))

    try:
        # Delete the file from filesystem
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], image.filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        # Delete from database
        db.session.delete(image)
        db.session.commit()

        flash("Image deleted successfully.", "success")
    except Exception:
        db.session.rollback()
        flash("An error occurred while deleting the image.", "error")

    return redirect(url_for("main.my_images"))
