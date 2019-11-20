import json

from flask import request, Blueprint
from flask_restful import Resource, marshal_with

from db import db
from structure.marshal_structure import books_structure
from structure.model import Book

book_bp = Blueprint('BookView', __name__)


class BookView(Resource):
    @marshal_with(books_structure)
    def get(self):
        data = Book.query.all()
        return data

    def post(self):
        data = json.loads(request.data)
        new_book = Book(**data)
        db.session.add(new_book)
        db.session.commit()
        return "Successfully added a new book"

    def put(self, book_id):
        data = json.loads(request.data)
        book = Book.query.get(book_id)
        book.name = data.get("name")
        book.author = data.get("author")
        db.session.commit()
        return "Successfully updated the book"

    def delete(self, book_id):
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        return "Successfully deleted the book"
