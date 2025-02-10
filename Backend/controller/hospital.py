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

blp = Blueprint("Hospitals", __name__, description="Operations on hospitals")


# Business Logic Functions

def check_hospital_role():
    """Check if the JWT contains the 'hospital' role."""
    claims = get_jwt()
    if claims.get("role") != "hospital":
        abort(403, message="Access forbidden: Hospital role required.")


def get_all_hospitals_logic():
    """Fetch all hospitals from the database."""
    hospitals = HospitalModel.query.all()
    hospital_schema = HospitalSchema(many=True)  # Serialize a list of users
    return hospital_schema.dump(hospitals)


def update_hospital_logic(hospital_id, hospital_data, partial=False):
    """Update hospital details (partial or full update)."""
    hospital = HospitalModel.query.get(hospital_id)
    if not hospital:
        abort(404, message="Hospital not found.")
    
    for key, value in hospital_data.items():
        if key == "admin_password":  # Hash the new password if it's being updated
            if len(value) < 6:
                abort(400, message="Password must be at least 6 characters long.")
            value = pbkdf2_sha256.hash(value)
        setattr(hospital, key, value)
    
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        abort(500, message="An error occurred while updating the hospital.")
    
    return hospital


def delete_hospital_logic(hospital_id):
    """Delete a hospital from the database."""
    hospital = HospitalModel.query.get(hospital_id)
    if not hospital:
        abort(404, message="Hospital not found.")
    
    try:
        db.session.delete(hospital)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        abort(500, message="An error occurred while deleting the hospital.")
    
    return {"message": "Hospital deleted successfully"}


# API Routes
@blp.route("/api/hospitals")
class HospitalList(MethodView):

    @jwt_required()
    @blp.response(200, HospitalSchema)
    def get(self):
        """Get the current hospital using the token."""
        check_hospital_role()
        hospital_id = get_jwt_identity()
        hospital = HospitalModel.query.get(hospital_id)
        if not hospital:
            abort(404, message="Hospital not found.")
        return hospital

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
        hospitals = get_all_hospitals_logic()
        if not hospitals:
            abort(404, message="No hospitals found.")
        return hospitals


@blp.route("/api/hospitals/login")
class HospitalLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, login_data):
        """Log in a hospital and return access and refresh tokens."""
        model = HospitalModel
        hospital = model.query.filter_by(name=login_data["name"]).first()
        
        if not hospital or not pbkdf2_sha256.verify(login_data["password"], hospital.password):
            abort(401, message="Invalid email or password.")
        
        access_token = create_access_token(identity=str(hospital.id), additional_claims={"role": "hospital"}, fresh=True)
        refresh_token = create_refresh_token(identity=str(hospital.id),additional_claims={"role": "hospital"})
        
        return {
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token
        }


@blp.route("/api/hospitals/logout")
class HospitalLogout(MethodView):
  @jwt_required()
  def post(self):
      """Log out the current hospital."""
      jti = get_jwt()["jti"]
      exp = get_jwt()["exp"]  # Token expiration timestamp
      return logout_logic(jti, exp)
