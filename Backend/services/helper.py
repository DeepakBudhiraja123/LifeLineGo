from tables import  *
from db import db
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_smorest import abort
from math import radians, sin, cos, sqrt, atan2

# Business Logic Functions for CRUD operations

# Create a new entry and generate tokens   
def create_logic(data, Model, entity):
    """Business logic to create a new entry and generate tokens."""
    
    field = {}
    
    if 'address' in data:
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
        field = {"city_state": city_state,"street": address["street"],"latitude": address["latitude"],"longitude": address["longitude"]}
    
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

def get_nearby_hospitals(entity,Model,id, radius_km=75):
    """Get a list of hospitals within the specified radius (in km) from the entity's location."""
    
    item = Model.query.get(id).first().to_dict()
    address = item.get("address")
    
    if not item or not item.address:
        abort(404, message=f"{entity.capitalize()} or {entity} address not found.")
        
    entity_lat = address['latitude']
    entity_lon = address['longitude']
    
    if entity_lat is None or entity_lon is None:
        abort(400, message=f"{entity.capitalize()}'s address must have latitude and longitude.")
        
    
    # Convert radius to degrees (approximation for SQL filtering)
    radius_deg = radius_km / 111  # 1 degree ≈ 111 km

    # Filter using SQLAlchemy attributes, not Marshmallow schema
    nearby_hospitals = (
    db.session.query(HospitalModel)
    .filter(
        (HospitalModel.latitude >= entity_lat - radius_deg) &
        (HospitalModel.latitude <= entity_lat + radius_deg) &
        (HospitalModel.longitude >= entity_lon - radius_deg) &
        (HospitalModel.longitude <= entity_lon + radius_deg)
    )
    .all()
    )

    # Refine results using Haversine formula for more accurate filtering
    result = []
    for hospital in nearby_hospitals:
        distance = haversine(entity_lat, entity_lon, hospital.latitude, hospital.address.longitude)
        if distance <= radius_km:
            result.append({
                "hospital": hospital.to_dict(),
                "distance_km": round(distance, 2)
            })

    return {"nearby_hospitals": result, "message": " Nearby hospitals fetched successfully", "status": 200}, 200
