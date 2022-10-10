from random import randint
import pygame as pygame
from network import Network
from game import Game
pygame.font.init()

# TilesX = 10
# TilesY = 10
# numOfPlayers = 3
# currentPlayer = 1  # sets current player to player 1 initially

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_GREY = (226, 226, 226)

WINDOW_HEIGHT = 900
WINDOW_WIDTH = 1200

pygame.display.set_caption("Minesweeper")

FPS = 60

BOARD_X_OFFSET = 400
BOARD_Y_OFFSET = 100

BLOCK_SIZE = 30

# GAME_HEIGHT = TilesY * BLOCK_SIZE  # used to check board isn't bigger than window height
# GAME_WIDTH = TilesX * BLOCK_SIZE  # used to check board isn't bigger than window width

# numOfFlags = 25
# flagsFound = 0

# WINNING_SCORE = int(numOfFlags/2) + 1

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

scorefont = pygame.font.SysFont("comic sans", 25)
piecefont = pygame.font.SysFont("monospace", 20)

# flags = []  # flag positions
# board = [[0 for j in range(TilesY)] for i in range(TilesX)]  # creating 2d array to match grid, to store board in
# boardState = [[0 for k in range(TilesY)] for n in range(TilesX)]  # creating 2d array to match grid
# to store board state in
# playerScores = {}  # dictionary
# scoresText = []  # stores the score strings


# def drawScores():  # fix, get info from server
#     rect = pygame.Rect(80, 80, 320, 600)  # area of the screen where the score goes
#     pygame.draw.rect(SCREEN, WHITE, rect)  # making it blank again so the score doesn't write on top of each other
#     y = 200
#     for x in range(0, numOfPlayers, 1):
#         playerText = scorefont.render(scoresText[x], True, BLACK)
#         SCREEN.blit(playerText, (100, y))
#
#         y += 100

# def drawGrid():
#     for x in range(BOARD_X_OFFSET, (BLOCK_SIZE * TilesX) + BOARD_X_OFFSET, BLOCK_SIZE):
#         for y in range(BOARD_Y_OFFSET, (BLOCK_SIZE * TilesY) + BOARD_Y_OFFSET, BLOCK_SIZE):
#             rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
#             pygame.draw.rect(SCREEN, BLACK, rect, 1)

def main():
    pygame.init()
    n = Network()

    clock = pygame.time.Clock()
    SCREEN.fill(WHITE)
    player = int(n.getP())
    print("You are player", player)

    # drawGrid()  # maybe move to while true loop below, or update cell independantly

    while True:  # game loop
        clock.tick(FPS)
        try:
            pass
            # game = n.send("get")
        except:
            break

        # drawScores()
        #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = (event.pos[0], event.pos[1])
                # checkIfFlag(mouseX, mouseY, currentPlayer)
        # flagsRemainingText = scorefont.render(f'Found {flagsFound} out of {numOfFlags} flags', True, BLACK)
        # SCREEN.blit(flagsRemainingText, (100, 100))
        #
        # xpos = 90
        # ypos = 195 + (currentPlayer - 1) * 100
        # border = pygame.Rect(xpos, ypos, 280, 50)
        # pygame.draw.rect(SCREEN, BLACK, border, 3)
        pygame.display.update()


if __name__ == "__main__":
    main()
