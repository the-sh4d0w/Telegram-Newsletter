import json
import tkinter
import telepot
from telepot.loop import MessageLoop


def addnew(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg["text"])
    if msg["text"] == ("/start" or "START"):
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
        label.pack()
        text = tkinter.Text(master=popup, width=75, height=3)
        text.pack(side=tkinter.LEFT)
        button = tkinter.Button(master=popup, text="Senden",
                                command=x, width=10, height=1)
        button.pack(side=tkinter.RIGHT)


def send_messages():
    text = message.get("1.0", tkinter.END)
    message.delete("1.0", tkinter.END)
    NewsletterBot = telepot.Bot(config["token"])
    for user in users:
        try:
            NewsletterBot.sendMessage(user, text)
        except:
            pass


with open("config.json", "r") as f:
    config = json.loads(f.read())
users = config["users"]

NewsletterBot = telepot.Bot(config["token"])
MessageLoop(NewsletterBot, addnew).run_as_thread()

root = tkinter.Tk()
root.title("Newsletter")
root.geometry("700x200")
root.resizable(False, False)
message = tkinter.Text(master=root, width=75, height=5)
message.pack(side=tkinter.LEFT)
send = tkinter.Button(master=root, text="Senden",
                      command=send_messages, width=10, height=1)
send.pack(side=tkinter.RIGHT)
root.mainloop()
with open("config.json", "w") as f:
    f.write(json.dumps({
        "token": config['token'],
        "users": users
    }))
