#!/usr/bin/env python


from marshmallow import schema  # noqa: F401
from marshmallow import fields

__copyright__ = "Copyright (c) HealthifyMe Wellness Products and Services PVT. LTD."


class SendMessageSchema(schema.Schema):
    receiver_email = fields.String(required=True)
    text = fields.String(required=True)


class GetMessageSchema(schema.Schema):
    sender_id = fields.Integer(required=False)
