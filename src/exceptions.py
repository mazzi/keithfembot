class KeithFemException(Exception):
    """Base class for all KeithFem Exceptions"""


class HTTPError(KeithFemException):
    """Error happening when querying an external service"""
