# Subscribe Youtube : Ninja Code 
# Simple Point Collection Game | Collect Points and Avoid Obstacles


import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Star Shooter Game | Press 'R' to Reset, 'Q' to Quit")

# Define the Colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BLACK = (0,0,0)

# Set Up Fonts
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont (None, 24)

# Set up clock
clock = pygame.time.Clock()

# Define classes
class Shooter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill (RED)
        pygame.draw.rect(self.image, GREEN, (0,0,50,10))
        self.rect = self.image.get_rect ()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 8

    def update(self):
        keys = pygame.key.get_pressed()
        if keys [pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys [pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys [pygame.K_UP]:
            self.rect.y -= self.speed
        if keys [pygame.K_DOWN]:
            self.rect.y += self.speed

        # Keep the shooter within the screen
        self.rect.clamp_ip(screen.get_rect())


# Create class for Target
class Target (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill(YELLOW)
        pygame.draw.polygon(self.image, WHITE, [(25,0), (40, 40), (10,20)])
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange (0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = 6

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()


# Create class for Obstacles
class Obstacle (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill (BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange (0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = 6

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()


# Set up sprite groups
all_sprites = pygame.sprite.Group()
targets = pygame.sprite.Group()
obstacles = pygame.sprite.Group()


# Create the Shooter
shooter = Shooter()
all_sprites.add(shooter)


# Set up game variables
score = 0
game_over = False
start_time = pygame.time.get_ticks()
game_duration = 15000  # 15 seconds


# Main game Loop
while True:
    #Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reset the game
                score = 0
                game_over = False
                start_time = pygame.time.get_ticks()
                all_sprites.empty()
                targets.empty()
                obstacles.empty() 

                # Recreate the shooter 
                shooter = Shooter()
                all_sprites.add (shooter)
            elif event.key == pygame.K_q:
                # Quit the game
                pygame.quit()
                sys.exit()     

    if not game_over:
        # Spawn targets and obstacles
        if random.randrange (100) < 2:
            target = Target ()
            all_sprites.add (target)
            targets.add (target)
        if random.randrange (100) < 2:
            obstacle = Obstacle ()
            all_sprites.add (obstacle)
            obstacles.add(obstacle)

        # Update sprites
        all_sprites.update()

        # Check for collisions 
        hits = pygame.sprite.spritecollide(shooter, obstacles, False)
        if hits:
            game_over = True   

        # Check for collisions between shooter and targets
        hits = pygame.sprite.spritecollide(shooter, targets, True)
        for hit in hits:
            score += 1

        # Draw everything
        screen.fill (BLACK)
        all_sprites.draw(screen)     

        # Display score 
        score_text = font.render ("Score: " + str(score), True, WHITE)
        screen.blit (score_text, (10,10))

        # Display time remaining
        elapsed_time = pygame.time.get_ticks() - start_time
        time_remaining = max(0, game_duration - elapsed_time)
        time_text = font.render ("Time: " + str(time_remaining // 1000), True, WHITE)
        screen.blit (time_text, (SCREEN_WIDTH - 120, 10))

        # Check if the time is up
        if time_remaining == 0:
            game_over = True
    
    else:
        # Game over screen
        game_over_text = font.render ("Game Over", True, RED)
        screen.blit (game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
        final_score_text = font.render ("Final Score: " + str(score), True, WHITE)
        screen.blit (final_score_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 120))


    # Display instructions
    instructions_text = small_font.render("Press 'R' to Reset, 'Q' to Quit", True, WHITE)
    screen.blit (instructions_text, (SCREEN_WIDTH - 250, SCREEN_HEIGHT - 30))

    pygame.display.flip()
    clock.tick(60)
