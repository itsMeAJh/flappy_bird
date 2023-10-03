<<<<<<< HEAD
import random
import pygame
import sys
from pygame.locals import *

=======
import pygame
import random
import sys

from pygame.locals import *
>>>>>>> c8a891f (Initial commit)
from const import *
from game import Game, Bird, Pipe


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.flying = False

        self.game = Game()

        self.bird_group = pygame.sprite.Group()
        self.flappy = Bird(initialBirdPosX, initialBirdPosY)
        # noinspection PyTypeChecker
        self.bird_group.add(self.flappy)

        self.pipe_group = pygame.sprite.Group()
        self.pipe_frequency = 1500  # milliseconds
        self.last_pipe = pygame.time.get_ticks()

    def mainloop(self):
        while True:
            self._check_event()
            self._update_screen()

    def _check_event(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and not self.flappy.flying_ and not self.flappy.game.game_over_:
                self.flappy.flying(True)

    def _update_screen(self):
        screen = self.screen
        _game = self.game

        _game.show_bg(screen)
        self.bird_group.draw(screen)
        self.bird_group.update()
        self.pipe_group.draw(screen)
<<<<<<< HEAD
        self.pipe_group.update()
        screen.blit(BASE, (0, SCREEN_HEIGHT - BASE.get_height()))
        if not self.flappy.game.game_over_ and self.flappy.flying_:
            _game.base(screen)
            current_time = pygame.time.get_ticks()
            pipe_height = random.randrange(int(-offset), int(offset/2))
            if current_time - self.last_pipe > self.pipe_frequency:
                top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, 1)
                bottom_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, -1)
=======
        self.pipe_group.update(self.flappy.flying_)

        screen.blit(BASE, (0, SCREEN_HEIGHT - BASE.get_height()))

        if not self.flappy.game.game_over_ and self.flappy.flying_:
            _game.base(screen)
            current_time = pygame.time.get_ticks()
            pipe_height = random.randrange(int(offset), int(free_height - offset))

            if current_time - self.last_pipe > self.pipe_frequency:
                top_pipe = Pipe(SCREEN_WIDTH, pipe_height, 1)
                bottom_pipe = Pipe(SCREEN_WIDTH, pipe_height, -1)
>>>>>>> c8a891f (Initial commit)
                # noinspection PyTypeChecker
                self.pipe_group.add(top_pipe)
                # noinspection PyTypeChecker
                self.pipe_group.add(bottom_pipe)
                self.last_pipe = current_time
<<<<<<< HEAD
=======

>>>>>>> c8a891f (Initial commit)
        self.flappy.hit()
        self.clock.tick(FPS)
        pygame.display.update()


if __name__ == '__main__':
    game = Main()
    game.mainloop()
