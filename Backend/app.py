from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from db import db  # Ensure db is the same instance used in your models
from controller.user import blp as UserBlp
from tables import *  # Make sure tables use db from db.py
from blocklist import BLOCKLIST

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "LifeLineGo API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "3e7fa6f5a6ba9143faca1463"
app.config["DEBUG"] = True

# Initialize SQLAlchemy
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()
    


# Initialize JWT
app.config['JWT_SECRET_KEY'] = "283762210800390904068900059553747386636"
jwt = JWTManager(app)

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == '1':  # Admin-specific logic
        return {"isAdmin": True}
    return {"isAdmin": False}

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "message": "The token has expired.",
        "error": "token_expired"
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "message": "Signature verification failed.",
        "error": "invalid_token"
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request doesn't contain an access token.",
        "error": "authorization_required"
    }), 401

# API Home Route
@app.route("/")
def home():
    return "Welcome to LifeLineGo API"

# Register Blueprints
api = Api(app)
api.register_blueprint(UserBlp)

if __name__ == "__main__":
    app.run()
