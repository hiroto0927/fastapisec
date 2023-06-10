class NotFoundException(Exception):
    pass


class NotUserExistException(Exception):
    pass


class ExpiredError(Exception):
    pass


class AlreadyExistUserError(Exception):
    pass


class PasswordNotMatchError(Exception):
    pass
