import pygame
import sys
import random
import math

# Constants
WIDTH, HEIGHT = 600, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 60, 20
BRICK_ROWS, BRICK_COLS = 4, 10
BRICK_PADDING = 5
WHITE = (255, 255, 255)
PADDLE_SPEED = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Initialize Pygame
pygame.init()

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Initialize game variables
paddle_x = (WIDTH - PADDLE_WIDTH) // 2
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = BALL_SPEED_X, BALL_SPEED_Y
lives = 3  

paddle = pygame.Rect(paddle_x, HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT)

# Function to create random brick colors
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Initialize levels with random brick colors
levels = [
    [
        [random.choice([1, 0]) for _ in range(BRICK_COLS)] for _ in range(BRICK_ROWS)
    ],
    [
        [random.choice([1, 0]) for _ in range(BRICK_COLS)] for _ in range(BRICK_ROWS)
    ],
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    ]
]

current_level = 2
bricks = []
for row in levels[current_level]:
    for brick_exists in row:
        if brick_exists:
            brick = pygame.Rect(
                len(bricks) % BRICK_COLS * (BRICK_WIDTH + BRICK_PADDING),
                len(bricks) // BRICK_COLS * (BRICK_HEIGHT + BRICK_PADDING),
                BRICK_WIDTH, BRICK_HEIGHT
            )
            bricks.append((brick, random_color()))

# Game state variables
game_over = False
you_win = False
start_screen = True

# Function to reset the game
def reset_game():
    global paddle, ball_x, ball_y, ball_dx, ball_dy, bricks, game_over, you_win, start_screen
    paddle = pygame.Rect(paddle_x, HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_dx, ball_dy = BALL_SPEED_X, BALL_SPEED_Y
    bricks = []
    for row in levels[current_level]:
        for brick_exists in row:
            if brick_exists:
                brick = pygame.Rect(
                    len(bricks) % BRICK_COLS * (BRICK_WIDTH + BRICK_PADDING),
                    len(bricks) // BRICK_COLS * (BRICK_HEIGHT + BRICK_PADDING),
                    BRICK_WIDTH, BRICK_HEIGHT
                )
                bricks.append((brick, random_color()))
    game_over = False
    you_win = False
    start_screen = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if start_screen:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_screen = False
        elif game_over or you_win:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Check if the player has lives remaining before resetting
                if lives > 0:
                    reset_game()
                    lives -= 1  # Deduct a life when starting a new game

    if not start_screen:
        if not game_over and not you_win:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and paddle.left > 0:
                paddle.move_ip(-PADDLE_SPEED, 0)
            if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
                paddle.move_ip(PADDLE_SPEED, 0)

            ball_x += ball_dx
            ball_y += ball_dy

            # Ball collisions with walls
            if ball_x <= 0 or ball_x >= WIDTH:
                ball_dx *= -1
            if ball_y <= 0:
                ball_dy *= -1

            # Ball collision with paddle
            if paddle.colliderect(pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)):
                ball_dy *= -1

            # Ball collision with bricks
            for brick, brick_color in bricks[:]:
                if brick.colliderect(pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)):
                    bricks.remove((brick, brick_color))
                    ball_dy *= -1

            # Check if the player has won the level
            if len(bricks) == 0:
                you_win = True

            # Check if the player has lost a life
            if ball_y >= HEIGHT:
                # Deduct a life
                lives -= 1

                if lives > 0:
                    reset_game()
                else:
                    game_over = True

        # Clear the screen
        window.fill((0, 0, 0))

        # Draw bricks with random colors
        for brick, brick_color in bricks:
            pygame.draw.rect(window, brick_color, brick)

        # Draw paddle
        pygame.draw.rect(window, WHITE, paddle)

        # Draw ball
        pygame.draw.circle(window, WHITE, (int(ball_x), int(ball_y)), BALL_RADIUS)

        # Draw "Game Over" or "You Win" message and "Play Again" instructions
        if game_over:
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over!", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            window.blit(text, text_rect)

            play_again_text = font.render("Press SPACE to Play Again", True, WHITE)
            play_again_rect = play_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            window.blit(play_again_text, play_again_rect)
        elif you_win:
            font = pygame.font.Font(None, 36)
            text = font.render("You Win!", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            window.blit(text, text_rect)

            play_again_text = font.render("Press SPACE to Play Again", True, WHITE)
            play_again_rect = play_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            window.blit(play_again_text, play_again_rect)

        # Draw lives
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        window.blit(lives_text, (500, 350))

    # Draw start screen
    if start_screen:
        font = pygame.font.Font(None, 36)
        start_text = font.render("Brick Breaker Game", True, WHITE)
        start_text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        window.blit(start_text, start_text_rect)

        start_text2 = font.render("Press SPACE to Start", True, WHITE)
        start_text_rect2 = start_text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        window.blit(start_text2, start_text_rect2)

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
sys.exit()
