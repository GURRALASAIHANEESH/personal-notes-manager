from marshmallow import Schema, fields, validate, ValidationError

class NoteCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    content = fields.Str(required=True, validate=validate.Length(min=1))
    tags = fields.List(fields.Str(), load_default=[])
    is_private = fields.Bool(load_default=True)

class NoteUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=255))
    content = fields.Str(validate=validate.Length(min=1))
    tags = fields.List(fields.Str())
    is_private = fields.Bool()

def validate_payload(schema, data):
    try:
        return schema.load(data), {}
    except ValidationError as err:
        return {}, err.messages
