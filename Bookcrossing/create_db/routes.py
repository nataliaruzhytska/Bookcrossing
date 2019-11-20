from flask_restful import Resource
from db import db


class CreateDB(Resource):

    def post(self):
        db.create_all()
        db.session.commit()
        return "ok"
