class BaseException(Exception):
    message: str = 'Initial Server Error'
    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message

class NotFoundException(BaseException):
    message = 'Not Found'

class InsertErrorException(BaseException):
    message = 'Error while inserting data'