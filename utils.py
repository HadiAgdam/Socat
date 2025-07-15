class ConnectionError:
    pass


def log(txt: str):
    print(txt)


class GuestModel:
    
    def __init__(self, c, addr):
        self.c = c
        self.addr = addr

    def __eq__(self, other):
        return self.addr == other.addr if isinstance(other, GuestModel) else False