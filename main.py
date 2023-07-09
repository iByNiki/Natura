import socket
import threading
import sys
import logger
from tcpserver import TCPServer
from cache import Cache
from settings import Settings

class ServerThread(threading.Thread):
    def __init__(self, settings, cache, type):
        threading.Thread.__init__(self)
        self.tcpserver = TCPServer(settings, cache)
    def run(self):
        self.tcpserver.start()
        self.tcpserver.loop()

if (__name__ == "__main__"):
    settings = Settings()
    settings.load()

    cache = Cache(settings)

    httpThread = ServerThread(settings, cache, "http")
    #sslThread = ServerThread(settings, cache, "https")

    httpThread.start()
    #sslThread.start()
    

# TODO: ADD SUPPORT FOR FILE SENDING WTF
# TODO: Idea - add a plugin system to intercept requests etc
# TODO: Idea - make a sort of php but with python