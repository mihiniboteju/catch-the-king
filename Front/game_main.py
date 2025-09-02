from math import trunc
import pygame
import sys
import os

# Import backend functionality
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Back'))
from gamestate import GameState
from checkmate import checkmate
from solver import can_still_win, find_remaining_solution, find_complete_solution
import random
import chessgame


pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound

# ---------------- Settings ----------------
SCREEN_W, SCREEN_H = 700, 700
BOARD_SIZE = 8              # 8x8 chessboard
CELL_SIZE = 50
PANEL_HEIGHT = 150
FRAME_THICKNESS = 20        # edge/frame width of board sprite
bg = (240,244,220)

# Get the folder where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define an assets folder
ASSETS_DIR = os.path.join(BASE_DIR, "Asset")
FONT = os.path.join(ASSETS_DIR,"PixelifySans-VariableFont_wght.ttf")
use_font = pygame.font.Font(FONT, 32)

# ---------------- Sound Effects ----------------
# Load sound effects (you'll need to add these audio files to your Asset folder)
try:
    PIECE_PLACE_SFX = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "Piece Down.wav"))
    PIECE_PICKUP_SFX = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "Piece Move.wav"))
    WIN_SFX = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "win.wav"))
    LOSE_SFX = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "lose.wav"))
    BUTTON_CLICK_SFX = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "Button press.wav"))
    RESTART_SFX = pygame.mixer.Sound(os.path.join(ASSETS_DIR,"Restart.wav"))
except:
    # If sound files don't exist, create dummy sounds
    PIECE_PLACE_SFX = None
    PIECE_PICKUP_SFX = None
    WIN_SFX = None
    LOSE_SFX = None
    BUTTON_CLICK_SFX = None
    RESTART_SFX = None
# board area size
BOARD_PIXEL_SIZE = BOARD_SIZE * CELL_SIZE

# create window
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Chess Drag & Drop Demo")
clock = pygame.time.Clock()

# ---------------- Load board ----------------
board_img = pygame.image.load(os.path.join(ASSETS_DIR,"board_plain_01.png")).convert_alpha()
board_img = pygame.transform.scale(
    board_img,
    (BOARD_PIXEL_SIZE + FRAME_THICKNESS * 2, BOARD_PIXEL_SIZE + FRAME_THICKNESS * 2)
)

# compute playable grid area
INNER_SIZE = BOARD_PIXEL_SIZE
grid_origin_x = (SCREEN_W - INNER_SIZE) // 2
grid_origin_y = (SCREEN_H - INNER_SIZE) // 2

# align board rect so grid centers correctly
board_rect = board_img.get_rect()
board_rect.topleft = (grid_origin_x - FRAME_THICKNESS,
                      grid_origin_y - FRAME_THICKNESS)  # Move board up by one row

# ---------------- Piece Assets ----------------
PIECE_IMG = {
    "King": os.path.join(ASSETS_DIR,"W_King.png"),
    "Queen": os.path.join(ASSETS_DIR,"W_Queen.png"),
    "Rook": os.path.join(ASSETS_DIR,"W_Rook.png"),
    "Bishop": os.path.join(ASSETS_DIR,"W_Bishop.png"),
    "Pawn": os.path.join(ASSETS_DIR,"W_Pawn.png"),
}

# Piece mapping for backend
PIECE_MAPPING = {
    "Queen": "Q",
    "Rook": "R", 
    "Bishop": "B",
    "Pawn": "P"
}

def play_sfx(sound):
    """Play a sound effect if it exists"""
    if sound is not None:
        sound.play()

def draw_grid(surface):
    """Overlay grid lines for debugging alignment"""
    # Draw horizontal lines (rows)
    for r in range(BOARD_SIZE + 1):
        y = grid_origin_y + r * CELL_SIZE
        pygame.draw.line(surface, (255, 0, 0), (grid_origin_x, y), (grid_origin_x + INNER_SIZE, y))
    # Draw vertical lines (columns)
    for c in range(BOARD_SIZE + 1):
        x = grid_origin_x + c * CELL_SIZE
        pygame.draw.line(surface, (255, 0, 0), (x, grid_origin_y), (x, grid_origin_y + INNER_SIZE))

# ---------------- Piece Class ----------------
class Piece(pygame.sprite.Sprite):
    STOCK_Y = grid_origin_y + INNER_SIZE + 20  # panel y-coordinate

    stock_registry = {}  # name -> stock info {count, pos}

    def __init__(self, name, image, pos, is_stock=False):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE*2))
        self.rect = self.image.get_rect(topleft=pos)

        self.dragging = False
        self.locked = False
        self.is_stock = is_stock  # stock icon in the panel
        self.grid_pos = None  # (row, col) position on the board

        if is_stock:
            # Register stock info if first time
            if name not in Piece.stock_registry:
                Piece.stock_registry[name] = {"count": 0, "pos": pos}
            Piece.stock_registry[name]["count"] += 1

        self.mouse_offset = (0, 0)
        self.font = pygame.font.Font(FONT, 24)  # Change to Arial font

    # ---------------- Event handling ----------------
    def update(self, events, scene=None):
        if self.locked:
            return
        for event in events: 
            if self.is_stock:
                # Click on stock → spawn new piece
                if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                    stock_info = Piece.stock_registry[self.name]
                    if stock_info["count"] > 0:
                        stock_info["count"] -= 1
                        
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        # spawn new piece exactly at mouse position
                        new_piece = Piece(self.name, PIECE_IMG[self.name],(mouse_x-25, mouse_y-70))
                        new_piece.dragging = True
                        new_piece.mouse_offset = (-25, -70)  # No offset since we're spawning at mouse position
                        play_sfx(PIECE_PICKUP_SFX)
                        # remove icon when stock is empty
                        if stock_info["count"] == 0 and scene:
                            scene.pieces.remove(self)

                        return new_piece
                return None

            # Dragging logic for placed piece
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.dragging = True
                self.mouse_offset = (self.rect.x - event.pos[0], self.rect.y - event.pos[1])
                  # Play pickup sound
            elif event.type == pygame.MOUSEBUTTONUP and self.dragging:
                self.dragging = False
                self.snap_to_grid(scene)
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self.rect.x = event.pos[0] + self.mouse_offset[0]
                self.rect.y = event.pos[1] + self.mouse_offset[1]

        return None

    # ---------------- Drawing ----------------
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.is_stock:
            count = Piece.stock_registry[self.name]["count"]
            if count > 0:
                text = self.font.render("x "+str(count), True, (0, 0, 0))
                surface.blit(text, (self.rect.right + 5, self.rect.y+80))

    # ---------------- Snap to grid ----------------
    def snap_to_grid(self, scene):
        # Get current mouse position for snapping
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # snap only if mouse is inside grid
        if (grid_origin_x <= mouse_x <= grid_origin_x + INNER_SIZE and
            grid_origin_y <= mouse_y <= grid_origin_y + INNER_SIZE):
            col = (mouse_x - grid_origin_x) // CELL_SIZE
            row = (mouse_y - grid_origin_y) // CELL_SIZE
            
            # Validate that row and col are within the valid 8x8 grid (0-7)
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                if (row, col) not in GameScene.placed_positions:
                    # Center the piece vertically within the cell
                    piece_x = grid_origin_x + col * CELL_SIZE
                    piece_y = grid_origin_y + row * CELL_SIZE - CELL_SIZE // 2 - 25
                    self.rect.topleft = (piece_x, piece_y)
                    self.grid_pos = (row, col)
                    print(row,col)
                    GameScene.placed_positions.add((row, col))
                    self.locked = True
                    play_sfx(PIECE_PLACE_SFX)  # Play place sound
                    # Update backend game state
                    if scene and scene.game_state:
                        scene.update_backend_state(self.name, row, col)
                        
                        
                else:
                    # Invalid spot → return to panel
                    self.rect.topleft = (self.rect.x, Piece.STOCK_Y)
                    self.grid_pos = None
            else:
                # Out of valid grid range → return to panel
                self.rect.topleft = (self.rect.x, Piece.STOCK_Y)
                self.grid_pos = None
        else:
            # Out of board → return to panel
            self.rect.topleft = (self.rect.x, Piece.STOCK_Y)
            self.grid_pos = None

# ---------------- Main ----------------
class GameScene():
    placed_positions = set()  # moved here so Piece.snap_to_grid works

    def __init__(self, settings, game):
        self.settings = settings
        self.game = game  # Add the game reference
        self.pieces = pygame.sprite.Group()
        
        # Initialize backend game state
        self.game_state = GameState(BOARD_SIZE)
        self.game_state.remaining_pieces = {}
        
        # Convert frontend settings to backend format
        for piece_name, count in settings.items():
            if piece_name in PIECE_MAPPING:
                backend_piece = PIECE_MAPPING[piece_name]
                self.game_state.remaining_pieces[backend_piece] = count
        
        # Generate random king position
        self.king_pos = (random.randint(0, BOARD_SIZE-1), random.randint(0, BOARD_SIZE-1))
        self.game_state.used_positions.add(self.king_pos)
        
        # Game state variables
        self.game_won = False
        self.solution = False
        self.game_over = False
        self.show_king = False
        
        # UI elements
        self.font = pygame.font.Font(FONT, 24)  # Main game status font
        self.small_font = pygame.font.Font(FONT, 24)

        # spawn stock icons with counts from settings
        x_offset = 20
        for name, count in settings.items():
            if count > 0:
                stock_piece = Piece(name, PIECE_IMG[name], (x_offset, Piece.STOCK_Y), is_stock=True)
                Piece.stock_registry[name] = {"count": count, "pos": (x_offset, Piece.STOCK_Y)}
                self.pieces.add(stock_piece)
                x_offset += CELL_SIZE + 60
    
    def update_backend_state(self, piece_name, row, col):
        """Update the backend game state when a piece is placed"""
        if piece_name in PIECE_MAPPING:
            backend_piece = PIECE_MAPPING[piece_name]
            self.game_state.board[row][col] = backend_piece
            self.game_state.remaining_pieces[backend_piece] -= 1
            chessgame.display_board(self.game_state.board, hide_king=True)
            # Check win conditions
            self.check_win_conditions(row, col)
    
    
    def check_win_conditions(self, row, col):
        """Check if the game is won after placing a piece"""
        # Check if king was found
        if (row, col) == self.king_pos:
            self.game_won = True
            self.game_over = True
            self.show_king = True
            return
        
        # Check for checkmate
        board_str = self.board_to_string()
        if checkmate(board_str):
            self.game_won = True
            self.game_over = True
            self.show_king = True
            play_sfx(WIN_SFX)
            return
        
        # Check if no more pieces available
        if all(count == 0 for count in self.game_state.remaining_pieces.values()):
            self.game_over = True
            self.show_king = True
            if not self.game_won:
                play_sfx(LOSE_SFX)  # Play lose sound
    
    def board_to_string(self):
        """Convert backend board to string format for checkmate function"""
        test_board = [row[:] for row in self.game_state.board]
        king_row, king_col = self.king_pos
        test_board[king_row][king_col] = 'K'
        return '\n'.join(' '.join(row) for row in test_board)
    
    def can_still_win(self):
        """Check if it's still possible to win with remaining pieces"""
        return can_still_win(self.game_state.board, self.game_state.remaining_pieces, self.king_pos)
    
    def show_solution(self):
        """Display the complete solution on the board"""
        # Get the complete solution - note the parameter order: (king_pos, available_pieces, board_size)
        solution = find_complete_solution(self.king_pos, self.game_state.remaining_pieces, BOARD_SIZE)
        print(self.game_state.remaining_pieces)
        
        if solution:
            # Clear current board
            
            # Place all pieces from the solution
            for move in solution:
                piece_type, row, col = move
                # Convert backend piece type to frontend name
                piece_name = None
                for name, backend_type in PIECE_MAPPING.items():
                    if backend_type == piece_type:
                        piece_name = name
                        break
                
                if piece_name:
                    # Create piece at solution position
                    piece_x = grid_origin_x + col * CELL_SIZE
                    piece_y = grid_origin_y + row * CELL_SIZE - CELL_SIZE // 2 - 25
                    
                    solution_piece = Piece(piece_name, PIECE_IMG[piece_name], (piece_x, piece_y))
                    solution_piece.grid_pos = (row, col)
                    solution_piece.locked = True
                    GameScene.placed_positions.add((row, col))
                    self.pieces.add(solution_piece)
                    
                    # Update backend state
                    self.game_state.board[row][col] = piece_type
            
            # Show the king
            self.show_king = True
            
            # End the game
            self.game_over = True
            self.solution = True
            
            return True
        else:
            return False
    
    def restart_game(self):
        """Restart the game with the same settings"""
        # Clear all placed pieces
        GameScene.placed_positions.clear()
        
        # Clear all pieces from the scene
        self.pieces.empty()
        
        # Reset game state
        self.game_state = GameState(BOARD_SIZE)
        self.game_state.remaining_pieces = {}
        
        # Convert frontend settings to backend format
        for piece_name, count in self.settings.items():
            if piece_name in PIECE_MAPPING:
                backend_piece = PIECE_MAPPING[piece_name]
                self.game_state.remaining_pieces[backend_piece] = count
        
        # Generate new random king position
        self.king_pos = (random.randint(0, BOARD_SIZE-1), random.randint(0, BOARD_SIZE-1))
        self.game_state.used_positions.add(self.king_pos)
        
        # Reset game state variables
        self.game_won = False
        self.solution = False
        self.game_over = False
        self.show_king = False
        
        # Reset stock registry
        Piece.stock_registry.clear()
        
        # Spawn stock icons with counts from settings
        x_offset = 20
        for name, count in self.settings.items():
            if count > 0:
                stock_piece = Piece(name, PIECE_IMG[name], (x_offset, Piece.STOCK_Y), is_stock=True)
                Piece.stock_registry[name] = {"count": count, "pos": (x_offset, Piece.STOCK_Y)}
                self.pieces.add(stock_piece)
                x_offset += CELL_SIZE + 60
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.running = False
            elif event.key == pygame.K_h and not self.game_over:
                # Show AI hint
                play_sfx(LOSE_SFX)  # Play button click sound
                self.show_solution()
            elif event.key == pygame.K_a and not self.game_over:
                # Check if still possible to win
                if self.can_still_win():
                    print("Still possible to win!")
                else:
                    print("No possible way to catch the King!")
            elif event.key == pygame.K_r and self.game_over:
                # Reset the game with the same settings
                self.restart_game()
                play_sfx(RESTART_SFX)

    def draw(self, screens):
        screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                
                # Handle game events
                self.handle_event(event)

            # Update all pieces with the event list
            new_pieces = []
            for piece in list(self.pieces):
                spawned = piece.update(events, self)
                if spawned:
                    self.pieces.add(spawned)

            # Draw
            screen.fill(bg)
            screen.blit(board_img, board_rect)
            # draw_grid(screen)

            # Draw king if game is over
            if self.show_king:
                king_img = pygame.image.load(PIECE_IMG["King"]).convert_alpha()
                king_img = pygame.transform.scale(king_img, (CELL_SIZE, CELL_SIZE*2))
                king_rect = king_img.get_rect()
                # Center the king vertically within the cell
                king_x = grid_origin_x + self.king_pos[1] * CELL_SIZE
                king_y = grid_origin_y + self.king_pos[0] * CELL_SIZE - CELL_SIZE // 2 - 25
                king_rect.topleft = (king_x, king_y)
                screen.blit(king_img, king_rect)

            # draw each piece manually (so counts appear)
            for piece in self.pieces:
                piece.draw(screen)
            
            # Draw game status
            self.draw_game_status(screen)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()
    
    def draw_game_status(self, screen):
        """Draw game status messages"""
        if self.game_over:
            if self.game_won:
                text = self.font.render("YOU WIN!", True, (0, 255, 0))
            elif self.solution:
                text = self.font.render("SOLUTION", True, (50, 50, 50))
            else:
                text = self.font.render("GAME OVER - You Lose!", True, (255, 0, 0))
            
            text_rect = text.get_rect(center=(SCREEN_W // 2, 50))
            screen.blit(text, text_rect)
            
            # Draw restart instruction
            restart_text = self.font.render("Press R to Restart", True, (0, 0, 255))
            restart_rect = restart_text.get_rect(center=(SCREEN_W // 2, 100))
            screen.blit(restart_text, restart_rect)
        
        # Draw controls hint
        controls = [
            "Press H for solution",
        ]
        
        y_offset = 50
        for control in controls:
            text = self.small_font.render(control, True, (0, 0, 0))
            screen.blit(text, (10, y_offset))
            y_offset += 25