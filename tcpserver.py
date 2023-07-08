import socket
import threading
import logger
import natparser
import structures
import cache
import os

WEBDIR, HOST, PORT = None, None, None

threads = []
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class ClientThread(threading.Thread):
    def __init__(self, ip, port, socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket

        logger.info("New thread started for " + ip + ":" + str(port))

    def run(self):
        rawreq = self.socket.recv(1024).decode()
        request = natparser.parseRequest(rawreq)

        if (request["type"] == structures.Requests.GET):
            # TODO: if file exists
            cache.getFile(request[dir])

        """lines = request.split("\n")
        
        dir = lines[0].split(" ")[1]
        if (dir[-1] == "/"):
            dir += "index.html"

        try:
            f = open(WEBDIR + dir, "r")
            data = f.read()
            f.close()
        except FileNotFoundError:
            self.socket.send("HTTP/1.1 404 Not Found\n\nFile not found.".encode())
            self.socket.close()
            return

        self.socket.send(("HTTP/1.1 200 OK\n\n" + data).encode())
        self.socket.close()"""
    

def start(webdir, host, port):
    global WEBDIR, HOST, PORT, sock
    WEBDIR, HOST, PORT = webdir, host, port

    logger.info("Starting server...")

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))

def loop():
    global sock

    logger.info("Listening in port " + str(PORT))

    while (True):
        sock.listen(1)
        (clientsock, (ip, port)) = sock.accept()

        clientThread = ClientThread(ip, port, clientsock)
        clientThread.start()

        threads.append(clientThread)


# TODO: Maybe move the main server onto another thread?