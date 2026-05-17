# app/comments/schemas.py
from marshmallow import Schema, fields, validate

class CommentCreateSchema(Schema):
    body = fields.Str(required=True, validate=validate.Length(min=1))
