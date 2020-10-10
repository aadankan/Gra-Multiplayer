import socket
import pickle
import threading

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = "UTF-8"
DISCONNECT_MESSAGE = "!DISCONNECTED"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind(ADDR)
except socket.error as e:
    str(e)

s.listen()
print("Waiting for connection, Server has already started")


def thread_client(conn, player):
    connected = True
    while connected:
        data = pickle.loads(conn.recv(2048))
        print(data)


while True:
    conn, addr = s.accept()
    thread = threading.Thread(target=thread_client, args=(conn, addr))
    thread.start()

