from datetime import timedelta

from flask_restful import Api

from config import run_config
from flask import Flask

from create_db import CreateDB, create_db
from db import db, migrate
from routes.books import BookView, book_bp
from routes.library import LibraryView, lib_bp
from routes.user_books_view import user_book_bp, UserBookView
from routes.users import UserView, user_bp

app = Flask(__name__)
api = Api(app)

app.config.from_object(run_config())

db.init_app(app)
migrate.init_app(app, db)

app.permanent_session_lifetime = timedelta(minutes=20)

app.register_blueprint(create_db)
app.register_blueprint(user_bp)
app.register_blueprint(book_bp)
app.register_blueprint(lib_bp)
app.register_blueprint(user_book_bp)

api.add_resource(CreateDB, "/create_db")
api.add_resource(BookView, "/books", "/books/<book_id>")
api.add_resource(UserView, "/users", "/users/<user_id>")
api.add_resource(LibraryView, "/library", "/library/<lib_id>")
api.add_resource(UserBookView, "/user_books")


if __name__ == '__main__':
    app.run()
