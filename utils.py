from base64 import b64encode, b64decode
from socket import socket

class ConnectionError:
    pass

def log(text: str):
    f = open("log.txt", '+a')
    f.writelines(text + "\n")
    f.close()



class GuestModel:
    
    def __init__(self, c: socket, id: str, addr, username: str=None,):
        self.c = c
        self.username = username
        self.addr = addr
        self.id = id

    def __eq__(self, other):
        return self.id == other.id if isinstance(other, GuestModel) else False


pre_generated_usernames = [
    "Hadi",
    "KolahGhermezi",
    "Qmarth",
    "Javad",
    "Badoom",
    "Bidandon",
    "Mmd",
    "Dragon",
    "Coach",
    "Steve",
    "Alex",
    "Zombie",
    "Tokyo",
    "Professor",
    "HarryPotter",
    "SpiderMan",
    "BatMan",
    "Hitler",
    "Adolf",
    "Ahmad",
    "Saghi",
    "PesarKhale",
    "DokhtarKhale",
    "BobEsfanji",
    "Patrik",
    "GholamReza",
    "Cyrus",
    "Sasan",
    "Nader",
    "Abbas",
    "Killer",
    "Assasin",
    "Homa",
    "Golnar",
    "Kaaveh"
]


def encode(text: str) -> str:
    return b64encode(text.encode()).decode()

def decode(text: str) -> str:
    return b64decode(text.encode()).decode()
