from datetime import datetime
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError
from flask_smorest import abort
from db import db
from tables import UserModel
from schemas import UserSchema
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)


def login_user_logic(user_data):
    """Business logic to log in a user."""
    user = UserModel.query.filter_by(name=user_data["name"]).first()
    if not user or not pbkdf2_sha256.verify(user_data["password"], user.password):
        abort(401, message="Invalid username or password.")
    
    access_token = create_access_token(identity=str(user.id), additional_claims={"role": "user"}, fresh=True)
    refresh_token = create_refresh_token(identity=str(user.id),additional_claims={"role": "user"})
    
    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token
    }



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
    refresh_token = create_refresh_token(identity=str(user.id),additional_claims={"role": "user"})
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
        if key == "password":  # Check if we're updating the password
            if len(value) < 6:
                abort(400, message="Password must be at least 6 characters long.")
            value = pbkdf2_sha256.hash(value)  # Hash the new password
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

