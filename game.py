import math
import pygame
import os, sys

from const import *


class Game(object):
    def __init__(self):
        self.base_vel = 0
        self.game_over_ = False

    @staticmethod
    def show_bg(surface):
        surface.blit(BACKGROUND, (0, 0))

    def base(self, surface):
        base_rect = BASE.get_rect()
        tiles = math.ceil(SCREEN_WIDTH / BASE.get_width()) + 1
        for i in range(0, tiles):
            base_rect.bottomleft = (i * BASE.get_width() + self.base_vel, SCREEN_HEIGHT)
            surface.blit(BASE, base_rect)

        self.base_vel -= scroll_speed
        if abs(self.base_vel) > BASE.get_width():
            self.base_vel = 0

    def game_over(self, game_over=False):
        self.game_over_ = game_over
        return self.game_over_


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        self.vel = 0
        self.angle = 0
        self.flap = False
        self.flying_ = False

        for num in range(1, 4):
            img = pygame.image.load(IMAGE_PATH + f"red_bird-{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.game = Game()

    def flying(self, fly=False):
        self.flying_ = fly
        return self.flying_

    def hit(self):
        if self.rect.bottom > free_height:
            self.game.game_over(True)
            self.flying_ = False

    def update(self):
        # gravity acting on bird
        if self.flying_:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8

            if self.rect.bottom < free_height:
                self.rect.y += int(self.vel)

            # rotate the bird
            self.angle += 3
            if self.angle > 90:
                self.angle = 90

        if not self.game.game_over_:
            # Bird flap(jump)
            if pygame.mouse.get_pressed()[0] == 1 and not self.flap:
                self.flap = True
                self.vel = -8
                self.angle = -45

            if pygame.mouse.get_pressed()[0] == 0:
                self.flap = False

            # Handle Animation
            flap_cooldown = 5
            self.counter += 1

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0

            self.image = pygame.transform.rotate(self.images[self.index], -self.angle)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = PIPE
        self.rect = self.image.get_rect()
        if position == 1:  # for upper pipe
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(halfPipeGap)]
        if position == -1:  # for lower pipe
            self.rect.topleft = [x, y + int(halfPipeGap)]

    def update(self, flying):
        if flying:
            self.rect.x -= scroll_speed
            if self.rect.right < 0:
                self.kill()
