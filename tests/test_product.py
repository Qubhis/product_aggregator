import json

from app import flask_app


def test_post_product_missing_name():
    response = flask_app.test_client().post(
        "/api/products",
        data=json.dumps({"description": "Some description"}),
        content_type="application/json",
    )

    data = response.get_json()

    assert response.status_code == 400
    assert data["message"] == "Name and Description must be provided"


def test_post_product_missing_description():
    response = flask_app.test_client().post(
        "/api/products",
        data=json.dumps({"name": "Some name"}),
        content_type="application/json",
    )

    data = response.get_json()

    assert response.status_code == 400
    assert data["message"] == "Name and Description must be provided"
