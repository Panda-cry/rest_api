from flask import Flask
from flask_smorest import Api
from resources_item import blp as ItemBlueprint
from resources_store import blp as StoreBlueprint
from db import db
import models


#ova fja bi trebalo da se poziva pre svega
#namena da se sve lepo setuje i da se kaznije mozda prebaci
#na 2 verzije jedna za produkciju 2 za unapredjivanje aplikacije!!!
#ja sam ovde bazu bacio na docker POSTGRES je baza !!!
def create_app():
    app = Flask(__name__)
    app.config["PROPAGETE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] ="postgresql://eclecticiq:test@localhost:5432/test"
    app.config[
        'SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Ovo se često postavlja na False da bi se izbegli upozorenja

    db.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app

app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5002)
