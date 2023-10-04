from const import *  # All Constants, Variables
from game import Game, Bird, Pipe, Score
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

        self.score = 0
        self.is_pipe_pass = False
        self.number_group = pygame.sprite.Group()
        self.score_board = Score(SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.12)
        # noinspection PyTypeChecker
        self.number_group.add(self.score_board)

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
        if pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False) or self.flappy.rect.top < 0:
            self.flappy.game.game_over = True

        # Checks whether the bird hits on to the ground
        self.flappy.hit()

    def _create_pipes(self):
        if not self.flappy.game.game_over and self.flappy.flying:
            self.game.base(self.screen)  # moving base
            current_pipe = pygame.time.get_ticks()
            # pipe_height = randrange(int(offset), int(height_to_bottom - offset))  # random pipes values
            pipe_height = int(SCREEN_WIDTH/2)
            # Creating Pipes on the screen
            if current_pipe - self.last_pipe > self.pipe_frequency:
                top_pipe = Pipe(SCREEN_WIDTH, pipe_height, 1)
                bottom_pipe = Pipe(SCREEN_WIDTH, pipe_height, -1)

                # noinspection PyTypeChecker
                self.pipe_group.add(top_pipe)
                # noinspection PyTypeChecker
                self.pipe_group.add(bottom_pipe)
                self.last_pipe = current_pipe

    def _check_score(self):
        if len(self.pipe_group) > 0:
            if (self.bird_group.sprites()[0].rect.left > self.pipe_group.sprites()[0].rect.left
                    and self.bird_group.sprites()[0].rect.right < self.pipe_group.sprites()[0].rect.right
                    and not self.is_pipe_pass):
                self.is_pipe_pass = True
            if self.is_pipe_pass:
                if self.bird_group.sprites()[0].rect.left > self.pipe_group.sprites()[0].rect.right:
                    self.score += 1
                    self.is_pipe_pass = False
                    point_sound.play()

    def _update_screen(self):
        """ Update whole game """
        screen = self.screen

        self.game.show_bg(screen)  # show background image

        self._check_collision()
        # if self.flappy.game.game_over:
        #     die_sound.play()

        # score check
        self._check_score()

        # draw pipes and base on screen
        self.pipe_group.draw(screen)
        self.pipe_group.update(self.flappy.flying, self.flappy.game.game_over)
        screen.blit(base_image, (0, SCREEN_HEIGHT - base_image.get_height()))  # base image
        self._create_pipes()

        # draw score on screen
        self.number_group.draw(screen)
        self.number_group.update(self.score)

        # draw bird on screen
        self.bird_group.draw(screen)
        self.bird_group.update()

        self.clock.tick(FPS)  # frame per second
        pygame.display.update()  # update screen


# Main Execution Start from here
if __name__ == '__main__':
    game = Main()
    game.mainloop()
