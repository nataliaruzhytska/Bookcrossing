import json

from flask import request, Blueprint
from flask_restful import Resource, marshal_with

from db import db
from structure.marshal_structure import books_structure
from structure.model import Book
from structure.parsers import book_parser


book_bp = Blueprint('BookView', __name__)


class BookView(Resource):
    @marshal_with(books_structure)
    def get(self):
        try:
            data = [book for book in Book.query.all() if book.is_visible is True]
            if book_parser.parse_args().get('book_id'):
                book = Book.query.get(book_parser.parse_args().get('book_id'))
                if book.is_visible is True:
                    return book
                else:
                    return data, f"Cannot find a book {book.name}"
            return data
        except (ValueError, KeyError, TypeError) as error:
            return error, f"Cannot find a book. {error}"

    @marshal_with(books_structure)
    def post(self):
        try:
            data = json.loads(request.data)
            new_book = Book(**data)
            db.session.add(new_book)
            db.session.commit()
            return new_book, f"Successfully added a new book {new_book.name}"
        except (ValueError, KeyError, TypeError) as error:
            return Book.query.all(), f"Cannot create a book. {error}"

    @marshal_with(books_structure)
    def put(self, book_id):
        data = json.loads(request.data)
        book = Book.query.get(book_id)
        try:
            book.is_visible = data["is_visible"]
            book.lib_id = data["lib_id"]
            db.session.commit()
            return book, f"Successfully updated the book {book.name}"
        except (ValueError, KeyError, TypeError) as error:
            return book, f"Cannot update a book {book.name}. {error}"

    @marshal_with(books_structure)
    def delete(self, book_id):
        book = Book.query.get(book_id)
        try:
            db.session.delete(book)
            db.session.commit()
            return book, f"Successfully deleted the book {book.name}"
        except (ValueError, KeyError, TypeError) as error:
            return book, f"Cannot delete a book {book.name}. {error}"
