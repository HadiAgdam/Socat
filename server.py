import socket
from threading import Thread
from time import sleep
from encryption import hash_password
from utils import log


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

    def listen_for_authenticated_quest(self, c, addr):
        while True:
            try:
                data = c.recv(1024)
                if not data:
                    continue
                data = data.decode()
                log("got message from auth user [" + addr + "]:" + data)
            except Exception as ex:
                log("error :" + str(ex))
            

    def listen_for_not_authenticated_quest(self, c, addr):
        while True:
            data = c.recv(1024)
            if not data:
                continue
            data = data.decode()
            log("log message from [" + str(addr) + "]:" + data)
            if data.startswith("auth:"):
                _, hash, salt = data.split(":")
                if hash_password(self.password, salt)[0] == hash:
                    self.authenticated_guests.append((c, addr))
                    self.not_authenticated_quests.remove((c, addr))
                    log("auth successful")
                    Thread(target=self.listen_for_authenticated_quest, args=(c, addr)).start()
                    return
                log("auth failed")
                log("hash: " + hash)
                log("password hash: " + hash_password(self.password, salt)[0])

    def listen_for_connections(self):
        while True:
            c, addr = self.socket.accept()
            self.not_authenticated_quests.append((c, addr))
            log("got new client:" + str(addr))
            Thread(target=self.listen_for_not_authenticated_quest, args=(c, addr)).start()

    
    def __init__(self, password):
        self.guests = []
        self.password = password
        self.is_up = False
        self.not_authenticated_quests = []
        self.authenticated_guests = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def create(self, port) -> str: # returns the ip of the host on network
        self.socket.bind(('', port))
        self.socket.listen(5)
        self.is_up = True
        self.thread = Thread(target=self.listen_for_connections)
        self.thread.start()
        return get_local_ip()