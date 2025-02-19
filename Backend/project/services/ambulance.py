from project.tables import AmbulanceModel, BookingModel
from project.db import db
from project.services.driver import *

from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import abort

def validate_ambulance_data(ambulance_data, hospital_id):
    """Validate ambulance data for hospital_id and driver_id."""

    # Validate driver_id if present
    if 'driver_id' in ambulance_data:
        driver_id = ambulance_data['driver_id']
        if not driver_exists(driver_id):
            abort(404, description="Driver not found")
        if not is_driver_associated_with_hospital(driver_id, hospital_id):
            abort(403, description="Driver is not associated with your hospital")
        if is_driver_in_active_booking(driver_id):
            abort(400, description="Driver is currently assigned to an active booking")



def is_ambulance_in_active_booking(ambulance_id):
    """Check if the ambulance is involved in any active booking."""
    return BookingModel.query.filter_by(ambulance_id=ambulance_id, status="active").first() is not None

def get_ambulance_by_id(ambulance_id, hospital_id):
    """Fetch an ambulance by ID and hospital_id or raise 404 if not found."""
    return AmbulanceModel.query.filter(
        AmbulanceModel.id == ambulance_id,
        AmbulanceModel.hospital_id == hospital_id
    ).first()


def get_all_ambulances():
    """Return all ambulances."""
    return AmbulanceModel.query.all()

def create_ambulance(ambulance_data):
    """Create a new ambulance and save it to the database."""
    ambulance = AmbulanceModel(**ambulance_data)
    try:
        db.session.add(ambulance)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(500, message=str(e))
    return ambulance

def update_ambulance(ambulance, ambulance_data):
    """Update the fields of an existing ambulance."""
    for key, value in ambulance_data.items():
        setattr(ambulance, key, value)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(500, message=str(e))
    return ambulance

def delete_ambulance(ambulance_id):
    """Delete an ambulance if it's not currently in an active booking."""
    ambulance = AmbulanceModel.query.get_or_404(ambulance_id)
    if is_ambulance_in_active_booking(ambulance_id):
        abort(400, message="Cannot delete an ambulance with an active booking")
    try:
        db.session.delete(ambulance)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(500, message=str(e))
    return {"message": "Ambulance deleted successfully"}
