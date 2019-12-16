from db import db

user_books = db.Table(
    'user_books',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.book_id'))
)


class Users(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    libraries = db.relationship('Library', backref='user')
    books = db.relationship('Book', secondary=user_books, backref=db.backref('users'))


class Book(db.Model):
    __tablename__ = "book"

    book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    author = db.Column(db.String)
    edition = db.Column(db.String)
    year_ed = db.Column(db.Integer)
    translator = db.Column(db.String)
    lib_id = db.Column(db.Integer, db.ForeignKey('library.lib_id'))
    is_visible = db.Column(db.Boolean)



class Library(db.Model):
    __tablename__ = "library"

    lib_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    books = db.relationship('Book', backref='library')
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

