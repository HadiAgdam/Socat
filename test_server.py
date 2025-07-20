from server import Room
from display import Display

port = 8587

if __name__ == "__main__":
    r = Room("123")

    r.create(port)

    print("created")


    d = Display(r.send_server_message)
    r.message_callback = d.new_incoming_message
    r.status_callback = d.set_status

    d.run()