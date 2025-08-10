import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration class."""

    # Basic Flask config
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # Database config
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", 3306)
    DB_NAME = os.getenv("DB_NAME", "demo_gallery")
    SQLALCHEMY_DATABASE_URI = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_SERVER_URI = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload configuration
    UPLOAD_FOLDER = "static/uploads"
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

    @staticmethod
    def init_app(app):
        """Initialize application with this config."""
        # Ensure upload folder exists
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
