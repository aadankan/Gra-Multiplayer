import pygame

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
    run = True
    n = Network()
    connection = n.connection
    clock = pygame.time.Clock()

    player = connection[0]
    while run:
        enemies = connection[1]
        clock.tick(60)
        player2, enemies = n.send((player, enemies))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        players = (player, player2)
        player.move()
        redrawWindow(win, players, enemies)


main()
