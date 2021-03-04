from database.db import db
from database.models import Offer
from external.offers import get_offers


def update_db_with_offers(product_id, offers):

    # add/update offer in db
    for offer in offers:
        # check db first
        existing_offer = Offer.query.filter_by(offers_ms_id=offer["id"]).first()
        if not existing_offer:
            new_offer = Offer(
                price=offer["price"],
                offers_ms_id=offer["id"],
                items_in_stock=offer["items_in_stock"],
                product_id=product_id,
            )
            db.session.add(new_offer)
        else:
            existing_offer.price = offer["price"]
            existing_offer.items_in_stock = offer["items_in_stock"]

        db.session.commit()
    else:
        # product updated
        return True
