class UserAlreadyExists(Exception):
    error_message = "User alread exists"
    error_code = "userAlreadyExists"


class UserDoesNotExists(Exception):
    error_message = "User does not exists for given email"
    error_code = "userDoesNotExists"


class InvalidUserCredentials(Exception):
    error_message = "Invalid user credentials"
    error_code = "invalidUserCredentials"


class ApiKeyDoesNotExists(Exception):
    error_message = "API key does not exists for given user"
    error_code = "apiKeyDoesNotExists"
