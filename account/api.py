#!/usr/bin/env python
"""API for the account app goes here."""
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

from account import api_schema
from account import private
from account import exceptions


class AccountResource(Resource):
    class Meta:
        resource_name = "account"
        allowed_methods = ["get", "post"]
        authentication = MultiAuthentication(
            SessionAuthentication(), ApiKeyAuthentication()
        )

    def prepend_urls(self):
        return [
            url(
                rf"^(?P<resource_name>{self._meta.resource_name})/ping{trailing_slash()}$",
                self.wrap_view("ping"),
                name="api_ping",
            ),
            url(
                rf"^(?P<resource_name>{self._meta.resource_name})/signup{trailing_slash()}$",
                self.wrap_view("signup"),
                name="api_signup",
            ),
            url(
                rf"^(?P<resource_name>{self._meta.resource_name})/login{trailing_slash()}$",
                self.wrap_view("login"),
                name="api_login",
            ),
        ]

    @secure_view(authenticate=True, allowed_methods=["get", "post"])
    def ping(self, request, *args, **kwargs):
        return self.create_response(request, {"message": "Working fine!!"})

    @validate_post_data(schema=api_schema.SignUpSchema)
    @secure_view(authenticate=False, allowed_methods=["post"])
    def signup(self, request, api_data, *args, **kwargs):
        try:
            private.sign_up(
                api_data["email"],
                api_data["first_name"],
                api_data["last_name"],
                api_data["password"],
            )
            return self.create_response(request, {"result": {"success": True}})
        except exceptions.UserAlreadyExists as exc:
            return self.create_response(
                request,
                {
                    "result": {
                        "success": False,
                        "error_message": exc.error_message,
                        "error_code": exc.error_code,
                    }
                },
                response_class=HttpBadRequest,
            )

    @validate_post_data(schema=api_schema.LoginSchema)
    @secure_view(authenticate=False, allowed_methods=["post"])
    def login(self, request, api_data, *args, **kwargs):
        try:
            user = private.login_user(api_data["email"], api_data["password"])
            api_key = private.get_api_key_for_user(user)
        except (
            exceptions.UserDoesNotExists,
            exceptions.InvalidUserCredentials,
            exceptions.ApiKeyDoesNotExists,
        ) as exc:
            return self.create_response(
                request,
                {
                    "result": {
                        "success": False,
                        "error_message": exc.error_message,
                        "error_code": exc.error_code,
                    }
                },
                response_class=HttpBadRequest,
            )
        if user:
            return self.create_response(
                request,
                {
                    "result": {
                        "success": True,
                        "api_key": api_key,
                        "username": user.username,
                    }
                },
            )
        return self.create_response(
            request, {"result": {"success": False}}, response_class=HttpApplicationError
        )
