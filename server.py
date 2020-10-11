import socket
import pickle
import threading
import random
import math

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


# Create enemy
def enemies_create():
    enemies.append(Enemy(random.randint(0, 700), random.choice((0, 64))))


# Detect collision between bullet and enemy
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Count of enemies
count_enemies = 7
# List of players (2 players with stable start position)
players = [Player(300, 480), Player(500, 480)]
# Create list of enemies to create later
enemies = []
# Loop to create enemies
for i in range(count_enemies):
    enemies_create()

# Combine players and enemies to easier sending in the future
scene = (players, enemies)

# Start value stan of the game (if doesn't exist black screen in client bcs data wasn't sent)
pause = False

def thread_client(conn, player):
    # Start data contains player and enemies
    start_data = scene[0][player], scene[1]
    # Sending start data
    conn.send(pickle.dumps(start_data))
    # Stable variable connected
    connected = True
    while connected:
        try:
            data = pickle.loads(conn.recv(2048))
            bullets = data[2]
            print(bullets)
            if data[0] != "pause":
                if not pause:
                    players[player] = data[0]

                    for enemy in enemies:
                        enemy.move()

                    for bullet in bullets:
                        bullet.move()

            if not data:
                print("Disconnected")
                break

            else:
                if player == 1:
                    reply = scene[0][0], enemies, bullets
                else:
                    reply = scene[0][1], enemies, bullets

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
