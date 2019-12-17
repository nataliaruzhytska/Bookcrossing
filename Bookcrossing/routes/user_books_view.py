import json

from flask import request, Blueprint
from flask_restful import Resource, marshal_with

from db import db

from structure.marshal_structure import book_structure
from structure.model import Users, Book, user_books
from structure.parsers import user_book_parser

user_book_bp = Blueprint('UserBookView', __name__)


class UserBookView(Resource):
    def post(self):
        try:
            data = json.loads(request.data)
            user_name = data.get("user_name")
            book_name = data.get("book_name")
            user = Users.query.filter_by(name=user_name).first()
            book = Book.query.filter_by(name=book_name).first()
            user.books.append(book)
            db.session.commit()
            return f"Successfully added {book.name} to {user.name}"
        except (ValueError, KeyError, TypeError) as error:
            return f"Cannot create a user. {error}"

    @marshal_with(book_structure)
    def get(self):
        try:
            args = user_book_parser.parse_args(strict=True)
            user = Users.query.filter_by(name=args.get("name")).first()
            data = [book for book in user.books if book.is_visible is True]
            return data
        except (ValueError, KeyError, TypeError) as error:
            return error

    @marshal_with(book_structure)
    def put(self, name):
        args = user_book_parser.parse_args(strict=True)
        user = Users.query.filter_by(name=name).first()
        try:
            if args.get('book_id'):
                book = Book.query.get(args.get('book_id'))
                book.is_visible = args.get('is_visible')
                db.session.commit()
                return book
            else:
                for book in user.books:
                    book.is_visible = args.get('is_visible')
                db.session.commit()

        except (ValueError, KeyError, TypeError) as error:
            return error
