from flask_marshmallow import Marshmallow
from marshmallow import fields, validate, EXCLUDE, pre_load
from .model import Post, User

ma =  Marshmallow()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ('id', 'name')
        load_instance = False

class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        exclude = ('author_id',)
        unknown = EXCLUDE
        load_instance = False

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    subtitle = fields.Str(allow_none=True, validate=validate.Length(max=200))
    body = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    create_date = fields.DateTime(dump_only=True)
    author = fields.Nested(UserSchema, dump_only=True)

class RegisterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('create_date',)
        unknown = EXCLUDE
        load_instance = False

    id = fields.Int(dump_only=True)
    email = fields.Email(required=True, validate=validate.Length(min=1,  max=50))
    password = fields.Str(required=True, validate=validate.Length(min=5, max=20))
    name = fields.Str(required=True, validate=validate.Length(min=5, max=50))

    @pre_load()
    def normalize_email(self, data, **kwargs):
        if 'email' in data and isinstance(data['email'], str):
            data['email'] = data['email'].strip().lower()
        return data

class LoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ('create_date', 'name')
        unknown = EXCLUDE
        load_instance = False

    id = fields.Int(dump_only=True)
    email = fields.Email(required=True, validate=validate.Length(min=1, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=5, max=20))

    @pre_load()
    def normalize_email(self, data, **kwargs):
        if 'email' in data and isinstance(data['email'], str):
            data['email'] = data['email'].strip().lower()
        return data
