from flask import jsonify, request, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.api import bp
from app.models import User, user_schema
from app.errors import error_response
from marshmallow import ValidationError




@bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify(user_schema.dump(users, many=True))



@bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if user is None:
        return error_response(404)
    return jsonify(user_schema.dump(user))


@bp.route("/users/crear/", methods=["POST"])
def create_user():
    try:
        user_data = user_schema.loads(request.data)
    except ValidationError as err:
        return error_response(400, err.messages)

    if User.query.filter_by(name=user_data["name"]).first():
        return error_response(400, "User already exists.")

    user = User(**user_data)  # Crea el objeto User con los datos

    db.session.add(user)
    db.session.commit()

    response = jsonify(user_schema.dump(user))
    response.status_code = 201
    response.headers["Location"] = url_for("api.get_user", id=user.id)
    return response


@bp.route("/users/actualizar/<int:id>", methods=["PUT"])
@jwt_required()
def update_user(id):
    if id != get_jwt_identity():
        return error_response(403)

    user = User.query.get(id)
    if user is None:
        return error_response(404)

    try:
        user_data = user_schema.loads(request.data)
    except ValidationError as err:
        return error_response(400, err.messages)

    user.name = user_data.get("name", user.name)
    user.email = user_data.get("email", user.email)
    user.roles = user_data.get("roles", user.roles)

    db.session.commit()  # Guarda los cambios en la BD

    return jsonify(user_schema.dump(user))


@bp.route("/users/delete/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    if id != get_jwt_identity():
        return error_response(403)

    user = User.query.get(id)
    if user is None:
        return error_response(404)

    db.session.delete(user)
    db.session.commit()

    return "", 204  # Código 204 significa "Sin contenido"
