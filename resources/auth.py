import datetime
import json

from flask import Response
from flask_restful import Resource
from flask_jwt_extended import create_access_token


class Auth(Resource):
    def post(self):
        access_token = create_access_token(
            identity="guest", expires_delta=datetime.timedelta(minutes=60)
        )
        return Response(
            response=json.dumps({"access_token": access_token}),
            mimetype="application/json",
            status=201,
        )
