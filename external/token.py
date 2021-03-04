import os
import requests
import time


def get_and_set_offers_service_token():
    BASE_URL = os.getenv("OFFERS_BASE_URL")
    attempts = 0
    while attempts < 240:
        response = requests.post(url=f"{BASE_URL}/auth")
        if response.status_code == 201:
            os.environ["OFFERS_TOKEN"] = response.json()["access_token"]
            return True
        else:
            # wait 15 seconds before the next attempt to get the token
            time.wait(15)
    # couldn't get a token most probably due to unavailability of the api point
    return False
