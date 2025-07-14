from client import Guest

g = Guest()

g.connect("127.0.0.1", 8787)

print("connected")

g.auth("123")



