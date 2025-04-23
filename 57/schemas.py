from marshmallow import Schema, fields, validate, EXCLUDE, pre_load


class PostSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    subtitle = fields.Str(allow_none=True, validate=validate.Length(min=1, max=200))
    body = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    author = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    create_date = fields.DateTime(dump_only=True)


class RegisterSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    email = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=5, max=20))
    name = fields.Str(required=True, validate=validate.Length(min=4, max=50))
    create_date = fields.DateTime(dump_only=True)

    @pre_load
    def normalize_email(self, data, **kwargs):
        if 'email' in data and isinstance(data['email'], str):
            data['email'] = data['email'].strip().lower()
        return data


class LoginSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True)
    email = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=5, max=20))
    name = fields.Str(dump_only=True)
    create_date = fields.DateTime(dump_only=True)

    @pre_load
    def normalize_email(self, data, **kwargs):
        if 'email' in data and isinstance(data['email'], str):
            data['email'] = data['email'].strip().lower()
        return data