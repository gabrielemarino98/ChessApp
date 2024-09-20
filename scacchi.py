import RPi.GPIO as GPIO
import chess

GPIO.setmode(GPIO.BCM)
gpiosx = [11, 0, 5, 6, 13, 19, 26, 21]
gpiosy = [2, 3, 4, 17, 27, 22, 10, 9]

for gpio in gpiosx:
    GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
for gpio in gpiosy:
    GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
def readboard(chessboard):

    for gpiox in gpiosx:
        for gpioy in gpiosy:
            #To read the state
            statex = GPIO.input(gpiox)
            statey = GPIO.input(gpioy)
            print(gpiox,gpioy,statex*statey)

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

# Example usage
board = chess.Board()
make_move(board, "e2e5")  #illegal move
make_move(board, "e2e4")  # e2 to e4
make_move(board, "e7e5")  # e7 to e5
readboard(chessboard)

GPIO.cleanup()
