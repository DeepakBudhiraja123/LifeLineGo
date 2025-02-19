from project.tables import  *
from project.services.driver import is_driver_in_active_booking
from project.db import db

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_smorest import abort
from math import radians, sin, cos, sqrt, atan2

# Business Logic Functions for CRUD operations



# 
def manage_address_field(data):
    # Extract address data from hospital_data
    address = data.pop("address")

    # Create and save the address in the Address table
    city_state = CityStateModel.query.filter_by(
        postal_code=address["postal_code"]
    ).first()
    if not city_state:
        city_state = CityStateModel(
        city=address["city"],
        state=address["state"],
        postal_code=address["postal_code"]
    )
    field = {"city_state": city_state,"street": address["street"],"latitude":                               address["latitude"],"longitude": address["longitude"]}
    return field

# Create a new entry and generate tokens   
def create_logic(data, Model, entity):
    """Business logic to create a new entry and generate tokens."""
    
    field = {}
    
    if 'address' in data:
        # Extract address data from hospital_data
        field = manage_address_field(data)
    
    # Add the address_id to hospital_data and create the hospital
    if len(data["password"]) < 6:
        abort(400, message="Password must be at least 6 characters long.")
    data["password"] = pbkdf2_sha256.hash(data["password"])
    item = Model(**data, **field)
    
    try:
        db.session.add(item)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        if "email" in str(e.orig):
            abort(400, message=f"{entity} with this email already exists.")
        elif "name" in str(e.orig):
            abort(400, message=f"{entity} with this name already exists.")
        elif "phone" in str(e.orig):
            abort(400, message=f"{entity} with this phone number already exists.")
        else:
            abort(500, message=f"{e.orig}")
    except SQLAlchemyError as e:
        db.session.rollback()
        print("error",e)
        abort(500, message=f"An error occurred while creating the entity.")
    
    # Generate tokens
    access_token = create_access_token(identity=str(item.id), additional_claims={"role": f"{entity}"}, fresh=True)
    refresh_token = create_refresh_token(identity=str(item.id),additional_claims={"role": f"{entity}"})
    
    return {
        f"{entity}": item.to_dict(),
        "access_token": access_token,
        "refresh_token": refresh_token,
        "message": f"{entity.capitalize()} created successfully",
        "status": 201
    } , 201


# Fetch all items from the database

def get_all_item_logic(Model, entity):
    """Fetch all items from the database."""
    items = Model.query.all()
    return {f"{entity}s": [item.to_dict() for item in items], "message":f"all {entity}s fetched successfully", "status":200}, 200
  

# Fetch an item by ID

def get_item_by_id_logic(id, Model, entity):
    """Fetch an item by ID."""
    item = Model.query.get(id)
    if not item:
        return abort(404, message=f"{entity} not found.")
    return {f"{entity}": item.to_dict(), "message": f"{entity} fetched successfully", "status": 200}, 200
 
# Update an item & address

def update_address(data,item):
    item.street = data.get("street", item.street)
    item.latitude = data.get("latitude", item.latitude)
    item.longitude = data.get("longitude", item.longitude)
    
    # Update or create CityStateModel and assign it directly
    city_state = CityStateModel.query.filter_by(postal_code=data["postal_code"]).first()
    if not city_state:
        city_state = CityStateModel(
            city=data['city'],
            state=data['state'],
            postal_code=data["postal_code"]
        )
    item.city_state = city_state  # Pass the object directly, no need for flush
   

def update_logic(id, Model,data, entity):
    try:
        item = Model.query.get(id)
        if not item:
            return {f"message": "no {entity} found"}, 404
        if 'password' in data:
            if len(data["password"]) < 6:
                abort(400, message="Password must be at least 6 characters long.")
            data["password"] = pbkdf2_sha256.hash(data["password"])
        # Update fields
        item.name = data.get("name", item.name)
        item.email = data.get("email", item.email)
        item.phone = data.get("phone", item.phone)
        item.password = data.get("password", item.password)
        if 'address' in data:
            update_address(data['address'], item)
        
        db.session.commit()
        return {f"{entity}": item.to_dict(), "message": f"{entity.capitalize()} updated successfully", "status": 200} , 200

    except IntegrityError as e:
        db.session.rollback()
        if "email" in str(e.orig):
            return abort(400, message=f"A {entity} with this email already exists")
        elif "name" in str(e.orig):
            return abort(400, message=f"A {entity} with this name already exists")
        elif "phone" in str(e.orig):
            return abort(400, message=f"A {entity} with this phone number already exists")
        else:
            abort(500, message=f"An error occurred while updating the {entity}.")   
 
# Login a user

def login_logic(login_data, Model, entity):
    """Business logic to log in a user."""
    item = Model.query.filter_by(name=login_data["name"]).first()
    if not item or not pbkdf2_sha256.verify(login_data["password"], item.password):
        return abort(401, message="Invalid username or password.")
    
    access_token = create_access_token(identity=str(item.id), additional_claims={"role": f"{entity}"}, fresh=True)
    refresh_token = create_refresh_token(identity=str(item.id),additional_claims={"role": f"{entity}"})
    
    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "status": 200
    }, 200

# Delete an item

def delete_logic(id, Model, entity):
    """Delete an item."""
    item = Model.query.get(id)
    if not item:
        return abort(404, message=f"{entity} not found.")
    
    db.session.delete(item)
    db.session.commit()
    return {"message": f"{entity} deleted successfully", "status": 204}, 204

# Haversine formula for calculating distance

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points on the Earth in km."""
    R = 6371  # Earth's radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c



# Get nearby hospitals

def get_nearby_items(entity_id,item_name, radius_km=75):
    """Get a list of hospitals within the specified radius (in km) from the entity's location."""
    model = HospitalModel if item_name == "driver" else DriverModel
    entity = model.query.get(entity_id)
    
    item_ids = {item.id for item in entity.hospitals} if item_name == "hospital" else {item.id for item in entity.drivers}
    entity = entity.to_dict()
    address = entity['address']
    entity_name = "hsopital" if item_name == "driver" else "driver"
    if not entity or not address:
        abort(404, message=f"{entity_name.capitalize()} or {entity_name} address not found.")
        
    entity_lat = address['latitude']
    entity_lon = address['longitude']
    
    if entity_lat is None or entity_lon is None:
        abort(400, message=f"{entity_name.capitalize()}'s address must have latitude and longitude.")
    item_model = HospitalModel if item_name == "hospital" else DriverModel
    nearby_items = get_items_in_range(entity_lat, entity_lon,item_model,item_name, radius_km)[0].get(f"nearby_{item_name}s")
    
    # Add 'isConnected' flag for each hospital
    
    items_with_status = []
    for data in nearby_items:
        print(data)
        data["isConnected"] = data[f"{item_name}"]['id'] in item_ids
        items_with_status.append(data)
    
    return items_with_status
    
    


def get_items_in_range(entity_lat, entity_lon, item_model,item_name,radius_km=75):
    # Convert radius to degrees (approximation for SQL filtering)
    radius_deg = radius_km / 111  # 1 degree ≈ 111 km

    # Filter using SQLAlchemy attributes, not Marshmallow schema
    nearby_items = (
    db.session.query(item_model)
    .filter(
        (item_model.latitude >= entity_lat - radius_deg) &
        (item_model.latitude <= entity_lat + radius_deg) &
        (item_model.longitude >= entity_lon - radius_deg) &
        (item_model.longitude <= entity_lon + radius_deg)
    )
    .all()
    )

    # Refine results using Haversine formula for more accurate filtering
    result = []
    for item in nearby_items:
        distance = haversine(entity_lat, entity_lon, item.latitude, item.longitude)
        if distance <= radius_km:
            result.append({
                f"{item_name}": item.to_dict(),
                "distance_km": round(distance, 2)
            })
    if not result:
        return abort(404, message=f"No {item_name}s found within the specified range.")
    return {f"nearby_{item_name}s": result, "message": f" Nearby {item_name}s fetched successfully", "status": 200}, 200



def send_connection_request(sender_type, driver_id, hospital_id):
    """General function to send a connection request from driver or hospital."""
    if sender_type not in ["driver", "hospital"]:
        abort(400, message="Invalid sender type. Must be 'driver' or 'hospital'.")
    
    existing_request = ConnectRequestModel.query.filter_by(
        driver_id=driver_id, hospital_id=hospital_id, status="pending"
    ).first()
    
    if existing_request:
        abort(400, message="A pending request already exists.")

    new_request = ConnectRequestModel(
        driver_id=driver_id, 
        hospital_id=hospital_id, 
        sender_type=sender_type
    )
    db.session.add(new_request)
    db.session.commit()
    
    sender = "Driver" if sender_type == "driver" else "Hospital"
    return {"message": f"{sender} connection request sent successfully.", "status": 201, }, 201

def get_connection_requests(Model,item_id):
    item = Model.query.get(item_id)
    if not item:
        return abort(404, message=f"{Model} not found.")
    connection_requests = [connection_request for connection_request in item.connection_requests if connection_request.status == "pending"]
    if not connection_requests:
        return abort(404, message="No pending connection requests found.")
    return {"connection_requests": [request.to_dict() for request in connection_requests], "message": "Connection requests fetched successfully", "status": 200}, 200


def respond_to_connection_request(connection_request, response_status):
    """
    Respond to a connection request (accept or reject).
    
    Parameters:
    - request_id: The ID of the connection request.
    - response_status: 'accepted' or 'rejected'
    
    Returns:
    - A success message or an error if the request is not found or already responded to.
    """
    if response_status not in ["accepted", "rejected"]:
        abort(400, message="Invalid response status. Must be 'accepted' or 'rejected'.")
    
    if connection_request.status != "pending":
        abort(400, message="Connection request has already been responded to.")
    
    # Update the status
    connection_request.status = response_status
    if response_status == "accepted":
        driver = DriverModel.query.get(connection_request.driver_id)
        hospital = HospitalModel.query.get(connection_request.hospital_id)
        driver.hospitals.append(hospital)
    db.session.commit()
    
    return {"message": f"Connection request {response_status} successfully." , "status": 200}, 200


def remove_connection(hospital_id=None, driver_id=None):
    """
    Remove an existing connection between a hospital and a driver.
    
    Parameters:
    - hospital_id: ID of the hospital.
    - driver_id: ID of the driver.
    
    Returns:
    - A success message or an error if no connection exists.
    """
    if not hospital_id or not driver_id:
        abort(400, message="Both hospital_id and driver_id are required.")
    
    # Find the hospital and driver
    hospital = HospitalModel.query.get(hospital_id)
    driver = DriverModel.query.get(driver_id)
    
    if not hospital or not driver:
        abort(404, message="Hospital or Driver not found.")
    
    # Check if they are connected
    if driver not in hospital.drivers:
        abort(400, message="No connection exists between the hospital and driver.")
        
    if is_driver_in_active_booking(driver_id):
        abort(400, message="Driver is currently involved in an active booking.")
    
    # Remove the relationship
    hospital.drivers.remove(driver)
    db.session.commit()
    
    return {"message": "Connection removed successfully."},204

