import pygame
import sys
import random

class VictoryScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        try:
            self.background_image = pygame.image.load('assets/img/victory_screen.png').convert_alpha()
            self.bg_image_rect = self.background_image.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            # Load and potentially resize the rain sock image
            self.rain_sock_image = pygame.image.load('assets/img/Victory_rain_sock.png').convert_alpha()
            self.rain_sock_image = pygame.transform.scale(self.rain_sock_image, (50, 50))  # Adjust size as needed
        except pygame.error as e:
            print(f"Failed to load an image: {e}")
            sys.exit()
        
        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        self.gold = (255, 215, 0)
        
        # Initialize raining socks
        self.raining_socks = self.init_raining_socks(30)  # Adjust the number of socks as needed

    def init_raining_socks(self, num_socks):
        """Initialize raining socks with random positions and velocities."""
        socks = []
        for _ in range(num_socks):
            x_pos = random.randint(0, self.screen.get_width())
            y_pos = random.randint(-self.screen.get_height(), 0)  # Start above the screen
            speed = random.randint(2, 6)  # Adjust speed as needed
            socks.append([x_pos, y_pos, speed])
        return socks

    def update_raining_socks(self):
        """Update the positions of the raining socks for the animation."""
        for sock in self.raining_socks:
            sock[1] += sock[2]  # Move sock down by its velocity
            # Reset sock to top after it falls beyond the screen
            if sock[1] > self.screen.get_height():
                sock[0] = random.randint(0, self.screen.get_width())
                sock[1] = random.randint(-100, 0)  # Start above the screen for continuous effect

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background_image, self.bg_image_rect.topleft)
        
        # Update and draw raining socks
        self.update_raining_socks()
        for sock in self.raining_socks:
            self.screen.blit(self.rain_sock_image, (sock[0], sock[1]))
        
        text_victory = self.font_large.render('Congratulations!', True, self.gold)
        text_rect = text_victory.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(text_victory, text_rect)
        
        score_text = f'Score: {getattr(self.game.player, "score", "N/A")}'
        text_score = self.font_small.render(score_text, True, self.gold)
        score_rect = text_score.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(text_score, score_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("ESC pressed - Transitioning to another state not implemented.")
