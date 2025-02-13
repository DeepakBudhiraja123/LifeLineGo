from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import  jwt_required, get_jwt_identity, get_jwt
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from db import db
from schemas import AdminSchema, LoginSchema
from services.logout import logout_logic
from services.helper import *

blp = Blueprint("Admins", __name__, description="Operations on admins")


# Business Logic Functions

def check_admin_role():
    claims = get_jwt()
    if claims.get("role") != "admin":
        abort(403, message="Access forbidden: Admin role required.")


# API Routes
@blp.route("/api/admins")
class AdminList(MethodView):
    @blp.arguments(AdminSchema)
    def post(self, admin_data):
        """Create a new admin and return the created admin with tokens."""
        return create_logic(admin_data, AdminModel, "admin")

    @jwt_required()
    def get(self):
        """Get the current admin using the token."""
        check_admin_role()  # Ensure only admins can access this
        admin_id = get_jwt_identity()
        return get_item_by_id_logic(admin_id, AdminModel, "admin")

    @jwt_required()
    @blp.arguments(AdminSchema)
    def put(self, admin_data):
        """Replace the current admin """
        check_admin_role()  # Ensure only admins can access this
        admin_id = get_jwt_identity()
        return update_logic(admin_id, AdminModel, admin_data, "admin")

    @jwt_required()
    @blp.arguments(AdminSchema(partial=True))
    def patch(self, admin_data):
        """Update the current admin """
        check_admin_role()  # Ensure only admins can access this
        admin_id = get_jwt_identity()
        return update_logic(admin_id, AdminModel, admin_data, "admin")

    @jwt_required()
    def delete(self):
        """Delete the current admin."""
        check_admin_role()  # Ensure only admins can access this
        admin_id = get_jwt_identity()
        return delete_logic(admin_id, AdminModel, "admin")

@blp.route("/api/admins/all")
class AllAdmins(MethodView):
    def get(self):
        """Get all admins without any authentication."""
        return get_all_item_logic(AdminModel, "admin")

@blp.route("/api/admins/login")
class AdminLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, login_data):
        """Log in an admin and return access and refresh tokens."""
        return login_logic(login_data, AdminModel, "admin")



@blp.route("/api/admins/logout")
class AdminLogout(MethodView):
  @jwt_required()
  def post(self):
    """Log out the current admin."""
    jti = get_jwt()["jti"]
    exp = get_jwt()["exp"]  # Token expiration timestamp
    return logout_logic(jti, exp)
