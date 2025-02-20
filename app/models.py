#app/models.py

from marshmallow import Schema, fields, post_load, validate
from app import db

class Ship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    affiliation = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    crew = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    manufacturer = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(120), nullable=False)
    ship_class = db.Column(db.String(120), nullable=False)
    roles = db.Column(db.Text, nullable=False)  # Se almacenará como JSON en una cadena

    def __repr__(self):
        return f"<Ship({self.model})>"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    roles = db.Column(db.Text, nullable=False)  # Se almacenará como JSON en una cadena
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User({self.username})>"


class ShipSchema(Schema):
    id = fields.Integer(validate=validate.Range(min=1), missing=0)
    affiliation = fields.Str(required=True)
    category = fields.Str(required=True)
    crew = fields.Integer(required=True, validate=validate.Range(min=1))
    length = fields.Integer(required=True, validate=validate.Range(min=1))
    manufacturer = fields.Str(required=True)
    model = fields.Str(required=True)
    ship_class = fields.Str(required=True)
    roles = fields.List(fields.Str(), required=True)

    @post_load
    def make_ship(self, data, **kwargs):
        return Ship(**data)



class UserSchema(Schema):
    id = fields.Integer(validate=validate.Range(min=1), missing=0)
    username = fields.Str(required=True, validate=validate.Length(min=2))
    password = fields.Str(required=True, validate=validate.Length(min=4), load_only=True)
    roles = fields.List(fields.Str(), required=True)
    email = fields.Email(required=True)
    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

user_schema = UserSchema()
ship_schema = ShipSchema()
