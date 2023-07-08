import socket
import threading
import sys

HOST = "0.0.0.0"
PORT = int(sys.argv[1])
WEBDIR = sys.argv[2]

class ClientThread(threading.Thread):
    def __init__(self, ip, port, socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        print("[+] New thread started for " + ip + ":" + str(port))
    def run(self):
        request = self.socket.recv(1024).decode()
        lines = request.split("\n")
        
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
        self.socket.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))

threads = []

while (True):
    sock.listen(1)
    (clientsock, (ip, port)) = sock.accept()
    clientThread = ClientThread(ip, port, clientsock)
    clientThread.start()
    threads.append(clientThread)

for thread in threads:
    thread.join()