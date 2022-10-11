import pickle
from random import randint
import pygame as pygame
from network import Network
import time
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

game_data = {}

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

def drawGrid(board, boardState, TilesX, TilesY):
    rect = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(SCREEN, WHITE, rect)
    currentX = 0
    currentY = 0
    for x in range(BOARD_X_OFFSET, (BLOCK_SIZE * TilesX) + BOARD_X_OFFSET, BLOCK_SIZE):
        currentY = 0
        # print(f'current X: {currentX}')
        for y in range(BOARD_Y_OFFSET, (BLOCK_SIZE * TilesY) + BOARD_Y_OFFSET, BLOCK_SIZE):
            # print(f'current Y: {currentY}')
            startX = BOARD_X_OFFSET + (BLOCK_SIZE * currentX)
            startY = BOARD_Y_OFFSET + (BLOCK_SIZE * currentY)

            if boardState[currentX][currentY] == 0:  # tile not played yet and needs to be hidden
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(SCREEN, BLACK, rect, 1)
            else:  # tile played and can be shown to players
                number = str(board[currentX][currentY])
                if board[currentX][currentY] == 10:  # indicates flag in tile
                    rect = pygame.Rect(startX, startY, BLOCK_SIZE, BLOCK_SIZE)
                    border = pygame.Rect(startX, startY, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(SCREEN, RED, rect)
                    pygame.draw.rect(SCREEN, BLACK, border, 1)
                elif board[currentX][currentY] != 0:  # display number of adjacent flags with number printed in piece
                    pieceText = piecefont.render(number, True, BLACK)
                    SCREEN.blit(pieceText, (startX + 9, startY + 4))
                    border = pygame.Rect(startX, startY, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(SCREEN, BLACK, border, 1)
                else:  # empty square with no flags around
                    rect = pygame.Rect(startX, startY, BLOCK_SIZE, BLOCK_SIZE)
                    border = pygame.Rect(startX, startY, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(SCREEN, LIGHT_GREY, rect)
                    pygame.draw.rect(SCREEN, BLACK, border, 1)
            currentY += 1
        currentX += 1


def checkIfValidMove(mouseX, mouseY, n, TilesX, TilesY):
    # global board, boardState,
    tileX = int((mouseX - BOARD_X_OFFSET) / BLOCK_SIZE)
    tileY = int((mouseY - BOARD_Y_OFFSET) / BLOCK_SIZE)
    startX = BOARD_X_OFFSET + (tileX * BLOCK_SIZE)
    startY = BOARD_Y_OFFSET + (tileY * BLOCK_SIZE)
    xcheck = BOARD_X_OFFSET < mouseX < BOARD_X_OFFSET + (BLOCK_SIZE * TilesX)  # get TilesX from server
    ycheck = BOARD_Y_OFFSET < mouseY < BOARD_Y_OFFSET + (BLOCK_SIZE * TilesY)  # get TilesY from server

    if xcheck and ycheck:  # checking that player clicked within the board area
        global game_data
        game_data = n.send(f'{tileX},{tileY}')  # send server board co-ordinate of clicked tile
        print(game_data)
        board = game_data['board']
        boardState = game_data['boardState']
        tilesX = game_data['TilesX']
        tilesY = game_data['TilesY']
        drawGrid(board, boardState, tilesX, tilesY)
        # return True  # if player clicked within board boundaries then move is valid
        # board = game_data['board']
        # boardState = game_data['boardState']
        # tilesX = game_data['TilesX']
        # tilesY = game_data['TilesY']
        # playerScores = game_data['playerScores']
        # currentPlayer = game_data['currentPlayer']
        # flagsFound = game_data['flagsFound']
        #
        # print(board)
        # print(boardState)
        # print(tilesX)
        # print(tilesY)
        # print(playerScores)
        # print(currentPlayer)
        # print(flagsFound)

def refreshGame(n):
    global game_data
    game_data = n.send("-1,-1")  # dummy data
    print(game_data)
    board = game_data['board']
    boardState = game_data['boardState']
    tilesX = game_data['TilesX']
    tilesY = game_data['TilesY']
    drawGrid(board, boardState, tilesX, tilesY)
    time.sleep(0.05)


def main():
    pygame.init()
    n = Network()

    clock = pygame.time.Clock()
    SCREEN.fill(WHITE)
    # player = int(n.getP())
    # print("You are player", player)

    game_data = n.send("-1,-1")
    print(game_data)

    board = game_data['board']
    boardState = game_data['boardState']
    tilesX = game_data['TilesX']
    tilesY = game_data['TilesY']
    playerScores = game_data['playerScores']
    currentPlayer = game_data['currentPlayer']
    flagsFound = game_data['flagsFound']

    print(board)
    print(boardState)
    print(tilesX)
    print(tilesY)
    print(playerScores)
    print(currentPlayer)
    print(flagsFound)

    drawGrid(board, boardState, tilesX, tilesY)  # initially draw grid

    while True:  # game loop
        clock.tick(FPS)
        try:
            pass
            # game = n.send("get")
        except:
            break

        refreshGame(n)  # refresh game every 0.5 seconds for players
        # drawScores()
        #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = (event.pos[0], event.pos[1])
                checkIfValidMove(mouseX, mouseY, n, tilesX, tilesY)
                # if validMove == True:
                #     print(game_data)
                #     drawGrid(board, boardState, tilesX, tilesY)
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
