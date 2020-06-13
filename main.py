import json
import os
import threading
import time
import tkinter

import telepot
from telepot.loop import MessageLoop


def addnew(msg: str) -> None:
    """Listens for messages and ...

    ... adds new user.
    ... removes user.
    """
    _, _, chat_id = telepot.glance(msg)
    if msg["text"] == "/start" or msg["text"] == "START":
        if not chat_id in users:
            users.append(chat_id)
            NewsletterBot.sendMessage(
                chat_id, "Vielen Dank für die Anmeldung bei unserem Newsletter.\nEine Abmeldung ist jederzeit durch das Senden von 'STOPP' möglich.")
        else:
            NewsletterBot.sendMessage(
                chat_id, "Sie sind schon bei unserem Newsletter angemeldet.\nEin Abmeldung ist jederzeit duch das Senden von 'STOPP' möglich.")
    elif msg["text"] == "STOPP":
        if chat_id in users:
            users.remove(chat_id)
            NewsletterBot.sendMessage(
                chat_id, "Sie wurden hiermit von unserem Newsletter abgemeldet.\nEine Anmeldung ist jederzeit durch das Senden von 'START' möglich.")
        else:
            NewsletterBot.sendMessage(
                chat_id, "Sie scheinen nicht bei unserem Newsletter angemeldet zu sein.\nEine Anmeldung ist jederzeit durch das Senden von 'START' möglich.")
    else:
        def x():
            txt = text.get("1.0", tkinter.END)
            text.delete("1.0", tkinter.END)
            try:
                NewsletterBot.sendMessage(chat_id, txt)
            except:
                pass
            popup.destroy()
        popup = tkinter.Toplevel()
        popup.title("Nachricht")
        label = tkinter.Label(
            master=popup, text=msg["text"], width=75, height=5)
        text = tkinter.Text(master=popup, width=75, height=3)
        button = tkinter.Button(
            master=popup, text="Senden", command=x, width=10, height=1)
        label.pack()
        text.pack(side=tkinter.LEFT)
        button.pack(side=tkinter.RIGHT)


def send_plan_message(time_: int, text: str) -> None:
    """Sleeps for a given time, then sends the given message to all users."""
    time.sleep(time_)
    for user in users:
        try:
            NewsletterBot.sendMessage(user, text)
        except Exception as e:
            print(e)


def plan_message() -> None:
    """Opens a popup that asks for the time."""
    def x():
        time_ = int(time_input.get("1.0", tkinter.END)) * 60
        threading.Thread(target=send_plan_message, args=(time_, text)).start()
        popup.destroy()
    text = message.get("1.0", tkinter.END)
    message.delete("1.0", tkinter.END)
    popup = tkinter.Tk("Zeit in Minuten")
    time_input = tkinter.Text(master=popup, width=10, height=1)
    send_button = tkinter.Button(
        master=popup, text="Senden", command=x, width=10, height=1)
    time_input.pack()
    send_button.pack(side=tkinter.BOTTOM)


def send_message() -> None:
    """Sends a message to all users."""
    text = message.get("1.0", tkinter.END)
    message.delete("1.0", tkinter.END)
    NewsletterBot = telepot.Bot(config["token"])
    for user in users:
        try:
            NewsletterBot.sendMessage(user, text)
        except:
            pass


CONFIG = "config.json"

# asks for a token if config file doesn't exist
if not os.path.isfile(CONFIG):
    def do():
        text = token.get("1.0", tkinter.END)
        token.delete("1.0", tkinter.END)
        token_ = text.replace("\n", "")
        popup.destroy()
        with open(CONFIG, "w") as f:
            f.write(json.dumps({"token": token_, "users": []}))
    popup = tkinter.Tk("Token hinzufügen")
    token = tkinter.Text(master=popup, width=30, height=1)
    token.pack(side=tkinter.LEFT)
    add = tkinter.Button(master=popup, text="Hinzufügen",
                         command=do, width=15, height=1)
    add.pack(side=tkinter.RIGHT)
    popup.mainloop()

# gets the Bot's token and all registerd users
with open(CONFIG, "r") as f:
    config = json.loads(f.read())
users = config["users"]
token = config["token"]

# starts the loop to add and delete users
NewsletterBot = telepot.Bot(token)
MessageLoop(NewsletterBot, addnew).run_as_thread()

# starts main gui
root = tkinter.Tk("Newsletter")
root.resizable(False, False)
message = tkinter.Text(master=root, width=50, height=10)
plan_button = tkinter.Button(
    master=root, text="Planen", command=plan_message, width=10, height=1)
send_button = tkinter.Button(
    master=root, text="Senden", command=send_message, width=10, height=1)
message.pack(side=tkinter.LEFT, anchor=tkinter.N)
plan_button.pack(side=tkinter.TOP, anchor=tkinter.E)
send_button.pack(side=tkinter.TOP, anchor=tkinter.E)
root.mainloop()

# saves data in the file config.json
with open(CONFIG, "w") as f:
    f.write(json.dumps(config))
quit()
