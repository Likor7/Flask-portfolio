import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException
from flask_migrate import Migrate
from flask_mail import Mail

# Initialize instances
login_manager = LoginManager()
db = SQLAlchemy()
migration = Migrate()
mail = Mail()


def create_app(environment="development"):
    from config import config
    from app.views import (
        auth_blueprint, 
        main_blueprint, 
        company_blueprint,
        employee_blueprint,
        recipient_blueprint,
        upload_blueprint,
    )
    from app.models import User, AnonymousUser

    # Instantiate app
    app = Flask(__name__)

    # Setup configs
    env = os.getenv("FLASK_ENV", environment)
    app.config.from_object(config[env])
    config[env].configure(app)

    # Setup extensions
    db.init_app(app)
    migration.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # Register blueprints here
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(company_blueprint)
    app.register_blueprint(employee_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(recipient_blueprint)
    app.register_blueprint(upload_blueprint)

    @login_manager.user_loader
    def get_user(id):
        return User.query.get(int(id))

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    login_manager.anonymous_user = AnonymousUser

    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return render_template("error.html", error=exc), exc.code

    return app