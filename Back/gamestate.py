# gamestate.py
class GameState:
    def __init__(self, size=8):
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.size = size
        self.remaining_pieces = {'Q': 1, 'R': 2, 'B': 2, 'P': 8}
        self.used_positions = set()
