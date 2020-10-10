import pygame


pygame.init()
playerImg = pygame.image.load('space.png')

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 4

    def draw(self, win):
        win.blit(playerImg, (self.x, self.y))

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.x > 0:
                self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            if self.x < 836:
                self.x += self.vel

