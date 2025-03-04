from flask import jsonify, request, url_for
from flask_jwt_extended import jwt_required,get_jwt_identity
from app import db
from app.api import bp
from app.models import ship_schema
from app.errors import error_response
from marshmallow import ValidationError


@bp.route("/ships", methods=["GET"])
@jwt_required()
def get_ships():
    ships = db.all_ships()
    return jsonify(ship_schema.dump(ships, many=True))


@bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@bp.route("/ships/<int:id>", methods=["GET"])
def get_ship(id):
    ship = db.get_ship(id)
    if ship is None:
        return error_response(404)
    return jsonify(ship_schema.dump(ship))


@bp.route("/ships/crear/", methods=["POST"])
@jwt_required(refresh=True)
def create_ship():
    try:
        ship = ship_schema.loads(request.data)
    except ValidationError as err:
        return error_response(400, err.messages)
    ship = db.add_ship(ship)
    if ship is None:
        return error_response(400)
    response = jsonify(ship_schema.dump(ship))
    response.status_code = 201
    response.headers["Location"] = url_for("api.get_ship", id=ship.id)
    return response


@bp.route("/ships/actualizar/<int:id>", methods=["PUT"])
@jwt_required(refresh=True)
def update_ship(id):
    try:
        ship = ship_schema.loads(request.data)
    except ValidationError as err:
        return error_response(400, err.messages)
    if db.get_ship(id) is None:
        return error_response(404)
    # "id" in request data is optional
    if ship.id == 0:
        ship.id = id
    # if "id" was provided in request data then it has to match the resource id
    if ship.id != id:
        return error_response(400, "Request data id has to match resource id.")
    if not db.update_ship(ship):
        return error_response(400)
    response = jsonify(ship_schema.dump(ship))
    return response


@bp.route("/ships/delete/<int:id>", methods=["DELETE"])
@jwt_required(refresh=True)
def delete_ship(id):
    if db.get_ship(id) is None:
        return error_response(404)
    if db.delete_ship(id) is False:
        return error_response(400)
    return "", 204
