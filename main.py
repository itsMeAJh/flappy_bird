from const import *  # All Constants, Variables
from game import Game, Bird, Pipe
from pygame.locals import *
from random import randrange

import sys
import pygame


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(window_title)
        self.clock = pygame.time.Clock()
        self.flying = False

        self.game = Game()
        self.flappy = Bird(initialBirdPosX, initialBirdPosY)

        self.bird_group = pygame.sprite.Group()
        # noinspection PyTypeChecker
        self.bird_group.add(self.flappy)

        self.pipe_group = pygame.sprite.Group()
        self.pipe_frequency = 1500  # milliseconds
        self.last_pipe = pygame.time.get_ticks()

    def mainloop(self):
        """ Main Game Loop """
        while True:
            self._check_event()
            self._update_screen()

    def _check_event(self):
        """ Handle all Inputs keys (events) """
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and not self.flappy.flying and not self.flappy.game.game_over:
                self.flappy.flying = True

    def _check_collision(self):
        # if Bird hits the Pipe, then game will be over
        if pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False):
            self.flappy.game.game_over = True

        # Checks whether the bird hits on to the ground
        self.flappy.hit()

    def _create_pipes(self):
        if not self.flappy.game.game_over and self.flappy.flying:
            self.game.base(self.screen)  # moving base
            current_pipe = pygame.time.get_ticks()
            pipe_height = randrange(int(offset), int(height_to_bottom - offset))  # random pipes values
            # Creating Pipes on the screen
            if current_pipe - self.last_pipe > self.pipe_frequency:
                top_pipe = Pipe(SCREEN_WIDTH, pipe_height, 1)
                bottom_pipe = Pipe(SCREEN_WIDTH, pipe_height, -1)

                # noinspection PyTypeChecker
                self.pipe_group.add(top_pipe)
                # noinspection PyTypeChecker
                self.pipe_group.add(bottom_pipe)
                self.last_pipe = current_pipe

    def _update_screen(self):
        """ Update whole game """
        # Variables
        screen = self.screen
        _game = self.game

        self._check_collision()
        # if self.flappy.game.game_over:
        #     die_sound.play()

        _game.show_bg(screen)  # game background image

        # blit Pipes on the screen
        self.pipe_group.draw(screen)
        self.pipe_group.update(self.flappy.flying, self.flappy.game.game_over)

        screen.blit(base_image, (0, SCREEN_HEIGHT - base_image.get_height()))  # base image
        self._create_pipes()

        # blit Bird on the screen
        self.bird_group.draw(screen)
        self.bird_group.update()

        self.clock.tick(FPS)  # frame per second
        pygame.display.update()  # update screen


# Main Execution Start from here
if __name__ == '__main__':
    game = Main()
    game.mainloop()
