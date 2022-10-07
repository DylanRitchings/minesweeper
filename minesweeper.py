from random import randint
import sys
import pygame as pygame

pygame.font.init()

TilesX = 10
TilesY = 10
numOfPlayers = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

WINDOW_HEIGHT = 900
WINDOW_WIDTH = 1200

pygame.display.set_caption("Minesweeper")

FPS = 60

BOARD_X_OFFSET = 400
BOARD_Y_OFFSET = 100

BLOCK_SIZE = 30

GAME_HEIGHT = TilesY * BLOCK_SIZE # used to check board isn't bigger than window height
GAME_WIDTH = TilesX * BLOCK_SIZE # used to check board isn't bigger than window width

numOfFlags = 25
WINNING_SCORE = int(numOfFlags/2) + 1

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

scorefont = pygame.font.SysFont("comic sans", 25)
piecefont = pygame.font.SysFont("monospace", 20)

flags=[]  # flag positions
board=[[0 for j in range(TilesY)] for i in range(TilesX)]  # creating 2d array to match grid, to store board in
playerScores={} #  dictionary
scoresText=[] # stores the score strings

def createFlags(numOfFlags,TilesX,TilesY):
    for n in range(numOfFlags):
        x = randint(0,TilesX-1)
        y = randint(0,TilesY-1)
        if [x,y] in flags:
            n = n-1
        else:
            flags.append([x,y])
            board[x][y] = 10
    return(flags)

def checkIfFlag(mouseX, mouseY):
    tileX = int((mouseX - BOARD_X_OFFSET)/BLOCK_SIZE)
    tileY = int((mouseY - BOARD_Y_OFFSET)/BLOCK_SIZE)
    startX = BOARD_X_OFFSET + (tileX * BLOCK_SIZE)
    startY = BOARD_Y_OFFSET + (tileY * BLOCK_SIZE)
    # if [tileX, tileY] in flags:
    if board[tileX][tileY] == 10:
        # startX = BOARD_X_OFFSET + (tileX * BLOCK_SIZE)
        # startY = BOARD_Y_OFFSET + (tileY * BLOCK_SIZE)
        rect = pygame.Rect(startX, startY, BLOCK_SIZE, BLOCK_SIZE)
        border = pygame.Rect(startX, startY, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, RED, rect)
        pygame.draw.rect(SCREEN, BLACK, border, 1)
        playerScores[0]['score'] += 1
        scoresText[0] = f"{playerScores[0]['name']} score - {playerScores[0]['score']}"
        print(playerScores[0]['score'])
    else:  # print number of adjacent flags
        number = str(board[tileX][tileY])
        pieceText = piecefont.render(number, True, BLACK)
        SCREEN.blit(pieceText, (startX + 9, startY + 4))
    # print(tileX,tileY)

def edgePieces(currentX, currentY, adjacentFlags):
    if board[currentX][currentY] != 10:
        if currentX == 0 and currentY == 0: #  top left piece
            for i in range(currentX, currentX + 2, 1):
                for j in range(currentY, currentY + 2, 1):
                    if board[i][j] == 10:
                        adjacentFlags += 1  # add 1 to flags adjacent
        elif currentX == TilesX - 1 and currentY == 0: #  top right piece
            for i in range(currentX - 1, currentX + 1, 1):
                for j in range(currentY, currentY + 2, 1):
                    if board[i][j] == 10:
                        adjacentFlags += 1  # add 1 to flags adjacent
        elif currentX == 0 and currentY == TilesY - 1: #  bottom left piece
            for i in range(currentX, currentX + 2, 1):
                for j in range(currentY - 1, currentY + 1, 1):
                    if board[i][j] == 10:
                        adjacentFlags += 1  # add 1 to flags adjacent
        elif currentX == TilesX - 1 and currentY == TilesY - 1: #  bottom right piece
            for i in range(currentX - 1, currentX + 1, 1):
                for j in range(currentY - 1, currentY + 1, 1):
                    if board[i][j] == 10:
                        adjacentFlags += 1  # add 1 to flags adjacent
        elif currentY == 0: #  top row
            for i in range(currentX - 1, currentX + 2, 1):
                for j in range(currentY, currentY + 2, 1):
                    if board[i][j] == 10:
                        adjacentFlags += 1  # add 1 to flags adjacent
        elif currentY == TilesY - 1: #  bottom row
            for i in range(currentX - 1, currentX + 2, 1):
                for j in range(currentY - 1, currentY + 1, 1):
                    if board[i][j] == 10:
                        adjacentFlags += 1  # add 1 to flags adjacent
        elif currentX == 0: #  first column
            for i in range(currentX, currentX + 2, 1):
                for j in range(currentY - 1, currentY + 2, 1):
                    if board[i][j] == 10:
                        adjacentFlags += 1  # add 1 to flags adjacent
        elif currentX == TilesX - 1: #  last column
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
                # if currentX - 1 >= 0 and currentX + 1 < TilesX - 1 and
            # board.append([currentX,currentY,adjacentFlags])
            # print([currentX,currentY,adjacentFlags])

def initialisePlayers():

    # y = 100
    for x in range(0, numOfPlayers, 1):
        playerScores[x] = {'name': f"Player {x+1}", 'score': 0}
        scoresText.append(f"{playerScores[x]['name']} score - {playerScores[x]['score']}")
        # textToDisplay = f"{playerScores[x]['name']} score - {playerScores[x]['score']}"
        # textToDisplay = f"{playerScores[x]['name']} score - "
        # playerText = scorefont.render(textToDisplay, True, BLACK)
        # SCREEN.blit(playerText, (100, y))
        #
        # y += 100

def drawScores():
    rect = pygame.Rect(100, 100, 250, 600)  # area of the screen where the score goes
    pygame.draw.rect(SCREEN, WHITE, rect)  # making it blank again so the score doesn't write on top of each other
    # SCREEN.fill(WHITE)
    y = 100
    for x in range(0, numOfPlayers, 1):
        # textToDisplay = f"{playerScores[x]['name']} score - {playerScores[x]['score']}"
        playerText = scorefont.render(scoresText[x], True, BLACK)
        SCREEN.blit(playerText, (100, y))

        y += 100

def main():

    pygame.init()
    clock = pygame.time.Clock()
    SCREEN.fill(WHITE)
    flags = createFlags(numOfFlags, TilesX, TilesY)
    # print(flags)

    initialisePlayers()

    drawGrid()
    howManyAdjacentFlags()
    # print(board)

    while True:
        clock.tick(FPS)
        drawScores()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = (event.pos[0], event.pos[1])
                checkIfFlag(mouseX, mouseY)

        pygame.display.update()

def drawGrid():
    for x in range(BOARD_X_OFFSET, (BLOCK_SIZE * TilesX) + BOARD_X_OFFSET, BLOCK_SIZE):
        for y in range(BOARD_Y_OFFSET, (BLOCK_SIZE * TilesY) + BOARD_Y_OFFSET, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)

if __name__ == "__main__":
    main()
