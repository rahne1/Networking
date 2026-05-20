import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("", 8128))
while True:
    chat = input("Input a chat message: ")
    s.send(chat.encode())
