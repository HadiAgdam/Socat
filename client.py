import socket
from encryption import hash_password
from utils import log
from threading import Thread

class Guest:

    def __listen_for_incoming_message(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if not data:
                    continue
                data = data.decode()
                if data == "Auth successful":
                    self.authenticated = True
                    # return   this was the fucking bug I was looking for since last night
                    continue
                if self.message_callback:
                    self.message_callback(data)
            except Exception as ex:
                raise ex
                log("error :", str(ex))
    
    def __init__(self):
        self.connected = False
        self.authenticated = False
        self.socket = socket.socket()
        self.message_callback = None
    

    def connect(self, room_ip, port):
        self.socket.connect((room_ip, port))
        self.room_ip = room_ip
        self.port = port
        Thread(target=self.__listen_for_incoming_message).start()
        self.connected = True

    def auth(self, password: str):
        hash, salt = hash_password(password)
        self.socket.send(("auth:" + hash + ":" + salt).encode())
    
    def send_message(self, text: str):
        self.socket.send(text.encode())
