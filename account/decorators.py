from functools import wraps
from tastypie import http
from tastypie.exceptions import ImmediateHttpResponse
import functools

import marshmallow
import webargs
import webargs.djangoparser


def secure_view(
    authenticate=True,
    allowed_methods=None,
):
    if allowed_methods is None:
        allowed_methods = []

    def decorator(view):
        @wraps(view)
        def view_wrapper(self, request, *args, **kwargs):
            self.method_check(request, allowed=allowed_methods)
            try:
                self.is_authenticated(request)
            except ImmediateHttpResponse:
                if authenticate:
                    raise
            return view(self, request, *args, **kwargs)

        return view_wrapper

    return decorator


def validate_api_args(schema: marshmallow.schema.Schema, locations=None):
    """Validates/Deserializes tastypie API params/post data using webargs.

    Args:
        schema (marshmallow.schema.Schema): The schema to be used for validating the API data.
        locations (list of string): The list of locations where we should check for the api arguments.

    eg Schema
        {'status': webargs.fields.Integer(required=True)}

    Returns:
        400: if the validation faills.
        The status returned by the API view, if the validation passes.

    """

    def decorator(view):
        @functools.wraps(view)
        def view_wrapper(self, request, *args, **kwargs):
            try:
                parsed_data = webargs.djangoparser.parser.parse(
                    schema, request, locations=locations
                )
            except webargs.ValidationError as exc:
                return self.error_response(
                    request,
                    {
                        "error_code": "ValidationError",
                        "error_message": "Invalid params sent for API",
                        "error_data": exc.normalized_messages(),
                    },
                )
            except webargs.djangoparser.json.JSONDecodeError:
                return self.error_response(
                    request,
                    {
                        "error_code": "ValidationError",
                        "error_message": "Invalid JSON body",
                    },
                )
            kwargs.update({"api_data": parsed_data})
            return view(self, request, *args, **kwargs)

        return view_wrapper

    return decorator


validate_post_data = functools.partial(validate_api_args, locations=["json", "form"])
validate_query_params = functools.partial(validate_api_args, locations=["query"])
