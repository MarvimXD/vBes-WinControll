
from getpass import getuser
import getpass
from pathlib import Path
from PySimpleGUI import PySimpleGUI as sg
import os
from subprocess import Popen
import subprocess as sp
import socket
import keyboard
import time


def autoInit():

    sg.theme('Dark')
    sg.theme_button_color(('black', 'white'))

    layout = [
        [sg.Text('Processos de Automatização')],
        [sg.Text('')],
        [sg.Button('Liberar Porta no Firewall', key='btnPorta', size=(20, 1))]
    ]

    janela = sg.Window('Automatização', layout, size=(250,200), finalize=True)

    while True:
        event, val = janela.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'btnPorta':
            firewallPorta()


def firewallPorta():
    sg.theme('Dark')
    sg.theme_button_color(('black', 'white'))

    layout = [
        [sg.Text('Liberar Porta no Firewall')],
        [sg.Text('')],
        [sg.Text('Nome da Regra (Entrada e Saída):')],
        [sg.Input(key='inpNome')],
        [sg.Text('Protocolo:')],
        [sg.Input('TCP', key='inpProto')],
        [sg.Text('Porta:')],
        [sg.Input(key='inpPorta')],
        [sg.Text('')],
        [sg.Button('Liberar', key='btnCmd', size=(20, 1))]
    ]

    janela = sg.Window('Automatização', layout, size=(250,300), finalize=True)

    while True:
        event, val = janela.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'btnCmd':
            nome = val['inpNome']
            porta = val['inpPorta']
            proto = val['inpProto']
            user = os.getlogin()
            domain = getpass.getuser() + '@' + os.environ['userdomain']
            print(domain)
            exit()
            command = "netsh advfirewall firewall add rule name="+ nome +" protocol="+ proto +" dir=in localport="+ porta +" action=allow"
            with open('build/cache/firewall.bat', 'w') as arquivo:
                arquivo.write(command)
            
            sg.popup("Liberada!")

firewallPorta()