import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas.store_schema import StoreSchema

blp = Blueprint("stores", __name__, description="CRUD operations on store")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found")

    def delete(self, store_id):
        if store_id not in stores:
            abort(400, message="We don't have that store!!!")
        stores.pop(store_id)

        return {"store_id": store_id}


@blp.route("/store")
class StoreList(MethodView):

    def get(self):
        return {"stores": list(stores.values())}

    @blp.arguments(StoreSchema)
    def post(self, store_data):

        for store in stores.values():
            if store_data.get('name') == store.get('name'):
                abort(400, message="We contain that store!")

        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store
        return new_store, 201
