import pygame


pygame.init()
enemyImg = pygame.image.load('enemy.png')


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 4

    def draw(self, win):
        win.blit(enemyImg, (self.x, self.y))

    def move(self):
        self.x += self.vel
        if self.x <= 0:
            self.vel = 2
            self.y += 32
        elif self.x >= 836:
            self.vel = -2
            self.y += 30
