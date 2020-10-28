import pygame
from pygame import font
from pygame import mixer

from network import Network

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

width = 900
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("War in space")
background = pygame.image.load("background.png")

mixer.music.load("background.wav")
mixer.music.set_volume(0.1)
mixer.music.play(-1)


def redrawWindow(win, players, enemies, bullets, textsurface):
    win.blit(background, (0, 0))
    win.blit(textsurface, (0, 0))

    for player in players:
        player.draw(win)

    for enemy in enemies:
        enemy.draw(win)

    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


def main():
    run = True
    n = Network()
    connection = n.connection
    clock = pygame.time.Clock()

    bullet = False
    player = connection[0]
    enemies = connection[1]
    bullets_list = connection[2]
    bullets_obj = connection[3]
    points = connection[4]
    sounds = connection[5]

    bullet_cooldown = 0
    while run:
        textsurface = myfont.render("Points: " + str(points), False, (255, 255, 255))
        player2, enemies, bullets_list, bullets_obj, points, sounds = n.send((player, enemies, bullets_list, bullets_obj, points, sounds))
        if sounds == "explosion":
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.set_volume(0.1)
            explosionSound.play()
        clock.tick(60)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not bullet and bullet_cooldown == 0:
            bulletSound = mixer.Sound("laser.wav")
            bulletSound.set_volume(0.2)
            bulletSound.play()
            bullets_list.append(player.x)
            bullet_cooldown = 50

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        players = (player, player2)

        player.move()
        redrawWindow(win, players, enemies, bullets_obj, textsurface)


        if bullet_cooldown > 0:
            bullet_cooldown -= 1


main()
