import socket
import pickle
import threading
import random

from player import Player
from enemy import Enemy

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

s.listen(2)
print("Waiting for connection, Server has already started")

count_enemies = 5
players = [Player(300, 480), Player(500, 480)]
enemies = []
for i in range(count_enemies):
    enemies.append(Enemy(random.randint(0, 700), random.choice((0, 64))))

scene = (players, enemies)

pause = False

def thread_client(conn, player):
    start_data = scene[0][player], scene[1]
    conn.send(pickle.dumps(start_data))
    connected = True
    while connected:

        try:
            data = pickle.loads(conn.recv(2048))
            if data[0] != "pause":
                if not pause:
                    players[player] = data[0]

                    for enemy in enemies:
                        enemy.move()

            if not data:
                print("Disconnected")
                break

            else:
                if player == 1:
                    reply = scene[0][0], enemies
                else:
                    reply = scene[0][1], enemies

            conn.send(pickle.dumps(reply))

        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    thread = threading.Thread(target=thread_client, args=(conn, currentPlayer))
    thread.start()
    currentPlayer += 1
