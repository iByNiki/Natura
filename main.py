import socket
import threading
import sys
import tcpserver
import logger

HOST = "0.0.0.0"
PORT = int(sys.argv[1])
WEBDIR = sys.argv[2]


if (__name__ == "__main__"):
    tcpserver.start(WEBDIR, HOST, PORT)
    tcpserver.loop()

# TODO: Idea - add a plugin system to intercept requests etc
# TODO: Idea - make a sort of php but with python