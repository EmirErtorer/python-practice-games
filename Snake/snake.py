import pygame, random

# initialize pygame
pygame.init()

# Set FPS and clock
FPS = 20
clock = pygame.time.Clock()

# Set the display
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake")

# Set game values
SNAKE_SIZE = 20

head_x = WINDOW_WIDTH//2
head_y = WINDOW_HEIGHT//2 

snake_dx = 0
snake_dy = 0

score = 0

# Set colors
GREEN = (0, 255, 0)
DARKGREEN = (10, 50, 10)
RED = (255, 0, 0)
DARKRED = (150, 0, 0)
WHITE = (255, 255, 255)

# Set Fonts
font = pygame.font.SysFont("gabriola", 48)

# Set texts
title_text = font.render("Snake", True, DARKGREEN)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH // 2
title_rect.y = 10

score_text = font.render("Score: " + str(score), True, GREEN)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

game_over_text = font.render("GAME OVER", True, RED, DARKRED)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press any key to play again", True, RED, DARKRED)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

# Set images (using simple rects)
apple_coord =  (500, 500, SNAKE_SIZE, SNAKE_SIZE)
apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)

head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)

body_coords = []

# Load Sound
pick_up_sound = pygame.mixer.Sound("pick_up_sound.wav")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Moving the snake
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                snake_dx = -1 * SNAKE_SIZE
                snake_dy = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                snake_dx = SNAKE_SIZE
                snake_dy = 0
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                snake_dx = 0
                snake_dy = -1 * SNAKE_SIZE
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                snake_dx = 0
                snake_dy = SNAKE_SIZE

    # Add the head coordinate to the first index of the body coordinate
    body_coords.insert(0, head_coord)
    # Pop the last item to maintain the same length of the snake's body
    body_coords.pop()

    # Upate the x-y position of snake's head
    head_x += snake_dx
    head_y += snake_dy
    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

    # Check for game over
    if (head_rect.left < 0 or head_rect.right > WINDOW_WIDTH
        or head_rect.top < 0 or head_rect.bottom > WINDOW_HEIGHT
        or head_coord in body_coords):
        
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        # Pause the game until player presses a key
        is_pause = True
        while is_pause:
            for event in pygame.event.get():
                # The player wants to play again
                if event.type == pygame.KEYDOWN:
                    score = 0

                    head_x = WINDOW_WIDTH // 2
                    head_y = WINDOW_HEIGHT // 2
                    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

                    body_coords = []

                    snake_dx = 0
                    snake_dy = 0

                    is_pause = False

                # The player wants to quit the game
                if event.type == pygame.QUIT:
                    is_pause = False
                    running = False


    # Check for collisions
    if head_rect.colliderect(apple_rect):
        score += 1
        pick_up_sound.play()

        # Move the apple
        apple_x = random.randint(0, WINDOW_WIDTH - SNAKE_SIZE)
        apple_y = random.randint(0, WINDOW_HEIGHT - SNAKE_SIZE)
        apple_coord = (apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE)

        # Add to the body
        body_coords.append(head_coord)
    
    # Update HUD
    score_text = font.render("Score: " + str(score), True, GREEN)

    # Fill the surface
    display_surface.fill(WHITE)

    # Blit assets
    for body in body_coords:
        pygame.draw.rect(display_surface, DARKGREEN, body)

    head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)
    apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)
    

    # Blit HUD
    display_surface.blit(title_text, title_rect)
    display_surface.blit(score_text, score_rect)
 
    # Update the display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
