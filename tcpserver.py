import socket
import threading
import logger
import natparser
import structures
import os

WEBDIR, HOST, PORT = None, None, None

class ClientThread(threading.Thread):
    def __init__(self, settings, ip, port, socket, cache):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        self.cache = cache
        self.settings = settings

        logger.info("New thread started for " + ip + ":" + str(port))

    def run(self):
        rawreq = self.socket.recv(1024).decode()
        request = natparser.parseRequest(rawreq)

        if (request != None):
            if (request["type"] == structures.RequestTypes.GET.value):
                if (os.path.exists(self.settings.get("webdir") + request["dir"])):
                    fileData = self.cache.getFile(request["dir"])
                    response = structures.Response(structures.ResponseTypes.OK)
                    response.setData(fileData)
                    self.socket.send(response.getEncoded())
                    self.socket.close()
                    
                else:
                    # TODO: display 404
                    logger.warning("404 by " + self.ip + ":" + str(self.port))
                    pass
            else:
                # TODO: invalid request 2 (or not supported)
                pass
        else:
            # TODO: display invalid request
            logger.warning("Invalid req by " + self.ip + ":" + str(self.port))
    
class TCPServer():
    def __init__(self, settings, cache):
        self.threads = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.settings = settings
        self.cache = cache

    def start(self):
        logger.info("Starting server...")

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.settings.get("host"), self.settings.get("port")))

    def loop(self):
        logger.info("Listening in port " + str(self.settings.get("port")))

        while (True):
            self.sock.listen(1)
            (clientsock, (ip, port)) = self.sock.accept()

            clientThread = ClientThread(self.settings, ip, port, clientsock, self.cache)
            clientThread.start()

            self.threads.append(clientThread)


# TODO: Maybe move the main server onto another thread?