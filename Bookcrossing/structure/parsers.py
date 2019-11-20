from flask_restful import reqparse

user_book_parser = reqparse.RequestParser()
user_book_parser.add_argument("name", type=str)


book_parser = reqparse.RequestParser()
book_parser.add_argument("name", type=str)

user_parser = reqparse.RequestParser()
user_parser.add_argument("name", type=str)

lib_parser = reqparse.RequestParser()
lib_parser.add_argument("name", type=str)
