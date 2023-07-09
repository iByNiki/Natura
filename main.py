import socket
import threading
import sys
import logger
from tcpserver import TCPServer
from cache import Cache
from settings import Settings

class ServerThread(threading.Thread):
    def __init__(self, settings, cache, cert=None, key=None):
        threading.Thread.__init__(self)

        if (cert == None):
            self.tcpserver = TCPServer(settings, cache)
        else:
            self.tcpserver = TCPServer(settings, cache, cert=cert, key=key)
    def run(self):
        self.tcpserver.start()
        self.tcpserver.loop()

if (__name__ == "__main__"):
    settings = Settings()
    settings.load()

    cache = Cache(settings)

    httpThread = ServerThread(settings, cache)
    httpThread.start()

    if (settings.get("enable_ssl")):
        sslThread = ServerThread(settings, cache, cert=settings.get("cert_path"), key=settings.get("key_path"))
        sslThread.start()
    

# TODO: ADD SUPPORT FOR FILE SENDING WTF
# TODO: Idea - add a plugin system to intercept requests etc
# TODO: Idea - make a sort of php but with python