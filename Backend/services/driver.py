from tables import hospital_driver_association, DriverModel

def driver_exists(driver_id):
    """Check if the driver exists in the database."""
    return DriverModel.query.get(driver_id) is not None

def is_driver_associated_with_hospital(driver_id, hospital_id):
    """Check if the driver is associated with the given hospital."""
    return hospital_driver_association.query.filter_by(driver_id=driver_id, hospital_id=hospital_id).first() is not None

def is_driver_in_active_booking(driver_id):
    """Check if the driver is involved in any active booking."""
    return BookingModel.query.filter_by(driver_id=driver_id, status="active").first() is not None
