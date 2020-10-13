import pygame

from network import Network

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
    run = True
    n = Network()
    connection = n.connection
    clock = pygame.time.Clock()

    bullet = False
    player = connection[0]
    enemies = connection[1]
    bullets_list = connection[2]
    bullets_obj = connection[3]

    bullet_cooldown = 0
    while run:
        player2, enemies, bullets_list, bullets_obj = n.send((player, enemies, bullets_list, bullets_obj))
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
        redrawWindow(win, players, enemies, bullets_obj)

        if bullet_cooldown > 0:
            bullet_cooldown -= 1


main()
