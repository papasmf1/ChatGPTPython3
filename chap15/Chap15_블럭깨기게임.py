import pygame
import sys

# 초기화
pygame.init()
WIDTH, HEIGHT = 480, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("블럭깨기 게임")
clock = pygame.time.Clock()

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 패들
paddle = pygame.Rect(WIDTH // 2 - 40, HEIGHT - 30, 80, 10)
paddle_speed = 7

# 공
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)
ball_speed = [5, -5]

# 블럭
block_rows = 5
block_cols = 8
block_width = 50
block_height = 20
blocks = []
for row in range(block_rows):
    for col in range(block_cols):
        block = pygame.Rect(10 + col * (block_width + 10), 40 + row * (block_height + 10), block_width, block_height)
        blocks.append(block)

running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 패들 이동
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    # 공 이동
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # 벽 충돌
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] = -ball_speed[0]
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]
    if ball.bottom >= HEIGHT:
        # 게임 오버
        font = pygame.font.SysFont(None, 48)
        text = font.render("Game Over", True, RED)
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 24))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # 패들 충돌
    if ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1]

    # 블럭 충돌
    hit_index = ball.collidelist(blocks)
    if hit_index != -1:
        del blocks[hit_index]
        ball_speed[1] = -ball_speed[1]

    # 그리기
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    for block in blocks:
        pygame.draw.rect(screen, GREEN, block)

    # 클리어
    if not blocks:
        font = pygame.font.SysFont(None, 48)
        text = font.render("Clear!", True, BLUE)
        screen.blit(text, (WIDTH // 2 - 60, HEIGHT // 2 - 24))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()