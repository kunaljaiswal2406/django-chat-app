#!/usr/bin/env python

from marshmallow import schema
from marshmallow import fields


class SignUpSchema(schema.Schema):
    email = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    password = fields.String(required=True)


class LoginSchema(schema.Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)
