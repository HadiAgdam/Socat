import socket
from threading import Thread
from time import sleep

class Room:

    def listen(self):
        while True:
            c, addr = self.socket.accept()
            self.not_authenticated_quests.append((c, addr))
            print("got new client:", addr)

    
    def __init__(self, password):
        self.guests = []
        self.password = password
        self.is_up = False
        self.not_authenticated_quests = []
        self.authenticated_guests = []
        self.socket = socket.socket()
    
    def create(self, port):
        self.socket.bind(('', port))
        self.socket.listen(5)
        self.is_up = True
        # self.thread = Thread(target=self.listen)
        # self.thread.start()