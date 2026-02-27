from marshmallow import Schema, fields, validate, ValidationError

class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8), load_only=True)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)

def validate_payload(schema, data):
    try:
        return schema.load(data), {}
    except ValidationError as err:
        return {}, err.messages
