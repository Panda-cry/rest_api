import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas.item_schema import ItemSchema, ItemUpdateSchema

from db import items,stores

blp = Blueprint("Items", __name__, description="CRUD operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):

    @blp.response(200,ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found")

    def delete(self, item_id):
        if item_id not in items:
            abort(400, message=f"We don't have item"
                               f" with that id {item_id}")
        items.pop(item_id)

        return {"item_id": item_id}

    #ovde prvo ide data sa validacije a na kraju url parametar
    #prvo request pa onda response paziti na redosled
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self,item_data,item_id):
        if item_id not in items:
            abort(400, message=f"We don't have item"
                               f" with that id {item_id}")

        item = items[item_id]
        item |= item_data
        # if item_data.get('name'):
        #     item['name'] = item_data.get('name')
        # if item_data.get('price'):
        #     item['price'] = item_data.get('price')
        # if item_data.get('store_id'):
        #     item['store_id'] = item_data.get('store_id')

        items[item_id] = item

        return item


@blp.route('/items')
class ItemsList(MethodView):


    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return list(items.values())

    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self,request_data):

        if request_data.get('store_id') not in stores:
            abort(404, message="Store not found")

        for item in items.values():
            if (request_data.get('name') == item['name']
                    and request_data.get('store_id') == item['store_id']):
                abort(400, message="Item already exists")

        item_id = uuid.uuid4().hex
        item = {**request_data, "id": item_id}
        items[item_id] = item

        return item

