from flask import request, Blueprint
from flask_restful import Resource, marshal_with
import json

from db import db
from structure.marshal_structure import user_structure
from structure.model import Users
from structure.parsers import user_parser

user_bp = Blueprint('UserView', __name__)


class UserView(Resource):

    @marshal_with(user_structure)
    def get(self):
        try:
            data = Users.query.all()
            if user_parser.parse_args().get('user_id'):
                user = Users.query.get(user_parser.parse_args().get('user_id'))
                return user
            else:
                return data
        except (ValueError, KeyError, TypeError) as error:
            return error, f"Cannot find a user. {error}"

    @marshal_with(user_structure)
    def post(self):
        try:
            data = json.loads(request.data)
            new_user = Users(**data)
            db.session.add(new_user)
            db.session.commit()
            return new_user, f"Successfully added a new user {new_user.name}"
        except (ValueError, KeyError, TypeError) as error:
            return Users.query.all(), f"Cannot create a user. {error}"

    @marshal_with(user_structure)
    def put(self, user_id):
        data = json.loads(request.data)
        user = Users.query.get(user_id)
        try:
            user.name = data.get("name")
            user.email = data.get("email")
            user.library_id = data.get("library_id")
            db.session.commit()
            return user, f"Successfully updated the user {user.name}"
        except (ValueError, KeyError, TypeError) as error:
            return user, f"Cannot update a user {user.name}. {error}"

    @marshal_with(user_structure)
    def delete(self, user_id):
        user = Users.query.get(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
            return user, f"Successfully deleted the user {user.name}"
        except (ValueError, KeyError, TypeError) as error:
            return user, f"Cannot delete a user {user.name}. {error}"
