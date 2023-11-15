from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas.schemas import ItemSchema,ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
blp = Blueprint("Items", __name__, description="CRUD operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):

    @blp.response(200,ItemSchema)
    def get(self, item_id):
        item: ItemModel = ItemModel.query.get_or_404(item_id)
        print(item)
        sc = ItemSchema().dump(item)
        print(sc)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": f"We deleted item with: {item_id} id"}

    #ovde prvo ide data sa validacije a na kraju url parametar
    #prvo request pa onda response paziti na redosled
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self,item_data,item_id):
        item = ItemModel.query.get_or_404(item_id)
        if item:
            item.price = item_data.get('price')
            item.name = item_data.get('name')
        else:
            #ovo je neka greska u prepisivanju
            #moje zapazanje je ako nema taj id u bazi
            #bacice 404 !!!
            item = ItemModel(id=item_id,**item_data)
        # if item_id not in items:
        #     abort(400, message=f"We don't have item"
        #                        f" with that id {item_id}")

        db.session.add(item)
        db.session.commit()
        # if item_data.get('name'):
        #     item['name'] = item_data.get('name')
        # if item_data.get('price'):
        #     item['price'] = item_data.get('price')
        # if item_data.get('store_id'):
        #     item['store_id'] = item_data.get('store_id')

        return item


@blp.route('/items')
class ItemsList(MethodView):


    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self,request_data):
        #ovde je raspakovan dict moramo da ga zapakujemo i posaljemo dalje
        item = ItemModel(**request_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
        return item

