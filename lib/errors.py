class BaseError(Exception):
    def __init__(self, token, message):
        self.token   = token
        self.message = message


# class Error(BaseError):
#     pass


# class RuntimeError(BaseError):
#     pass
