from flask import request
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

from project.tables import HospitalModel, ConnectRequestModel
from project.db import db
from project.schemas import HospitalSchema, LoginSchema
from project.services.logout import logout_logic
from project.services.helper import *
from project.services.ambulanceBooking import *

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

@blp.route("/api/hospitals/order-requests/all", methods=["GET"])
@jwt_required()
def find_order_requests():
    """Retrieve order requests for the logged-in user"""
    user_id = get_jwt_identity()
    check_hospital_role()
    return get_order_requests(user_id,"hospital")




@blp.route("/api/hospitals/booking-response/<int:booking_id>", methods=["POST"])
@jwt_required()
def handle_respond_to_booking(booking_id):
    """Step 1: Hospital responds with accepted/rejected."""
    hospital_id = get_jwt_identity()
    check_hospital_role()  # Ensure only hospitals can access this
    data = request.get_json()
    if not data:
        abort(400, message="No input data provided.")
    return respond_to_booking(data,booking_id,hospital_id)


@blp.route("/api/hospitals/assign-booking-details/<int:booking_request_id>", methods=["POST"])
@jwt_required()
@blp.arguments(BookingSchema)
def handle_assign_booking_details(data, booking_request_id):
    """Step 2: Hospital assigns driver & ambulance details, generates OTP."""
    hospital_id = get_jwt_identity()
    check_hospital_role()  # Ensure only hospitals can access this

    return assign_booking_details(data,booking_request_id,hospital_id)
    

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
  
@blp.route("/api/hospitals/nearby-drivers")
class NearbyHospitals(MethodView):
    @jwt_required()
    def get(self):
      """Get drivers within a 75 km range of the hospital’s address."""
      check_hospital_role()
      hospital_id = get_jwt_identity()
      result = get_nearby_items(hospital_id, 'driver' ,radius_km=75)
      return {"drivers": result, "status": 200, "message":"Drivers fetched successfully"}, 200
  
@blp.route("/api/hospitals/connect-driver/<int:driver_id>")
class connectToHospitals(MethodView):
    @jwt_required()
    def post(self, driver_id):
      """Connect to drivers."""
      check_hospital_role()
      hospital_id = get_jwt_identity()
      return send_connection_request("hospital",driver_id, hospital_id)
  

@blp.route("/api/hospitals/connection-requests")
class ConnectionRequests(MethodView):
    @jwt_required()
    def get(self):
      """Get connection requests."""
      check_hospital_role()
      hospital_id = get_jwt_identity()
      return get_connection_requests(HospitalModel, hospital_id)
  
  
@blp.route("/api/hospitals/respond-connection/<int:req_id>/<string:response>")
class AcceptConnection(MethodView):
    @jwt_required()
    def post(self, req_id, response):
        """Accept connection requests."""
        check_hospital_role()
        hospital_id = int(get_jwt_identity())
        connection_request = ConnectRequestModel.query.get(req_id)
        if not connection_request:
            abort(404, message="Connection request not found.")
        print(connection_request.hospital_id, hospital_id)
        if connection_request.hospital_id != hospital_id:
            abort(403, message="Access forbidden: Connection request not for this hospital.")
        if connection_request.sender_type != "driver":
            abort(403, message="Access forbidden: Connection request not from a driver.")
        return respond_to_connection_request(connection_request, response)

@blp.route("/api/hospitals/drivers")
class HospitalDrivers(MethodView):
    @jwt_required()
    def get(self):
        """Get drivers associated with the hospital."""
        check_hospital_role()
        hospital_id = get_jwt_identity()
        drivers = HospitalModel.query.get(hospital_id).drivers
        if not drivers:
            return abort(404, message="No drivers associated with the hospital.")
        drivers = [{**driver.to_dict() , "status":driver.status} for driver in drivers]
        return {"drivers":drivers, "status": 200, "message":"Drivers fetched successfully"}, 200

@blp.route("/api/hospitals/remove-driver/<int:driver_id>")
class RemoveDriver(MethodView):
    @jwt_required()
    def post(self, driver_id):
        """Remove driver from hospital."""
        check_hospital_role()
        hospital_id = get_jwt_identity()
        return remove_connection(hospital_id, driver_id)
    
    