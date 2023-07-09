import socket
import threading
import logger
import natparser
import structures
import os
import ssl

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
                    self.socket.send(response.getRaw())
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
    def __init__(self, settings, cache, cert=None, key=None):
        self.threads = []
        self.settings = settings
        self.cache = cache
        self.cert = cert
        self.key = key

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if (self.cert != None):
            print("ssl enabled")
            ctx = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
            ctx.load_cert_chain(certfile=self.cert, keyfile=self.key)
            self.sock = ctx.wrap_socket(self.sock, server_side=True)
            print("wrapped")

    def start(self):
        logger.info("Starting server...")

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if (self.cert == None):
            self.sock.bind((self.settings.get("host"), self.settings.get("port")))
        else:
            self.sock.bind((self.settings.get("host"), self.settings.get("ssl_port")))

    def loop(self):
        if (self.cert == None):
            logger.info("Listening in port " + str(self.settings.get("port")))
        else:
            logger.info("Listening in port " + str(self.settings.get("ssl_port")))

        while (True):
            self.sock.listen(1)
            (clientsock, (ip, port)) = self.sock.accept()

            clientThread = ClientThread(self.settings, ip, port, clientsock, self.cache)
            clientThread.start()

            self.threads.append(clientThread)


# TODO: Maybe move the main server onto another thread?