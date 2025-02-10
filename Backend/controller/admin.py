from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from tables import AdminModel, HospitalModel, AddressModel
from db import db
from schemas import AdminSchema, LoginSchema, HospitalSchema
from blocklist import BLOCKLIST

blp = Blueprint("Admins", __name__, description="Operations on admins")


# Business Logic Functions

def check_admin_role():
    claims = get_jwt()
    if claims.get("role") != "admin":
        abort(403, message="Access forbidden: Admin role required.")


def create_hospital_logic(hospital_data):
    """Business logic to create a new hospital and generate tokens."""
    
    # Extract address data from hospital_data
    address_data = {
        "address": hospital_data.pop("address"),
        "latitude": hospital_data.pop("latitude"),
        "longitude": hospital_data.pop("longitude")
    }
    
    # Create and save the address in the Address table
    address = AddressModel(**address_data)
    try:
        db.session.add(address)
        db.session.flush()  # Use flush to get the address.id without committing
    except SQLAlchemyError:
        db.session.rollback()
        abort(500, message="An error occurred while creating the address.")
    
    # Add the address_id to hospital_data and create the hospital
    hospital_data["address_id"] = address.id
    hospital_data["password"] = pbkdf2_sha256.hash(hospital_data["password"])
    hospital = HospitalModel(**hospital_data)
    
    try:
        db.session.add(hospital)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, message="Hospital with this name or email already exists.")
    except SQLAlchemyError as e:
        db.session.rollback()
        print("error",e)
        abort(500, message="An error occurred while creating the hospital.")
    
    # Generate tokens
    access_token = create_access_token(identity=str(hospital.id), additional_claims={"role": "hospital"}, fresh=True)
    refresh_token = create_refresh_token(identity=str(hospital.id),additional_claims={"role": "hospital"})
    
    return {
        "hospital": HospitalSchema().dump(hospital),
        "access_token": access_token,
        "refresh_token": refresh_token
    }

def get_all_admins_logic():
    """Fetch all users from the database."""
    admins = AdminModel.query.all()
    admin_schema = AdminSchema(many=True)  # Serialize a list of users
    return admin_schema.dump(admins)


def create_admin_logic(admin_data):
    """Business logic to create an admin."""
    if len(admin_data["password"]) < 6:
        abort(400, message="Password must be at least 6 characters long.")
    
    hashed_password = pbkdf2_sha256.hash(admin_data["password"])
    admin_data["password"] = hashed_password
    admin = AdminModel(**admin_data)
    
    try:
        db.session.add(admin)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        if "UNIQUE constraint failed: admins.email" in str(e):
            abort(400, message="Email already exists.")
        elif "UNIQUE constraint failed: admins.name" in str(e):
            abort(400, message="Name already exists.")
        else:
            abort(400, message="Integrity error occurred.")
    except SQLAlchemyError:
        db.session.rollback()
        abort(500, message="An error occurred while creating the admin.")
    
    access_token = create_access_token(identity=str(admin.id), additional_claims={"role": "admin"}, fresh=True)
    refresh_token = create_refresh_token(identity=str(admin.id), additional_claims={"role": "admin"})
    return {
        "admin": AdminSchema().dump(admin),
        "access_token": access_token,
        "refresh_token": refresh_token
    }

def login_admin_logic(login_data):
    """Business logic to log in an admin."""
    admin = AdminModel.query.filter_by(name=login_data["name"]).first()
    if not admin or not pbkdf2_sha256.verify(login_data["password"], admin.password):
        abort(401, message="Invalid username or password.")
    
    access_token = create_access_token(identity=str(admin.id), additional_claims={"role": "admin"}, fresh=True)
    refresh_token = create_refresh_token(identity=str(admin.id),additional_claims={"role": "admin"})
    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token
    }

def logout_admin_logic(jti):
    """Business logic to log out an admin."""
    BLOCKLIST.add(jti)
    return {"message": "Logged out successfully"}

def get_admin_logic(admin_id):
    """Business logic to get an admin by ID."""
    admin = AdminModel.query.get(admin_id)
    if not admin:
        abort(404, message="Admin not found.")
    return admin

def update_admin_logic(admin_id, admin_data):
    """Business logic to update an admin."""
    admin = AdminModel.query.get(admin_id)
    if not admin:
        abort(404, message="Admin not found.")
    
    for key, value in admin_data.items():
        if key == "password":  # Hash the new password
            if len(value) < 6:
                abort(400, message="Password must be at least 6 characters long.")
            value = pbkdf2_sha256.hash(value)
        setattr(admin, key, value)
    
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        abort(500, message="An error occurred while updating the admin.")
    
    return admin

def delete_admin_logic(admin_id):
    """Business logic to delete an admin."""
    admin = AdminModel.query.get(admin_id)
    if not admin:
        abort(404, message="Admin not found.")
    
    try:
        db.session.delete(admin)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        abort(500, message="An error occurred while deleting the admin.")

# API Routes
@blp.route("/api/admins")
class AdminList(MethodView):
    @blp.arguments(AdminSchema)
    def post(self, admin_data):
        """Create a new admin and return the created admin with tokens."""
        return create_admin_logic(admin_data)

    @jwt_required()
    @blp.response(200, AdminSchema)
    def get(self):
        """Get the current admin using the token."""
        check_admin_role()  # Ensure only admins can access this
        admin_id = get_jwt_identity()
        return get_admin_logic(admin_id)

    @jwt_required()
    @blp.arguments(AdminSchema)
    @blp.response(200, AdminSchema)
    def put(self, admin_data):
        """Replace the current admin (PUT, idempotent)."""
        check_admin_role()  # Ensure only admins can access this
        admin_id = get_jwt_identity()
        return update_admin_logic(admin_id, admin_data)

    @jwt_required()
    @blp.arguments(AdminSchema(partial=True))
    @blp.response(200, AdminSchema)
    def patch(self, admin_data):
        """Update the current admin (PATCH, partial update)."""
        check_admin_role()  # Ensure only admins can access this
        admin_id = get_jwt_identity()
        return update_admin_logic(admin_id, admin_data)

    @jwt_required()
    @blp.response(204)
    def delete(self):
        """Delete the current admin."""
        check_admin_role()  # Ensure only admins can access this
        admin_id = get_jwt_identity()
        delete_admin_logic(admin_id)
        return "", 204

@blp.route("/api/admins/all")
class AllAdmins(MethodView):
    @blp.response(200, AdminSchema(many=True))
    def get(self):
        """Get all admins without any authentication."""
        admins = get_all_admins_logic()
        if not admins:
            abort(404, message="No admins found.")
        return admins

@blp.route("/api/admins/hospitals")
class HospitalCreate(MethodView):
    @jwt_required()
    @blp.arguments(HospitalSchema)
    def post(self, hospital_data):
        """Create a new hospital (Admin-only)."""
        check_admin_role()  # Ensure only admins can access this
        admin_id = get_jwt_identity()
        hospital_data["admin_id"] = admin_id
        hospital_data["address"] =hospital_data.pop("location")
        return create_hospital_logic(hospital_data)

@blp.route("/api/admins/login")
class AdminLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, login_data):
        """Log in an admin and return access and refresh tokens."""
        return login_admin_logic(login_data)

@blp.route("/api/admins/logout")
class AdminLogout(MethodView):
    @jwt_required()
    def post(self):
        """Log out the current admin."""
        jti = get_jwt()["jti"]
        return logout_admin_logic(jti)
