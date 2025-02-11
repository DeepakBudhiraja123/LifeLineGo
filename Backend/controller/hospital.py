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
from services.hospital import *

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
    @blp.response(200, HospitalSchema)
    def get(self):
        """Get the current hospital using the token."""
        check_hospital_role()
        hospital_id = get_jwt_identity()
        return get_hospital_by_id(hospital_id)

    @jwt_required()
    @blp.arguments(HospitalSchema)
    @blp.response(200, HospitalSchema)
    def put(self, hospital_data):
        """Fully update the current hospital."""
        check_hospital_role()
        hospital_id = get_jwt_identity()
        return update_hospital_logic(hospital_id, hospital_data)

    @jwt_required()
    @blp.arguments(HospitalSchema(partial=True))
    @blp.response(200, HospitalSchema)
    def patch(self, hospital_data):
        """Partially update the current hospital."""
        check_hospital_role()
        hospital_id = get_jwt_identity()
        return update_hospital_logic(hospital_id, hospital_data, partial=True)

    @jwt_required()
    @blp.response(204)
    def delete(self):
        """Delete the current hospital."""
        check_hospital_role()
        hospital_id = get_jwt_identity()
        delete_hospital_logic(hospital_id)
        return "", 204


@blp.route("/api/hospitals/all")
class AllUsers(MethodView):
    @blp.response(200, HospitalSchema(many=True))
    def get(self):
        """Get all hospitals without any authentication."""
        return get_all_hospitals_logic()


@blp.route("/api/hospitals/login")
class HospitalLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, login_data):
        """Log in a hospital and return access and refresh tokens."""
        return login_hospital_logic


@blp.route("/api/hospitals/logout")
class HospitalLogout(MethodView):
  @jwt_required()
  def post(self):
      """Log out the current hospital."""
      jti = get_jwt()["jti"]
      exp = get_jwt()["exp"]  # Token expiration timestamp
      return logout_logic(jti, exp)
