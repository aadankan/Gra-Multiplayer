import pygame
import keyboard

from network import Network

pygame.init()

width = 900
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("War in space")
background = pygame.image.load("background.png")


def redrawWindow(win, players, enemies):
    win.blit(background, (0, 0))

    for player in players:
        player.draw(win)

    for enemy in enemies:
        enemy.draw(win)

    pygame.display.update()


def main():
    pause = False
    run = True
    n = Network()
    connection = n.connection
    clock = pygame.time.Clock()

    player = connection[0]
    enemies = connection[1]

    cooldown = 0
    start_pause = 1
    while run:
        clock.tick(60)
        if keyboard.get_hotkey_name() == "esc" and not pause and cooldown == 0:
            pause = True
            cooldown = 10

        elif keyboard.get_hotkey_name() == "esc" and pause and cooldown == 0:
            pause = False
            cooldown = 10

        if not pause:
            player2, enemies = n.send((player, enemies))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        players = (player, player2)
        player.move()
        redrawWindow(win, players, enemies)

        if cooldown > 0:
            cooldown -= 1

        if start_pause == 1:
            pause = True
            start_pause = 0
main()
