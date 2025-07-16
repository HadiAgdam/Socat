from client import Guest
from display import Display
from time import sleep
from test_server import port

g = Guest()

g.connect("127.0.0.1", port)

print("connected")

g.auth("123")

while not g.authenticated:
    pass

def typed_new_message(text):
    print("typed_new_message:", text)
    g.send_message(text)

d = Display(g.send_message)
g.message_callback = d.new_message



d.run()
