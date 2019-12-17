from flask_restful import reqparse

user_book_parser = reqparse.RequestParser()
user_book_parser.add_argument("name", type=str)
user_book_parser.add_argument("book_id", type=int)
user_book_parser.add_argument("is_visible", type=bool)

book_parser = reqparse.RequestParser()
book_parser.add_argument("name", type=str)
book_parser.add_argument("author", type=str)
book_parser.add_argument("book_id", type=int)

user_parser = reqparse.RequestParser()
user_parser.add_argument("name", type=str)
user_parser.add_argument("book_id", type=int)
user_parser.add_argument("is_visible", type=bool)

lib_parser = reqparse.RequestParser()
lib_parser.add_argument("name", type=str)
