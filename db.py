from flask_sqlalchemy import  SQLAlchemy

db = SQLAlchemy()




items = {
    1: {
        "name": "Chair",
        "price": 17.99,
        "store_id" : 1
    },
    2: {
        "name": "Table",
        "price": 180.50,
        "store_id": 1
    }
}
stores = {
    1: {
        "name": "Store1",
        "items": items
    }
}

