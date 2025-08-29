from checkmate import checkmate
from gamestate import GameState

def get_empty_squares(board):
    empty = []
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == '.':
                empty.append((row, col))
    return empty

def place_piece(state, piece, row, col):
    new_state = GameState(state.size)
    for r in range(state.size):
        for c in range(state.size):
            new_state.board[r][c] = state.board[r][c]
    new_state.board[row][col] = piece
    new_state.remaining_pieces = state.remaining_pieces.copy()
    new_state.remaining_pieces[piece] -= 1
    new_state.used_positions = state.used_positions.copy()
    new_state.used_positions.add((row, col))
    return new_state

def board_to_string(board, king_pos):
    test_board = [row[:] for row in board]
    king_row, king_col = king_pos
    test_board[king_row][king_col] = 'K'
    return '\n'.join(' '.join(row) for row in test_board)

def dfs_search(state, king_pos, find_solution=False, solution=None):
    if solution is None:
        solution = []
        
    board_str = board_to_string(state.board, king_pos)
    if checkmate(board_str): #assuming checkmate return True/False
        if find_solution:
            return solution
        return True
    
    if all(state.remaining_pieces[piece] == 0 for piece in state.remaining_pieces):
        return [] if find_solution else False
    
    empty_squares = get_empty_squares(state.board)
    
    for row, col in empty_squares:
        for piece, count in state.remaining_pieces.items():
            if count > 0:
                new_state = place_piece(state, piece, row, col)
                new_solution = solution + [(piece, row, col)] if find_solution else []
                result = dfs_search(new_state, king_pos, find_solution, new_solution)
                if (find_solution and result) or (not find_solution and result):
                    return result
    if find_solution:
        return []
    return False

def _create_game_state_from_board(current_board, remaining_pieces, king_pos):
    board_size = len(current_board)
    state = GameState(board_size)
    state.board = [row[:] for row in current_board]
    state.remaining_pieces = remaining_pieces.copy()

    state.used_positions = set()
    for r in range(board_size):
        for c in range(board_size):
            if current_board[r][c] != '.':
                state.used_positions.add((r, c))
    state.used_positions.add(king_pos)  # King position is also used
    return state

def can_still_win(current_board, remaining_pieces, king_pos):
    state = _create_game_state_from_board(current_board, remaining_pieces, king_pos)
    return dfs_search(state, king_pos)

def find_complete_solution(king_pos, board_size=8):
    initial_state = GameState(board_size)
    solution = dfs_search(initial_state, king_pos, find_solution=True)
    if solution:
        current_state = GameState(board_size)
        for i, (piece, row, col) in enumerate(solution, 1):
            current_state = place_piece(current_state, piece, row, col)
            board_str = board_to_string(current_state.board, king_pos)
            remaining_str = ', '.join([f"{p}: {count}" for p, count in current_state.remaining_pieces.items() if count > 0])
            print(f"   Board state:\n{board_str}")
            # print(f"   Remaining pieces: {remaining_str}\n")
        return solution
    else:
        print("No solution exists for this king position")
        return None

def find_remaining_solution(current_board, remaining_pieces, king_pos):
    state = _create_game_state_from_board(current_board, remaining_pieces, king_pos)
    solution = dfs_search(state, king_pos, find_solution=True)
    
    if solution:
        current_state = _create_game_state_from_board(current_board, remaining_pieces, king_pos)
        
        print("Solution found with remaining pieces!")
        print("Continue by placing:")
        for i, (piece, row, col) in enumerate(solution, 1):
            print(f"{i}. Place {piece} at ({row}, {col})")
            current_state = place_piece(current_state, piece, row, col)
            board_str = board_to_string(current_state.board, king_pos)
            remaining_str = ', '.join([f"{p}: {count}" for p, count in current_state.remaining_pieces.items() if count > 0])
            print(f"   Board state:\n{board_str}")
            # print(f"   Remaining pieces: {remaining_str}\n")
        return solution
    else:
        print("No solution possible with remaining pieces")
        return None
    
# if __name__ == "__main__":
#     # Test finding a solution
#     print("Testing solution finder...")
#     solution = find_complete_solution((1, 5))

#     print("Testing remaining pieces finder...")
#     remaining_pieces = {'Q': 0, 'R': 0, 'B': 0, 'P': 0}
#     test_board = [['.', '.', '.', '.', '.', '.', '.', '.'],
#                 ['.', '.', '.', '.', '.', '.', '.', '.'],
#                 ['.', '.', '.', 'P', '.', '.', '.', '.'],
#                 ['.', '.', '.', '.', '.', '.', '.', '.'],
#                 ['.', 'P', '.', '.', '.', '.', '.', '.'],
#                 ['.', '.', '.', '.', '.', '.', '.', '.'],
#                 ['.', '.', '.', '.', '.', '.', '.', '.'],
#                 ['.', '.', '.', '.', '.', '.', '.', '.']]
#     solution = find_remaining_solution(test_board, remaining_pieces, (1, 5))
    
#     can_still_win_result = can_still_win(test_board, remaining_pieces, (1, 5))
#     print(f"Can still win: {can_still_win_result}")
                                        
    

