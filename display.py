from curses import newwin, KEY_BACKSPACE, wrapper, curs_set, color_pair, start_color, init_pair, COLOR_BLACK, COLOR_WHITE
from utils import encode, decode
from datetime import datetime


class Display:

    queue = []

    def __get_current_time(self) -> str:
        return datetime.now().strftime("%I:%M:%S")

    def __init__(self, on_send_message):
        self.on_send_message = on_send_message
    

    def set_status(self, text: str):
        self.status_win.erase()
        self.status_win.bkgd(' ', color_pair(1))
        self.status_win.addstr(0, 0, text, color_pair(1))
        self.status_win.refresh()

    def new_incoming_message(self, text: str):
        command = text.split(":")[0]
        text = text[len(command) + 1:]
        match (command):
            case "public_message":
                role, username, id, text = text.split(":")

                role = decode(role)
                username = decode(username)
                id = decode(id)
                text = decode(text)

                # [2025/6/15 4:58pm] (127.0.0.1) <guest> user1 ▶ Hello This is some fucking text
                self.__add_text(f"[{self.__get_current_time()}] ({id}) <{role}> {username} ▶ {text}")

            case "log":
                self.__add_text(f"[{self.__get_current_time()}] ROOM ▶ {decode(text)}")


    def __add_text(self, text):
        try:
            self.queue.append(text)
            self.chat_win.addstr(text + "\n")
            self.chat_win.refresh()
        except:
            self.queue.pop(0)
            self.chat_win.clear()
            for t in self.queue:
                self.chat_win.addstr(t + "\n")
                self.chat_win.refresh()
    

    def __main(self, stdscr):
        start_color()
        init_pair(1, COLOR_BLACK, COLOR_WHITE)
        curs_set(1)
        stdscr.clear()


        self.height, self.width = stdscr.getmaxyx()
        status_height = 1
        input_height = 3
        chat_height = self.height - status_height - input_height

        self.status_win = newwin(status_height, self.width, 0, 0)
        self.chat_win = newwin(chat_height, self.width, status_height, 0)
        self.input_win = newwin(input_height, self.width, self.height - input_height, 0)

        self.input_win.addstr("You: ")
        self.input_win.refresh()

        typed = ""
        
        self.set_status("")

        while True:
            ch = self.input_win.getch()

            # ENTER key pressed
            if ch == 10:
                self.on_send_message(typed)
                typed = ""
                self.input_win.clear()
                self.input_win.addstr("You: ")
                self.input_win.refresh()

            # BACKSPACE
            elif ch in (KEY_BACKSPACE, 127):
                if len(typed) > 0:
                    typed = typed[:-1]
                    y, x = self.input_win.getyx()
                    self.input_win.move(y, x - 1)
                    self.input_win.delch()
                    self.input_win.refresh()

            # Printable characters
            elif 32 <= ch <= 126:
                typed += chr(ch)
                self.input_win.addch(ch)
                self.input_win.refresh()

    def run(self):
        wrapper(lambda stdscr: self.__main(stdscr))