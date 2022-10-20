import socket
from abc import ABC, abstractmethod

class TCPServer:

    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port

    def start(self):
        # create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Enable port reuse
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket object to the address and port
        s.bind((self.host, self.port))

        s.listen(5)

        print(f"Listening at {s.getsockname()}")

        while True:
            # accept new connection
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            data = conn.recv(1024)

            response = self.handle_request(data)

            conn.sendall(response)
            conn.close()

    @abstractmethod
    def handle_request(self, data):
        """
        handle incoming data and returns a response.
        To be overriden in subclass.
        """
        pass