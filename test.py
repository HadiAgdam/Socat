from display import Display
from threading import Thread
from time import sleep


d = Display(None)

def send_message(text: str):
    d.new_message("text: " + text)

def mock_incoming_message():
    while True:
        sleep(2)
        d.new_message('thread')

d.on_send_message = send_message

t = Thread(target=mock_incoming_message)
t.start()

d.run()



