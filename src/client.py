import pygame
from network import Network
from test_player import Player

width = 860
height = 480
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


def redrawWindow(win, players, player_id):
    win.fill((255, 255, 255))
    for idx, player in enumerate(players):
        # Set the controlled player's color to green, others to red
        player.color = (0, 255, 0) if idx == player_id else (255, 0, 0)
        player.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    player_id = n.player_id  # Get assigned player ID
    players = n.get_players()
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        players = n.send(players[player_id])  # Update this client's player data

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        players[player_id].move()
        redrawWindow(win, players, player_id)


main()
