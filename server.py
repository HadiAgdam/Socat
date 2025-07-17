import socket
from threading import Thread
from time import sleep
from encryption import hash_password
from utils import GuestModel, pre_generated_usernames, encode, decode, log
from random import choice
from string import ascii_lowercase
from datetime import datetime


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

    def message_callback(txt):  # default callback
        pass

    def __get_guest_id(self, socket, addr):
        return str(addr[1])

    def __on_guest_disconnect(self, guest: GuestModel):
        self.authenticated_guests.remove(guest)
        guest.c.close()
        self.__log_to_all(f"{guest.username} disconnected!")

    def __listen_for_authenticated_quest(self, guest: GuestModel):
        while True:
            try:
                data = guest.c.recv(1024)
                log("recv")
                if not data:
                    self.__on_guest_disconnect(guest)
                    return
                data = data.decode()
                if data.startswith("/"):
                    # TODO
                    continue
                log("received in server data: " + data)
                self.__send_message_to_all("guest", guest.username, guest.id, data)
            except ConnectionResetError:
                self.__on_guest_disconnect(guest)
                return
            except Exception as ex:
                log("server received message error :" + str(ex))
                raise ex
            

    def __listen_for_not_authenticated_quest(self, c, addr):
        guest = GuestModel(c, self.__get_guest_id(c, addr), addr)
        while True:
            data = guest.c.recv(1024)
            if not data:
                continue
            data = data.decode()
            if data.startswith("auth:"):
                _, hash, salt = data.split(":")
                if hash_password(self.password, salt)[0] == hash:

                    while not False:
                        username = choice(pre_generated_usernames)
                        duplicate_count = 0
                        for guest in self.authenticated_guests:
                            if guest.username == username:
                                duplicate_count += 1
                                break
                        if duplicate_count == 0:
                            break

                        # It is going to freeze inside loop if all of pregenerated usernames are taken
                        # So I just generate a random string :)
                        if duplicate_count == len(pre_generated_usernames):
                            username = ''.join(choice(ascii_lowercase) for _ in range(6))
                            break
                    guest.username = username

                    self.authenticated_guests.append(guest)
                    self.not_authenticated_guests.remove((c, addr))
                    Thread(target=self.__listen_for_authenticated_quest, args=[guest]).start()
                    guest.c.send("Auth successful".encode())
                    self.__log_to_all(f"{guest.username} joined to the room.")
                    return
                    

    def listen_for_connections(self):
        while True:
            c, addr = self.socket.accept()
            self.not_authenticated_guests.append((c ,addr))
            Thread(target=self.__listen_for_not_authenticated_quest, args=(c, addr)).start()

    
    def __init__(self, password):
        self.guests = []
        self.password = password
        self.is_up = False
        self.not_authenticated_guests = []
        self.authenticated_guests = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__admin_username = "Admin"
    
    def create(self, port) -> str: # returns the ip of the host on network
        self.socket.bind(('', port))
        self.socket.listen(5)
        self.is_up = True
        self.thread = Thread(target=self.listen_for_connections)
        self.thread.start()
        return get_local_ip()
    
    def __send_message_to_all(self, role: str, username: str, id: str, text: str):
        role = encode(role)
        username = encode(username)
        text = encode(text)
        id = encode(id)
        text = f"public_message:{role}:{username}:{id}:{text}"
        for guest in self.authenticated_guests:
            guest.c.send(text.encode())
        
        self.message_callback(text)
    
    def __log_to_all(self, text: str):
        text = f"log:{encode(text)}"
        for guest in self.authenticated_guests:
            guest.c.send(text.encode())

        self.message_callback(text)
    
    def send_server_message(self, text: str):
        # also check for commands
        if text.startswith("/"):
            command = text.split(":")
            match(command[0]):
                case "/set_name":
                    self.__admin_username = command[1]
        else:
            self.__send_message_to_all("Host", self.__admin_username, "127.0.0.1", text)
