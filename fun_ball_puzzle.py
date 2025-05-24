#!/usr/bin/env python3
"""
Fun Ball Puzzle Game
A simple game where the player controls a paddle to catch colorful balls.
"""
import pygame
import sys
import random
import os
from pygame import mixer

# Initialize pygame
pygame.init()
mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (255, 165, 0),  # Orange
    (128, 0, 128)   # Purple
]

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fun Ball Puzzle")
clock = pygame.time.Clock()

# Load fonts
title_font = pygame.font.SysFont('Arial', 64, bold=True)
font = pygame.font.SysFont('Arial', 32)
small_font = pygame.font.SysFont('Arial', 24)

# Try to load sound effects
try:
    catch_sound = mixer.Sound(os.path.join('sounds', 'catch.wav'))
    # If sound file doesn't exist, we'll create a simple one
    if not os.path.exists(os.path.join('sounds', 'catch.wav')):
        # Create sounds directory if it doesn't exist
        if not os.path.exists('sounds'):
            os.makedirs('sounds')

        # Generate a simple sound using pygame
        pygame.sndarray.use_arraytype('numpy')
        import numpy as np
        sample_rate = 44100
        duration = 0.5  # seconds
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        tone = np.sin(2 * np.pi * 440 * t) * 0.5
        stereo_tone = np.column_stack([tone, tone])
        sound_array = (stereo_tone * 32767).astype(np.int16)
        catch_sound = pygame.sndarray.make_sound(sound_array)
except:
    # If we can't create a sound, use a dummy sound object
    class DummySound:
        def play(self):
            pass
    catch_sound = DummySound()

class Ball:
    """Class representing a ball in the game."""

    def __init__(self):
        """Initialize a new ball with random properties."""
        self.radius = random.randint(15, 30)
        self.color = random.choice(COLORS)
        self.x = random.randint(self.radius, SCREEN_WIDTH - self.radius)
        self.y = -self.radius  # Start above the screen
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(2, 5)
        self.points = max(1, 6 - self.radius // 5)  # Smaller balls are worth more points

    def update(self):
        """Update the ball's position."""
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off the walls
        if self.x <= self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.speed_x = -self.speed_x

        # Keep the ball within the screen bounds
        self.x = max(self.radius, min(self.x, SCREEN_WIDTH - self.radius))

    def draw(self, surface):
        """Draw the ball on the given surface."""
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius, 2)

    def is_off_screen(self):
        """Check if the ball has moved off the bottom of the screen."""
        return self.y > SCREEN_HEIGHT + self.radius

    def is_caught(self, paddle):
        """Check if the ball has been caught by the paddle."""
        if self.y + self.radius >= paddle.y and self.x >= paddle.x and self.x <= paddle.x + paddle.width:
            return True
        return False


class Paddle:
    """Class representing the player's paddle."""

    def __init__(self):
        """Initialize the paddle."""
        self.width = 120
        self.height = 20
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 40
        self.speed = 8
        self.color = (50, 150, 200)

    def update(self, keys):
        """Update the paddle's position based on keyboard input."""
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        # Keep the paddle within the screen bounds
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))

    def draw(self, surface):
        """Draw the paddle on the given surface."""
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height), 2)


class Game:
    """Main game class."""

    def __init__(self):
        """Initialize the game."""
        self.state = "start"  # start, playing, game_over
        self.score = 0
        self.balls = []
        self.paddle = Paddle()
        self.ball_spawn_timer = 0
        self.ball_spawn_delay = 60  # Frames between ball spawns

        # Game timer (in seconds)
        self.time_limit = 60  # 60 seconds game time
        self.time_remaining = self.time_limit
        self.last_time = pygame.time.get_ticks()

        # Create a colorful background
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for _ in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            radius = random.randint(5, 20)
            color = random.choice(COLORS)
            pygame.draw.circle(self.background, color, (x, y), radius, 1)

        # Dim the background
        self.background.set_alpha(50)

    def handle_events(self):
        """Handle game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if self.state == "start" and event.key == pygame.K_SPACE:
                    self.state = "playing"

                if self.state == "game_over" and event.key == pygame.K_SPACE:
                    self.__init__()  # Reset the game

    def update(self):
        """Update game state."""
        keys = pygame.key.get_pressed()

        if self.state == "playing":
            # Update timer
            current_time = pygame.time.get_ticks()
            dt = (current_time - self.last_time) / 1000.0  # Convert to seconds
            self.last_time = current_time
            self.time_remaining -= dt

            # Check if time is up
            if self.time_remaining <= 0:
                self.state = "game_over"
                self.time_remaining = 0

            self.paddle.update(keys)

            # Spawn new balls
            self.ball_spawn_timer += 1
            if self.ball_spawn_timer >= self.ball_spawn_delay:
                self.balls.append(Ball())
                self.ball_spawn_timer = 0
                # Gradually increase difficulty by spawning balls more frequently
                self.ball_spawn_delay = max(20, self.ball_spawn_delay - 0.2)

            # Update balls and check for catches
            for ball in self.balls[:]:
                ball.update()

                if ball.is_caught(self.paddle):
                    self.score += ball.points
                    catch_sound.play()
                    self.balls.remove(ball)
                elif ball.is_off_screen():
                    self.balls.remove(ball)

            # End the game if there are too many balls (player is overwhelmed)
            if len(self.balls) > 20:
                self.state = "game_over"

    def draw(self):
        """Draw the game."""
        screen.fill((20, 20, 50))  # Dark blue background
        screen.blit(self.background, (0, 0))

        if self.state == "start":
            self.draw_start_screen()
        elif self.state == "playing":
            self.draw_game_screen()
        elif self.state == "game_over":
            self.draw_game_over_screen()

        pygame.display.flip()

    def draw_start_screen(self):
        """Draw the start screen."""
        title = title_font.render("Fun Ball Puzzle", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))

        instructions = [
            "Catch the falling balls with your paddle",
            "Use LEFT and RIGHT arrow keys to move",
            "Smaller balls are worth more points!",
            f"You have {self.time_limit} seconds to score as many points as possible",
            "",
            "Press SPACE to start"
        ]

        y = 300
        for line in instructions:
            text = small_font.render(line, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))
            y += 40

    def draw_game_screen(self):
        """Draw the main game screen."""
        # Draw score
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (20, 20))

        # Draw timer
        minutes = int(self.time_remaining) // 60
        seconds = int(self.time_remaining) % 60
        timer_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, WHITE)
        screen.blit(timer_text, (SCREEN_WIDTH - timer_text.get_width() - 20, 20))

        # Draw paddle and balls
        self.paddle.draw(screen)
        for ball in self.balls:
            ball.draw(screen)

    def draw_game_over_screen(self):
        """Draw the game over screen."""
        title = title_font.render("Game Over", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))

        score_text = font.render(f"Final Score: {self.score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))

        # Show reason for game over
        if self.time_remaining <= 0:
            reason_text = small_font.render("Time's up!", True, WHITE)
        else:
            reason_text = small_font.render("Too many balls!", True, WHITE)
        screen.blit(reason_text, (SCREEN_WIDTH // 2 - reason_text.get_width() // 2, 300))

        restart_text = small_font.render("Press SPACE to play again", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 350))

    def run(self):
        """Main game loop."""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
