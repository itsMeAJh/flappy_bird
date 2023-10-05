import sys
import pygame
from pygame.locals import *
from random import randrange

# Import constants and game classes from other modules
from const import *
from game import Game, Bird, Pipe


class Main:
    def __init__(self):
        pygame.init()
        self.init_game_window()
        self.init_game_objects()

    def init_game_window(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.flying = False

    def init_game_objects(self):
        self.game = Game()
        self.flappy = Bird(INITIAL_BIRD_POS_X, INITIAL_BIRD_POS_Y)
        self.bird_group = pygame.sprite.Group()
        self.bird_group.add(self.flappy)
        self.pipe_group = pygame.sprite.Group()
        self.pipe_frequency = 1500  # milliseconds
        self.last_pipe = pygame.time.get_ticks()
        self.score = 0
        self.is_pipe_pass = False

    def mainloop(self):
        """ Main Game Loop """
        while True:
            self.handle_event()
            self._update_game()
            self.render_game()

    def handle_event(self):
        """ Handle all input events """
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and not self.flappy.flying and not self.flappy.game.game_over:
                self.flappy.flying = True

    def check_collision(self):
        # Check for collisions between bird, pipes and ground or top
        if pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False) or self.flappy.rect.top < 0:
            self.flappy.game.game_over = True
            if not self.flappy.any_collision_occurred:
                HIT_SOUND.play()  # Play the hit sound
                DIE_SOUND.play()
                self.flappy.any_collision_occurred = True  # Set the collision occurred flag

        self.flappy.hit()  # Checks the bird to the ground

    def create_pipes(self):
        if not self.flappy.game.game_over and self.flappy.flying:
            self.game.base(self.screen)  # Move the base
            current_pipe = pygame.time.get_ticks()
            pipe_height = randrange(int(OFFSET), int(HEIGHT_TO_BOTTOM - OFFSET))
            if current_pipe - self.last_pipe > self.pipe_frequency:
                top_pipe = Pipe(SCREEN_WIDTH*2, pipe_height, 1)
                bottom_pipe = Pipe(SCREEN_WIDTH*2, pipe_height, -1)
                self.pipe_group.add(top_pipe)
                self.pipe_group.add(bottom_pipe)
                self.last_pipe = current_pipe

    def update_score(self):
        if len(self.pipe_group) > 0:
            bird_rect = self.bird_group.sprites()[0].rect
            pipe_rect = self.pipe_group.sprites()[0].rect
            if (bird_rect.left > pipe_rect.left
                    and bird_rect.right < pipe_rect.right
                    and not self.is_pipe_pass):
                self.is_pipe_pass = True
            if self.is_pipe_pass and bird_rect.left > pipe_rect.right:
                self.score += 1
                self.is_pipe_pass = False
                POINT_SOUND.play()

    def render_score(self):
        digits = [int(digit) for digit in str(self.score)]
        digit_width = sum(self.game.images[digit].get_width() for digit in digits)
        offset_x = (SCREEN_WIDTH - digit_width) / 2
        score_y = SCREEN_HEIGHT * 0.12

        for digit in digits:
            digit_image = self.game.images[digit]
            self.screen.blit(digit_image, (offset_x, score_y))
            offset_x += digit_image.get_width()

    def _update_game(self):
        """ Update whole game """

        self.check_collision()

        # Update score
        self.update_score()

        # Update pipes
        self.pipe_group.update(self.flappy.flying, self.flappy.game.game_over)

        # Update bird
        self.bird_group.update()

    def render_game(self):
        self.screen.fill(BLACK_COLOR)  # Clear the screen with a black background

        # Draw game elements (background, pipes, bird, etc.)

        self.game.show_bg(self.screen)  # Draw background
        self.pipe_group.draw(self.screen)  # Draw pipes
        self.screen.blit(BASE_IMAGE, (0, SCREEN_HEIGHT - BASE_IMAGE.get_height()))  # Draw base
        self.create_pipes()  # Create pipes
        self.bird_group.draw(self.screen)  # Draw bird
        self.render_score()  # Render the score

        self.clock.tick(FPS)  # Control frame rate
        pygame.display.update()  # Update the display


# Main Execution
if __name__ == '__main__':
    game = Main()
    game.mainloop()
