from urllib import response
from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required,get_jwt
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from tables import UserModel
from db import db
from schemas import UserSchema, LoginSchema
from services.logout import logout_logic
from services.user import *

blp = Blueprint("Users", __name__, description="Operations on users")

# Business Logic Functions

def check_user_role():
    """Check if the JWT contains the 'user' role."""
    claims = get_jwt()
    if claims.get("role") != "user":
        abort(403, message="Access forbidden: User role required.")



# API Routes
@blp.route("/api/users")
class UserList(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """Create a new user and return the created user with tokens."""
        return create_user_logic(user_data)

    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self):
        """Get the current user using the token."""
        check_user_role()  # Ensure only users can access this
        user_id = get_jwt_identity()
        return get_user_logic(user_id)

    @jwt_required()
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def put(self, user_data):
        """Replace the current user (PUT, idempotent)."""
        check_user_role()
        user_id = get_jwt_identity()
        return update_user_logic(user_id, user_data)

    @jwt_required()
    @blp.arguments(UserSchema(partial=True))
    @blp.response(200, UserSchema)
    def patch(self, user_data):
        """Update the current user (PATCH, partial update)."""
        check_user_role()
        user_id = get_jwt_identity()
        return update_user_logic(user_id, user_data)

    @jwt_required()
    @blp.response(204)
    def delete(self):
        """Delete the current user."""
        check_user_role()
        user_id = get_jwt_identity()
        delete_user_logic(user_id)
        return "", 204

@blp.route("/api/users/all")
class AllUsers(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        """Get all users without any authentication."""
        users = get_all_users_logic()
        if not users:
            abort(404, message="No users found.")
        return users



@blp.route("/api/users/login")
class UserLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, user_data):
        """Log in a user and return access and refresh tokens."""
        return login_user_logic(user_data)


@blp.route("/api/users/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        """Log out the current user."""
        jti = get_jwt()["jti"]
        exp = get_jwt()["exp"]  # Token expiration timestamp
        return logout_logic(jti, exp)
