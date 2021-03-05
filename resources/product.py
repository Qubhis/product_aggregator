import json

from flask import Response, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from sqlalchemy import exc


from database.models import db, Product
from external.offers import register_product


def _400_product_missing_body_parameter():
    return Response(
        response=json.dumps({"message": "Name and Description must be provided"}),
        mimetype="application/json",
        status=400,
    )


def _404_product_not_exist():
    return Response(
        response=json.dumps({"message": "Product doesn't exists"}),
        mimetype="application/json",
        status=404,
    )


def _409_product_name_already_exist():
    return Response(
        response=json.dumps(
            {"message": "Product already exists with the provided name"}
        ),
        mimetype="application/json",
        status=409,
    )


def fetch_products_from_db():
    return [product.id for product in Product.query.all()]


class Products(Resource):
    @jwt_required()
    def post(self):
        # get data from request
        body = request.get_json()
        name = body.get("name")
        description = body.get("description")

        if name is None or description is None:
            return _400_product_missing_body_parameter()

        # create product in db
        product = Product(name=name, description=description)
        db.session.add(product)
        try:
            db.session.commit()
        except exc.IntegrityError:  # sql duplicate
            db.session.rollback()
            return _409_product_name_already_exist()

        # register product in offers microservice
        registration = register_product(
            product_id=product.id, name=product.name, description=product.description
        )

        if registration.status_code != 201:
            # remove product from our db
            db.session.delete(product)
            db.session.commit()
            # send erroneous response
            data = {
                "message": "product couldn't be registered",
                "error": registration.json()["msg"],
            }
            return Response(
                response=json.dumps(data),
                mimetype="application/json",
                status=registration.status_code,
            )

        data = {"message": "product has been created", "id": product.id}
        return Response(
            response=json.dumps(data), mimetype="application/json", status=201
        )


class ProductManage(Resource):
    @jwt_required()
    def put(self, product_id):
        # check if product exists
        product = Product.query.filter_by(id=product_id).first()
        if product is None:
            return _404_product_not_exist()
        # get data from body
        request_body = request.get_json()
        name = request_body.get("name")
        description = request_body.get("description")

        if name:
            product.name = name
        if description:
            product.description = description
        # update db
        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            return _409_product_name_already_exist()

        data = {"message": "Product has been updated"}
        return Response(
            response=json.dumps(data), mimetype="application/json", status=200
        )

    @jwt_required()
    def delete(self, product_id):
        # check if product exists
        product = Product.query.filter_by(id=product_id).first()
        if product is None:
            return _404_product_not_exist()
        # delete product from db and related offers
        db.session.delete(product)
        db.session.commit()

        data = {"message": "Product has been deleted"}
        return Response(
            response=json.dumps(data), mimetype="application/json", status=200
        )
