from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    
    # Application configuration
    app.config['SECRET_KEY'] = 'jeofejafoiaejfoihjof'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:qwerty@localhost:5432"
    app.config['SQLALCHEMY_BINDS'] = {
        "auth": "postgresql://postgres:qwerty@localhost:5432/auth"
    }

    # Initialize database with the application
    db.init_app(app)

    # Import Blueprints
    from .routes import routes
    from .auth import auth
    from .admin import admin

    # Register Blueprints
    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    # Import models after app and db are set up
    from .models import User

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Set up Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Name of the login route
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
