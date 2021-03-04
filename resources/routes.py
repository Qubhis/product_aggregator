from .product import Products, ProductManage


def initialize_routes(api):
    api.add_resource(Products, "/api/products")
    api.add_resource(ProductManage, "/api/product/<int:product_id>")
