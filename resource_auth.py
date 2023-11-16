from flask.views import MethodView
from flask_smorest import Blueprint, abort
import bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_required, get_jwt, get_jwt_identity
from schemas.schemas import UserSchema
from models import UserModel
from db import db
from blacklist import BLOCKLIST
from sqlalchemy.exc import SQLAlchemyError
import redis
from  rq import Queue
from  task import send_user_registration_email


blp = Blueprint("Auth", "auth", "CRUD operations for JWT token")

# redis = redis.from_url("blabla")
# queue = Queue("email" , connection=redis)
# queue.enqueue(send_user_registration_email,"blbla email" , "blabla username")
# rq worker -u <insert your Redis url here> emails iz terminala treba da se odradi
# da imamo workera koji ce da salje emailove
#na kursu je to u dokeru se pravio iz terminala dokera
#ali mozda po meni bolje da se napravi skripta koja ce da pokrene worker i tjt
#malo mail da se osvezi treba da se doda neki html da to izgleda lepo
#isto na deploy mozda je bolje da se to radi preko skripte ali
#render.com moze da napravi jednog workera i tjt ceo kurs prodje
@blp.route("/user/<int:user_id>")
class UserView(MethodView):

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Something bad happened")
        return {"message": "User deleted."}, 200


@blp.route("/register")
class UserRegister(MethodView):

    @blp.arguments(UserSchema)
    def post(self, user_data):
        salt = bcrypt.gensalt()
        user = UserModel(username=user_data.get('username'),
                         password=bcrypt.hashpw(
                             user_data.get('password').encode('utf-8'),
                             salt).decode())
        try:
            db.session.add(user)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="Something bad happened")

        return {"message": "User created successfully."}, 201


@blp.route("/login")
class Login(MethodView):

    @blp.arguments(UserSchema)
    def post(self, login_data):
        user = UserModel.query.filter(
            UserModel.username == login_data.get('username')).first()

        if user and bcrypt.checkpw(login_data.get('password').encode('utf-8'),
                                   user.password.encode("utf-8")):
            # iz nekog razloga odavde je bolje da kreiram claims nego iz app
            # jer onda baca 422 error da je jwt lose enkodovan
            # svakako ce to negde u realnoj app da se setuje ovde
            # zavisi ako imamo neke role za nase usere admin/reader/writter itd
            refresh = create_refresh_token(identity=user.id)
            acces = access_token = (
                create_access_token(identity=user.id, fresh=True,
                                    additional_claims={
                                        "is_admin": False}))
            return {"access_token": acces, "refresh_token": refresh}

        abort(401, message="Invalid credantials")


@blp.route("/logout")
class Logout(MethodView):

    @jwt_required()
    def post(self):
        jti = get_jwt().get('jti')
        BLOCKLIST.add(jti)
        return {"message": "User logged out"}, 200


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200


# @jwt_required(fresh=True) kada treba da neka ruta ima obnovljen token

def admin_required():
    def wrapper(fn):
        def decorator(*args, **kwargs):

            claims = get_jwt()
            if claims["is_admin"]:
                return fn(*args, **kwargs)
            else:

                abort(403, message="Admins only!")

        return decorator

    return wrapper


@blp.route("/test")
class TryJWY(MethodView):

    @jwt_required()
    @admin_required()
    def get(self):
        return {"message": "We made it"}



