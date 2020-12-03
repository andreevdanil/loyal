class AccountError(Exception):
    pass


class UserNotFoundError(AccountError):
    pass


class UserLoginError(AccountError):
    message = "Incorrect login or password"
