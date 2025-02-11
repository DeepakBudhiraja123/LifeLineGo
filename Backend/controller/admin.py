from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import  jwt_required, get_jwt_identity, get_jwt
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from db import db
from schemas import AdminSchema, LoginSchema, HospitalSchema
from services.logout import logout_logic
from services.admin import *

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
        return create_admin_logic(admin_data)

    @jwt_required()
    @blp.response(200, AdminSchema)
    def get(self):
        """Get the current admin using the token."""
        check_admin_role()  # Ensure only admins can access this
        admin_id = get_jwt_identity()
        return get_admin_logic(admin_id)

    @jwt_required()
    @blp.arguments(AdminSchema)
    @blp.response(200, AdminSchema)
    def put(self, admin_data):
        """Replace the current admin (PUT, idempotent)."""
        check_admin_role()  # Ensure only admins can access this
        admin_id = get_jwt_identity()
        return update_admin_logic(admin_id, admin_data)

    @jwt_required()
    @blp.arguments(AdminSchema(partial=True))
    @blp.response(200, AdminSchema)
    def patch(self, admin_data):
        """Update the current admin (PATCH, partial update)."""
        check_admin_role()  # Ensure only admins can access this
        admin_id = get_jwt_identity()
        return update_admin_logic(admin_id, admin_data)

    @jwt_required()
    @blp.response(204)
    def delete(self):
        """Delete the current admin."""
        check_admin_role()  # Ensure only admins can access this
        admin_id = get_jwt_identity()
        delete_admin_logic(admin_id)
        return "", 204

@blp.route("/api/admins/all")
class AllAdmins(MethodView):
    @blp.response(200, AdminSchema(many=True))
    def get(self):
        """Get all admins without any authentication."""
        admins = get_all_admins_logic()
        if not admins:
            abort(404, message="No admins found.")
        return admins

@blp.route("/api/admins/hospitals")
class HospitalCreate(MethodView):
    @jwt_required()
    @blp.arguments(HospitalSchema)
    def post(self, hospital_data):
        """Create a new hospital (Admin-only)."""
        check_admin_role()  # Ensure only admins can access this
        admin_id = get_jwt_identity()
        hospital_data["admin_id"] = admin_id
        hospital_data["address"] =hospital_data.pop("location")
        return create_hospital_logic(hospital_data)

@blp.route("/api/admins/login")
class AdminLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, login_data):
        """Log in an admin and return access and refresh tokens."""
        return login_admin_logic(login_data)



@blp.route("/api/admins/logout")
class AdminLogout(MethodView):
  @jwt_required()
  def post(self):
    """Log out the current admin."""
    jti = get_jwt()["jti"]
    exp = get_jwt()["exp"]  # Token expiration timestamp
    return logout_logic(jti, exp)
