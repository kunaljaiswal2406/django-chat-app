#!/usr/bin/env python
"""API for the chat app goes here."""
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authentication import MultiAuthentication
from tastypie.authentication import SessionAuthentication

from tastypie.http import HttpApplicationError
from tastypie.http import HttpBadRequest
from tastypie.resources import Resource
from tastypie.utils.urls import trailing_slash

from django.conf.urls import url

from account.decorators import secure_view
from account.decorators import validate_post_data
from account.decorators import validate_query_params

from chat import api_schema
from chat import private
from account import public as account_public


class ChatResource(Resource):
    class Meta:
        resource_name = "chat"
        allowed_methods = ["get", "post"]
        authentication = MultiAuthentication(
            SessionAuthentication(), ApiKeyAuthentication()
        )

    def prepend_urls(self):
        return [
            url(
                rf"^(?P<resource_name>{self._meta.resource_name})/send-message{trailing_slash()}$",
                self.wrap_view("send_message"),
                name="api_send_message",
            ),
            url(
                rf"^(?P<resource_name>{self._meta.resource_name})/unread-messages{trailing_slash()}$",
                self.wrap_view("get_unread_messages"),
                name="api_get_unread_messages",
            ),
            url(
                rf"^(?P<resource_name>{self._meta.resource_name})/all-messages{trailing_slash()}$",
                self.wrap_view("get_all_messages"),
                name="api_get_all_messages",
            ),
        ]

    @validate_post_data(schema=api_schema.SendMessageSchema)
    @secure_view(authenticate=True, allowed_methods=["post"])
    def send_message(self, request, api_data, *args, **kwargs):
        sender = request.user
        receiver = account_public.get_user_for_email(api_data["receiver_email"])
        if not receiver:
            return self.create_response(
                request,
                {
                    "error_message": "receiverNotFound",
                    "error_code": "Receiver not found",
                },
                response_class=HttpBadRequest,
            )
        if private.send_message(sender.id, receiver.id, api_data["text"]):
            return self.create_response(request, {"result": {"success": True}})
        return self.create_response(
            request, {"result": {"success": False}}, response_class=HttpApplicationError
        )

    @validate_query_params(schema=api_schema.GetMessageSchema)
    @secure_view(authenticate=True, allowed_methods=["get"])
    def get_unread_messages(self, request, api_data, *args, **kwargs):
        user = request.user
        sender_id = api_data.get("sender_id")
        return self.create_response(
            request,
            {
                "unread_messages": private.get_unread_message_for_user(
                    user.id, sender_id
                )
            },
        )

    @validate_query_params(schema=api_schema.GetMessageSchema)
    @secure_view(authenticate=True, allowed_methods=["get"])
    def get_all_messages(self, request, api_data, *args, **kwargs):
        user = request.user
        sender_id = api_data.get("sender_id")
        return self.create_response(
            request,
            {"all_messages": private.get_all_messages_for_user(user.id, sender_id)},
        )
