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

from tables import DriverModel, ConnectRequestModel
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
      chck_driver_role()
      driver_id = get_jwt_identity()
      result = get_nearby_items(driver_id, 'hospital' ,radius_km=75)
      return {"hospitals": result, "status": 200, "message":"Hospitals fetched successfully"}, 200
  
  
@blp.route("/api/drivers/connect-hospital/<int:hospital_id>")
class connectToHospitals(MethodView):
    @jwt_required()
    def post(self, hospital_id):
      """Connect to hospitals."""
      check_driver_role()
      driver_id = get_jwt_identity()
      return send_connection_request("driver",driver_id, hospital_id)
  

@blp.route("/api/drivers/connection-requests")
class ConnectionRequests(MethodView):
    @jwt_required()
    def get(self):
      """Get connection requests."""
      check_driver_role()
      driver_id = get_jwt_identity()
      return get_connection_requests(DriverModel, driver_id)
  
@blp.route("/api/drivers/respond-connection/<int:req_id>/<string:response>")
class AcceptConnection(MethodView):
    @jwt_required()
    def post(self, req_id, response):
        """Accept connection requests."""
        check_driver_role()
        driver_id = int(get_jwt_identity())
        connection_request = ConnectRequestModel.query.get(req_id)
        if not connection_request:
            abort(404, message="Connection request not found.")
        if connection_request.driver_id != driver_id:
            abort(403, message="Access forbidden: Connection request not for this driver.")
        if connection_request.sender_type != "hospital":
            abort(403, message="Access forbidden: Connection request not from a hospital.")
        return respond_to_connection_request(connection_request, response)


@blp.route("/api/drivers/hospitals")
class HospitalDrivers(MethodView):
    @jwt_required()
    def get(self):
        """Get drivers associated with the hospital."""
        check_driver_role()
        driver_id = get_jwt_identity()
        hospitals = DriverModel.query.get(driver_id).hospitals
        if not hospitals:
            return abort(404, message="No hospitals associated with the driver.")
        hospitals = [hospital.to_dict() for hospital in hospitals]
        
        return {"hospitals":hospitals, "status": 200, "message":"Hospitals fetched successfully"}, 200
    
@blp.route("/api/drivers/remove-hospital/<int:hospital_id>")
class RemoveHospital(MethodView):
    @jwt_required()
    def delete(self, hospital_id):
        """Remove the hospital from the driver's associated hospitals."""
        check_driver_role()
        driver_id = get_jwt_identity()
        return remove_connection( hospital_id, driver_id)

     