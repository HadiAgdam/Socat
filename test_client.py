from client import Guest
from display import Display

g = Guest()

g.connect("127.0.0.1", 8980)

print("connected")

g.auth("123")


d = Display(g.send_message)
g.message_callback = d.new_message


d.run()
