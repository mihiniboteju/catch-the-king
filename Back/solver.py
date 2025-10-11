from checkmate import checkmate, checkmate_astar
from gamestate import GameState
import heapq

def heuristic(board, king_pos):
    score = 0
    ky, kx = king_pos

    for y in range(len(board)):
        for x in range(len(board)):
            piece = board[y][x]
            if piece == '.': 
                continue
            dist = abs(ky - y) + abs(kx - x)
            if piece == 'Q':
                score += 5 / (dist + 1)
            elif piece == 'R':
                if y == ky or x == kx:
                    score += 4 / (dist + 1)
            elif piece == 'B':
                if abs(ky - y) == abs(kx - x):
                    score += 3 / (dist + 1)
            elif piece == 'P':
                if ky == y - 1 and abs(kx - x) == 1:
                    score += 2
    return -score  

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

def astar_search(state, king_pos):
    start_board_str = board_to_string(state.board, king_pos)
    frontier = []
    
    counter = 0
    h = heuristic(state.board, king_pos)
    heapq.heappush(frontier, (h, counter, state, []))
    
    visited = set()

    while frontier:
        f, _, current_state, path = heapq.heappop(frontier)
        board_str = board_to_string(current_state.board, king_pos)
        
        if board_str in visited:
            continue
        visited.add(board_str)
        is_check, _ = checkmate_astar(board_str)
        if is_check:
            return path
        
        for row, col in get_empty_squares(current_state.board):
            for piece, count in current_state.remaining_pieces.items():
                if count > 0:
                    new_state = place_piece(current_state, piece, row, col)
                    new_path = path + [(piece, row, col)]
                    
                    g = len(new_path)
                    h = heuristic(new_state.board, king_pos)
                    f_new = g + h
                    
                    counter += 1
                    
                    heapq.heappush(frontier, (f_new, counter, new_state, new_path))

    return None

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

def can_still_win(current_board, remaining_pieces, king_pos, search_type='astar'):
    state = _create_game_state_from_board(current_board, remaining_pieces, king_pos)
    if search_type == 'astar':
        return astar_search(state, king_pos)
    return dfs_search(state, king_pos)

def find_complete_solution(king_pos, available_pieces, board_size=8, search_type='astar'):
    initial_state = GameState(board_size)
    if available_pieces:
        initial_state.remaining_pieces = available_pieces.copy()
    if search_type == 'astar':
        solution = astar_search(initial_state, king_pos)
    else:
        solution = dfs_search(initial_state, king_pos, find_solution=True)
    
    if solution:
        current_state = GameState(board_size)
        for i, (piece, row, col) in enumerate(solution, 1):
            current_state = place_piece(current_state, piece, row, col)
            board_str = board_to_string(current_state.board, king_pos)
            # remaining_str = ', '.join([f"{p}: {count}" for p, count in current_state.remaining_pieces.items() if count > 0])
            # print(f"   Board state:\n{board_str}")
            # print(f"   Remaining pieces: {remaining_str}\n")
        print(f"   Board state:\n{board_str}")
        return solution
    else:
        print("No solution exists for this king position")
        return None

def find_remaining_solution(current_board, remaining_pieces, king_pos, search_type='astar'):
    state = _create_game_state_from_board(current_board, remaining_pieces, king_pos)
    if search_type == 'astar':
        solution = astar_search(state, king_pos)#, find_solution=True)
    else:
        solution = dfs_search(state, king_pos, find_solution=True)
    
    if solution:
        current_state = _create_game_state_from_board(current_board, remaining_pieces, king_pos)
    
        for i, (piece, row, col) in enumerate(solution, 1):
            # print(f"{i}. Place {piece} at ({row}, {col})")
            current_state = place_piece(current_state, piece, row, col)
            board_str = board_to_string(current_state.board, king_pos)
            # remaining_str = ', '.join([f"{p}: {count}" for p, count in current_state.remaining_pieces.items() if count > 0])
            # print(f"   Board state:\n{board_str}")
            # print(f"   Remaining pieces: {remaining_str}\n")
        print(f"   Board state:\n{board_str}")
        return solution
    else:
        print("No solution possible with remaining pieces")
        return None
    
if __name__ == "__main__":
    # Test finding a solution
    print("Testing solution finder...")
    # solution = find_complete_solution((1, 5))

    print("Testing remaining pieces finder...")
    remaining_pieces = {'Q': 0, 'R': 1, 'B': 1, 'P': 1}
    test_board = [['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', 'P', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', 'P', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.']]
    solution = find_remaining_solution(test_board, remaining_pieces, (1, 5))
    solution = find_remaining_solution(test_board, remaining_pieces, (1, 5),search_type='dfs')
    # can_still_win_result = can_still_win(test_board, remaining_pieces, (1, 5))
    # print(f"Can still win: {can_still_win_result}")
                                        
    

