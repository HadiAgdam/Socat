# DeepSeek generated

import curses
import threading
import time
from datetime import datetime

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
            try:
                win.addstr(t + "\n")
            except curses.error:
                pass
        win.refresh()

def update_status(win, text, width):
    win.erase()
    win.bkgd(' ', curses.color_pair(1))
    display_text = f" {text} "
    if len(display_text) > width:
        display_text = display_text[:width-3] + "..."
    try:
        win.addstr(0, 0, display_text.ljust(width)[:width], curses.color_pair(1))
    except curses.error:
        pass
    win.refresh()

def draw_bordered_window(win, width, height, title=""):
    win.border()
    if title:
        try:
            win.addstr(0, 2, f" {title} ")
        except curses.error:
            pass

def listen_messages(chat_win, status_win, lock, width):
    messages = ["Hello!", "How are you?", "This is a test."]
    i = 0
    while True:
        timestamp = datetime.now().strftime("%H:%M:%S")
        with lock:
            add_text(chat_win, f"[{timestamp}] Friend: {messages[i % len(messages)]}")
            update_status(status_win, f"Chat App | Last: {timestamp}", width)
        i += 1
        time.sleep(7)

def main(stdscr):
    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    curses.curs_set(1)
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Calculate window sizes
    status_height = 1
    input_height = 3
    user_info_height = 5  # Height for the new user info section
    chat_height = height - status_height - input_height - user_info_height

    # Create windows
    status_win = curses.newwin(status_height, width, 0, 0)
    chat_win = curses.newwin(chat_height, width, status_height, 0)
    user_win = curses.newwin(user_info_height, width, status_height + chat_height, 0)
    input_win = curses.newwin(input_height, width, height - input_height, 0)

    # Enable scrolling for chat window
    chat_win.scrollok(True)
    chat_win.idlok(True)
    
    # Draw initial UI
    update_status(status_win, "Chat App | Ready", width)
    
    # Draw bordered user info window
    draw_bordered_window(user_win, width, user_info_height, "")
    user_win.addstr(1, 2, "Name: John Doe")
    user_win.addstr(2, 2, "Status: Online")
    user_win.addstr(3, 2, "Last active: Now")
    user_win.refresh()
    
    input_win.addstr(0, 0, "You: ")
    input_win.refresh()

    lock = threading.Lock()
    threading.Thread(target=listen_messages, 
                   args=(chat_win, status_win, lock, width), 
                   daemon=True).start()

    typed = ""

    while True:
        try:
            ch = input_win.getch()

            if ch == 10:  # ENTER
                if typed.strip():
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    with lock:
                        add_text(chat_win, f"[{timestamp}] You: {typed}")
                        update_status(status_win, f"Chat App | Sent: {timestamp}", width)
                    typed = ""
                    input_win.clear()
                    input_win.addstr(0, 0, "You: ")
                    input_win.refresh()

            elif ch in (curses.KEY_BACKSPACE, 127):  # BACKSPACE
                if len(typed) > 0:
                    typed = typed[:-1]
                    y, x = input_win.getyx()
                    input_win.move(y, x - 1)
                    input_win.delch()
                    input_win.refresh()

            elif 32 <= ch <= 126:  # Printable characters
                typed += chr(ch)
                input_win.addch(ch)
                input_win.refresh()
        except curses.error:
            pass

if __name__ == "__main__":
    curses.wrapper(main)