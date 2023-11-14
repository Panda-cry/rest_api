from marshmallow import Schema, fields


# Ovo delimo jer ce Store schema da ima ovaj deo!!!
class ItemMixinSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class StoreMixinSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class ItemSchema(ItemMixinSchema):
    store_id = fields.Int(required=True,load_only=True)
    store = fields.Nested(StoreMixinSchema(),dump_only=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Str()


class StoreSchema(StoreMixinSchema):
    items = fields.Nested(ItemMixinSchema(),dump_only=True)