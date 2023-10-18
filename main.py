import sys
import ctypes
import pygame
from pygame.locals import *
from random import randrange

# Import constants and game classes from other modules
from const import *
from game import Game
from bird import Bird
from pipe import Pipe


class Main:
    def __init__(self):
        pygame.init()
        self.init_game_window()
        self.init_game_objects()

    def init_game_window(self):
        my_appid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_appid)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
        self.game = Game()
        pygame.display.set_caption(WINDOW_TITLE)
        pygame.display.set_icon(self.game.images['flappy_bird_icon'])
        self.clock = pygame.time.Clock()
        self.flying = False

    def init_game_objects(self):
        self.flappy = Bird(INITIAL_BIRD_POS_X, INITIAL_BIRD_POS_Y)
        self.bird_group = pygame.sprite.Group()
        self.bird_group.add(self.flappy)
        self.pipe_group = pygame.sprite.Group()
        self.button_clicked = False

    def mainloop(self):
        """ Main Game Loop Execution """
        while True:
            self.handle_event()
            self._update_game()
            self.render_game()
            self.reset_game()

    def handle_event(self):
        """ Handle all input events """
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                pygame.quit()
                sys.exit()

            if not self.flappy.game_over:
                self.flappy.events(event)

            self.button_clicked = self.game.restart_button_clicked(event)

    def render_pipes(self):
        if not self.flappy.game_over and self.flappy.flying:
            current_time = pygame.time.get_ticks()
            height = SCREEN_HEIGHT - self.game.images['base'].get_height()
            offset = height * 0.3
            pipe_height = randrange(int(offset), int(height - offset))

            # Check if enough time has passed to create next random pipe
            if current_time - self.game.last_pipe > self.game.pipe_frequency:
                pipe_image = self.game.pipe_image
                top_pipe = Pipe(SCREEN_WIDTH*2, pipe_height, 1, pipe_image)
                bottom_pipe = Pipe(SCREEN_WIDTH*2, pipe_height, -1, pipe_image)
                self.game.last_pipe = current_time
                self.pipe_group.add(top_pipe)
                self.pipe_group.add(bottom_pipe)

    def update_score(self):
        if len(self.pipe_group) > 0:
            bird_rect = self.bird_group.sprites()[0].rect
            pipe_rect = self.pipe_group.sprites()[0].rect
            if (bird_rect.left > pipe_rect.left
                    and bird_rect.right < pipe_rect.right
                    and not self.game.is_pipe_pass):
                self.game.is_pipe_pass = True
            if self.game.is_pipe_pass and bird_rect.left > pipe_rect.right:
                self.game.score += 1
                self.game.is_pipe_pass = False
                self.game.sounds['point'].play()
        self.game.read_score()
        self.game.write_score()

    def _update_game(self):
        """ Update whole game """

        # Checks Any collisions to bird
        self.flappy.hit(self.bird_group, self.pipe_group)

        # Update score
        self.update_score()

        # Update pipes
        self.pipe_group.update(self.flappy.flying, self.flappy.game_over)

        # Update bird
        self.bird_group.update()

    def render_game(self):
        # All set to their priority to image overlap each other
        self.screen.fill(BLACK_COLOR)  # Clear the screen with a black background

        # Draw game elements (background, pipes, bird, etc.)
        self.game.render_bg(self.screen, self.flappy.game_over)  # Render the background
        self.pipe_group.draw(self.screen)  # Draw pipes
        self.render_pipes()  # Render the pipes
        self.game.render_base(self.screen, self.flappy.game_over)  # Render the pipes
        self.bird_group.draw(self.screen)  # Draw bird

        if self.flappy.game_over:
            self.game.show_game_over_screen(self.screen)  # Draw game over text, score board and replay button
            self.game.show_my_score(self.screen)
            self.game.show_best_score(self.screen)
        elif not self.flappy.flying:
            if self.game.initial_screen:
                self.game.show_initial_screen(self.screen)  # Draw title, text
                self.flappy.initial_animation()  # Bird Animation
        else:
            self.game.initial_screen = False
            self.game.render_score(self.screen)  # Render the score

        self.clock.tick(FPS)  # Control frame rate
        pygame.display.update()  # Update the display

    def reset_game(self):
        if self.button_clicked:
            self.button_clicked = False
            self.pipe_group.empty()
            self.game.reset()
            self.flappy.reset()


# Main Execution
if __name__ == '__main__':
    game = Main()
    game.mainloop()
