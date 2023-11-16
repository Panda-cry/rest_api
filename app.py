from flask import Flask, jsonify
from flask_smorest import Api
from resources_item import blp as ItemBlueprint
from resources_store import blp as StoreBlueprint
from resources_tag import blp as TagBlueprint
from resource_auth import blp as AuthBlueprint
from db import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import models
from blacklist import BLOCKLIST

# ova fja bi trebalo da se poziva pre svega
# namena da se sve lepo setuje i da se kaznije mozda prebaci
# na 2 verzije jedna za produkciju 2 za unapredjivanje aplikacije!!!
# ja sam ovde bazu bacio na docker POSTGRES je baza !!!


#alembic ako smo imali ranije bazu moramo da je izbrisemo
#da se ponovo krene sve !!! inace ce da se zali

pg_pass = "7OqRu1iHlVeLB7O8suzjZRl8MUxqGkeN"
internal_url = "postgres://test:7OqRu1iHlVeLB7O8suzjZRl8MUxqGkeN@dpg-clavig616hkc73816s70-a/test_pan1"
external_url = "postgres://test:7OqRu1iHlVeLB7O8suzjZRl8MUxqGkeN@dpg-clavig616hkc73816s70-a.frankfurt-postgres.render.com/test_pan1"
pg_command = "PGPASSWORD=7OqRu1iHlVeLB7O8suzjZRl8MUxqGkeN psql -h dpg-clavig616hkc73816s70-a.frankfurt-postgres.render.com -U test test_pan1"
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
    app.config[
        "SQLALCHEMY_DATABASE_URI"] = external_url
    app.config[
        'SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Ovo se često postavlja na False da bi se izbegli upozorenja
    app.config['JWT_SECRET_KEY'] = "rest_api"
    db.init_app(app)
    api = Api(app)
    migrate = Migrate(app,db)
    jwt = JWTManager(app)
    @jwt.token_in_blocklist_loader
    def check_if_toke_is_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload.get('jti') in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"Description" : "The token has been revoked",
                     "error": "token_revoked"}, 401)
        )

    # @jwt.additional_claims_loader
    # def add_claims_to_jwt(identity):
    #     if identity == 1:
    #         return {"is_admin": True}
    #     return {"is_admin": False}
    # We are using now migrate :D
    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(AuthBlueprint)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5002)
