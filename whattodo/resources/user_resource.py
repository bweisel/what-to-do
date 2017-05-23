from flask import request
from marshmallow import fields
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt import jwt_required
from whattodo.common.auth_utils import bcrypt

from whattodo.common.schema_utils import BaseAPISchema
from whattodo.extensions import db
from whattodo.models import User


class UserSchema(BaseAPISchema):

    email = fields.Email(required=True)
    password = fields.String(required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'created', 'last_updated')


class UserDetail(Resource):

    schema = UserSchema()
    summary_schema = UserSchema(only=('id', 'email', 'created', 'last_updated'))

    @jwt_required()
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        data = self.summary_schema.dump(user)
        return data

    @jwt_required()
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        updated = self.schema.load(request.get_json(), instance=user, partial=True)
        db.session.commit()
        return self.summary_schema.dump(updated)

    @jwt_required()
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "OK"}, 202


class UserList(Resource):
    @jwt_required()
    def get(self):
        schema = UserSchema(many=True, only=('id', 'email', 'created', 'last_updated'))
        users = User.query.all()
        results = schema.dump(users)
        return results

    def post(self):
        schema = UserSchema()
        summary_schema = UserSchema(only=('id', 'email', 'created', 'last_updated'))

        try:
            user = schema.load(request.get_json())
            hashed_password = bcrypt.generate_password_hash(user.password)
            user.password = hashed_password
            db.session.add(user)
            db.session.commit()
            return summary_schema.dump(user), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return str(e), 500
