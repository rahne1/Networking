import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 8128))
s.listen(5)
conn, addr = s.accept()
while True:
    output = conn.recv(2048)
    print(output.decode())
    if not output:
        break
