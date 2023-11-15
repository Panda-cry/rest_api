from marshmallow import Schema, fields, pre_dump, pre_load, post_dump, \
    post_load


# Ovo delimo jer ce Store schema da ima ovaj deo!!!
class ItemMixinSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class StoreMixinSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class TagMixinSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class TagSchema(TagMixinSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(StoreMixinSchema(), dump_only=True)
    items = fields.List(fields.Nested(ItemMixinSchema()), dump_only=True)


class ItemSchema(ItemMixinSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(StoreMixinSchema(), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema())
    tag = fields.Nested(TagSchema())


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchema(StoreMixinSchema):
    items = fields.List(fields.Nested(ItemMixinSchema()), dump_only=True)
    tags = fields.List(fields.Nested(TagMixinSchema()), dump_only=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
