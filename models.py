from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy (will be configured in app.py)
db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication and image ownership."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to images
    images = db.relationship("Image", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        """Set password hash for user."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if provided password matches user's password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Image(db.Model):
    """Image model for storing uploaded images."""

    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Image {self.filename}>"
