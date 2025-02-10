from urllib import response
from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from tables import UserModel
from db import db
from schemas import UserSchema

blp = Blueprint("Users", __name__, description="Operations on users")

# Business Logic Functions


def get_all_users_logic():
    """Fetch all users from the database."""
    users = UserModel.query.all()
    user_schema = UserSchema(many=True)  # Serialize a list of users
    return user_schema.dump(users)


def create_user_logic(user_data):
    """Business logic to create a user."""
    if len(user_data["password"]) < 6:
        abort(400, message="Password must be at least 6 characters long.")
    
    hashed_password = pbkdf2_sha256.hash(user_data["password"])
    user_data["password"] = hashed_password
    user = UserModel(**user_data)
    
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        if "UNIQUE constraint failed: User.email" in str(e):
            abort(400, message="Email already exists.")
        elif "UNIQUE constraint failed: User.name" in str(e):
            abort(400, message="Name already exists.")
        else:
            abort(400, message="Integrity error occurred.")
    except SQLAlchemyError:
        db.session.rollback()
        abort(500, message="An error occurred while creating the user.")
    
    access_token = create_access_token(identity=str(user.id), additional_claims={"role": "user"}, fresh=True)
    refresh_token = create_refresh_token(identity=str(user.id))
    return {
        "user": UserSchema().dump(user),
        "access_token": access_token,
        "refresh_token": refresh_token
    }



def get_user_logic(user_id):
    """Business logic to get a user by ID."""
    user = UserModel.query.get(user_id)
    if not user:
        abort(404, message="User not found.")
    return user



def update_user_logic(user_id, user_data):
    """Business logic to update a user."""
    user = UserModel.query.get(user_id)
    if not user:
        abort(404, message="User not found.")
    
    for key, value in user_data.items():
        setattr(user, key, value)
    
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        abort(500, message="An error occurred while updating the user.")
    
    return user



def delete_user_logic(user_id):
    """Business logic to delete a user."""
    user = UserModel.query.get(user_id)
    if not user:
        abort(404, message="User not found.")
    
    try:
        db.session.delete(user)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        abort(500, message="An error occurred while deleting the user.")




# API Routes
@blp.route("/api/users")
class UserList(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        print("I'm called")
        """Create a new user and return the created user with tokens."""
        return create_user_logic(user_data)

    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self):
        """Get the current user using the token."""
        user_id = get_jwt_identity()
        return get_user_logic(user_id)

    @jwt_required()
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def put(self, user_data):
        """Replace the current user (PUT, idempotent)."""
        user_id = get_jwt_identity()
        return update_user_logic(user_id, user_data)

    @jwt_required()
    @blp.arguments(UserSchema(partial=True))
    @blp.response(200, UserSchema)
    def patch(self, user_data):
        """Update the current user (PATCH, partial update)."""
        user_id = get_jwt_identity()
        return update_user_logic(user_id, user_data)

    @jwt_required()
    @blp.response(204)
    def delete(self):
        """Delete the current user."""
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
