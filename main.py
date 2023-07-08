import socket
import threading
import sys

HOST = "0.0.0.0"
PORT = int(sys.argv[1])

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
        print(dir)

        self.socket.send("HTTP/1.1 200 OK\n\nHELLO!".encode())
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