from enum import Enum

class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class Requests(ExtendedEnum):
    GET = "GET"
    POST = "POST"
