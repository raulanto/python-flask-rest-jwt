from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, get_jwt,
)
from app import db, jwt
from app.auth import bp
from app.errors import error_response
from app.models import user_schema

blacklist = set()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]  # Obtiene el identificador único del token
    return jti in blacklist  # Verifica si el token está en la lista negra


@bp.route("/login", methods=["POST"])
def login():
    if not request.form:
        return error_response(400)

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return error_response(400, "Nombre de usuario o contraseña faltante.")

    user = db.get_user_by_name(username)

    if not user:
        return error_response(401, "Username invalido.")
    if user.password != password:
        return error_response(401, "Password invalido.")

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return jsonify(access_token=access_token, refresh_token=refresh_token, user=user_schema.dump(user))


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user = db.get_user(get_jwt_identity())
    if not user:
        return error_response(401, "Unknown user.")
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify(access_token=access_token, refresh_token=refresh_token)

# revoke current access token
@bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout_access_token():
    blacklist.add(get_jwt()["jti"])
    return jsonify(message="Successfully logged out.")


# revoke current refresh token
@bp.route("/logout2", methods=["DELETE"])
@jwt_required(refresh=True)
def logout_refresh_token():
    blacklist.add(get_jwt()["jti"])
    return jsonify(message="Successfully logged out.")


