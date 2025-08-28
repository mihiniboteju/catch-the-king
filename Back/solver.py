from checkmate import checkmate
# this class can be replaced according to the main game flow
class GameState:
    def __init__(self, size=8):
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.size = size
        self.remaining_pieces = {'Q': 1, 'R': 2, 'B': 2, 'P': 8, 'N': 1} #can remove Knight if we won't use that
        self.can_win = False

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

def can_still_win(current_board, remaining_pieces, king_pos):
    state = GameState()
    state.board = current_board
    state.remaining_pieces = remaining_pieces
    state.can_win = dfs_search(state, king_pos)
    return state.can_win

def find_complete_solution(king_pos, board_size=8):
    initial_state = GameState(board_size)
    solution = dfs_search(initial_state, king_pos, find_solution=True)
    if solution:
        print("Solution found!")
        print("Place pieces in this order:")
        for i, (piece, row, col) in enumerate(solution, 1):
            print(f"{i}. Place {piece} at ({row}, {col})")
        return solution
    else:
        print("No solution exists for this king position")
        return None

def find_remaining_solution(current_board, remaining_pieces, king_pos):
    board_size = len(current_board)
    state = GameState(board_size)
    state.board = [row[:] for row in current_board]
    state.remaining_pieces = remaining_pieces.copy()
    
    solution = dfs_search(state, king_pos, find_solution=True)
    
    if solution:
        print("Solution found with remaining pieces!")
        print("Continue by placing:")
        for i, (piece, row, col) in enumerate(solution, 1):
            print(f"{i}. Place {piece} at ({row}, {col})")
        return solution
    else:
        print("No solution possible with remaining pieces")
        return None
    
if __name__ == "__main__":
    # Test finding a solution
    print("Testing solution finder...")
    solution = find_complete_solution((7, 7))
    
    if solution:
        print(f"\nFound solution with {len(solution)} moves")
    else:
        print("No solution found")

