from collections import deque
import heapq
import math 

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

    # Pawn attack rule
    def pawn_attacks(yk, xk, py, px):
        return (py == yk + 1 and (px == xk - 1 or px == xk + 1))

    # BFS layer by layer
    def is_king_in_check():
        visited = set()
        queue = deque([(yk, xk, 0)])  # (y, x, distance)

        while queue:
            y, x, d = queue.popleft()
            if (y, x) in visited:
                continue
            visited.add((y, x))

            # skip king’s own square
            if d > 0:
                piece = board[y][x]
                if piece != '.':
                    # Check piece rules
                    if piece == 'P' and pawn_attacks(yk, xk, y, x):
                        return True
                    if piece == 'R' and (y == yk or x == xk):
                        return True
                    if piece == 'B' and abs(y - yk) == abs(x - xk):
                        return True
                    if piece == 'Q' and (y == yk or x == xk or abs(y - yk) == abs(x - xk)):
                        return True
                    # Blocked by another piece
                    continue

            # expand neighbors layer by layer
            for dy, dx in [(-1,0),(1,0),(0,-1),(0,1),
                           (-1,-1),(-1,1),(1,-1),(1,1)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < size and 0 <= nx < size and (ny, nx) not in visited:
                    queue.append((ny, nx, d + 1))

        return False

    return is_king_in_check()

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

    def pawn_attacks(yk, xk, py, px):
        return (py == yk + 1 and (px == xk - 1 or px == xk + 1))

    def is_attacking(piece, py, px):
        if piece == 'P' and pawn_attacks(yk, xk, py, px): return True
        if piece == 'R' and (py == yk or px == xk): return True
        if piece == 'B' and abs(py - yk) == abs(px - xk): return True
        if piece == 'Q' and (py == yk or px == xk or abs(py - yk) == abs(px - xk)): return True
        return False

    enemies = [(y, x, board[y][x]) for y in range(size) for x in range(size)
               if board[y][x] in ('Q', 'R', 'B', 'P')]

    if not enemies:
        return False, 0

    def heuristic(y, x):
        return min(math.hypot(y - ey, x - ex) for ey, ex, _ in enemies)

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
        if piece in ('Q', 'R', 'B', 'P') and is_attacking(piece, y, x):
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