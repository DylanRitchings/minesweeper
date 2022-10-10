import socket
from _thread import *
import pickle
from random import randint
from game import Game

server = "192.168.0.17"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

TilesX = 10
TilesY = 10
numOfPlayers = 3
currentPlayer = 1  # sets current player to player 1 initially

numOfFlags = 25
flagsFound = 0

WINNING_SCORE = int(numOfFlags/2) + 1

flags = []  # flag positions
board = [[0 for j in range(TilesY)] for i in range(TilesX)]  # creating 2d array to match grid, to store board in
boardState = [[0 for k in range(TilesY)] for n in range(TilesX)]  # creating 2d array to match grid
# to store board state in
playerScores = {}  # dictionary
scoresText = []  # stores the score strings

try:
    s.bind((server, port))
except socket.error as e:
    str(e)


s.listen(numOfPlayers)  # max of six players can connect
print("Waiting for a connection, Server Started")


# connected = set()
# games = {}
idCount = 0


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


def threaded_client(conn, playerId):
    global idCount, flags
    conn.send(str.encode(str(playerId)))
    reply = ""

    if idCount == 1:  # only want to do the board creation if it's the first player connecting, not for all players
        createFlags(numOfFlags, TilesX, TilesY)
        print(board)

        initialisePlayers()
        howManyAdjacentFlags()

    while True:
        try:
            data = conn.recv(2048*4).decode()

            if not data:
                print("Disconnected")
                break
            else:
                if data == "reset":
                    break  # code resetting game eventually
                elif data != "get":
                    break  # code move stuff here

                # print("Received: ", reply)
                # print("Sending: ", reply)

                # conn.sendall(pickle.dumps(game))
                conn.sendall(pickle.dumps(reply))  # change to game
        except:
            break

    print("Lost connection")
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1

    start_new_thread(threaded_client, (conn, idCount))
