from flask import request
from flask_jwt import jwt_required
from flask_restful import Resource
from marshmallow import fields
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt import current_identity

from whattodo.extensions import marshmallow
from whattodo.common.schema_utils import BaseAPISchema
from whattodo.extensions import db
from whattodo.models import Item


class CreateItemRequestSchema(marshmallow.Schema):
    description = fields.String(required=True)

    class Meta:
        fields = ('id', 'description')


class ItemSchema(BaseAPISchema):

    description = fields.String(required=True)
    user_id = fields.Number(required=True)

    class Meta:
        model = Item
        fields = ('id', 'description', 'user_id', 'created', 'last_updated')


class ItemDetail(Resource):
    schema = ItemSchema()

    @jwt_required()
    def get(self, item_id):
        schema = ItemSchema()
        item = Item.query.get_or_404(item_id)
        if item.user_id != current_identity.id:
            return {"error": "Invalid item"}, 400

        return schema.dump(item)

    @jwt_required()
    def put(self, item_id):
        item = Item.query.get_or_404(item_id)
        if item.user_id != current_identity.id:
            return {"error": "Invalid item"}, 400

        updated = self.schema.load(request.get_json(), instance=item, partial=True)
        db.session.commit()
        return self.schema.dump(updated), 202

    @jwt_required()
    def delete(self, item_id):
        item = Item.query.get_or_404(item_id)
        if item.user_id != current_identity.id:
            return {"error": "Invalid item"}, 400

        db.session.delete(item)
        db.session.commit()
        return '', 204


class ItemList(Resource):

    @jwt_required()
    def post(self):
        try:
            schema = ItemSchema()
            item = schema.load(request.get_json())
            db.session.add(item)
            db.session.commit()
            return schema.dump(item), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return str(e), 500

    @jwt_required()
    def get(self):
        print(current_identity)
        schema = ItemSchema(many=True)
        items = Item.query.filter_by(user_id=current_identity.id).all()
        results = schema.dump(items)
        return results
