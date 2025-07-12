import socket

class Guest:
    
    def __init__(self):
        self.connected = False
        self.authenticated = False
        self.socket = socket.socket()
    

    def connect(self, room_ip, port):
        self.socket.connect((room_ip, port))
        self.room_ip = room_ip
        self.port = port

    def auth(self, password):
        pass