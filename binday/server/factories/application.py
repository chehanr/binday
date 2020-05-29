import os
import pymysql
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MIGRATIONS_DIR = os.path.join(BASE_DIR, "models", "migrations")
LOCAL_SQLITE_DB_PATH = os.path.join(BASE_DIR, "db.sqlite3")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")


db = SQLAlchemy()
migrate = Migrate(directory=MIGRATIONS_DIR)
login_manager = LoginManager()
csrf = CSRFProtect()


def create_application():
    app = Flask(
        __name__,
        static_url_path="",
        static_folder=STATIC_DIR,
        template_folder=TEMPLATE_DIR,
    )

    # Local Database
    # app.config.from_mapping(
    #     SECRET_KEY=os.getenv("SECRET_KEY", "key"),
    #     TEMPLATES_AUTO_RELOAD=True,
    #     SQLALCHEMY_TRACK_MODIFICATIONS=True,
    #     SQLALCHEMY_DATABASE_URI=os.getenv(
    #         "SQLALCHEMY_DATABASE_URI", f"sqlite:///{LOCAL_SQLITE_DB_PATH}"
    #     ),
    # )

    #Remote Database
    remote_db_ip="192.168.1.20"
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "key"),
        TEMPLATES_AUTO_RELOAD=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "SQLALCHEMY_DATABASE_URI", f"mysql+pymysql://assignment:assignment3@" + remote_db_ip + "/binday"
        ),
    )

    # Import models.
    from binday.server.models.user import User
    from binday.server.models.my_bin import MyBin
    from binday.server.models.bin_day import BinDay
    from binday.server.models.bin_reading import BinReading

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)

    Bootstrap(app)

    # Import views.
    from binday.server.views.main import blueprint as main_bp
    from binday.server.views.auth import blueprint as auth_bp
    from binday.server.views.my_bin import blueprint as my_bin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(my_bin_bp)

    csrf.init_app(app)

    return app
