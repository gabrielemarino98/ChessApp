import RPi.GPIO as GPIO
import chess
from time import sleep


GPIO.setmode(GPIO.BCM)

x = {
    "a": 11
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

for gpio in x:
    GPIO.setup(x[gpio], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for gpio in y:
    GPIO.setup(y[gpio], GPIO.OUT)
    GPIO.output(y[gpio], GPIO.LOW)

def readboard(chessboard):
    
        for indexrow, (row, gpioy) in enumerate(y.items()):
            GPIO.output(gpioy, GPIO.HIGH)
            sleep(0.01) #20ms
            
            for indexbox, (box, gpiox) in enumerate(x.items()): #to read the piece
                chessboard[indexrow][indexbox] = GPIO.input(gpiox)

            GPIO.output(gpioy, GPIO.LOW)

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
    else:
        print(f"Illegal move: {move_uci}")

chessboard = [[0 for _ in range(8)] for _ in range(8)]

readboard(chessboard)

for row in chessboard:
    print(row)

# Example usage
board = chess.Board()
make_move(board, "e2e5")  #illegal move
make_move(board, "e2e4")  # e2 to e4
make_move(board, "e7e5")  # e7 to e5
readboard(chessboard)

GPIO.cleanup()
