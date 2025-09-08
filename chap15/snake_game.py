import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)

# Snake properties
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_speed = 15
direction = 'RIGHT'
change_to = direction

# Apple properties
apple_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10)) * 10]
apple_spawn = True

# Score
score = 0

# Game over function
def game_over():
    font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (width/2, height/4)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    quit()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Validate direction change
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Move the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == apple_pos[0] and snake_pos[1] == apple_pos[1]:
        score += 10
        apple_spawn = False
    else:
        snake_body.pop()

    if not apple_spawn:
        apple_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10)) * 10]
    apple_spawn = True

    screen.fill(black)

    for pos in snake_body:
        pygame.draw.rect(screen, blue, pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(screen, red, pygame.Rect(apple_pos[0], apple_pos[1], 10, 10))

    # Game Over conditions
    if snake_pos[0] < 0 or snake_pos[0] > width-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > height-10:
        game_over()

    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    pygame.display.update()
    pygame.time.Clock().tick(snake_speed)
