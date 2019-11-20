import json

from flask import request, Blueprint
from flask_restful import Resource, marshal_with

from db import db
from structure.marshal_structure import lib_structure
from structure.model import Library


lib_bp = Blueprint('LibraryView', __name__)


class LibraryView(Resource):
    @marshal_with(lib_structure)
    def get(self):
        data = Library.query.all()
        return data

    def post(self):
        data = json.loads(request.data)
        new_lib = Library(**data)
        db.session.add(new_lib)
        db.session.commit()
        return "Successfully added a new library"

    def put(self, lib_id):
        data = json.loads(request.data)
        lib = Library.query.get(lib_id)
        lib.name = data.get("name")
        lib.user_id = data.get("user_id")
        return "Successfully updated the library"

    def delete(self, lib_id):
        lib = Library.query.get(lib_id)
        db.session.delete(lib)
        db.session.commit()
        return "Successfully deleted the library"
