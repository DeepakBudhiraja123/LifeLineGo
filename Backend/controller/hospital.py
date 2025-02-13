from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from tables import HospitalModel
from db import db
from schemas import HospitalSchema, LoginSchema
from services.logout import logout_logic
from services.helper import *

blp = Blueprint("Hospitals", __name__, description="Operations on hospitals")


# Business Logic Functions

def check_hospital_role():
    """Check if the JWT contains the 'hospital' role."""
    claims = get_jwt()
    if claims.get("role") != "hospital":
        abort(403, message="Access forbidden: Hospital role required.")


# API Routes
@blp.route("/api/hospitals")
class HospitalList(MethodView):

    @jwt_required()
    def get(self):
        """Get the current hospital using the token."""
        check_hospital_role()
        hospital_id = get_jwt_identity()
        return get_item_by_id_logic(hospital_id, HospitalModel, "hospital")
    
    @blp.arguments(HospitalSchema)
    def post(self, hospital_data):
        """Create a new hospital (Admin-only)."""
        return create_logic(hospital_data, HospitalModel, "hospital")

    @jwt_required()
    @blp.arguments(HospitalSchema)
    def put(self, hospital_data):
        """Fully update the current hospital."""
        check_hospital_role()
        hospital_id = get_jwt_identity()
        return update_logic(hospital_id, HospitalModel, hospital_data, "hospital")

    @jwt_required()
    @blp.arguments(HospitalSchema(partial=True))
    def patch(self, hospital_data):
        """Partially update the current hospital."""
        check_hospital_role()
        hospital_id = get_jwt_identity()
        return update_logic(hospital_id, HospitalModel, hospital_data, "hospital")

    @jwt_required()
    def delete(self):
        """Delete the current hospital."""
        check_hospital_role()
        hospital_id = get_jwt_identity()
        return delete_logic(hospital_id, HospitalModel, "hospital")


@blp.route("/api/hospitals/all")
class AllUsers(MethodView):
    def get(self):
        """Get all hospitals without any authentication."""
        return get_all_item_logic(HospitalModel, "hospitals")


@blp.route("/api/hospitals/login")
class HospitalLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, login_data):
        """Log in a hospital and return access and refresh tokens."""
        return login_logic(login_data, HospitalModel, "hospital")


@blp.route("/api/hospitals/logout")
class HospitalLogout(MethodView):
  @jwt_required()
  def post(self):
      """Log out the current hospital."""
      jti = get_jwt()["jti"]
      exp = get_jwt()["exp"]  # Token expiration timestamp
      return logout_logic(jti, exp)
