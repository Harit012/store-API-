import os
import secrets

from flask import Flask, jsonify 
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

from blocklist import BLOCKLIST
from db import db
import models

def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"]= True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config ["QLALCHEMY_TRACK_MODIFICATIONS"]= False
    db.init_app(app)

    migrate= Migrate(app,db)
    api = Api(app)
    
    app.config["JWT_SECRET_KEY"] = "185643595816751538281226579352349784952"
    jwt = JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_is_blocked(jwt_header , jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def jwt_revoked_callback(jwt_header, jwt_payload):
        return (jsonify({"description":"The token has been revoked","error":"token_revoked"}), 401,)
    
    @jwt.additional_claims_loader
    def additional_claims_loader(identity):
        if identity == 1:
            return {"is_admin":True}
        return {"is_admin":False}
    
    @jwt.expired_token_loader
    def expire_token_callback(jwt_header , jwt_payload):
        return (jsonify({"message":"Token expired", "error":"token_expired"}), 401,)
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (jsonify({"message":"signature varification failed","error":"invalid_token"}), 401,)

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (jsonify({"Description":"Request does not contain any access token",
                         "error":"authorization_required"}), 401,)
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header,jwt_payload):
        return jsonify({
            "description":"The token is not fresh",
            "error":"fresh_token_required"  
        })    
        
    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)
    
    return app

 


# http://localhost:5005/swagger-ui