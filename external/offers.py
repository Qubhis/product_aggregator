import os
import requests

from dotenv import find_dotenv, load_dotenv

from database.db import db
from database.models import Offer
from external.token import get_and_set_offers_service_token


load_dotenv(find_dotenv(".env"))
BASE_URL = os.getenv("OFFERS_BASE_URL")


def register_product(product_id, name, description) -> requests.Response:
    TOKEN = os.getenv("OFFERS_TOKEN")
    if TOKEN is None:
        if get_and_set_offers_service_token() is False:
            raise TimeoutError("Service is not available")
        else:
            TOKEN = os.getenv("OFFERS_TOKEN")

    headers = {"Bearer": TOKEN}
    payload = {
        "id": product_id,
        "name": name,
        "description": description,
    }
    response = requests.post(
        url=f"{BASE_URL}/products/register", headers=headers, data=payload
    )
    # return response (errors are handled in caller)
    return response


def get_offers(product_id) -> requests.Response:
    TOKEN = os.getenv("OFFERS_TOKEN")
    if TOKEN is None:
        if get_and_set_offers_service_token() is False:
            raise TimeoutError("Service is not available")
        else:
            TOKEN = os.getenv("OFFERS_TOKEN")

    headers = {"Bearer": TOKEN}
    response = requests.get(
        url=f"{BASE_URL}/products/{str(product_id)}/offers",
        headers=headers,
    )
    # return response (errors are handled in caller)
    return response


def update_db_with_offers(product_id, offers, timestamp):
    # add/update offer in db
    for offer in offers:
        # check db first
        existing_offer = Offer.query.filter_by(
            id=offer["id"], product_id=product_id, timestamp=timestamp
        ).first()
        if not existing_offer:
            new_offer = Offer(
                id=offer["id"],
                product_id=product_id,
                timestamp=timestamp,
                price=offer["price"],
                items_in_stock=offer["items_in_stock"],
            )
            db.session.add(new_offer)
        else:
            existing_offer.price = offer["price"]
            existing_offer.items_in_stock = offer["items_in_stock"]

        db.session.commit()
    else:
        # product updated with all offers
        return True
