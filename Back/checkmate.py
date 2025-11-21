from collections import deque
import heapq
import math 


# ============================================================================
# Shared Helper Functions
# ============================================================================

def has_clear_path(board, from_y, from_x, to_y, to_x):
    """
    Check if the path between two positions is clear (no blocking pieces).
    Used for sliding pieces: Rook, Bishop, Queen.
    
    Args:
        board: 2D list representing the chess board
        from_y, from_x: Starting position (piece location)
        to_y, to_x: Ending position (king location)
    
    Returns:
        True if all cells between start and end are empty, False otherwise
    """
    # Calculate step direction for each axis (-1, 0, or 1)
    # This determines how to step from the piece toward the king
    # Examples:
    #   Rook (horizontal): dy=0, dx=±1 (move left/right only)
    #   Rook (vertical):   dy=±1, dx=0 (move up/down only)
    #   Bishop (diagonal): dy=±1, dx=±1 (move diagonally)
    #   Queen: any combination of the above
    dy = 0 if from_y == to_y else (1 if to_y > from_y else -1)
    dx = 0 if from_x == to_x else (1 if to_x > from_x else -1)
    
    # Start from next cell after the piece
    y, x = from_y + dy, from_x + dx
    
    # Walk along the path until we reach the king
    while (y, x) != (to_y, to_x):
        if board[y][x] != '.':
            return False  # Path is blocked by another piece
        y, x = y + dy, x + dx
    
    return True  # Path is clear


def is_piece_attacking_king(piece, piece_pos, king_pos, board):
    """
    Unified attack checker with line-of-sight blocking.
    This is the single source of truth for piece attack logic.
    
    Args:
        piece: Piece type ('P', 'R', 'B', 'Q')
        piece_pos: (y, x) position of the piece
        king_pos: (y, x) position of the king
        board: 2D list representing the chess board
    
    Returns:
        True if piece attacks king (with clear path for sliding pieces)
    """
    py, px = piece_pos
    ky, kx = king_pos
    
    # Pawn: diagonal attack one square forward (moving down the board)
    if piece == 'P':
        return (py == ky + 1 and abs(px - kx) == 1)
    
    # Check alignment first
    same_row = (py == ky)
    same_col = (px == kx)
    same_diagonal = (abs(py - ky) == abs(px - kx))
    
    # Rook: horizontal or vertical with clear path
    if piece == 'R':
        if same_row or same_col:
            return has_clear_path(board, py, px, ky, kx)
        return False
    
    # Bishop: diagonal with clear path
    if piece == 'B':
        if same_diagonal:
            return has_clear_path(board, py, px, ky, kx)
        return False
    
    # Queen: horizontal, vertical, or diagonal with clear path
    if piece == 'Q':
        if same_row or same_col or same_diagonal:
            return has_clear_path(board, py, px, ky, kx)
        return False
    
    return False


# ============================================================================
# BFS-based Check Detection
# ============================================================================

def checkmate(board_str):
    # Parse board
    board = []
    for row in board_str.strip().split("\n"):
        if " " in row:
            board.append(row.strip().split())  # spaced format
        else:
            board.append(list(row.strip()))
    size = len(board)

    # Find King
    king_pos = None
    for y in range(size):
        for x in range(size):
            if board[y][x] == "K":
                king_pos = (y, x)
                break
        if king_pos:
            break

    if not king_pos:
        print("Fail!!! No King on the board!!!")
        return False

    yk, xk = king_pos

    # BFS layer by layer
    def is_king_in_check():
        visited = set()
        queue = deque([(yk, xk, 0)])  # (y, x, distance)

        while queue:
            y, x, d = queue.popleft()
            if (y, x) in visited:
                continue
            visited.add((y, x))

            # skip king's own square
            if d > 0:
                piece = board[y][x]
                if piece != '.':
                    # Use unified attack checker
                    if is_piece_attacking_king(piece, (y, x), (yk, xk), board):
                        return True
                    
                    # Stop expansion from this piece (optimization: reduces cells visited)
                    continue

            # expand neighbors layer by layer
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1),
                           (-1,-1),(-1,1),(1,-1),(1,1)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < size and 0 <= nx < size and (ny, nx) not in visited:
                    queue.append((ny, nx, d + 1))

        return False

    return is_king_in_check()


# ============================================================================
# A*-based Check Detection with Threat Level
# ============================================================================

def checkmate_astar(board_str):
    # Parse board
    board = []
    for row in board_str.strip().split("\n"):
        if " " in row:
            board.append(row.strip().split())
        else:
            board.append(list(row.strip()))
    size = len(board)

    # Find King
    king_pos = None
    for y in range(size):
        for x in range(size):
            if board[y][x] == "K":
                king_pos = (y, x)
                break
        if king_pos:
            break

    if not king_pos:
        return False, 0

    yk, xk = king_pos

    # Find all enemy pieces
    enemies = [(y, x, board[y][x]) for y in range(size) for x in range(size)
               if board[y][x] in ('Q', 'R', 'B', 'P')]

    if not enemies:
        return False, 0

    # A* heuristic: Euclidean distance to nearest enemy
    def heuristic(y, x):
        return min(math.hypot(y - ey, x - ex) for ey, ex, _ in enemies)

    # A* search from King to find threatening pieces
    open_set = [(heuristic(yk, xk), 0, (yk, xk))]
    visited = set()
    found_threat = False
    min_distance = math.inf

    while open_set:
        f, g, (y, x) = heapq.heappop(open_set)
        if (y, x) in visited:
            continue
        visited.add((y, x))

        piece = board[y][x]
        # Use unified attack checker
        if piece in ('Q', 'R', 'B', 'P') and is_piece_attacking_king(piece, (y, x), (yk, xk), board):
            found_threat = True
            min_distance = min(min_distance, g)
            break

        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < size and 0 <= nx < size and (ny, nx) not in visited:
                heapq.heappush(open_set, (g + 1 + heuristic(ny, nx), g + 1, (ny, nx)))

    if found_threat:
        threat_level = max(0, 100 - min_distance * 15)
        return True, threat_level
    else:
        return False, 0


# ============================================================================
# Unified API Wrapper
# ============================================================================

def check_king_threat(board_str, use_astar=False):
    """
    Unified API for both check detection methods.
    
    Args:
        board_str: String representation of the chess board
        use_astar: If True, use A* method with threat level; if False, use BFS
    
    Returns:
        tuple: (in_check: bool, threat_level: int)
            - in_check: True if king is in check
            - threat_level: 0-100 for A*, always 0 for BFS
    """
    if use_astar:
        return checkmate_astar(board_str)
    else:
        is_check = checkmate(board_str)
        return is_check, 0