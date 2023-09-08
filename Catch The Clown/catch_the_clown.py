import pygame
import random

# initialize pygame
pygame.init()

WINDOW_WIDTH = 945
WINDOW_HEIGHT = 600
display_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Catch The Clown")

# Set the FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game constants
STARTING_PLAYER_LIVES = 5
CLOWN_STARTING_VELOCITY = 5
CLOWN_ACCELARITION = .5

score = 0
player_lives = STARTING_PLAYER_LIVES

clown_velocity = CLOWN_STARTING_VELOCITY
clown_dx = random.choice([-1, 1]) # left or right
clown_dy = random.choice([-1, 1]) # up or down


# Set the colors
YELLOW = (248, 231, 28)
BLUE = (1, 175, 209)

# Load the images
clown_image = pygame.image.load("clown.png")
clown_rect = clown_image.get_rect()
clown_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

background_image = pygame.image.load("background.png")
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0) # Align the background image with the display screen

# Load the sounds
miss_sound = pygame.mixer.Sound("miss_sound.wav")
click_sound = pygame.mixer.Sound("click_sound.wav")
pygame.mixer.music.load("ctc_background_music.wav")

# Set Font
font = pygame.font.Font("Franxurter.ttf", 32)

# Set the text
title_text = font.render("Catch The Clown", True, BLUE)
title_rect = title_text.get_rect()
title_rect.topleft = (50, 10)

score_text = font.render("Score: " + str(score), True, YELLOW)
score_rect = score_text.get_rect()
score_rect.topright = (WINDOW_WIDTH - 50, 10)

lives_text = font.render("Lives: " + str(player_lives), True, YELLOW)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 50, 50)

game_over_text = font.render("GAME OVER", True, BLUE, YELLOW)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Click anywhere to play again", True, YELLOW, BLUE)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

# Main game loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # A click is made
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]

            # The clown was clicked
            if clown_rect.collidepoint(mouse_x, mouse_y):
                click_sound.play()
                score += 1
                clown_velocity += CLOWN_ACCELARITION

                # Move the clown in new direction
                previous_dx = clown_dx
                previous_dy = clown_dy

                # Guarentees that the direction will change
                while (previous_dx == clown_dx and previous_dy == clown_dy):
                    clown_dx = random.choice([-1, 1]) # left or right
                    clown_dy = random.choice([-1, 1]) # up or down

            else:
                # We missed the clown
                miss_sound.play()
                player_lives -= 1

    # Move the clown
    clown_rect.x += clown_dx*clown_velocity 
    clown_rect.y += clown_dy*clown_velocity 

    #Bounce the clown off the edges of the display
    if clown_rect.left <= 0:
        clown_dx = 1
    if clown_rect.right >= WINDOW_WIDTH:
        clown_dx = -1
    if clown_rect.top <= 0:
        clown_dy = 1
    if clown_rect.bottom >= WINDOW_HEIGHT:
        clown_dy = -1

    # Update HUD
    score_text = font.render("Score: " + str(score), True, YELLOW)
    lives_text = font.render("Lives: " + str(player_lives), True, YELLOW)
    game_over_text = font.render("GAME OVER", True, BLUE, YELLOW)

    # Check for game over
    if player_lives == 0:
        display_screen.blit(game_over_text, game_over_rect)
        display_screen.blit(continue_text, continue_rect)
        pygame.display.update()

        # Pause the game until the player clicks then reset the game
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                # The player wants to play again
                if event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    player_lives = STARTING_PLAYER_LIVES

                    clown_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
                    clown_velocity = CLOWN_STARTING_VELOCITY
                    clown_dx = random.choice([-1, 1]) # left or right
                    clown_dy = random.choice([-1, 1]) # up or down

                    pygame.mixer.music.play(-1, 0.0)

                    is_paused = False
                
                # The players wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    # Blit the background
    display_screen.blit(background_image, background_rect)

    # Blit the HUD
    display_screen.blit(title_text, title_rect)
    display_screen.blit(score_text, score_rect)
    display_screen.blit(lives_text, lives_rect)

    # Blit the assets
    display_screen.blit(clown_image, clown_rect)
  
    # Tick the clock and update the game
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
    