import socket
from encryption import hash_password

class Guest:
    
    def __init__(self):
        self.connected = False
        self.authenticated = False
        self.socket = socket.socket()
    

    def connect(self, room_ip, port):
        self.socket.connect((room_ip, port))
        self.room_ip = room_ip
        self.port = port

    def auth(self, password: str):
        hash, salt = hash_password(password)
        self.socket.send(("auth:" + hash + ":" + salt).encode())