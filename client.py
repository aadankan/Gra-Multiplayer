import socket
import pickle

PORT = 5050
FORMAT = "UTF-8"
DISCONNECT_MESSAGE = "!DISCONNECTED"
SERVER = "217.144.222.58"
ADDR = (SERVER, PORT)


c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(ADDR)

def msg_send(msg):
    c.send(pickle.dumps(msg))

while True:
    msg = input("MSG: ")
    msg_send(msg)
