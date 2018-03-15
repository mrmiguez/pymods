"""
Framework for future exception classes.
"""


class PymodsException(Exception):
    pass


class NameSpaceInvalid(PymodsException):
    def __str__(self):
        return "Root is in an unexpected namespace"


class ElementNotFound(PymodsException):
    def __str__(self):
        return "Record does not contain the specified element"
