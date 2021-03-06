from .auth import Auth
from .offer_trend import OfferTrend
from .product import Products, ProductManage


def initialize_routes(api):
    api.add_resource(Auth, "/api/auth")
    api.add_resource(Products, "/api/products")
    api.add_resource(ProductManage, "/api/product/<int:product_id>")
    api.add_resource(
        OfferTrend,
        "/api/product/<int:product_id>/offer/<int:offers_ms_id>/trend/<int:minutes>",
    )
