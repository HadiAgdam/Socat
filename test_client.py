from client import Guest
from display import Display
from time import sleep
from test_server import port
from utils import log

g = Guest()

g.connect("127.0.0.1", port)

print("connected")

g.auth("123")

while not g.authenticated:
    pass

def typed_new_message(text):
    log("typed new message in client: " + text)
    g.send_message(text)
    print("typed new message in client: ", text)

d = Display(typed_new_message)
g.message_callback = d.new_message



d.run()
