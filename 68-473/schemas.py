from marshmallow import Schema, fields, validate, EXCLUDE


class UserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    email = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=5, max=20))
    name = fields.Str(required=True, validate=validate.Length(min=4, max=50))
    create_date = fields.DateTime(dump_only=True)