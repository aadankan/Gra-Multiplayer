import socket
import pickle
import threading
import random
import math

from player import Player
from enemy import Enemy
from bullet import Bullet


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
    if distance < 40:
        return True
    else:
        return False


bullets_obj = []
bullets_list = []
# Count of enemies
count_enemies = 7
# List of players (2 players with stable start position)
players = [Player(300, 480), Player(500, 480)]
# Create list of enemies to create later
enemies = []
# Loop to create enemies
for i in range(count_enemies):
    enemies_create()

points = 0
sounds = ""
# Combine players and enemies to easier sending in the future
scene = (players, enemies, bullets_list, bullets_obj, points, sounds)

bullets_v = []


def thread_client(conn, player):
    global sounds
    global points
    # Start data contains player and enemies
    start_data = scene[0][player], scene[1], scene[2], scene[3], scene[4], scene[5]
    # Sending start data
    conn.send(pickle.dumps(start_data))
    # Stable variable connected
    connected = True
    while connected:
        sounds = ""
        for bullet in bullets_obj:
            if bullet.y < 0:
                bullets_obj.remove(bullet)

        for bullet in bullets_obj:
            for enemy in enemies:
                if isCollision(enemy.x, enemy.y, bullet.x, bullet.y):
                    sounds = "explosion"
                    bullets_obj.remove(bullet)
                    enemies.remove(enemy)
                    points += 1

        if len(enemies) < 7:
            enemies_create()
        try:
            data = pickle.loads(conn.recv(2048))
            bullets_list = data[2]

            for bullet in bullets_obj:
                if bullet not in bullets_v:
                    bullets_v.append(bullet)
                    bullets_obj.append(bullet)

            players[player] = data[0]

            if len(bullets_list) > 0:
                for bullet in bullets_list:
                    bullets_list.remove(bullet)
                    bullets_obj.append(Bullet(bullet+15, 480-35))

            for enemy in enemies:
                enemy.move()

            for bullet in bullets_obj:
                bullet.move()

            if not data:
                print("Disconnected")
                break

            else:
                if player == 1:
                    reply = scene[0][0], enemies, bullets_list, bullets_obj, points, sounds
                else:
                    reply = scene[0][1], enemies, bullets_list, bullets_obj, points, sounds

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
