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
    ntr = ["ntr", "natura"]

class RequestTypes(ExtendedEnum):
    GET = "GET"
    POST = "POST"

class ResponseTypes(ExtendedEnum):
    OK = "200 OK"
    NOT_FOUND = "404 Not Found"
    MOVED_PERMANENTLY = "Moved Permanently"

class Response():
    def __init__(self, type):
        self.type = type
        self.version = "HTTP/1.1"
        self.headers = {"Server": "natura"}
        self.data = b""
    def addHeader(self, key, value):
        self.headers[key] = value
    def setData(self, data):
        self.data = data
    def getRaw(self):
        raw = (self.version + " " + self.type.value + "\r\n").encode()

        if ("Date" not in self.headers):
            now = datetime.now()
            stamp = mktime(now.timetuple())
            self.headers["Date"] = format_date_time(stamp)
            #self.headers["Content-Type"] = "image/png"
            #self.headers["Accept-Ranges"] = "bytes"

        for headKey in self.headers:
            raw += (headKey + ": " + self.headers[headKey] + "\r\n").encode()
        
        raw += "\n".encode()
        raw += self.data

        return raw
        
