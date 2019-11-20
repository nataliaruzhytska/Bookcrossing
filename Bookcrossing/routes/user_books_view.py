import json

from flask import request, Blueprint
from flask_restful import Resource, marshal_with

from db import db

from structure.marshal_structure import user_structure, book_structure
from structure.model import Users, Book
from structure.parsers import user_book_parser


user_book_bp = Blueprint('UserBookView', __name__)


class UserBookView(Resource):
    def post(self):
        data = json.loads(request.data)
        user_name = data.get("user_name")
        book_name = data.get("book_name")
        user = Users.query.filter_by(name=user_name).first()
        book = Book.query.filter_by(name=book_name).first()
        user.books.append(book)
        db.session.commit()
        return f"Successfully added {book.name} to {user.name}"

    @marshal_with(book_structure)
    def get(self):
        args = user_book_parser.parse_args(strict=True)
        user = Users.query.filter_by(name=args.get("name")).first()
        return user.books
