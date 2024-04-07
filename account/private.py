"""Private module for the challenge package."""

from django.contrib.auth import authenticate


from account import dal
from account import exceptions


get_user_for_email = dal.get_user_for_email


def get_api_key_for_user(user: dal.User) -> str:
    """Returns the API key for the given user.

    Args:
        user (Object(auth.User)): User object.

    Returns:
        str: API key for the given user.

    """
    api_key = dal.get_api_key_for_user(user)
    if api_key:
        return api_key
    raise exceptions.ApiKeyDoesNotExists


def sign_up(email: str, first_name: str, last_name: str, password: str) -> dal.User:
    """Sign up a new user with given email, first_name, last_name and password.

    Args:
        email (str): Email of the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        password (str): Password of the user.

    Returns:
        Object(auth.User): User object created in the database.

    """
    if dal.is_user_exists_for_given_email(email):
        raise exceptions.UserAlreadyExists
    return dal.create_user(email, first_name, last_name, password)


def login_user(email: str, password: str) -> dal.User:
    """Login user with given email and password. And returns the logged in user.

    Args:
        email (str): Email of the user.
        password (str): Password of the user.

    Returns:
        Object(auth.User): User object if login is successful.

    """
    user = authenticate(username=email, password=password)
    if not user:
        raise exceptions.InvalidUserCredentials
    return user
