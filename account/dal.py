"""Data Access Layer for the challenge app."""

from tastypie.models import ApiKey
from django.contrib.auth.models import User


def is_user_exists_for_given_email(email):
    """Checks if user exists for given email or not"""
    return bool(get_user_for_email(email))


def create_user(email, first_name, last_name, password):
    user = User.objects.create(
        email=email, username=email, first_name=first_name, last_name=last_name
    )
    user.set_password(password)
    user.save()
    if user:
        ApiKey.objects.create(user=user)
        return True


def get_user_for_email(email):
    """Returns user for given email"""
    user = User.objects.filter(email=email).last()
    if user:
        return user
    return User.objects.filter(username=email).last()


def get_api_key_for_user(user: User) -> str:
    """Returns the API key for the given user.

    Args:
        user (Object(auth.User)): User object.

    Returns:
        str: API key for the given user.

    """

    api_key = ApiKey.objects.filter(user=user).last()
    if api_key:
        return api_key.key
