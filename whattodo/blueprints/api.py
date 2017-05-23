from flask import Blueprint, jsonify
from flask_restful import Api

from whattodo.common.exceptions import SchemaValidationError
from whattodo.resources import UserDetail, UserList
from whattodo.resources import ItemDetail, ItemList


api_bp = Blueprint('api', __name__, url_prefix='')
api = Api(api_bp)

api.add_resource(UserDetail, '/users/<int:user_id>')
api.add_resource(UserList, '/users')

api.add_resource(ItemDetail, '/items/<int:item_id>')
api.add_resource(ItemList, '/items')


@api_bp.errorhandler(SchemaValidationError)
def handle_invalid_schema(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
