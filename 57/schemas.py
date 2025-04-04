from marshmallow import Schema, fields, validate, EXCLUDE


class PostSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    subtitle = fields.Str(allow_none=True, validate=validate.Length(min=1, max=200))
    body = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    author = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    create_date = fields.DateTime(dump_only=True)