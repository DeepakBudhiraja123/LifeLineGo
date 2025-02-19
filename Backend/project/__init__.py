from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

import os
from dotenv import load_dotenv

from .db import db  # Ensure db is the same instance used in your models

from .mail_config import mail
from .scheduler import scheduler
from .celery_config import make_celery

from .controller.user import blp as UserBlp
from .controller.admin import blp as AdminBlp
from .controller.hospital import blp as HospitalBlp
from .controller.driver import blp as DriverBlp

from .tables import *  # Make sure tables use db from db.py

from .services.logout import is_token_revoked

from datetime import datetime

def create_app():
    load_dotenv()  # Load environment variables from .env file

    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "LifeLineGo API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["DEBUG"] = True

    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")  # Use an App Password if using Gmail
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

    app.config["CELERY_CONFIG"]={
     'broker_url': 'redis://localhost:6379/0',  # Broker (Redis or RabbitMQ)
     'result_backend': 'redis://localhost:6379/0'
     }

    # Initialize SQLAlchemy
    db.init_app(app)

    mail.init_app(app)
    print("Mail object:", mail)
    print("Mail instance initialized successfully!")

    celery = make_celery(app)

    # Initialize JWT
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)
    
    from flask import jsonify
    from werkzeug.exceptions import HTTPException
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Customize Flask error responses"""
        response = e.get_response()
        response.data = jsonify({
            "code": e.code,
            "status": e.name,
            "message": e.description if isinstance(e.description, str) else e.description.get("message"),
            "old_booking": e.description.get("old_booking") if isinstance(e.description, dict) else None
        }).data
        response.content_type = "application/json"
        return response


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
        with app.app_context():
            print("called")
            now = datetime.utcnow()
            expired_tokens = TokenBlocklist.query.filter(TokenBlocklist.expires_at < now).all()
            if expired_tokens:
                print(f"Cleaning up {len(expired_tokens)} expired tokens...")
                for token in expired_tokens:
                    db.session.delete(token)
                db.session.commit()
            else:
                print("No expired tokens to clean up.")

    # Register Blueprints
    api = Api(app)
    api.register_blueprint(UserBlp)
    api.register_blueprint(AdminBlp)
    api.register_blueprint(HospitalBlp)
    api.register_blueprint(DriverBlp)

    
    
    # from celery.result import AsyncResult

    # @app.get("/result/<id>")
    # def task_result(id: str) -> dict[str, object]:
    #     result = AsyncResult(id)
    #     return {
    #         "ready": result.ready(),
    #         "successful": result.successful(),
    #         "value": result.result if result.ready() else None,
    #     }

    # Create tables if they don't exist
    with app.app_context():
        print("Here")
        print("Database URI:", os.getenv("SQLALCHEMY_DATABASE_URI"))
        db.create_all()
        scheduler.add_job(func=cleanup_expired_tokens, trigger="interval", hours=6)
        print("Scheduled Jobs after adding auto-reject:", scheduler.get_jobs())  # ✅ Print after scheduling
        

    return app, celery
