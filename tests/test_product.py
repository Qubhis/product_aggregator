import json

from flask_jwt_extended import create_access_token

from app import flask_app


def test_post_product_missing_name():
    # point is protected so we must first get a token
    with flask_app.test_request_context():
        access_token = create_access_token("pytest")

    response = flask_app.test_client().post(
        "/api/products",
        headers={"Authorization": access_token},
        data=json.dumps({"description": "Some description"}),
        content_type="application/json",
    )

    data = response.get_json()

    assert response.status_code == 400
    assert data["message"] == "Name and Description must be provided"


def test_post_product_missing_description():
    # point is protected so we must first get a token
    with flask_app.test_request_context():
        access_token = create_access_token("pytest")

    response = flask_app.test_client().post(
        "/api/products",
        headers={"Authorization": access_token},
        data=json.dumps({"name": "Some name"}),
        content_type="application/json",
    )

    data = response.get_json()

    assert response.status_code == 400
    assert data["message"] == "Name and Description must be provided"
