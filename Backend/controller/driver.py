from flask import request, jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
)

from passlib.hash import pbkdf2_sha256

from services.driver import *
from services.logout import logout_logic
from services.helper import *

from tables import DriverModel
from schemas import DriverSchema, LoginSchema
from db import db

blp = Blueprint("Drivers", __name__, description="Operations on drivers")

def check_driver_role():
    """Check if the JWT contains the 'hospital' role."""
    claims = get_jwt()
    if claims.get("role") != "driver":
        abort(403, message="Access forbidden: Driver role required.")



@blp.route("/api/drivers")
class DriverList(MethodView):
    @blp.arguments(DriverSchema)
    def post(self, driver_data):
      """Create a new driver and return the created driver with tokens."""
      return create_logic(driver_data, DriverModel, "driver")

    @jwt_required()
    def get(self):
        """Get the current driver's details using the token."""
        check_driver_role()
        driver_id = get_jwt_identity()
        return get_item_by_id_logic(driver_id, DriverModel, "driver")
      
    @jwt_required()
    @blp.arguments(DriverSchema)
    def put(self, driver_data):
        """Update the current driver (PUT, partial update)."""
        check_driver_role()
        driver_id = get_jwt_identity()
        return update_logic(driver_id, DriverModel, driver_data, "driver")

    @jwt_required()
    @blp.arguments(DriverSchema(partial=True))
    def patch(self, driver_data):
        """Update the current driver (PATCH, partial update)."""
        check_driver_role()
        driver_id = get_jwt_identity()
        return update_logic(driver_id, DriverModel, driver_data, "driver")

    @jwt_required()
    def delete(self):
        """Delete the current driver if not in an active booking."""
        driver_id = get_jwt_identity()
        
        return delete_logic(driver_id, DriverModel, "driver")


@blp.route("/api/drivers/all")
class AllDrivers(MethodView):
  def get(self):
    return get_all_item_logic(DriverModel, "driver")

@blp.route("/api/drivers/login")
class DriverLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, login_data):
      """Log in a driver and return access and refresh tokens."""
      return login_logic(login_data, DriverModel, "driver")


@blp.route("/api/drivers/logout")
class DriverLogout(MethodView):
    @jwt_required()
    def post(self):
        """Log out the current driver."""
        jti = get_jwt()["jti"]
        exp = get_jwt()["exp"]  # Token expiration timestamp
        return logout_logic(jti, exp)


@blp.route("/api/drivers/nearby-hospitals")
class NearbyHospitals(MethodView):
    @jwt_required()
    def get(self):
      """Get hospitals within a 75 km range of the driver’s address."""
      driver_id = get_jwt_identity()
      return get_nearby_hospitals("driver", DriverModel, driver_id, radius_km=75)