# app/posts/schemas.py
from marshmallow import Schema, fields, validate

class PostCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=3, max=200))
    body = fields.Str(required=True, validate=validate.Length(min=1))

class PostUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=3, max=200))
    body = fields.Str()
