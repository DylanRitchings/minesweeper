from random import randint

boardSize = 8
mineAmount = 15


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
        
def createMines(amount,board):
    mines=[]
    for n in range(amount):
        x = randint(0,len(board)-1)
        y = randint(0,len(board)-1)
        mines.append([x,y])
        board[y][x] = "M"
    return(mines)

def placeNumber(board,x,y):
    if x>=0 and y>=0 and x<boardSize and y<boardSize:
        current = board[y][x]
        if current!="M":
            if current.isdigit():
                board[y][x] = str(int(current)+1)
            else:
                board[y][x] = "1"

def placeNumbers(board,mines):
    for mine in mines:
        x = mine[0]
        y = mine[1]
        for x2 in range(x-1,x+2):
            for y2 in range(y-1,y+2):
                placeNumber(board,x2,y2)

            
        
        
def main():
    board = createBoard(boardSize)
    mines = createMines(mineAmount,board)
    placeNumbers(board,mines)
    printBoard(board)
    
if __name__ == "__main__":
    main()
