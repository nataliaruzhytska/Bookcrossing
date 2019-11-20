from flask_restful import fields

book_structure = {
    "name": fields.String
}

lib_structure = {
    "name": fields.String,
    "books": fields.Nested(book_structure)
}

user_structure = {
    "name": fields.String,
    "email": fields.String,
    "libraries": fields.Nested(lib_structure)
}

books_structure = {
    "name": fields.String,
    "author": fields.String,
    "edition": fields.String,
    "year_ed": fields.Integer,
    "translator": fields.String
}


