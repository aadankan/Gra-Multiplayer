import pygame

bulletImg = pygame.image.load('bullet.png')


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 5

    def draw(self, win):
        win.blit(bulletImg, (self.x, self.y))

    def move(self):
        self.y -= self.vel
