import socket
import threading
import logger
import natparser
import structures
import os
import ssl

WEBDIR, HOST, PORT = None, None, None

class ClientThread(threading.Thread):
    def __init__(self, settings, ip, port, socket, cache, isSSL):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        self.cache = cache
        self.settings = settings
        self.isSSL = isSSL

    def run(self):
        try:
            rawreq = self.socket.recv(1024).decode()
        except:
            logger.warning("Invalid req (on read) by " + self.ip + ":" + str(self.port))
            
        request = natparser.parseRequest(rawreq)

        if (request != None):

            # TODO: Check request has all necessary data

            logger.info(self.ip + ":" + str(self.port) + " - " + request["type"] + " " + request["dir"])

            if (not self.isSSL and self.settings.get("ssl_redirect") and self.settings.get("enable_ssl")):
                response = structures.Response(structures.ResponseTypes.MOVED_PERMANENTLY)
                response.addHeader("Location", self.settings.get("ssl_redirect_path").replace("/$1", request["dir"]))
                
                self.safeSend(response.getRaw())
                self.socket.close()

                return

            if (request["type"] == structures.RequestTypes.GET.value):

                request = natparser.checkDir(request)

                if (os.path.exists(self.settings.get("webdir") + request["dir"])):
                    fileData = self.cache.getFile(request["dir"])
                    response = structures.Response(structures.ResponseTypes.OK)
                    response.setData(fileData)
                    self.safeSend(response.getRaw())
                    self.socket.close()
                    
                else:
                    # TODO: display 404
                    logger.warning("404 by " + self.ip + ":" + str(self.port) + " in " + request["dir"])
                    pass
            else:
                # TODO: invalid request 2 (or not supported)
                pass
        else:
            # TODO: display invalid request
            logger.warning("Invalid req by " + self.ip + ":" + str(self.port))

    def safeSend(self, data):
        try:
            self.socket.send(data)
        except BrokenPipeError:
            logger.warning("Connection closed by " + self.ip + ":" + str(self.port))
    
class TCPServer():
    def __init__(self, settings, cache, cert=None, key=None):
        self.threads = []
        self.settings = settings
        self.cache = cache
        self.cert = cert
        self.key = key

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if (self.cert != None):
            ctx = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
            ctx.load_cert_chain(certfile=self.cert, keyfile=self.key)
            self.sock = ctx.wrap_socket(self.sock, server_side=True)

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
            isSSL = False
        else:
            logger.info("Listening in port " + str(self.settings.get("ssl_port")))
            isSSL = True

        while (True):
            self.sock.listen(1)

            try:
                (clientsock, (ip, port)) = self.sock.accept()
            except ssl.SSLError:
                pass

            clientThread = ClientThread(self.settings, ip, port, clientsock, self.cache, isSSL)
            clientThread.start()

            self.threads.append(clientThread)


# TODO: Maybe move the main server onto another thread?