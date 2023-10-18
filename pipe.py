from const import *
from game import GameObject
import pygame


class Pipe(pygame.sprite.Sprite, GameObject):
    def __init__(self, x: int, y: int, position: 1 or -1, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

        if position == 1:  # for upper pipe
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(HALF_PIPE_GAP)]

        if position == -1:  # for lower pipe
            self.rect.topleft = [x, y + int(HALF_PIPE_GAP)]

        self.pos = position

    def update(self, flying: bool, game_over: bool):
        if flying and not game_over:
            self.rect.x -= SCROLL_SPEED

            if self.rect.right < 0:
                self.kill()
