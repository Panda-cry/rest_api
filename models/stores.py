from  db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True,nullable=False)
    #Po meni cascade je ok za neke slucajeve ali nije ok
    #da brisemo sve sto je bilo povezano sa tim Store!!!
    items = db.relationship("ItemModel",back_populates="store",lazy="dynamic",cascade="all, delete")