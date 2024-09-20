import RPi.GPIO as GPIO
import chess

GPIO.setmode(GPIO.BCM)

chessboard = [[0 for _ in range(8)] for _ in range(8)]

gpios = [0, 5, 6, 9, 10, 11, 13, 19, 26]

for gpio in gpios:
	#To read the state
	GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	state = GPIO.input(gpio)
	print(gpio,state)

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

# Example usage
board = chess.Board()
make_move(board, "e2e5")  #illegal move
make_move(board, "e2e4")  # e2 to e4
make_move(board, "e7e5")  # e7 to e5


GPIO.cleanup()
