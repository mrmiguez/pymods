class PymodsExpection(Exception):
    pass


class NameSpaceInvalid(PymodsExpection):
    def __str__(self):
        return "Root is in an unexpected namespace"


class ElementNotFound(PymodsExpection):
    def __str__(self):
        return "Record does not contain the specified element"