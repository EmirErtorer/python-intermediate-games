import pygame, random

# Initialize pygame
pygame.init()

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set display surface
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Define Classes
class Game():
    """A class to control and update gameplay"""
    def __init__(self, player, alien_group, player_bullet_group, alien_bullet_group):
        """Initialize the game"""
        self.player = player
        self.alien_group = alien_group
        self.player_bullet_group = player_bullet_group
        self.alien_bullet_group = alien_bullet_group

        # Set game values
        self.score = 0
        self.current_round = 1

        # Set sounds 
        self.new_round_sound = pygame.mixer.Sound("Sounds/new_round.wav")
        self.player_hit_sound = pygame.mixer.Sound("Sounds/player_hit.wav")
        self.breach_sound = pygame.mixer.Sound("Sounds/breach.wav")
        self.alien_hit_sound = pygame.mixer.Sound("Sounds/alien_hit.wav")

        # Set font
        self.font = pygame.font.Font("Fonts/Facon.ttf", 32)
        
    def update(self):
        """Update the game"""
        self.shift_aliens()
        self.check_collision()
        self.chech_round_completion()

    def draw(self):
        """Draw the HUD and other information to display"""

        # Set colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        # Set text
        self.score_text = self.font.render("SCORE: " + str(self.score), True, WHITE)
        self.score_rect = self.score_text.get_rect()
        self.score_rect.centerx =  WINDOW_WIDTH//2
        self.score_rect.top = 10

        self.lives_text = self.font.render("LIVES: " + str(self.player.lives), True, WHITE)
        self.lives_rect = self.lives_text.get_rect()
        self.lives_rect.topright = (WINDOW_WIDTH - 20, 10)

        self.round_text = self.font.render("ROUND: " + str(self.current_round), True, WHITE)
        self.round_rect = self.round_text.get_rect()
        self.round_rect.topleft = (20, 10)

        # Blit the HUD
        display_surface.blit(self.score_text, self.score_rect)
        display_surface.blit(self.lives_text, self.lives_rect)
        display_surface.blit(self.round_text, self.round_rect)

        # Draw the lines
        pygame.draw.line(display_surface, WHITE, (0, 50), (WINDOW_WIDTH, 50), 4)
        pygame.draw.line(display_surface, WHITE, (0, WINDOW_HEIGHT - 100), (WINDOW_WIDTH, WINDOW_HEIGHT - 100), 4)

    def shift_aliens(self):
        """Shift a wave of aliens down the screen and the opposite direction"""
        # Determine if alien group has hit an edge
        shift = False
        for alien in (self.alien_group.sprites()):
            if alien.rect.left <= 0 or alien.rect.right >= WINDOW_WIDTH:
                shift = True
        
        # Shift every alien down, change direction and check for a breach
        if shift:
            breach = False
            for alien in self.alien_group.sprites():
                # Shift down
                alien.rect.y += 10*self.current_round
                
                # Reverse the direction and move the alien off the edge
                alien.direction *= -1
                alien.rect.x += alien.direction * alien.velocity

                # Check if an alien reached the ship
                if alien.rect.bottom >= WINDOW_HEIGHT - 100:
                    breach = True

            # Aliens breached the lines
            if breach:
                self.breach_sound.play()
                self.player.lives -= 1
                self.check_game_status("Aliens breached the line!", "Press 'ENTER' to continue")


    def check_collision(self):
        """Check for collisions"""
        # See if any bullet in the player bullet group hit an alien in the alien group
        if pygame.sprite.groupcollide(self.player_bullet_group, self.alien_group, True, True):
            self.alien_hit_sound.play()
            self.score += 100
        # See if any alien bullet in alien bullet group hit the player
        if pygame.sprite.spritecollide( self.player, self.alien_bullet_group, True):
            self.player_hit_sound.play()
            self.player.lives -= 1

            self.check_game_status("You've been hit!", "Press 'ENTER' to continue'")


    def chech_round_completion(self):
        """Check to see if a player has completed a single round"""
        # See if there are any aliens left
        if not (self.alien_group):
            self.current_round += 1
            self.score += 300*self.current_round

            self.new_round()

    def new_round(self):
        """Start a new round"""
        # Create a grid of Aliens: 11 columns and 5 rows
        for i in range(11):
            for j in range(5):
                alien = Aliens(64 + i*64, 64 + j*64, self.current_round, self.alien_bullet_group)
                self.alien_group.add(alien)
        
        # Pause the game and prompt user to start
        self.new_round_sound.play()
        self.pause_game("Space Invaders Round " + str(self.current_round), "Press 'ENTER' to begin")


    def check_game_status(self, main_text, sub_text):
        """Check to see the status of the game and how the player died"""
        # Empty the bullet groups and reset the player and remaining aliens
        self.alien_bullet_group.empty()
        self.player_bullet_group.empty()
        self.player.reset()
        for alien in self.alien_group:
            alien.reset()

        # Check if the game is over or a simple round reset
        if self.player.lives <= 0:
            self.reset_game()
        else:
            self.pause_game(main_text, sub_text)

    def pause_game(self, main_text, sub_text):
        """Pause the game"""
        global running

        # Set colors
        WHITE = (255, 255, 255)
        PURPLE = (49,0,71)

        # Create main pause text
        main_text = self.font.render(main_text, True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        # Create sub pause text
        sub_text = self.font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

        # Blit the pause text
        display_surface.fill(PURPLE)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        # Pause the game until user hits enter
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                # The user wants to play again
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                # The user wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False


    def reset_game(self):
        """Reset the game"""
        self.pause_game("Final Score: " + str(self.score), "Press 'ENTER' to play again")

        # Reset game values
        self.current_round = 1
        self.score = 0

        self.player.lives = 5

        # Empty groups
        self.alien_group.empty()
        self.alien_bullet_group.empty()
        self.player_bullet_group.empty()

        # Start a new game
        self.new_round()

class Player(pygame.sprite.Sprite):
    """A class to model a player spaceship"""

    def __init__(self, bullet_group):
        """Initialize the player"""
        super().__init__()

        self.image = pygame.image.load("Images/player_ship.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH//2
        self.rect.bottom = WINDOW_HEIGHT

        # Player sounds
        self.player_fire = pygame.mixer.Sound("Sounds/player_fire.wav")

        # Player attributes
        self.velocity = 8
        self.lives = 5

        self.bullet_group = bullet_group

    def update(self):
        """Update the spaceship"""
       
        keys = pygame.key.get_pressed()
        # Control the ship
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.velocity
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity

    def shoot(self):
        """Shoot bullets"""
        # Restrict the number of bullets at a time
        if len(self.bullet_group) < 2:
            self.player_fire.play()
            PlayerBullet(self.rect.centerx, self.rect.top, self.bullet_group)
        

    def reset(self):
        """Reset the player position"""
        self.rect.centerx = WINDOW_WIDTH//2
        

class PlayerBullet(pygame.sprite.Sprite):
    """A class to represent the lasers shot by the player"""
    def __init__(self, x, y, bullet_group):
        """Initialize the bullet"""
        super().__init__()

        self.image = pygame.image.load("Images/green_laser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_group.add(self)
    
    def update(self):
        """Update the bullet"""
        self.rect.y -= self.velocity

        # If the bullet is off the screen, remove it
        if self.rect.bottom < 0:
            self.kill() # removes it from sprite group


class Aliens(pygame.sprite.Sprite):
    """A class to mode enemy aliens"""
    def __init__(self, x, y,veloicty, bullet_group):
        super().__init__()
        self.image = pygame.image.load("Images/alien.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.bullet_group = bullet_group
        self.velocity = veloicty

        self.starting_x = x
        self.starting_y = y

        self.direction = 1

        # Alien sounds
        self.alien_fire = pygame.mixer.Sound("Sounds/alien_fire.wav")

    def update(self):
        """Update the aliens"""
        self.rect.x += self.direction * self.velocity

        # Randomly fire a bullet
        if random.randint(0, 1000) > 999 and len(self.bullet_group) < 3:
            self.shoot()

    def shoot(self):
        """Shoot a bullet"""
        self.alien_fire.play()
        AlienBullet(self.rect.centerx, self.rect.bottom, self.bullet_group)

    def reset(self):
        """Reset the alien position"""
        self.rect.topleft = (self.starting_x, self.starting_y)
        self.direction = 1

class AlienBullet(pygame.sprite.Sprite):
    """A class to represent the lasers shot by the player"""
    def __init__(self, x, y, bullet_group):
        super().__init__()
        self.image = pygame.image.load("Images/red_laser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        self.velocity = 10
        bullet_group.add(self)

    def update(self):
        """Update the bullet"""
        self.rect.y += self.velocity

        # If bullet goes off screen, kill it
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
        

# Create bullet groups
my_player_bullet_group = pygame.sprite.Group()
my_alien_bullet_group = pygame.sprite.Group()

# Create a player object and a sprite group
my_player = Player(my_player_bullet_group)
my_player_group = pygame.sprite.Group()
my_player_group.add(my_player)

# Create an alien group
my_alien_group = pygame.sprite.Group()

# Create a Game object
my_game = Game(my_player, my_alien_group, my_player_bullet_group, my_alien_bullet_group)
my_game.new_round()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # The player wants to shoot
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.shoot()
    
    # Fill the surface
    display_surface.fill((49,0,71))

    # Update and display the sprite groups
    my_player_group.update()
    my_player_group.draw(display_surface)

    my_alien_group.update()
    my_alien_group.draw(display_surface)

    my_player_bullet_group.update()
    my_player_bullet_group.draw(display_surface)

    my_alien_bullet_group.update()
    my_alien_bullet_group.draw(display_surface)
    
    # Update and draw game object
    my_game.update()
    my_game.draw()

    # Update the display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

# End the game
pygame.quit()