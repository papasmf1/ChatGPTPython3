import pygame
import random
import time

# 초기화
pygame.init()

# 한글 폰트 설정
def get_font(size):
    try:
        # Windows 기본 한글 폰트들
        font_names = ['malgun.ttf', 'gulim.ttc', 'batang.ttc', 'dotum.ttc']
        for font_name in font_names:
            try:
                return pygame.font.Font(f"C:/Windows/Fonts/{font_name}", size)
            except:
                continue
        # 폰트를 찾지 못한 경우 기본 폰트 사용
        return pygame.font.Font(None, size)
    except:
        return pygame.font.Font(None, size)

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# 게임 설정
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (BOARD_WIDTH + 8)
SCREEN_HEIGHT = BLOCK_SIZE * BOARD_HEIGHT

# 화면 설정
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("테트리스")
clock = pygame.time.Clock()

# 테트리스 블록 모양 정의
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

COLORS = [CYAN, YELLOW, PURPLE, ORANGE, BLUE, GREEN, RED]

class Tetris:
    def __init__(self):
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 0.5  # 초기 낙하 속도 (초)
        
    def new_piece(self):
        # 새로운 블록 생성
        shape_idx = random.randint(0, len(SHAPES) - 1)
        return {
            'shape': SHAPES[shape_idx],
            'color': COLORS[shape_idx],
            'x': BOARD_WIDTH // 2 - len(SHAPES[shape_idx][0]) // 2,
            'y': 0
        }
    
    def valid_move(self, piece, dx=0, dy=0, rotation=0):
        # 이동이나 회전이 유효한지 확인
        shape = piece['shape']
        if rotation:
            shape = self.rotate_piece(shape, rotation)
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece['x'] + x + dx
                    new_y = piece['y'] + y + dy
                    
                    if (new_x < 0 or new_x >= BOARD_WIDTH or 
                        new_y >= BOARD_HEIGHT or 
                        (new_y >= 0 and self.board[new_y][new_x])):
                        return False
        return True
    
    def rotate_piece(self, shape, direction):
        # 블록 회전
        if direction == 1:  # 시계방향
            return list(zip(*shape[::-1]))
        elif direction == -1:  # 반시계방향
            return list(zip(*shape))[::-1]
        return shape
    
    def place_piece(self):
        # 현재 블록을 보드에 배치
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    board_y = self.current_piece['y'] + y
                    board_x = self.current_piece['x'] + x
                    if board_y >= 0:
                        self.board[board_y][board_x] = self.current_piece['color']
        
        # 완성된 줄 제거
        self.clear_lines()
        
        # 새로운 블록 생성
        self.current_piece = self.new_piece()
        
        # 게임 오버 확인
        if not self.valid_move(self.current_piece):
            self.game_over = True
    
    def clear_lines(self):
        # 완성된 줄 제거
        lines_to_clear = []
        for y in range(BOARD_HEIGHT):
            if all(self.board[y]):
                lines_to_clear.append(y)
        
        for line in lines_to_clear:
            del self.board[line]
            self.board.insert(0, [0 for _ in range(BOARD_WIDTH)])
        
        # 점수 계산
        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            self.score += len(lines_to_clear) * 100 * self.level
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(0.1, 0.5 - (self.level - 1) * 0.05)
    
    def move_piece(self, dx, dy):
        # 블록 이동
        if self.valid_move(self.current_piece, dx, dy):
            self.current_piece['x'] += dx
            self.current_piece['y'] += dy
            return True
        return False
    
    def rotate_current_piece(self):
        # 현재 블록 회전
        rotated_shape = self.rotate_piece(self.current_piece['shape'], 1)
        original_shape = self.current_piece['shape']
        self.current_piece['shape'] = rotated_shape
        
        if not self.valid_move(self.current_piece):
            self.current_piece['shape'] = original_shape
    
    def drop_piece(self):
        # 블록을 아래로 떨어뜨림
        while self.move_piece(0, 1):
            pass
        self.place_piece()
    
    def update(self, dt):
        # 게임 업데이트
        if not self.game_over:
            self.fall_time += dt
            if self.fall_time >= self.fall_speed:
                if not self.move_piece(0, 1):
                    self.place_piece()
                self.fall_time = 0
    
    def draw(self):
        # 게임 화면 그리기
        screen.fill(BLACK)
        
        # 보드 그리기
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x]:
                    pygame.draw.rect(screen, self.board[y][x],
                                   (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, GRAY,
                               (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
        
        # 현재 블록 그리기
        if not self.game_over:
            for y, row in enumerate(self.current_piece['shape']):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(screen, self.current_piece['color'],
                                       ((self.current_piece['x'] + x) * BLOCK_SIZE,
                                        (self.current_piece['y'] + y) * BLOCK_SIZE,
                                        BLOCK_SIZE, BLOCK_SIZE))
        
        # UI 그리기
        font = get_font(36)
        
        # 점수
        score_text = font.render(f"점수: {self.score}", True, WHITE)
        screen.blit(score_text, (BOARD_WIDTH * BLOCK_SIZE + 10, 20))
        
        # 레벨
        level_text = font.render(f"레벨: {self.level}", True, WHITE)
        screen.blit(level_text, (BOARD_WIDTH * BLOCK_SIZE + 10, 60))
        
        # 줄 수
        lines_text = font.render(f"줄: {self.lines_cleared}", True, WHITE)
        screen.blit(lines_text, (BOARD_WIDTH * BLOCK_SIZE + 10, 100))
        
        # 조작법
        controls_font = get_font(24)
        controls = [
            "조작법:",
            "←→: 이동",
            "↓: 빠른 낙하",
            "↑: 회전",
            "스페이스: 즉시 낙하"
        ]
        
        for i, control in enumerate(controls):
            control_text = controls_font.render(control, True, WHITE)
            screen.blit(control_text, (BOARD_WIDTH * BLOCK_SIZE + 10, 200 + i * 30))
        
        # 게임 오버 메시지
        if self.game_over:
            game_over_font = get_font(48)
            game_over_text = game_over_font.render("게임 오버!", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)
            
            restart_font = get_font(24)
            restart_text = restart_font.render("R키를 눌러 재시작", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(restart_text, restart_rect)

def main():
    game = Tetris()
    running = True
    last_time = time.time()
    
    while running:
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if not game.game_over:
                    if event.key == pygame.K_LEFT:
                        game.move_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        game.move_piece(1, 0)
                    elif event.key == pygame.K_DOWN:
                        game.move_piece(0, 1)
                    elif event.key == pygame.K_UP:
                        game.rotate_current_piece()
                    elif event.key == pygame.K_SPACE:
                        game.drop_piece()
                else:
                    if event.key == pygame.K_r:
                        game = Tetris()
        
        game.update(dt)
        game.draw()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
