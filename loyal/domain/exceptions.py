class AccountError(Exception):
    pass


class UserNotFoundError(AccountError):
    pass


class IncorrectPasswordError(AccountError):
    pass
