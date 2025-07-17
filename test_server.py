from server import Room
from display import Display

port = 8585

if __name__ == "__main__":
    r = Room("123")

    r.create(port)

    print("created")


    d = Display(r.send_server_message)
    r.message_callback = d.new_message

    d.run()