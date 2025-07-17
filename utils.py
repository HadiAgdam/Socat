from base64 import b64encode, b64decode

class ConnectionError:
    pass

def log(text: str):
    f = open("log.txt", '+a')
    f.writelines(text + "\n")
    f.close()



class GuestModel:
    
    def __init__(self, c, addr, username=None):
        self.c = c
        self.addr = addr
        self.username = username

    def __eq__(self, other):
        return self.addr == other.addr if isinstance(other, GuestModel) else False


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
