import json
import os
import requests

from flask import Response

from dotenv import find_dotenv, load_dotenv
from external.token import get_and_set_offers_service_token

load_dotenv(find_dotenv(".env"))
TOKEN = os.getenv("OFFERS_TOKEN")
BASE_URL = os.getenv("OFFERS_BASE_URL")


def register_product(product_id, name, description) -> requests.Response:
    TOKEN = os.getenv("OFFERS_TOKEN")
    if TOKEN is None:
        if get_and_set_offers_service_token() is False:
            raise TimeoutError("Service is not available")
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

    headers = {"Bearer": TOKEN}
    response = requests.get(
        url=f"{BASE_URL}/products/{str(product_id)}/offers",
        headers=headers,
    )
    # return response (errors are handled in caller)
    return response
