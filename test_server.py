from server import Room
from display import Display


r = Room("123")

r.create(8980)

print("created")


d = Display(r.send_message)
r.message_callback = d.new_message

d.run()