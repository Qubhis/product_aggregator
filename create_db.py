from app import flask_app
from database.models import db, Offer, Product


# NOTE: to be run only when db doesn't exist
if __name__ == "__main__":
    with flask_app.app_context():
        db.init_app(flask_app)
        db.create_all()
