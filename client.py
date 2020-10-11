import pygame
import keyboard

from network import Network
from bullet import Bullet

pygame.init()

width = 900
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("War in space")
background = pygame.image.load("background.png")


def redrawWindow(win, players, enemies, bullets):
    win.blit(background, (0, 0))

    for player in players:
        player.draw(win)

    for enemy in enemies:
        enemy.draw(win)

    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


def main():
    pause = False
    run = True
    n = Network()
    connection = n.connection
    clock = pygame.time.Clock()

    bullet = False
    bullets = []
    player = connection[0]
    enemies = connection[1]

    pause_cooldown = 0
    bullet_cooldown = 0
    start_pause = 1
    while run:
        clock.tick(60)
        if keyboard.get_hotkey_name() == "esc" and not pause and pause_cooldown == 0:
            pause = True
            pause_cooldown = 10

        elif keyboard.get_hotkey_name() == "esc" and pause and pause_cooldown == 0:
            pause = False
            pause_cooldown = 10

        if keyboard.get_hotkey_name() == "space" and not bullet and bullet_cooldown == 0:
            bullets.append(Bullet(player.x+15, player.y-3))
            bullet_cooldown = 50

        if not pause:
            player2, enemies, bullets = n.send((player, enemies, bullets))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        players = (player, player2)

        # Pause
        if not pause:
            player.move()
        redrawWindow(win, players, enemies, bullets)

        if pause_cooldown > 0:
            pause_cooldown -= 1

        if start_pause == 1:
            pause = True
            start_pause = 0

        if bullet_cooldown > 0:
            bullet_cooldown -= 1


main()
