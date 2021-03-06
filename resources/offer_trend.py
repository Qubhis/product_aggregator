import datetime

from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource

import json

from database.models import Offer


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class OfferTrend(Resource):
    @jwt_required()
    def get(self, product_id, offers_ms_id, minutes):
        # determine from - to
        datetime_to = datetime.datetime.utcnow()
        datetime_from = datetime_to - datetime.timedelta(minutes=minutes)
        # get offers
        history_offers = (
            Offer.query.filter(
                Offer.product_id == product_id,
                Offer.offers_ms_id == offers_ms_id,
                Offer.timestamp >= datetime_from.strftime(DATETIME_FORMAT),
                Offer.timestamp <= datetime_to.strftime(DATETIME_FORMAT),
            )
            .order_by(Offer.timestamp)
            .all()
        )
        if not history_offers:
            return Response(
                response=json.dumps({"message": "No data found"}),
                mimetype="application/json",
                status=404,
            )
        # prepare output with offers and date
        data = {"offers": list(), "percentage_increase": None}
        for offer in history_offers:
            data["offers"].append(
                {
                    "price": offer.price,
                    "timestamp": offer.timestamp.strftime(DATETIME_FORMAT),
                }
            )
        # calculate trend
        first_price = data["offers"][0]["price"]
        last_price = data["offers"][-1]["price"]
        percentage_increase = ((last_price - first_price) / first_price) * 100
        data["percentage_increase"] = round(percentage_increase, 2)

        return Response(
            response=json.dumps(data), mimetype="application/json", status=200
        )
