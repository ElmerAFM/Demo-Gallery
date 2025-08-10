from flask import Flask
from flask_login import LoginManager
from sqlalchemy import create_engine, text
from config import Config
from models import db, User
from auth import auth_bp
from routes import main_bp


def create_app(config_class=Config):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)

    # Initialize app configuration
    config_class.init_app(app)

    # Create database tables
    with app.app_context():
        engine = create_engine(config_class.SQLALCHEMY_SERVER_URI)
        with engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {config_class.DB_NAME}"))
            conn.commit()
        db.create_all()

    return app


# Create the app instance
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
