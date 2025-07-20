import socket
from encryption import hash_password
from utils import log
from threading import Thread
from utils import encode, decode
from time import sleep, time

class Guest:

    def report_status(self, text: str):
        # abstract function
        pass

    def __start_heartbit(self):
        while True:
            self.t = int(time())
            self.socket.send(f"ping:{encode(str(self.t))}".encode())
            sleep(5)

    def __listen_for_incoming_message(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if not data:
                    continue
                data = data.decode()
                if data == "Auth successful":
                    self.authenticated = True
                    Thread(target=self.__start_heartbit).start()

                    continue
                if data == "pong":
                    if self.t:
                        self.report_status(f" {self.room_ip} | status: CONNECTED  ping: {int(time() - self.t)}ms")
                        self.t = None
                    continue
                if self.message_callback:
                    self.message_callback(data)
            except Exception as ex:
                raise ex
    
    def __init__(self):
        self.connected = False
        self.authenticated = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_callback = None
        self.t = None
    

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
        if text.startswith("/"):
            command = text.split(" ")[0]
            text = text[len(command):]
            match (command):
                case "/set_name":
                    self.socket.send(("set_name:" + encode(text)).encode())
        else:
            self.socket.send(("public_message:" + encode(text)).encode())
