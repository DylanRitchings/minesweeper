from random import randint
import sys
import pygame as pygame

pygame.font.init()

TilesX = 10
TilesY = 10
numOfPlayers = 3
currentPlayer = 1  # sets current player to player 1 initially

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

GAME_HEIGHT = TilesY * BLOCK_SIZE  # used to check board isn't bigger than window height
GAME_WIDTH = TilesX * BLOCK_SIZE  # used to check board isn't bigger than window width

numOfFlags = 25
flagsFound = 0

WINNING_SCORE = int(numOfFlags/2) + 1

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

scorefont = pygame.font.SysFont("comic sans", 25)
piecefont = pygame.font.SysFont("monospace", 20)

flags = []  # flag positions
board = [[0 for j in range(TilesY)] for i in range(TilesX)]  # creating 2d array to match grid, to store board in
boardState = [[0 for k in range(TilesY)] for n in range(TilesX)]  # creating 2d array to match grid
# to store board state in
playerScores = {}  # dictionary
scoresText = []  # stores the score strings


def createFlags(numOfFlags,TilesX,TilesY):
    for n in range(numOfFlags):
        newFlagPlaced = False
        while not newFlagPlaced:
            x = randint(0,TilesX-1)
            y = randint(0,TilesY-1)
            if [x, y] not in flags:
                flags.append([x, y])
                board[x][y] = 10
                newFlagPlaced = True



def updateCurrentPlayer():
    global currentPlayer
    if currentPlayer < numOfPlayers:  # e.g 3 players, p1 and p2 would be true, p3 would not
        currentPlayer += 1  # add 1 to current player
    else:
        currentPlayer = 1  # reset to player 1


def checkIfFlag(mouseX, mouseY, currentPlayer):

    global flagsFound
    tileX = int((mouseX - BOARD_X_OFFSET)/BLOCK_SIZE)
    tileY = int((mouseY - BOARD_Y_OFFSET)/BLOCK_SIZE)
    startX = BOARD_X_OFFSET + (tileX * BLOCK_SIZE)
    startY = BOARD_Y_OFFSET + (tileY * BLOCK_SIZE)
    xcheck = BOARD_X_OFFSET < mouseX < BOARD_X_OFFSET + (BLOCK_SIZE * TilesX)
    ycheck = BOARD_Y_OFFSET < mouseY < BOARD_Y_OFFSET + (BLOCK_SIZE * TilesY)

    if xcheck and ycheck:  # checking that player clicked within the board area
        if boardState[tileX][tileY] == 0:  # if 0 then piece is not yet clicked on, else it's already been played
            if board[tileX][tileY] == 10:
                rect = pygame.Rect(startX, startY, BLOCK_SIZE, BLOCK_SIZE)
                border = pygame.Rect(startX, startY, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(SCREEN, RED, rect)
                pygame.draw.rect(SCREEN, BLACK, border, 1)
                playerScores[currentPlayer - 1]['score'] += 1
                scoresText[currentPlayer - 1] = f"{playerScores[currentPlayer - 1]['name']} score - {playerScores[currentPlayer - 1]['score']}"
                flagsFound += 1
            else:  # print number of adjacent flags , and update current player to next player
                updateCurrentPlayer()
                number = str(board[tileX][tileY])
                if board[tileX][tileY] != 0:  # display number of adjacent flags with number printed in piece
                    pieceText = piecefont.render(number, True, BLACK)
                    SCREEN.blit(pieceText, (startX + 9, startY + 4))
                else:  # empty square with no flags around
                    rect = pygame.Rect(startX, startY, BLOCK_SIZE, BLOCK_SIZE)
                    border = pygame.Rect(startX, startY, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(SCREEN, LIGHT_GREY, rect)
                    pygame.draw.rect(SCREEN, BLACK, border, 1)
        boardState[tileX][tileY] = 1  # updating board state to indicate block already clicked


def edgePieces(currentX, currentY, adjacentFlags):
    if board[currentX][currentY] != 10:
        if currentX == 0 and currentY == 0:  # top left piece
            for i in range(currentX, currentX + 2, 1):
                for j in range(currentY, currentY + 2, 1):
                    if board[i][j] == 10:
                        adjacentFlags += 1  # add 1 to flags adjacent
        elif currentX == TilesX - 1 and currentY == 0:  # top right piece
            for i in range(currentX - 1, currentX + 1, 1):
                for j in range(currentY, currentY + 2, 1):
                    if board[i][j] == 10:
                        adjacentFlags += 1  # add 1 to flags adjacent
        elif currentX == 0 and currentY == TilesY - 1:  # bottom left piece
            for i in range(currentX, currentX + 2, 1):
                for j in range(currentY - 1, currentY + 1, 1):
                    if board[i][j] == 10:
                        adjacentFlags += 1  # add 1 to flags adjacent
        elif currentX == TilesX - 1 and currentY == TilesY - 1:  # bottom right piece
            for i in range(currentX - 1, currentX + 1, 1):
                for j in range(currentY - 1, currentY + 1, 1):
                    if board[i][j] == 10:
                        adjacentFlags += 1  # add 1 to flags adjacent
        elif currentY == 0:  # top row
            for i in range(currentX - 1, currentX + 2, 1):
                for j in range(currentY, currentY + 2, 1):
                    if board[i][j] == 10:
                        adjacentFlags += 1  # add 1 to flags adjacent
        elif currentY == TilesY - 1:  # bottom row
            for i in range(currentX - 1, currentX + 2, 1):
                for j in range(currentY - 1, currentY + 1, 1):
                    if board[i][j] == 10:
                        adjacentFlags += 1  # add 1 to flags adjacent
        elif currentX == 0:  # first column
            for i in range(currentX, currentX + 2, 1):
                for j in range(currentY - 1, currentY + 2, 1):
                    if board[i][j] == 10:
                        adjacentFlags += 1  # add 1 to flags adjacent
        elif currentX == TilesX - 1:  # last column
            for i in range(currentX - 1, currentX + 1, 1):
                for j in range(currentY - 1, currentY + 2, 1):
                    if board[i][j] == 10:
                        adjacentFlags += 1  # add 1 to flags adjacent

        board[currentX][currentY] = adjacentFlags


def howManyAdjacentFlags():  # check all adjacent squares around current pos
    for x in range(0,TilesX,1): # x starts at 0
        for y in range(0,TilesY,1): # y starts at 0
            if board[x][y] != 10:
                currentX = x
                currentY = y
                adjacentFlags = 0  # resetting every piece
                if x == 0 or x == TilesX - 1 or y == 0 or y == TilesY - 1:  # first and last columns/rows
                    edgePieces(currentX, currentY, adjacentFlags)
                else: # regular board piece with 8 surrounding pieces
                    for i in range(currentX - 1, currentX + 2, 1):
                        for j in range(currentY - 1, currentY + 2, 1):
                            if board[i][j] == 10:
                                adjacentFlags += 1 # add 1 to flags adjacent
                    board[currentX][currentY] = adjacentFlags


def initialisePlayers():

    for x in range(0, numOfPlayers, 1):
        playerScores[x] = {'name': f"Player {x+1}", 'score': 0}
        scoresText.append(f"{playerScores[x]['name']} score - {playerScores[x]['score']}")


def drawScores():
    rect = pygame.Rect(80, 80, 320, 600)  # area of the screen where the score goes
    pygame.draw.rect(SCREEN, WHITE, rect)  # making it blank again so the score doesn't write on top of each other
    y = 200
    for x in range(0, numOfPlayers, 1):
        playerText = scorefont.render(scoresText[x], True, BLACK)
        SCREEN.blit(playerText, (100, y))

        y += 100


def main():

    pygame.init()
    clock = pygame.time.Clock()
    SCREEN.fill(WHITE)
    createFlags(numOfFlags, TilesX, TilesY)

    print(len(flags))

    initialisePlayers()

    drawGrid()
    howManyAdjacentFlags()

    while True:  # game loop
        clock.tick(FPS)
        drawScores()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = (event.pos[0], event.pos[1])
                checkIfFlag(mouseX, mouseY, currentPlayer)
        flagsRemainingText = scorefont.render(f'Found {flagsFound} out of {numOfFlags} flags', True, BLACK)
        SCREEN.blit(flagsRemainingText, (100, 100))

        xpos = 90
        ypos = 195 + (currentPlayer - 1) * 100
        border = pygame.Rect(xpos, ypos, 280, 50)
        pygame.draw.rect(SCREEN, BLACK, border, 3)
        pygame.display.update()


def drawGrid():
    for x in range(BOARD_X_OFFSET, (BLOCK_SIZE * TilesX) + BOARD_X_OFFSET, BLOCK_SIZE):
        for y in range(BOARD_Y_OFFSET, (BLOCK_SIZE * TilesY) + BOARD_Y_OFFSET, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)


if __name__ == "__main__":
    main()
