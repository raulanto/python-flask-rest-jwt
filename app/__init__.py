from flask import Flask
from config import Config
from app.db import Database
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

db = Database()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "MyApp"})
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app

from app import models