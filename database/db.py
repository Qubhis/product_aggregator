from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def initialize_db(flask_app):
    db.init_app(flask_app)
