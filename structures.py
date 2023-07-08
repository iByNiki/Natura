from enum import Enum
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime

class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class FileTypes(ExtendedEnum):
    html = ["html", "htm"]
    js = ["js"]
    css = ["css"]

class RequestTypes(ExtendedEnum):
    GET = "GET"
    POST = "POST"

class ResponseTypes(ExtendedEnum):
    OK = "200 OK"
    NOT_FOUND = "404 Not Found"

class Response():
    def __init__(self, type):
        self.type = type
        self.version = "HTTP/1.1"
        self.headers = {"Server": "natura"}
        self.data = ""
    def addHeader(self, key, value):
        self.headers[key] = value
    def setData(self, data):
        self.data = data
    def getRaw(self):
        raw = self.version + " " + self.type.value + "\n"

        if ("Date" not in self.headers):
            now = datetime.now()
            stamp = mktime(now.timetuple())
            self.headers["Date"] = format_date_time(stamp)

        for headKey in self.headers:
            raw += headKey + ": " + self.headers[headKey] + "\n"
        
        raw += "\n\n"
        raw += self.data

        return raw
    
    def getEncoded(self):
        return self.getRaw().encode()
        
