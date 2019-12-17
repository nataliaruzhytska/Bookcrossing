import json

from flask import request, Blueprint
from flask_restful import Resource, marshal_with

from db import db
from structure.marshal_structure import lib_structure
from structure.model import Library
from structure.parsers import lib_parser

lib_bp = Blueprint('LibraryView', __name__)


class LibraryView(Resource):
    @marshal_with(lib_structure)
    def get(self):
        try:
            data = Library.query.all()
            if lib_parser.parse_args().get('lib_id'):
                library = Library.query.get(lib_parser.parse_args().get('lib_id'))
                return library
            else:
                return data
        except (ValueError, KeyError, TypeError) as error:
            return error, f"Cannot find a library. {error}"

    @marshal_with(lib_structure)
    def post(self):
        try:
            data = json.loads(request.data)
            new_lib = Library(**data)
            db.session.add(new_lib)
            db.session.commit()
            return new_lib, f"Successfully added a new library {new_lib.name}"
        except (ValueError, KeyError, TypeError) as error:
            return Library.query.all(), f"Cannot create a library. {error}"

    @marshal_with(lib_structure)
    def put(self, lib_id):
        data = json.loads(request.data)
        lib = Library.query.get(lib_id)
        try:
            lib.name = data.get("name")
            lib.user_id = data.get("user_id")
            return lib, f"Successfully updated the library {lib.name}"
        except (ValueError, KeyError, TypeError) as error:
            return lib, f"Cannot update a library {lib.name}. {error}"

    @marshal_with(lib_structure)
    def delete(self, lib_id):
        lib = Library.query.get(lib_id)
        try:
            db.session.delete(lib)
            db.session.commit()
            return "Successfully deleted the library"
        except (ValueError, KeyError, TypeError) as error:
            return lib, f"Cannot delete a library {lib.name}. {error}"
