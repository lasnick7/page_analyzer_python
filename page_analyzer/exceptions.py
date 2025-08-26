class EmptyUrlError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"EmptyUrlError, {self.message}"
        else:
            return "EmptyUrlError, Url should not be empty"


class TooLongUrlError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"TooLongUrlError, {self.message}"
        else:
            return "TooLongUrlError, Url should not be longer than 255 characters"


class InvalidUrlError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"InvalidUrlError, {self.message}"
        else:
            return "InvalidUrlError, Url is not valid"