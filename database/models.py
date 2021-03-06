from .db import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)
    offers = db.relationship("Offer", backref="product", lazy=True)


class Offer(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), primary_key=True)
    offers_ms_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    items_in_stock = db.Column(db.Integer)
