from random import randint

boardSize = 8
mineAmount = 7


def createBoard(size):
    board = []
    for n in range(size):
        board.append([])
        for x in range(size):
            board[n].append("_")
    return board

def printBoard(board):
    for row in board:
        print(row)
        
def placeMines(amount,board):
    for n in range(amount):
        x = randint(0,len(board)-1)
        y = randint(0,len(board)-1)
        board[x][y] = "M"
    
def main():
    board = createBoard(boardSize)
    placeMines(mineAmount,board)
    printBoard(board)
    
if __name__ == "__main__":
    main()
