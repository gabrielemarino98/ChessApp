import RPi.GPIO as GPIO
import chess
import time
from time import sleep
import copy

GPIO.setmode(GPIO.BCM)

x = {
    "a": 11,
    "b": 0,
    "c": 5,
    "d": 6,
    "e": 13,
    "f": 19,
    "g": 26,
    "h": 21,
}

y = {
    "8": 9,
    "7": 10,
    "6": 22,
    "5": 27,
    "4": 17,
    "3": 4,
    "2": 3,
    "1": 2
}

boardy = {
    7:"1",
    6:"2",
    5:"3",
    4:"4",
    3:"5",
    2:"6",
    1:"7",
    0:"8"
}
boardx = {
    0:"a",
    1:"b",
    2:"c",
    3:"d",
    4:"e",
    5:"f",
    6:"g",
    7:"h"
}

def init(x,y):
    for gpio in x:
        GPIO.setup(x[gpio], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    for gpio in y:
        GPIO.setup(y[gpio], GPIO.OUT)
        GPIO.output(y[gpio], GPIO.LOW)
    
    sleep(0.05) #50ms
    return scanboard()
    
    
def scanboard():
    chessboard = [[0 for _ in range(8)] for _ in range(8)]
    for indexrow, (row, gpioy) in enumerate(y.items()):
        GPIO.output(gpioy, GPIO.HIGH)
        sleep(0.01) #10ms
            
        for indexbox, (box, gpiox) in enumerate(x.items()): #to read the piece
            chessboard[indexrow][indexbox] = GPIO.input(gpiox)

        GPIO.output(gpioy, GPIO.LOW)
        sleep(0.01) #10ms
        return chessboard

def findmove():
    lastpos = ""
    nextpos = ""
    blastpos = False
    bnextpos = False

    for i in range(8):
            for j in range(8):
                if temp_board[i][j] != actual_board[i][j]:
                    if(temp_board[i][j] == 0):
                        lastpos = boardx[j] + boardy[i]
                        blastpos = True
                    else:
                        nextpos = boardx[j] + boardy[i]
                        bnextpos = True

    if(blastpos and bnextpos):       
        return True,lastpos,nextpos
    else:
        return False,lastpos,nextpos

# Function to validate the new move after cycles
def validatemove(foundlastpos,foundnextpos):
    
    t_end = time.time() + 1
    while time.time() < t_end:
        newmove ,currentlastpos ,currentnextpos = findmove()
        
        if(foundlastpos != currentlastpos and foundnextpos != currentnextpos):
            return False
    
    return True

                
            
def make_move(board, move_uci):
    """
    This function takes a chess board and a move in UCI format as arguments,
    then makes the move on the board.
    
    :param board: a chess.Board object
    :param move_uci: a move in UCI format (e.g., 'e2e4')
    """
    move = chess.Move.from_uci(move_uci)  # Convert the UCI string to a move
    if move in board.legal_moves:  # Check if the move is legal
        board.push(move)  # Make the move
        print(board)  # Print the updated board
        return True
    else:
        print(f"Illegal move: {move_uci}")
        return False
        
        
# Example of saving and loading the matrices (optional)
def save_matrix(matrix, filename):
    with open(filename, 'w') as f:
        for row in matrix:
            f.write(' '.join(map(str, row)) + '\n')

def load_matrix(filename):
    with open(filename, 'r') as f:
        return [list(map(int, line.split())) for line in f]


###################  START OF PROGRAM  ####################################

#Const
board = chess.Board()
lastpos = ""
nextpos = ""
newmove = False
#Main chessboard
actual_board = [[0 for _ in range(8)] for _ in range(8)]  # 8x8 matrix 0 filled
#Upcoming moves
temp_board = [[0 for _ in range(8)] for _ in range(8)]
#/Const


#init fresh board
actual_board=init(x,y)

#debug
actual_board[6][4] = 1
actual_board[1][4] = 1
temp_board[1][4] = 1
#debug
for row in actual_board:
    print(row)


i = 0
while(i < 50): #to set True after #debug

    if(i == 9):
        temp_board[6][4] = 0
        temp_board[4][4] = 1

    if(i == 40):
        temp_board[1][4] = 0
        temp_board[3][4] = 1    

    newmove, lastpos, nextpos = findmove()
    print(newmove,lastpos,nextpos)
    if(newmove):                                           #if a new move was found
        if(validatemove(lastpos, nextpos)):                #if said move is confirmed
            if(make_move(board, lastpos + nextpos)):       #if the move is legal
                actual_board = copy.deepcopy(temp_board)   #chessboard is updated to last move
            #make_move prints illegal move
        #move wasn't confirmed
    #no new move

    #print(lastpos,nextpos) #debug
    #print(newmove) #debug
    
    
    i+=1 #debug


# # Save actual matrix
# save_matrix(actual_board, 'actual_board.txt')

# # Load matrix from file
# loaded_matrix = load_matrix('actual_board.txt')
# print(loaded_matrix)


GPIO.cleanup()
###################  END OF PROGRAM  ####################################
