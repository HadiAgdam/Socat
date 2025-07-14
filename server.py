import socket
from threading import Thread
from time import sleep
from encryption import hash_password


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        return s.getsockname()[0]
    except:
        return None
    finally:
        s.close()

class Room:

    def __listen_for_authenticated_quest(self, c, addr):
        while True:
            try:
                data = c.recv(1024)
                if not data:
                    continue
                data = data.decode()
                if data.startswith("/"):
                    # TODO
                    continue
                if self.message_callback:
                    self.message_callback(data)
                for guest in self.authenticated_guests:
                    if addr != guest[1]:
                        self.send_message(data)
            except Exception as ex:
                raise ex
            

    def __listen_for_not_authenticated_quest(self, c, addr):
        while True:
            data = c.recv(1024)
            if not data:
                continue
            data = data.decode()
            if data.startswith("auth:"):
                _, hash, salt = data.split(":")
                if hash_password(self.password, salt)[0] == hash:
                    self.authenticated_guests.append((c, addr))
                    self.not_authenticated_quests.remove((c, addr))
                    Thread(target=self.__listen_for_authenticated_quest, args=(c, addr)).start()
                    return

    def listen_for_connections(self):
        while True:
            c, addr = self.socket.accept()
            self.not_authenticated_quests.append((c, addr))
            Thread(target=self.__listen_for_not_authenticated_quest, args=(c, addr)).start()

    
    def __init__(self, password):
        self.guests = []
        self.password = password
        self.is_up = False
        self.not_authenticated_quests = []
        self.authenticated_guests = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_callback = None
    
    def create(self, port) -> str: # returns the ip of the host on network
        self.socket.bind(('', port))
        self.socket.listen(5)
        self.is_up = True
        self.thread = Thread(target=self.listen_for_connections)
        self.thread.start()
        return get_local_ip()
    
    def send_message(self, text: str):
        for guest in self.authenticated_guests:
            guest[0].send(text.encode())
