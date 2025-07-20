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
    sleep(1)

def typed_new_message(text):
    log("typed new message in client: " + text)
    g.send_message(text)
    print("typed new message in client: ", text)

d = Display(typed_new_message)
g.message_callback = d.new_incoming_message
def set_status(status: str, ping: int):
    d.set_status(status, g.room_ip, ping)
        
g.report_status = set_status
print('here')

d.run()
