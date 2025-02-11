from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

import os
from dotenv import load_dotenv

from db import db  # Ensure db is the same instance used in your models

from controller.user import blp as UserBlp
from controller.admin import blp as AdminBlp
from controller.hospital import blp as HospitalBlp
from controller.ambulance import blp as AmbulanceBlp

from tables import *  # Make sure tables use db from db.py

from services.logout import is_token_revoked

from apscheduler.schedulers.background import BackgroundScheduler

from datetime import datetime

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "LifeLineGo API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DEBUG"] = True

# Initialize SQLAlchemy
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()
    


# Initialize JWT
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == '1':  # Admin-specific logic
        return {"isAdmin": True}
    return {"isAdmin": False}

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return is_token_revoked(jwt_payload)

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
    
# Function to clean up expired tokens
def cleanup_expired_tokens():
    now = datetime.utcnow()
    expired_tokens = TokenBlocklist.query.filter(TokenBlocklist.expires_at < now).all()
    if expired_tokens:
        print(f"Cleaning up {len(expired_tokens)} expired tokens...")
        for token in expired_tokens:
            db.session.delete(token)
        db.session.commit()
    else:
        print("No expired tokens to clean up.")

# Scheduler setup
scheduler = BackgroundScheduler()

def start_scheduler():
    """Start the scheduler if it's not already running."""
    if scheduler.state == STATE_STOPPED:
        scheduler.start()
        print("Scheduler started.")
    else:
        print("Scheduler is already running.")


@app.teardown_appcontext
def shutdown_scheduler(exception=None):
    """Shutdown the scheduler when the app context ends."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        print("Scheduler shutdown.")
    

# API Home Route
@app.route("/")
def home():
    return "Welcome to LifeLineGo API"

# Register Blueprints
api = Api(app)
api.register_blueprint(UserBlp)
api.register_blueprint(AdminBlp)
api.register_blueprint(HospitalBlp)
api.register_blueprint(AmbulanceBlp)

if __name__ == "__main__":
    scheduler.add_job(func=cleanup_expired_tokens, trigger="interval", minutes=30)
    scheduler.start()
    app.run()

