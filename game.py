from math import ceil
from const import *
import sprite_sheet
import pygame


class Game(object):
    def __init__(self):
        self.base_vel = 0
        self.game_over = False

        self.images = []
        for i in range(10):
            img = pygame.image.load(IMAGE_PATH + f"{i}.png")
            self.images.append(img)

    @staticmethod
    def show_bg(surface):
        surface.blit(BACKGROUND_IMAGE.convert_alpha(), (0, 0))

    def base(self, surface):
        base_rect = BASE_IMAGE.get_rect()
        tiles = ceil(SCREEN_WIDTH / BASE_IMAGE.get_width()) + 1
        for i in range(0, tiles):
            base_rect.bottomleft = (i * BASE_IMAGE.get_width() + self.base_vel, SCREEN_HEIGHT)
            surface.blit(BASE_IMAGE.convert_alpha(), base_rect)

        self.base_vel -= SCROLL_SPEED
        if abs(self.base_vel) > BASE_IMAGE.get_width():
            self.base_vel = 0


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        self.vel = 0
        self.angle = 0
        self.flap = False
        self.flying = False
        self.bird = sprite_sheet.SpriteSheet(IMAGE_PATH + "bird_sprite-sheet.png")
        self.action = RANDOM_ACTION
        self.any_collision_occurred = False  # Add a hit occurred flag
        step_counter = 0
        animation_steps = [3, 3, 3]

        for step in animation_steps:
            temp_list = []
            for _ in range(step):
                # img = pygame.image.load(IMAGE_PATH + f"red_bird-{num}.png")
                # self.images.append(img)
                temp_list.append(self.bird.image_at((BIRD_WIDTH * step_counter, 0, BIRD_WIDTH, BIRD_HEIGHT), -1))
                step_counter += 1
            self.images.append(temp_list)

        self.image = self.images[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.game = Game()

    def hit(self):
        """Checks whether the bottom part of the bird hits the ground"""
        if self.rect.bottom > HEIGHT_TO_BOTTOM:
            self.game.game_over = True
            self.flying = False
            if not self.any_collision_occurred:
                HIT_SOUND.play()  # Play the hit sound
                self.any_collision_occurred = True  # Set the hit occurred flag

    def update(self):
        # gravity acting on bird
        if self.flying:
            self.vel += 0.6
            if self.vel > 8:
                self.vel = 8

            if self.rect.bottom < HEIGHT_TO_BOTTOM:
                self.rect.y += int(self.vel)

            # rotate the bird
            self.angle += 3
            if self.angle > 90:
                self.angle = 90

        if not self.game.game_over:
            # Bird flap(jump)
            if pygame.mouse.get_pressed()[0] == 1 and not self.flap:
                self.flap = True
                self.vel = -8
                self.angle = -45
                FLAP_SOUND.play()

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

            self.image = pygame.transform.rotate(self.images[self.action][self.index], -self.angle)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = PIPE_IMAGE
        self.rect = self.image.get_rect()
        self.no_sound = True

        if position is 1:  # for upper pipe
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(HALF_PIPE_GAP)]
            self.no_sound = False

        if position is -1:  # for lower pipe
            self.rect.topleft = [x, y + int(HALF_PIPE_GAP)]

    def update(self, flying, game_over):
        if flying and not game_over:
            self.rect.x -= SCROLL_SPEED

            if self.rect.right < 0:
                self.kill()
