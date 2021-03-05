import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_restful import Api

from celeryapp.celeryapp import make_celery_app
from external.token import get_and_set_offers_service_token
from database.db import initialize_db
from resources.routes import initialize_routes


# load env configurations
load_dotenv(dotenv_path=find_dotenv(".env"))

flask_app = Flask(__name__)
# configure app
flask_app.config["SECRECT_KEY"] = os.getenv("FLASK_SECRET_KEY")
flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DB_URI")
# avoid sqlalchemy warning
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# instantiate db
initialize_db(flask_app)
# instantiate flask_restful
api = Api(flask_app)
# adding routes to our app
initialize_routes(api)

# create celery
celery_app = make_celery_app(flask_app)

from resources.product import fetch_products_from_db
from external.offers import get_offers, update_db_with_offers


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, update_offers.s())


@celery_app.task(name="update_offers")
def update_offers():
    # TODO: replace print with logging functions
    load_dotenv(dotenv_path=find_dotenv(".env"))
    print("Let's look if there are new prices...")
    products = fetch_products_from_db()
    if not products:
        print("But there are no products...")
        return

    for product_id in products:
        # call offers to get offer
        response = get_offers(product_id)
        # skip update if no offers
        if response.status_code != 200 or not response.json():
            print(response.text)
            continue

        if not update_db_with_offers(product_id=product_id, offers=response.json()):
            print(f"offers couldn't be updated for product {product_id}")
            continue

        print(f"Product {product_id} got new prices!")


if __name__ == "__main__":
    if get_and_set_offers_service_token() is False:
        raise TimeoutError("Service is not available")
    # FIXME: remove debug before releasing !
    flask_app.run(debug=True)
