import socket
import threading
import sys
import logger
from tcpserver import TCPServer
from cache import Cache
from settings import Settings

if (__name__ == "__main__"):
    settings = Settings()
    # settings.loadFromFile()
    cache = Cache(settings)

    tcpserver = TCPServer(settings, cache)
    tcpserver.start()
    tcpserver.loop()

# TODO: Idea - add a plugin system to intercept requests etc
# TODO: Idea - make a sort of php but with python