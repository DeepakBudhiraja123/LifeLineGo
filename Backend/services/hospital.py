from flask_smorest import  abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from tables import HospitalModel
from db import db
from schemas import HospitalSchema



def get_all_hospitals_logic():
    """Fetch all hospitals from the database."""
    hospitals = HospitalModel.query.all()
    hospital_schema = HospitalSchema(many=True)  # Serialize a list of users
    return hospital_schema.dump(hospitals)


def update_hospital_logic(hospital_id, hospital_data):
    """Update hospital details (partial or full update)."""
    try:
        hospital = HospitalModel.query.get(hospital_id)
        if not hospital:
            return {"message": "hospital not found"}, 404
        if 'password' in hospital_data:
          if len(hospital_data["password"]) < 6:
                abort(400, message="Password must be at least 6 characters long.")
          hospital_data["password"] = pbkdf2_sha256.hash(hospital_data["password"])
        # Update fields
        hospital.name = hospital_data.get("name", hostel.name)
        hospital.email = hospital_data.get("email", driver.email)
        hospital.address.address = hospital_data.get("location", driver.address.address)
        hospital.address.latitude = hospital_data.get("latitude", driver.address.latitude)
        hospital.address.longitude = hospital_data.get("longitude", driver.address.longitude)
        hospital.state = hospital_data.get("state", hostel.state)
        hospital.city = hospital_data.get("city", hostel.city)
        hospital.password = hospital_data.get("state", hostel.state)
        
        
        db.session.commit()
        return hospital

    except IntegrityError as e:
        db.session.rollback()
        if "email" in str(e.orig):
            return {"message": "A driver with this email already exists"}, 400
        elif "name" in str(e.orig):
            return {"message": "A driver with this name already exists"}, 400
        elif "phone" in str(e.orig):
            return {"message": "A driver with this phone number already exists"}, 400
        else:
            return {"message": "An unexpected error occurred"}, 500


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


def get_hospital_by_id(hospital_id):
  hospital = HospitalModel.query.get(hospital_id)
  if not hospital:
    abort(404, message="Hospital not found.")
  return hospital

def login_hospital_logic(login_data):
  hospital = HpspitalModel.query.filter_by(name=login_data["name"]).first()
  
  if not hospital or not pbkdf2_sha256.verify(login_data["password"], hospital.password):
      abort(401, message="Invalid username or password.")
  
  access_token = create_access_token(identity=str(hospital.id), additional_claims={"role": "hospital"}, fresh=True)
  refresh_token = create_refresh_token(identity=str(hospital.id),additional_claims={"role": "hospital"})
  
  return {
      "message": "Login successful",
      "access_token": access_token,
      "refresh_token": refresh_token
  }