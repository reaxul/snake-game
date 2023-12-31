import pygame
import random

# Initialize Pygame
pygame.init()

# Set up screen dimensions
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reazul's Snake Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
HEAD_COLOR = (41, 128, 185)  # Turquoise or another bright color
BODY_COLOR = (39, 174, 96)   # Green or another color that contrasts well
FOOD_COLOR = (192, 57, 43)   # Red or another color that stands out
GAME_OVER_COLOR = (231, 76, 60)

# Load fonts
font = pygame.font.Font(None, 24)
large_font = pygame.font.Font(None, 36)

# Load background image
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
screen.blit(background, (0, 0))

# Snake and food positions
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
food = (random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))

# Direction
direction = (1, 0)

# Game states
initial_screen = True
playing = False
paused = False
game_over = False
clock = pygame.time.Clock()
frame_rate = 6

# Draw grid lines
for x in range(0, WIDTH, GRID_SIZE):
    pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
for y in range(0, HEIGHT, GRID_SIZE):
    pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))


while initial_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            initial_screen = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            playing = True
            initial_screen = False
    
    screen.blit(background, (0, 0))
    
    # Display instructions and play button
    instructions = [
        "Welcome to the Snake Game!",
        "Use arrow keys to control the snake.",
        "Avoid running into walls and yourself.",
        "Eat the food to grow and score points."
    ]
    for idx, line in enumerate(instructions):
        text = font.render(line, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100 + idx * 40))
        screen.blit(text, text_rect)
    
    play_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 40, 120, 60)
    pygame.draw.rect(screen, GREEN, play_button)
    play_text = large_font.render("Play", True, BLACK)
    play_text_rect = play_text.get_rect(center=play_button.center)
    screen.blit(play_text, play_text_rect)
    
    pygame.display.flip()

while playing:
    prev_direction = direction  # Store previous direction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused  # Toggle pause state
            elif event.key == pygame.K_r and game_over:  # Restart when "R" key is pressed
                snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
                food = (random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))
                direction = (1, 0)
                game_over = False
            elif event.key == pygame.K_UP and prev_direction != (0, 1):  # Prevent moving down
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and prev_direction != (0, -1):  # Prevent moving up
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and prev_direction != (1, 0):  # Prevent moving right
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and prev_direction != (-1, 0):  # Prevent moving left
                direction = (1, 0)
    
    if not paused and not game_over:
        # Clear the screen
        screen.blit(background, (0, 0))

         # Draw grid lines
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

        
        # Update snake position and growth
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            direction = (0, -1)
        if keys[pygame.K_DOWN]:
            direction = (0, 1)
        if keys[pygame.K_LEFT]:
            direction = (-1, 0)
        if keys[pygame.K_RIGHT]:
            direction = (1, 0)
        
        new_head = (
            (snake[0][0] + direction[0]) % GRID_WIDTH,
            (snake[0][1] + direction[1]) % GRID_HEIGHT
        )
        
        # Check for collision with snake's body
        if new_head in snake:
            game_over = True
        else:
            snake.insert(0, new_head)
        
        # Check if snake ate the food
        if snake[0] == food:
            food = (random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT))
        else:
            snake.pop()
        
        # Draw snake with gradient colors and texture
        for index, segment in enumerate(snake):
            rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if index == 0:
                pygame.draw.rect(screen, HEAD_COLOR, rect)
            else:
                color_percentage = index / len(snake)
                gradient_color = (
                    int(HEAD_COLOR[0] * (1 - color_percentage) + BODY_COLOR[0] * color_percentage),
                    int(HEAD_COLOR[1] * (1 - color_percentage) + BODY_COLOR[1] * color_percentage),
                    int(HEAD_COLOR[2] * (1 - color_percentage) + BODY_COLOR[2] * color_percentage)
                )
                pygame.draw.rect(screen, gradient_color, rect)
                
                # Draw a simple texture pattern (scales)
                scale_texture = pygame.Surface((GRID_SIZE, GRID_SIZE))
                for y in range(0, GRID_SIZE, 2):
                    for x in range(GRID_SIZE):
                        pygame.draw.rect(scale_texture, (0, 0, 0), (x, y, 1, 1))
                screen.blit(scale_texture, rect)
        
        # Draw food
        food_rect = pygame.Rect(food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, FOOD_COLOR, food_rect)
    
    if game_over:
        # Display "Game Over" message and restart instructions
        screen.fill(GAME_OVER_COLOR)
        game_over_text = large_font.render("Game Over", True, BLACK)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect)
        
        restart_text = font.render("Press 'R' to restart", True, BLACK)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(restart_text, restart_rect)
    
    pygame.display.flip()
    
    clock.tick(frame_rate)  # Limit frame rate
    
# Quit Pygame
pygame.quit()
