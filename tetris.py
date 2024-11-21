import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Shapes of the Tetriminos
SHAPES = [
    [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']],
    [['.....',
      '..00.',
      '..00.',
      '.....',
      '.....']],
    [['.....',
      '..00.',
      '.00..',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']],
    [['.....',
      '.00..',
      '..00.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']],
    [['.....',
      '000..',
      '..0..',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '000..',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']],
    [['.....',
      '000..',
      '.0...',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '...0.',
      '000..',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']],
    [['.....',
      '000..',
      '...0.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.0...',
      '000..',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....']]
]

# Tetrimino class
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.rotation = 0

# Create the grid
def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(WIDTH // BLOCK_SIZE)] for _ in range(HEIGHT // BLOCK_SIZE)]

    # Add locked pieces
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

# Convert piece to a list of positions
def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))
    return positions

# Check if the piece is within grid boundaries
def valid_space(piece, grid):
    accepted_positions = [[(x, y) for x in range(WIDTH // BLOCK_SIZE) if grid[y][x] == BLACK] for y in range(HEIGHT // BLOCK_SIZE)]
    accepted_positions = [x for sublist in accepted_positions for x in sublist]

    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

# Check if game is over
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

# Get random shape
def get_shape():
    return Piece(WIDTH // 2 // BLOCK_SIZE, 0, random.choice(SHAPES))

# Draw grid lines
def draw_grid(surface):
    for y in range(HEIGHT // BLOCK_SIZE):
        pygame.draw.line(surface, WHITE, (0, y * BLOCK_SIZE), (WIDTH, y * BLOCK_SIZE))
    for x in range(WIDTH // BLOCK_SIZE):
        pygame.draw.line(surface, WHITE, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, HEIGHT))

# Clear rows if they are full
def clear_rows(grid, locked_positions):
    rows_to_clear = []
    for y in range(len(grid) - 1, -1, -1):
        if BLACK not in grid[y]:
            rows_to_clear.append(y)
            for x in range(WIDTH // BLOCK_SIZE):
                try:
                    del locked_positions[(x, y)]
                except:
                    continue
    if len(rows_to_clear) > 0:
        for key in sorted(list(locked_positions), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < min(rows_to_clear):
                newKey = (x, y + len(rows_to_clear))
                locked_positions[newKey] = locked_positions.pop(key)
    return len(rows_to_clear)

# Draw window
def draw_window(surface, grid):
    surface.fill(BLACK)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    draw_grid(surface)
    pygame.display.update()

# Main function
def main():
    locked_positions = {}
    grid = create_grid()

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.3
        fall_time += clock.get_rawtime()
        clock.tick()

        # Handle piece falling
        if fall_time / 1000 >= fall_speed:
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
            fall_time = 0

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        # Add piece to grid
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = RED

        # If the piece is locked
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = RED
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            clear_rows(grid, locked_positions)

        draw_window(screen, grid)

        if check_lost(locked_positions):
            run = False

    pygame.display.quit()

main()
