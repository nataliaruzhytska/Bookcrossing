from flask import request, Blueprint
from flask_restful import Resource, marshal_with
import json

from db import db
from structure.marshal_structure import user_structure
from structure.model import Users

user_bp = Blueprint('UserView', __name__)


class UserView(Resource):
    @marshal_with(user_structure)
    def get(self):
        data = Users.query.all()
        return data

    def post(self):
        data = json.loads(request.data)
        new_user = Users(**data)
        db.session.add(new_user)
        db.session.commit()
        return "Successfully added a new user"

    def put(self, user_id):
        data = json.loads(request.data)
        user = Users.query.get(user_id)
        user.name = data.get("name")
        user.email = data.get("email")
        user.library_id = data.get("library_id")
        db.session.commit()
        return "Successfully updated the user"

    def delete(self, user_id):
        user = Users.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return "Successfully deleted the user"
