from flask_smorest import Blueprint,  abort
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask.views import MethodView
from services.ambulance import *
from schemas import AmbulanceSchema

blp = Blueprint("Ambulance", __name__, description="Operations on ambulances")




@blp.route("/api/ambulances/<int:ambulance_id>")
class AmbulanceResource(MethodView):
    @jwt_required()
    @blp.response(200, AmbulanceSchema)
    def get(self, ambulance_id):
        """Get an ambulance by ID."""
        hospital_id = get_jwt_identity() 
        return get_ambulance_by_id(ambulance_id,hospital_id)

    @jwt_required()
    @blp.arguments(AmbulanceSchema)
    @blp.response(200, AmbulanceSchema)
    def put(self, ambulance_data, ambulance_id):
        """Update an ambulance's details."""
        hospital_id = get_jwt_identity()
        ambulance = get_ambulance_by_id(ambulance_id, hospital_id)
        if not ambulance:
            abort(404, description="Ambulance not found")

        # Validate the ambulance data
        validate_ambulance_data(ambulance_data, hospital_id)

        # Update ambulance with validated data
        updated_ambulance = update_ambulance(ambulance, ambulance_data)
        return updated_ambulance
    
    @jwt_required()
    @blp.arguments(AmbulanceSchema(partial=True))
    @blp.response(200, AmbulanceSchema)
    def patch(self, ambulance_data, ambulance_id):
        """Partially update an ambulance's details."""
        hospital_id = get_jwt_identity()
        ambulance = get_ambulance_by_id(ambulance_id, hospital_id)
        if not ambulance:
            abort(404, description="Ambulance not found")

        # Validate the ambulance data (same function as in PUT)
        validate_ambulance_data(ambulance_data, hospital_id)

        # Partially update ambulance with validated data
        updated_ambulance = update_ambulance(ambulance, ambulance_data)
        return updated_ambulance
    
    @jwt_required()
    @blp.response(204)
    def delete(self, ambulance_id):
        """Delete an ambulance if it's not in an active booking."""
        hospital_id = get_jwt_identity()
        ambulance = get_ambulance_by_id(ambulance_id, hospital_id)
        if not ambulance:
            abort(404, description="Ambulance not found")
        
        delete_ambulance(ambulance_id)
        return "", 204


@blp.route("/api/ambulances")
class AmbulanceListResource(MethodView):
    @blp.response(200, AmbulanceSchema(many=True))
    def get(self):
        """Get the list of all ambulances."""
        return get_all_ambulances()

    @jwt_required()
    @blp.arguments(AmbulanceSchema)
    @blp.response(201, AmbulanceSchema)
    def post(self, ambulance_data):
        """Create a new ambulance."""
        claims = get_jwt()
        if claims.get("role") != "hospital":
            abort(403, message="Permission denied")
        hospital_id = get_jwt_identity()
        ambulance_data['hospital_id'] = hospital_id
        return create_ambulance(ambulance_data)
