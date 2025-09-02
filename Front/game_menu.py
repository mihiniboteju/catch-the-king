import pygame
import sys
import os
from game_main import GameScene

DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(DIR, "Asset")
BUTTON_SFX = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "Button press.wav"))
# --- Constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60
FONT_NAME = os.path.join(ASSETS_DIR,"PixelifySans-VariableFont_wght.ttf")
BG_COLOR = (30, 30, 40)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
BLUE = (70, 130, 180)
GREEN = (60, 180, 120)
RED = (200, 60, 60)
BLACK = (0, 0, 0)
BUTTON_COLOR = (50, 50, 70)
BUTTON_HOVER = (80, 80, 120)



# --- Utility Classes ---
class Button:
    def __init__(self, rect, text, font, callback, color=BUTTON_COLOR, hover_color=BUTTON_HOVER, text_color=WHITE):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.callback = callback
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            if event.button == 1:
                BUTTON_SFX.play()
                self.callback()

# --- Scene Base ---
class Scene:
    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass

# --- Title Scene ---
class TitleScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        # Load and scale the background image (must be present in the project directory)
        self.bg_image = pygame.image.load(os.path.join(ASSETS_DIR,"title_bg_v2.png")).convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))
        self.font_med = pygame.font.Font(FONT_NAME, 32)
        btn_w, btn_h = 150, 50
        btn_x = (WIDTH - btn_w) // 2
        btn_y = HEIGHT - btn_h - 55  # 60px above the bottom
        self.start_button = Button(
            rect=(btn_x, btn_y, btn_w, btn_h),
            text="Start",
            font=self.font_med,
            callback=self.start_game
        )

    def start_game(self):
        self.game.change_scene(SettingScene(self.game))

    def handle_event(self, event):
        self.start_button.handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.running = False

    def draw(self, surface):
        # Draw the background image
        surface.blit(self.bg_image, (0, 0))
        # Draw the Start button at the center bottom
        self.start_button.draw(surface)

# --- Setting Scene ---
class SettingScene(Scene):
    PIECES = [
        {"name": "Queen", "min": 0, "max": 1, "color": RED},
        {"name": "Rook", "min": 1, "max": 2, "color": GRAY},
        {"name": "Bishop", "min": 1, "max": 2, "color": GREEN},
        {"name": "Pawn", "min": 1, "max": 8, "color": WHITE}
    ]

    def __init__(self, game):
        super().__init__(game)
        self.font_title = pygame.font.Font(FONT_NAME, 48)
        self.font_row = pygame.font.Font(FONT_NAME, 28)
        self.font_btn = pygame.font.Font(FONT_NAME, 24)
        self.counts = [piece["min"] for piece in self.PIECES]
        self.buttons = []
        self.create_piece_buttons()
        # Start button
        btn_w, btn_h = 180, 50
        btn_x = (WIDTH - btn_w) // 2
        btn_y = HEIGHT - 80
        self.start_button = Button(
            rect=(btn_x, btn_y, btn_w, btn_h),
            text="Start",
            font=self.font_btn,
            callback=self.start_game
        )

    def create_piece_buttons(self):
        self.buttons = []
        start_y = 160
        row_h = 60
        btn_size = 40
        margin_x = 180
        for i, piece in enumerate(self.PIECES):
            y = start_y + i * row_h
            # Only add +/- for pieces with max > min
            if piece["max"] > piece["min"]:
                minus_btn = Button(
                    rect=(margin_x, y, btn_size, btn_size),
                    text="–",
                    font=self.font_btn,
                    callback=lambda idx=i: self.change_count(idx, -1)
                )
                plus_btn = Button(
                    rect=(WIDTH - margin_x - btn_size, y, btn_size, btn_size),
                    text="+",
                    font=self.font_btn,
                    callback=lambda idx=i: self.change_count(idx, 1)
                )
                self.buttons.append((minus_btn, plus_btn))
            else:
                self.buttons.append((None, None))

    def change_count(self, idx, delta):
        piece = self.PIECES[idx]
        new_count = self.counts[idx] + delta
        if piece["min"] <= new_count <= piece["max"]:
            self.counts[idx] = new_count

    def start_game(self):
        settings = {piece["name"]: self.counts[i] for i, piece in enumerate(self.PIECES)}
        self.game.change_scene(GameScene(settings, self.game))

    def handle_event(self, event):
        for minus_btn, plus_btn in self.buttons:
            if minus_btn:
                minus_btn.handle_event(event)
            if plus_btn:
                plus_btn.handle_event(event)
        self.start_button.handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.running = False

    def draw(self, surface):
        surface.fill(BG_COLOR)
        # Title
        title_surf = self.font_title.render("Settings", True, WHITE)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 80))
        surface.blit(title_surf, title_rect)
        # Piece rows
        start_y = 160
        row_h = 60
        btn_size = 40
        element_spacing = 10  # spacing between counter elements
        left_margin = 200
        right_margin = 200
        for i, piece in enumerate(self.PIECES):
            y = start_y + i * row_h
            name = piece["name"]
            count = self.counts[i]
            minus_btn, plus_btn = self.buttons[i]
            # Piece name (left-aligned)
            name_surf = self.font_row.render(name, True, WHITE)
            name_rect = name_surf.get_rect(midleft=(left_margin, y + btn_size // 2))
            surface.blit(name_surf, name_rect)
            # Counter group (right-aligned)
            num_surf = self.font_row.render(str(count), True, WHITE)
            counter_w = 0
            if minus_btn:
                counter_w += btn_size + element_spacing
            counter_w += num_surf.get_width() + element_spacing
            if plus_btn:
                counter_w += btn_size
            counter_x = WIDTH - right_margin - counter_w
            x = counter_x
            # Draw minus button
            if minus_btn:
                minus_btn.rect.topleft = (x, y)
                minus_btn.draw(surface)
                x += btn_size + element_spacing
            # Draw number
            num_rect = num_surf.get_rect(topleft=(x, y + btn_size // 2 - num_surf.get_height() // 2))
            surface.blit(num_surf, num_rect)
            x += num_surf.get_width() + element_spacing
            # Draw plus button
            if plus_btn:
                plus_btn.rect.topleft = (x, y)
                plus_btn.draw(surface)
        # Start button
        self.start_button.draw(surface)

# --- Game Scene ---
# class GameScene(Scene):
#     PIECE_ORDER = ["Pawn", "Rook", "Knight", "Bishop", "Queen"]
#     PIECE_IMAGE_FILES = {
#         "Pawn": os.path.join(ASSETS_DIR,"W_Pawn.png"),
#         "Rook": os.path.join(ASSETS_DIR,"W_Rook.png"),
#         "Knight": os.path.join(ASSETS_DIR,"W_Knight.png"),
#         "Bishop": os.path.join(ASSETS_DIR,"W_Bishop.png"),
#         "Queen": os.path.join(ASSETS_DIR,"W_Queen.png"),
#     }

#     def __init__(self, game, settings):
#         super().__init__(game)
#         self.settings = settings
#         self.font_title = pygame.font.Font(FONT_NAME, 48)
#         self.font_piece = pygame.font.Font(FONT_NAME, 24)
#         self.font_count = pygame.font.Font(FONT_NAME, 20)
#         # Load images for each piece
#         self.piece_images = {}
#         for name in self.PIECE_ORDER:
#             img = pygame.image.load(self.PIECE_IMAGE_FILES[name]).convert_alpha()
#             img = pygame.transform.smoothscale(img, (50, 100))
#             self.piece_images[name] = img

#     def handle_event(self, event):
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
#             self.game.running = False

#     def draw(self, surface):
#         surface.fill(BG_COLOR)
#         # Title
#         title_surf = self.font_title.render("Game Started!", True, WHITE)
#         title_rect = title_surf.get_rect(center=(WIDTH // 2, 80))
#         surface.blit(title_surf, title_rect)
#         # Piece images
#         piece_w, piece_h = 50, 100
#         margin_bottom = 80
#         spacing = WIDTH // len(self.PIECE_ORDER)
#         y_img = HEIGHT - margin_bottom - piece_h
#         y_text = HEIGHT - margin_bottom + 10
#         for i, name in enumerate(self.PIECE_ORDER):
#             x = spacing // 2 + i * spacing
#             img = self.piece_images[name]
#             img_rect = img.get_rect(center=(x, y_img + piece_h // 2))
#             surface.blit(img, img_rect)
#             # Piece name
#             name_surf = self.font_piece.render(name, True, WHITE)
#             name_rect = name_surf.get_rect(center=(x, y_text))
#             surface.blit(name_surf, name_rect)
#             # Count
#             count = self.settings[name]
#             count_surf = self.font_count.render(f"x {count}", True, WHITE)
#             count_rect = count_surf.get_rect(center=(x, y_text + 28))
#             surface.blit(count_surf, count_rect)

# --- Game Manager ---
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene = TitleScene(self)

    def change_scene(self, scene):
        self.scene = scene

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.scene.handle_event(event)
            self.scene.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

# --- Main ---
if __name__ == "__main__":
    Game().run()