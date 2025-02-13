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
    street = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)
    postal_code = fields.Str(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)

class PlainHospitalSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)
    created_at = fields.DateTime(dump_only=True)

class PlainDriverSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    status = fields.Str(dump_only=True, required=False,allow_none=True)  # "available", "busy", "off-duty"
    created_at = fields.DateTime(dump_only=True)
    password = fields.Str(load_only=True, required=True)

class PlainAmbulanceSchema(Schema):
    id = fields.Int(dump_only=True)
    vehicle_number = fields.Str(required=True)
    vehicle_type = fields.Str(required=True)  # "basic", "advanced"
    status = fields.Str(dump_only=True, required=False,allow_none=True)  # "available", "busy", "maintenance"
    created_at = fields.DateTime(dump_only=True)

class PlainBookingSchema(Schema):
    id = fields.Int(dump_only=True)
    status = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)

# ===================== Extended Schemas ===================== #
class UserSchema(PlainUserSchema):
    bookings = fields.List(fields.Nested(PlainBookingSchema), dump_only=True)

class HospitalSchema(PlainHospitalSchema):
    address = fields.Nested(PlainAddressSchema, required=True)
    drivers = fields.List(fields.Nested(PlainDriverSchema), dump_only=True)
    ambulances = fields.List(fields.Nested(PlainAmbulanceSchema), dump_only=True)
    bookings = fields.List(fields.Nested(PlainBookingSchema), dump_only=True)

class DriverSchema(PlainDriverSchema):
    address = fields.Nested(PlainAddressSchema, required=True)
    hospitals = fields.List(fields.Nested(PlainHospitalSchema), dump_only=True)
    bookings = fields.List(fields.Nested(PlainBookingSchema), dump_only=True)

class AmbulanceSchema(PlainAmbulanceSchema):
    hospital = fields.Nested(PlainHospitalSchema, dump_only=True)
    driver = fields.Nested(PlainDriverSchema, dump_only=True)
    bookings = fields.List(fields.Nested(PlainBookingSchema), dump_only=True)

class BookingSchema(PlainBookingSchema):
    user = fields.Nested(PlainUserSchema, dump_only=True)
    hospital = fields.Nested(PlainHospitalSchema, dump_only=True)
    ambulance = fields.Nested(PlainAmbulanceSchema, dump_only=True)
    driver = fields.Nested(PlainDriverSchema, dump_only=True)

class AdminSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)
    phone = fields.Str(required=True)


class LoginSchema(Schema):
    name = fields.Str(required=True)
    password = fields.Str(required=True)
