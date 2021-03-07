import pytest

from database.models import Product, Offer


def test_new_product():
    product = Product(name="Test", description="Test Product")
    assert product.name == "Test"
    assert product.description == "Test Product"


def test_new_offer():
    offer = Offer(id=55354, product_id=1, price=99, items_in_stock=999)
    assert offer.id == 55354
    assert offer.product_id == 1
    assert offer.price == 99
    assert offer.items_in_stock == 999
