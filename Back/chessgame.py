from checkmate import checkmate
import random

class GameState:
    def __init__(self, size=8):
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.size = size
        self.remaining_pieces = {'Q': 1, 'R': 2, 'B': 2, 'P': 8}
        self.used_positions = set()

def kpos_generator(size): 
    return random.randint(0, size - 1)

def display_board(board, hide_king=True, king_pos=None):
    display_board = [row[:] for row in board]
    if not hide_king and king_pos:
        king_row, king_col = king_pos
        display_board[king_row][king_col] = 'K'
    
    print("\n=== Current Board ===")
    for row in display_board:
        print(" ".join(row))
    print()

def board_to_string(board, king_pos):
    test_board = [row[:] for row in board]
    king_row, king_col = king_pos
    test_board[king_row][king_col] = 'K'
    return '\n'.join(' '.join(row) for row in test_board)

def chessgame():
    print("==== Let's Play Chess Game (Catch The King If You Can!!!) ====")

    board_size = 8
    piece_limits = {
        'Q': 1,
        'R': 2, 
        'B': 2,
        'P': 8,
    }
    
    piece_counts = {}
    total_pieces = 0

    # Ask the user about piece counts
    for piece, max_allowed in piece_limits.items():
        while True:
            try:
                count = int(input(f"How many {piece}s do you want to place? (0 to {max_allowed}): "))
                if 0 <= count <= max_allowed:
                    piece_counts[piece] = count
                    total_pieces += count
                    break
                else:
                    print(f"Invalid!!! You can only place up to {max_allowed} {piece}(s).")
            except ValueError:
                print("Please Enter A Valid Number!")
    
    if total_pieces == 0:
        print("You need to select at least one piece to play!")
        return

    game_state = GameState(board_size)
    game_state.remaining_pieces = piece_counts
    
    
    king_row, king_col = kpos_generator(board_size), kpos_generator(board_size)
    king_pos = (king_row, king_col)
    game_state.used_positions.add(king_pos)
    
    display_board(game_state.board, hide_king=True)
    
    print("Available pieces:")
    for piece, count in game_state.remaining_pieces.items():
        piece_name = {'Q': 'Queen', 'R': 'Rook', 'B': 'Bishop', 'P': 'Pawn'}[piece]
        print(f"  {piece} ({piece_name}): {count}")
    
    while any(count > 0 for count in game_state.remaining_pieces.values()):
        print(f"\nRemaining pieces: {game_state.remaining_pieces}")
        
        while True:
            piece = input("Choose a piece to place (Q/R/B/P): ").upper().strip()
            if piece in game_state.remaining_pieces:
                if game_state.remaining_pieces[piece] > 0:
                    break
                else:
                    print(f"No more {piece}s available!")
            else:
                print("Invalid piece! Choose Q, R, B, or P")
        
        while True:
            try:
                row = int(input(f"Enter row for {piece} (0 to {board_size-1}): "))
                col = int(input(f"Enter column for {piece} (0 to {board_size-1}): "))
                
                if not (0 <= row < board_size and 0 <= col < board_size):
                    print("The Input Position Is Out Of Range!!!")
                    continue
                
                if (row, col) == king_pos:
                    print(f"\nCONGRATULATIONS! You found the King at ({row}, {col})!")
                    print("You Win!!!")
                    game_state.board[row][col] = piece
                    display_board(game_state.board, hide_king=False, king_pos=king_pos)
                    return
                
                if (row, col) in game_state.used_positions:
                    print("That Square Is already Taken by another piece!")
                    continue
                
                game_state.board[row][col] = piece
                game_state.used_positions.add((row, col))
                game_state.remaining_pieces[piece] -= 1
                break
                
            except ValueError:
                print("Please Enter Valid Numbers!")
        display_board(game_state.board, hide_king=True)
        
        # This is for checking the checkmate condition
        board_str = board_to_string(game_state.board, king_pos)
        if checkmate(board_str):
            print("\nYou Win!!! You have successfully catched the King!!!")
            display_board(game_state.board, hide_king=False, king_pos=king_pos)
            return
        
    
#This is for when all pieces are used and the player loses the game state
    print("\nGame Over!!! You have used all your pieces but could not catch the King!")
    print(f"The King was hiding at position ({king_row}, {king_col})")
    print("You Lose! Best of luck next time!")
    display_board(game_state.board, hide_king=False, king_pos=king_pos)

if __name__ == "__main__":
    chessgame()