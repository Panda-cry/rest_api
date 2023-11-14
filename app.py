import uuid

from flask import Flask, request
from flask_smorest import abort, Api
from resources_item import blp as ItemBlueprint
from resources_store import blp as StoreBlueprint


app = Flask(__name__)
app.config["PROPAGETE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1.0"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


api = Api(app)
api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)

@app.get('/try_docker')
def try_docker():
    return "Hello from docker"

if __name__ == "__main__":
    app.run(debug=True,port=5002)
