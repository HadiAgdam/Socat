# ChatGPT generated

import curses
import threading
import time

queue = []

def add_text(win, text):
    try:
        queue.append(text)
        win.addstr(text + "\n")
        win.refresh()
    except:
        queue.pop(0)
        win.clear()
        for t in queue:
            win.addstr(t + "\n")
            win.refresh()

def listen_messages(chat_win, lock):
    messages = ["Hello!", "How are you?", "This is a test."]
    i = 0
    while True:
        with lock:
            add_text(chat_win, f"Friend: {messages[i % len(messages)]}")
        i += 1
        time.sleep(7)

def main(stdscr):
    curses.curs_set(1)
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    chat_win = curses.newwin(height - 3, width, 0, 0)
    input_win = curses.newwin(3, width, height - 3, 0)
    input_win.addstr("You: ")
    input_win.refresh()

    lock = threading.Lock()
    threading.Thread(target=listen_messages, args=(chat_win, lock), daemon=True).start()

    typed = ""

    while True:
        ch = input_win.getch()

        # ENTER key pressed
        if ch == 10:
            with lock:
                add_text(chat_win, f"You: {typed}")
            typed = ""
            input_win.clear()
            input_win.addstr("You: ")
            input_win.refresh()

        # BACKSPACE
        elif ch in (curses.KEY_BACKSPACE, 127):
            if len(typed) > 0:
                typed = typed[:-1]
                y, x = input_win.getyx()
                input_win.move(y, x - 1)
                input_win.delch()
                input_win.refresh()

        # Printable characters
        elif 32 <= ch <= 126:
            typed += chr(ch)
            input_win.addch(ch)
            input_win.refresh()

curses.wrapper(main)
