from player import Player
from enemy import Enemy

class Scene:
    def __init__(self, x, y):
        self.players = Player(x, y)
        self.enemies = Enemy(x, y)