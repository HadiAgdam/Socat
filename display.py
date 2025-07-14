from curses import newwin, KEY_BACKSPACE, wrapper, curs_set


class Display:

    queue = []

    def __init__(self, on_send_message):
        self.on_send_message = on_send_message

    def new_message(self, text: str):
        self.__add_text(text)

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
        curs_set(1)
        stdscr.clear()

        height, width = stdscr.getmaxyx()

        self.chat_win = newwin(height - 3, width, 0, 0)
        self.input_win = newwin(3, width, height - 3, 0)
        self.input_win.addstr("You: ")
        self.input_win.refresh()

        typed = ""
        

        while True:
            ch = self.input_win.getch()

            # ENTER key pressed
            if ch == 10:
                self.on_send_message(typed)
                self.__add_text(f"You: {typed}")
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