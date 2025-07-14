from server import Room
from client import Guest
from time import sleep
from display import Display

# room -> server
# guest -> client

if __name__ == "__main__":
    print("Welcome to Socat!")
    choice = input("If you want to create room enter 1, if you want to join as guest enter 2 (1 / 2): ")

    if choice == "1":
        password = input("Enter the password of the room: ")
        room = Room(password)

        while True:
            port = int(input("Enter the port: "))
            try:
                ip = room.create(port)
                print("created room at:", ip)
            except Exception as ex:
                print("Feild to create room:", ex)
            
            if room.is_up:
                print("Created room successfully!")
                break

            print("Retrying....")
            sleep(2)
        
        d = Display(room.send_message)
        d.run()

        room.message_callback = d.new_message

        

    elif choice == "2":

        guest = Guest()

        while True:
            ip, port = input("Enter the IP of the room (example 127.0.0.1:8080): ").split(":")
            

            print("Connecting...")
            try:
                guest.connect(ip, port)
            except Exception as ex:
                print("Failed to connect:", ex)
                continue
            if guest.connected:
                print("Connected successfully!")
                break
        

        while True:
            password = input("Enter the password of the room: ")

            guest.auth(password)
            if guest.authenticated:
                print("Authenticated successfully!")
                break
            print("Auth failed!")
        

        d = Display(guest.send_message)
        d.run()

        guest.message_callback = d.new_message
    

        