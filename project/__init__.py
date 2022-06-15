import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_gravatar import Gravatar


db = SQLAlchemy()


def create_app():
    # INITIALIZE FLASK APP
    app = Flask(__name__)

    # INITIALIZE SQLALCHEMY OBJECT
   
    db.init_app(app=app)


    # INITIALIZE BOOTSTRAP
    Bootstrap(app=app)

    # INSTANTIATE GRAVATAR OBJECT
    # CREATE GRAVATAR OBJECT TO AUTO GENERATE AVATARS IN TEMPLATE
    gravatar = Gravatar(app,
                        size=30,
                        rating='g',
                        default='retro',
                        force_default=False,
                        force_lower=False,
                        use_ssl=False,
                        base_url=None)

    # LOGIN MANAGER OBJECT
    login_manager = LoginManager()
    login_manager.init_app(app=app)


    # CONFIGURE SQLALCHEMY
    app.config["SECRET_KEY"] = os.environ.get("SECRET_kEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

    # specify database pathway and sets postgres as priority if exists(for deployment purpose)
    uri = os.getenv("DATABASE_URI", "sqlite:///database.db")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    from project.models import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    # IMPORT AND REGISTER BLUEPRINTS
    from project.main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    from project.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)


    return app