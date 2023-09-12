import pygame, random

# initialize pygame 
pygame.init()

# set fps and clock
FPS = 60
clock = pygame.time.Clock()

# set the display
WINDOWS_WIDTH = 800
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOWS_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Burger Barker")

# set game values
PLAYER_STARTING_LIVES = 3
PLAYER_STARTING_VELOCITY = 5
PLAYER_BOOST_VELOCITY = 10
STARTING_BOOST_LEVEL = 100
STARTING_BURGER_VELOCITY = 3
BURGER_ACCELERATION = .25
BUFFER_DISTANCE = 100

score = 0 
burger_points = 0
burgers_eaten = 0

player_lives = PLAYER_STARTING_LIVES
player_velocity = PLAYER_STARTING_VELOCITY

boost_level = STARTING_BOOST_LEVEL

burger_velocity = STARTING_BURGER_VELOCITY

# set colors
ORANGE = (246, 170, 54)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# set fonts
font = pygame.font.Font("WashYourHand.ttf", 32)

# set text
points_text = font.render("Burger points: " + str(burger_points), True, ORANGE)
points_rect = points_text.get_rect()
points_rect.topleft = (10, 10)

score_text = font.render("Score: " + str(score), True, ORANGE)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 50)

title_text = font.render("Burger Barker", True, ORANGE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOWS_WIDTH // 2
title_rect.y = 10

eaten_text = font.render("Burgers eaten: " + str(burgers_eaten), True, ORANGE)
eaten_rect = eaten_text.get_rect()
eaten_rect.centerx = WINDOWS_WIDTH // 2
eaten_rect.y = 50

lives_text = font.render("Lives: " + str(player_lives), True, ORANGE)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOWS_WIDTH - 10, 10)

boost_text = font.render("Boost: " + str(boost_level), True, ORANGE)
boost_rect = boost_text.get_rect()
boost_rect.topright = (WINDOWS_WIDTH - 10, 50)

game_over_text = font.render("Final Score: " + str(score), True, ORANGE)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOWS_WIDTH // 2, WINDOW_HEIGHT // 2)

continue_text = font.render("Press any key to play again", True, ORANGE)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOWS_WIDTH // 2, WINDOW_HEIGHT // 2 - 64)

# set sounds and music
bark_sound = pygame.mixer.Sound("bark_sound.wav")
miss_sound = pygame.mixer.Sound("miss_sound.wav")
pygame.mixer.music.load("bd_background_music.wav")

# set images
player_image_left = pygame.image.load("dog_left.png")
player_image_right = pygame.image.load("dog_right.png")

player_image = player_image_left
player_rect = player_image.get_rect()
player_rect.centerx = WINDOWS_WIDTH // 2
player_rect.bottom = WINDOW_HEIGHT

burger_image = pygame.image.load("burger.png")
burger_rect = burger_image.get_rect()
burger_rect.topleft = (random.randint(0, WINDOWS_WIDTH - 32), -BUFFER_DISTANCE)

# main game loop 
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # move the player
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_rect.left > 0:
        player_rect.x -= player_velocity
        player_image = player_image_left
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_rect.right < WINDOWS_WIDTH:
        player_rect.x += player_velocity
        player_image = player_image_right
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_rect.top > 100 :
        player_rect.y -= player_velocity
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += player_velocity

    # Engage boost
    if keys[pygame.K_SPACE] and boost_level > 0:
        player_velocity = PLAYER_BOOST_VELOCITY
        boost_level -= 1
    else:
        player_velocity = PLAYER_STARTING_VELOCITY

    # Move the burger and update burger points
    burger_rect.y += burger_velocity
    burger_points = int(burger_velocity * (WINDOW_HEIGHT - burger_rect.y + 100))

    # Player missed the burger
    if burger_rect.y > WINDOW_HEIGHT:
        miss_sound.play()
        player_lives -= 1

        burger_rect.topleft = (random.randint(0, WINDOWS_WIDTH - 32), -BUFFER_DISTANCE)
        burger_velocity = STARTING_BURGER_VELOCITY

        player_rect.centerx = WINDOWS_WIDTH // 2
        player_rect.bottom = WINDOW_HEIGHT

        boost_level = STARTING_BOOST_LEVEL
    
    # Check for collision
    if player_rect.colliderect(burger_rect):
        bark_sound.play()
        score += burger_points
        burgers_eaten += 1

        burger_rect.topleft = (random.randint(0, WINDOWS_WIDTH - 32), -BUFFER_DISTANCE)
        burger_velocity += BURGER_ACCELERATION

        boost_level += 25
        if boost_level > STARTING_BOOST_LEVEL:
            boost_level = STARTING_BOOST_LEVEL

    # Update the HUD
    points_text = font.render("Burger Points: " + str(burger_points), True, ORANGE)
    score_text = font.render("Score: " + str(score), True, ORANGE)
    eaten_text = font.render("Burgers Eaten: " + str(burgers_eaten), True, ORANGE)
    lives_text = font.render("Lives: " + str(player_lives), True, ORANGE)
    boost_text = font.render("Boost: " + str(boost_level), True, ORANGE)

    # Game over
    if player_lives == 0:
        game_over_text = font.render("Final Score: " + str(score), True, ORANGE)
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        # Pause the game until player presses a game
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                # The player wants to play again
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    burger_velocity = STARTING_BURGER_VELOCITY
                    burgers_eaten = 0
                    boost_level = STARTING_BOOST_LEVEL

                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False
                # The player wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    # Fill the surface
    display_surface.fill(BLACK)

    # Blitting HUD
    display_surface.blit(points_text, points_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(eaten_text, eaten_rect)
    display_surface.blit(lives_text, lives_rect)
    display_surface.blit(boost_text, boost_rect)
    pygame.draw.line(display_surface, WHITE, (0, 100), (WINDOWS_WIDTH, 100), 3)
    pygame.draw.line(display_surface, WHITE, (WINDOWS_WIDTH // 2 - 100, 45), (WINDOWS_WIDTH // 2 + 100, 45), 3)

    # Blitting assets
    display_surface.blit(player_image, player_rect)
    display_surface.blit(burger_image, burger_rect)

    # Tick the clock and update the display
    pygame.display.update()
    clock.tick(FPS)

# exit the game
pygame.quit()
    