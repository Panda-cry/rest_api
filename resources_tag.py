import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from schemas.schemas import TagSchema, TagAndItemSchema
from models.stores import StoreModel
from models.items import ItemModel
from models.tag import TagModel
from db import db

blp = Blueprint("Tags", "tags", description="CRUD operations on tags")


@blp.route("/store/<int:store_id>/tag")
class TagStore(MethodView):

    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        # provera da li stvarno postoji taj store
        StoreModel.query.get_or_404(store_id)
        tag = TagModel.query.filter(TagModel.store_id == store_id,
                                    TagModel.name == tag_data.get(
                                        "name")).first()
        if tag:
            abort(400, message=f"Store with {store_id} already "
                               f"have that tag!!!")

        tag = TagModel(store_id=store_id, **tag_data)
        print(tag)
        try:
            db.session.add(tag)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="Something bad happened")
        return tag


@blp.route("/tag/<int:tag_id>")
class TagInfo(MethodView):

    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any items, then try again.",
        )


@blp.route("/item/<string:item_id>/tag/<int:tag_id>")
class TagItem(MethodView):

    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message="An error occurred while inserting the tag.")

        return tag

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message="An error occurred while inserting the tag.")

        return {"message": "Item removed from tag", "item": item, "tag": tag}
