from gamestate import GameState
from checkmate import checkmate
from solver import can_still_win, find_complete_solution, find_remaining_solution

import random

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

def check_win_possibility(game_state, king_pos):
    current_board = [row[:] for row in game_state.board]
    remaining = game_state.remaining_pieces.copy()
    can_win = can_still_win(current_board, remaining, king_pos)
    if not can_win:
        print("No possible way to catch the King with the remaining pieces!You lose!!!")
        return False
    else:
        print("There is still a possibility to catch the King with the remaining pieces!!!")
        while True:
            try:
                print("You Have option to choose Yes or No to see the Solution for remaining pieces. If you would like to see the solution, type 'y' and The soultion will show and the Game End. If not the game will continue!")
                findrem_sol = input("\nDo you want to see the solution for remaining piece?(y/n)").strip().lower()
                if findrem_sol == 'y':
                    print("\n=== Solution with Remaining Pieces ===")
                    solution = find_remaining_solution(current_board, remaining, king_pos)
                    if solution:
                        print(f"Move needed with remaining pieces: {len(solution)}")
                    else:
                        print("No soulution found!!!")
                    print("Game Over!!!")
                    return False
                    break
                elif findrem_sol == 'n':
                    print("Continuing the Game...")
                    return True
                else:
                    print("Please Enter y or n")
            except:
                print("Please Enter a valid choice")
    
# def find_solution(game_state, king_pos):
#     offer_help = input("Do you want to see a possible solution to catch the King? (y/n): ").strip().lower()
#     if offer_help == 'y':
#         current_board = [row[:] for row in game_state.board]
#         remaining = game_state.remaining_pieces.copy()
#         solution = find_remaining_solution(current_board, remaining, king_pos)
#         if not solution:
#             print("No possible solution found with the remaining pieces.")


def solution_analysis(game_state, king_pos,game_won=False):
    if game_won:
        print("Congratulations on catching the King! You win!!!")
    else:
        print("Game Over!!! Best of luck next time!")
    while True:
        try:
            findcom_sol = input("\nDo you want to see the complete solution?(y/n)").strip().lower()
            if findcom_sol == 'y':
                print("\n=== Complete Solution ===")
                solution = find_complete_solution(king_pos, board_size=8)
                if solution:
                    print(f"Total solution Move: {len(solution)}")
                else:
                    print("No soulution found!!!")
            elif findcom_sol == 'n':
                print("Thank You for Playing!!!")
            else:
                print("Please Enter y or n")
        except:
            print("Please Enter a valid choice")
        break
            
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
        
        # Check if player can still win before asking for piece input
        # can_continue = check_win_possibility(game_state, king_pos)
        # if not can_continue:
        #     # Player chose to see that they can't win, but let them continue if they want
        #     continue_anyway = input("\nDo you want to continue playing anyway? (y/n): ").strip().lower()
        #     if continue_anyway != 'y':
        #         break
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
                if not (0 <= row < board_size):
                    print("The Input Position Is Out Of Range!!!")
                    continue
                col = int(input(f"Enter column for {piece} (0 to {board_size-1}): "))
                if not (0 <= col < board_size):
                    print("The Input Position Is Out Of Range!!!")
                    continue
                
                if (row, col) == king_pos:
                    print(f"\nCONGRATULATIONS! You found the King at ({row}, {col})!")
                    print("You Win!!!")
                    game_state.board[row][col] = piece
                    display_board(game_state.board, hide_king=False, king_pos=king_pos)
                    solution_analysis(game_state, king_pos, game_won=True)
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
            solution_analysis(game_state, king_pos, game_won=True)
            return
        
        # After placing a piece, check win possibility and offer solutions again
        print(f"\n=== Analysis after placing {piece} at ({row}, {col}) ===")
        can_continue = check_win_possibility(game_state, king_pos)
        if not can_continue:
            return
    
#This is for when all pieces are used and the player loses the game state
    print("\nGame Over!!! You have used all your pieces but could not catch the King!")
    print(f"The King was hiding at position ({king_row}, {king_col})")
    print("You Lose! Best of luck next time!")
    display_board(game_state.board, hide_king=False, king_pos=king_pos)
    solution_analysis(game_state, king_pos, game_won=False)

if __name__ == "__main__":
    chessgame()