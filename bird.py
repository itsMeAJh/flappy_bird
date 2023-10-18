from random import randrange
import pygame
import sprite_sheet
from const import *
from game import GameObject


class Bird(pygame.sprite.Sprite, GameObject):
    def __init__(self, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)
        GameObject.__init__(self)
        self.images_ = []
        self.index = 0
        self.counter = 0
        self.vel = 0
        self.angle = 0
        self.flap = False
        self.flying = False
        self.bird = sprite_sheet.SpriteSheet(IMAGE_PATH + "bird_sprite-sheet.png")
        self.action = randrange(0, 2)
        self.any_collision_occurred = False  # Add a hit occurred flag
        self.hit_time = 0
        step_counter = 0
        animation_steps = [3, 3, 3]

        for step in animation_steps:
            temp_list = []
            for _ in range(step):
                temp_list.append(self.bird.image_at((BIRD_WIDTH * step_counter, 0, BIRD_WIDTH, BIRD_HEIGHT), -1))
                step_counter += 1
            self.images_.append(temp_list)

        self.image = self.images_[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def hit(self, bird, pipe):
        """Checks whether the bottom part of the bird hits the ground"""
        if (
            pygame.sprite.groupcollide(bird, pipe, False, False)
            or self.rect.bottom > (SCREEN_HEIGHT - self.images['base'].get_height())
            or self.rect.top < -50
        ):
            self.game_over = True
            self.flying = False
            if not self.any_collision_occurred:
                self.sounds['hit'].play()  # Play the hit sound
                self.any_collision_occurred = True  # Set the collision occurred flag

    def update(self):

        # gravity acting on bird
        if self.flying:
            self.vel += 0.7
            if self.vel > 8:
                self.vel = 8

            if self.rect.bottom < (SCREEN_HEIGHT - self.images['base'].get_height()):
                self.rect.y += int(self.vel)

            # rotate the bird
            self.angle += 3
            if self.angle > 90:
                self.angle = 90

        if not self.game_over and self.flying:
            # Bird flap(jump)
            if pygame.mouse.get_pressed()[0] == 1 and not self.flap:
                self.flap = True
                self.vel = -10
                self.angle = -45
                self.sounds['flap'].play()

            if pygame.mouse.get_pressed()[0] == 0:
                self.flap = False

        if not self.game_over:
            # Handle Animation
            flap_cooldown = 5
            self.counter += 1

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_):
                    self.index = 0

            self.image = pygame.transform.rotate(self.images_[self.action][self.index], -self.angle)

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.flying and not self.game_over:
            self.flying = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                self.flying = True
                if not self.flap and self.flying:
                    self.vel = -10
                    self.angle = -45
                    self.sounds['flap'].play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                self.flap = False

    def reset(self):
        self.game_over = False
        self.flap = False
        self.flying = False
        self.any_collision_occurred = False
        self.vel = 0
        self.angle = 0
        self.action = randrange(0, 2)
        self.rect.center = [INITIAL_BIRD_POS_X, INITIAL_BIRD_POS_Y]
        self.image = self.images_[self.action][self.index]

    def initial_animation(self):
        if self.rect.y < SCREEN_HEIGHT//1.9:
            self.vel += 0.4
        elif self.rect.y > SCREEN_HEIGHT//2:
            self.vel -= 0.4
        if self.vel > 5:
            self.vel = -5
        self.rect.centery += int(self.vel)
