import pygame
from pygame import font

from network import Network

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

width = 900
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("War in space")
background = pygame.image.load("background.png")


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

    bullet_cooldown = 0
    while run:
        textsurface = myfont.render("Points: " + str(points), False, (255, 255, 255))
        player2, enemies, bullets_list, bullets_obj, points = n.send((player, enemies, bullets_list, bullets_obj, points))
        clock.tick(60)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and not bullet and bullet_cooldown == 0:
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
