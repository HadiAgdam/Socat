from network.server import Room
from network.client import Guest
from time import sleep

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
                room.create(port)
            except Exception as ex:
                print("Feild to create room:", ex)
            
            if room.is_up:
                print("Created room successfully!")
                break

            print("Retrying....")
            sleep(2)
        

        # successfully created a room

        

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

        