from flask import request
from flask_jwt import jwt_required
from flask_restful import Resource
from marshmallow import fields, Schema
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt import current_identity

from whattodo.common.schema_utils import BaseAPISchema
from whattodo.extensions import db
from whattodo.models import Item


class CreateItemRequestSchema(Schema):
    description = fields.Str()


class ItemSchema(BaseAPISchema):
    description = fields.String(required=True)
    user_id = fields.Number(required=True)

    class Meta:
        model = Item


class ItemDetail(Resource):
    schema = ItemSchema()

    @jwt_required()
    def get(self, item_id):
        """Get an item by ID"""

        schema = ItemSchema()
        item = Item.query.get_or_404(item_id)
        if item.user_id != current_identity.id:
            return {"error": "Invalid item"}, 400

        return schema.dump(item)

    @jwt_required()
    def put(self, item_id):
        """Update an item"""

        item = Item.query.get_or_404(item_id)
        if item.user_id != current_identity.id:
            return {"error": "Invalid item"}, 400

        updated = self.schema.load(request.get_json(), instance=item, partial=True)
        db.session.commit()
        return self.schema.dump(updated), 202

    @jwt_required()
    def delete(self, item_id):
        """Delete an item by ID"""

        item = Item.query.get_or_404(item_id)
        if item.user_id != current_identity.id:
            return {"error": "Invalid item"}, 400

        db.session.delete(item)
        db.session.commit()
        return '', 204


class ItemList(Resource):
    @jwt_required()
    def post(self):
        """Create an item"""

        try:
            # Parse the request object and add user_id from token context
            request_schema = CreateItemRequestSchema()
            parsed_request_dict = request_schema.load(request.get_json()).data
            parsed_request_dict['user_id'] = current_identity.id

            # Convert to DB object and persist
            db_schema = ItemSchema()
            db_item = db_schema.load(parsed_request_dict)
            db.session.add(db_item)
            db.session.commit()
            return db_schema.dump(db_item), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return str(e), 500

    @jwt_required()
    def get(self):
        """Get all items for a user"""

        print(current_identity)
        schema = ItemSchema(many=True)
        items = Item.query.filter_by(user_id=current_identity.id).all()
        results = schema.dump(items)
        return results
