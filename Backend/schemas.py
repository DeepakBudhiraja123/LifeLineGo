from marshmallow import Schema, fields

# ===================== User Schemas ===================== #
class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)
    phone = fields.Str(required=True)
    
class PlainAddressSchema(Schema):
    id = fields.Int(dump_only=True)
    address = fields.Str(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    
class PlainHospitalSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)
    location = fields.Str(required=True,load_only=True)
    latitude = fields.Float(required=True,load_only=True)
    longitude = fields.Float(required=True,load_only=True)
    
class PlainDriverSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone_number = fields.Str(required=True)
    address = fields.Str(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    status = fields.Str(required=True)  # e.g., "active", "inactive"
    
class PlainAmbulanceSchema(Schema):
    id = fields.Int(dump_only=True)
    license_plate = fields.Str(required=True)
    vehicle_type = fields.Str(required=True)  # e.g., "basic", "advanced"
    status = fields.Str(required=True)  # e.g., "available", "on duty", "maintenance"
    
class PlainBookingSchema(Schema):
    id = fields.Int(dump_only=True)
    booking_time = fields.DateTime(dump_only=True)
    status = fields.Str(required=True)  # e.g., "pending", "confirmed", "completed"
    user_id = fields.Int(required=True)
    hospital_id = fields.Int(required=True)
    ambulance_id = fields.Int(required=True)
    
class PlainAdminSchema(PlainUserSchema):
    pass


class UserSchema(PlainUserSchema):
    access_token = fields.Str(dump_only=True)
    refresh_token = fields.Str(dump_only=True)
    bookings = fields.List(fields.Nested(lambda: PlainBookingSchema()), dump_only=True)  # Associated bookings


class HospitalSchema(PlainHospitalSchema):
    address = fields.Nested(PlainAddressSchema, required=True,dump_only=True)  # Full address details
    admin = fields.Nested(lambda: PlainAdminSchema(), dump_only=True)
    drivers = fields.List(fields.Nested(lambda: PlainDriverSchema()), dump_only=True)
    ambulances = fields.List(fields.Nested(lambda: PlainAmbulanceSchema()), dump_only=True)
    bookings = fields.List(fields.Nested(lambda: PlainBookingSchema()), dump_only=True)  # Associated bookings



class DriverSchema(PlainDriverSchema):
    hospital = fields.Nested(HospitalSchema, dump_only=True)



class AmbulanceSchema(PlainAmbulanceSchema):
    hospital = fields.Nested(HospitalSchema, dump_only=True)




class BookingSchema(PlainBookingSchema):
    user = fields.Nested(PlainUserSchema, dump_only=True)
    hospital = fields.Nested(PlainHospitalSchema, dump_only=True)
    ambulance = fields.Nested(PlainAmbulanceSchema, dump_only=True)



class AdminSchema(PlainAdminSchema):
    hospitals = fields.List(fields.Nested(PlainHospitalSchema), dump_only=True)
    
    
class LoginSchema(Schema):
    name = fields.Str(required=True)
    password = fields.Str(required=True)
