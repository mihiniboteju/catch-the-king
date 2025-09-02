from collections import deque

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
