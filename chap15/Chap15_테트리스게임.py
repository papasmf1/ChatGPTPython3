import pygame
import random

# 게임 설정
CELL_SIZE = 30
COLS = 10
ROWS = 20
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS
FPS = 60
DROP_SPEED = 500  # ms

# 블록 모양 (회전 포함)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
]
COLORS = [
    (0, 255, 255), (255, 255, 0), (128, 0, 128),
    (255, 165, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0)
]

def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

class Block:
    def __init__(self):
        self.type = random.randint(0, len(SHAPES) - 1)
        self.shape = [row[:] for row in SHAPES[self.type]]
        self.color = COLORS[self.type]
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = rotate(self.shape)

    def get_coords(self):
        coords = []
        for i, row in enumerate(self.shape):
            for j, val in enumerate(row):
                if val:
                    coords.append((self.x + j, self.y + i))
        return coords

def check_collision(board, block, dx=0, dy=0, rotated_shape=None):
    shape = rotated_shape if rotated_shape else block.shape
    for i, row in enumerate(shape):
        for j, val in enumerate(row):
            if val:
                x = block.x + j + dx
                y = block.y + i + dy
                if x < 0 or x >= COLS or y < 0 or y >= ROWS:
                    return True
                if board[y][x]:
                    return True
    return False

def merge_block(board, block):
    for x, y in block.get_coords():
        board[y][x] = block.color

def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = ROWS - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0] * COLS)
    return new_board, lines_cleared

def draw_board(screen, board, block):
    screen.fill((0, 0, 0))
    # Draw board
    for y in range(ROWS):
        for x in range(COLS):
            color = board[y][x]
            if color:
                pygame.draw.rect(screen, color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Draw current block
    for x, y in block.get_coords():
        pygame.draw.rect(screen, block.color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    # Draw grid
    for x in range(COLS):
        pygame.draw.line(screen, (40, 40, 40), (x*CELL_SIZE, 0), (x*CELL_SIZE, HEIGHT))
    for y in range(ROWS):
        pygame.draw.line(screen, (40, 40, 40), (0, y*CELL_SIZE), (WIDTH, y*CELL_SIZE))
    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("테트리스")
    clock = pygame.time.Clock()
    board = [[0] * COLS for _ in range(ROWS)]
    block = Block()
    drop_event = pygame.USEREVENT + 1
    pygame.time.set_timer(drop_event, DROP_SPEED)
    running = True
    fast_drop = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == drop_event:
                if not check_collision(board, block, dy=1):
                    block.y += 1
                else:
                    merge_block(board, block)
                    board, _ = clear_lines(board)
                    block = Block()
                    if check_collision(board, block):
                        running = False  # Game Over
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(board, block, dx=-1):
                        block.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(board, block, dx=1):
                        block.x += 1
                elif event.key == pygame.K_DOWN:
                    fast_drop = True
                elif event.key == pygame.K_UP:
                    rotated = rotate(block.shape)
                    if not check_collision(board, block, rotated_shape=rotated):
                        block.shape = rotated
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    fast_drop = False

        if fast_drop:
            if not check_collision(board, block, dy=1):
                block.y += 1
            else:
                merge_block(board, block)
                board, _ = clear_lines(board)
                block = Block()
                if check_collision(board, block):
                    running = False

        draw_board(screen, board, block)
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()