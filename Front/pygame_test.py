import pygame
import sys

pygame.init()

# ---------------- Settings ----------------
SCREEN_W, SCREEN_H = 700, 700
BOARD_SIZE = 8              # 8x8 chessboard
CELL_SIZE = 50
PANEL_HEIGHT = 150
FRAME_THICKNESS = 20        # edge/frame width of board sprite
bg = (240,244,220)

# board area size
BOARD_PIXEL_SIZE = BOARD_SIZE * CELL_SIZE

# create window
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Chess Drag & Drop Demo")
clock = pygame.time.Clock()

# ---------------- Load board ----------------
board_img = pygame.image.load("Front/board_plain_01.png").convert_alpha()
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
                      grid_origin_y - FRAME_THICKNESS)

# ---------------- Piece Assets ----------------
PIECE_IMG = {
    "K": "Front/W_King.png",
    "Q": "Front/W_Queen.png",
    "R": "Front/W_Rook.png",
    "B": "Front/W_Bishop.png",
    "P": "Front/W_Pawn.png",
}


def draw_grid(surface):
    """Overlay grid lines for debugging alignment"""
    for r in range(BOARD_SIZE + 1):
        y = grid_origin_y + r * CELL_SIZE
        pygame.draw.line(surface, (255, 0, 0), (grid_origin_x, y), (grid_origin_x + INNER_SIZE, y))
    for c in range(BOARD_SIZE + 1):
        x = grid_origin_x + c * CELL_SIZE
        pygame.draw.line(surface, (255, 0, 0), (x, grid_origin_y), (x, grid_origin_y + INNER_SIZE))


# ---------------- Piece Class ----------------
class Piece(pygame.sprite.Sprite):
    def __init__(self, name, image, pos):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE *2 ))
        self.rect = self.image.get_rect(topleft=pos)
        self.dragging = False

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.dragging = True
                self.mouse_offset = (self.rect.x - event.pos[0], self.rect.y - event.pos[1])
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging:
                    self.dragging = False
                    self.snap_to_grid()
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self.rect.x = event.pos[0] + self.mouse_offset[0]
                self.rect.y = event.pos[1] + self.mouse_offset[1]

    def snap_to_grid(self):
        # snap only if inside grid
        if (grid_origin_x <= self.rect.centerx <= grid_origin_x + INNER_SIZE and
            grid_origin_y <= self.rect.centery <= grid_origin_y + INNER_SIZE):
            col = (self.rect.centerx - grid_origin_x) // CELL_SIZE
            row = (self.rect.centery - grid_origin_y) // CELL_SIZE
            self.rect.topleft = (grid_origin_x + col * CELL_SIZE,
                                 grid_origin_y + row * CELL_SIZE)
        else:
            # stay in panel if dropped outside board
            self.rect.y = grid_origin_y + INNER_SIZE + 20


# ---------------- Main ----------------
def main():
    # create pieces in the panel
    pieces = pygame.sprite.Group()
    x_offset = 20
    for i, (name, img) in enumerate(PIECE_IMG.items()):
        piece = Piece(name, img, (x_offset + i * (CELL_SIZE + 20), grid_origin_y + INNER_SIZE + 20))
        pieces.add(piece)

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        for piece in pieces:
            piece.update(events)

        screen.fill(bg)
        screen.blit(board_img, board_rect)  # board
        draw_grid(screen)                   # grid overlay
        pieces.draw(screen)                 # pieces

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
