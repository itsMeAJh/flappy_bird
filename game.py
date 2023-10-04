from math import ceil
from const import *
import sprite_sheet
import pygame


class Game(object):
    def __init__(self):
        self.base_vel = 0
        self.game_over = False

    @staticmethod
    def show_bg(surface):
        surface.blit(background_image.convert_alpha(), (0, 0))

    def base(self, surface):
        base_rect = base_image.get_rect()
        tiles = ceil(SCREEN_WIDTH / base_image.get_width()) + 1
        for i in range(0, tiles):
            base_rect.bottomleft = (i * base_image.get_width() + self.base_vel, SCREEN_HEIGHT)
            surface.blit(base_image.convert_alpha(), base_rect)

        self.base_vel -= scroll_speed
        if abs(self.base_vel) > base_image.get_width():
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
        self.action = random_action
        step_counter = 0
        animation_steps = [3, 3, 3]

        for step in animation_steps:
            temp_list = []
            for _ in range(step):
                # img = pygame.image.load(IMAGE_PATH + f"red_bird-{num}.png")
                # self.images.append(img)
                temp_list.append(self.bird.image_at((bird_width * step_counter, 0, bird_width, bird_height), -1))
                step_counter += 1
            self.images.append(temp_list)

        self.image = self.images[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.game = Game()

    def hit(self):
        """Checks whether the bottom part of the bird hits the ground"""
        if self.rect.bottom > height_to_bottom:
            self.game.game_over = True
            self.flying = False

    def update(self):
        # gravity acting on bird
        if self.flying:
            self.vel += 0.6
            if self.vel > 8:
                self.vel = 8

            if self.rect.bottom < height_to_bottom:
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
                flap_sound.play()

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
        self.image = pipe_image
        self.rect = self.image.get_rect()
        self.no_sound = True

        if position is 1:  # for upper pipe
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(halfPipeGap)]
            self.no_sound = False

        if position is -1:  # for lower pipe
            self.rect.topleft = [x, y + int(halfPipeGap)]

    def update(self, flying, game_over):
        if flying and not game_over:
            self.rect.x -= scroll_speed

            if self.rect.right < 0:
                self.kill()


class Score(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        for i in range(10):
            img = pygame.image.load(IMAGE_PATH + f"{i}.png")
            self.images.append(img)
        self.image_width = self.images[0].get_width()  # Assuming all digits have the same width
        self.rects = []
        self.image = self.images[0]  # Default image
        self.rect = self.image.get_rect()  # Create a rect
        self.update_position(x, y)

    def update_position(self, x, y):
        self.rects.clear()
        self.rect.center = [x, y]

    def update(self, score):
        digits = [int(x) for x in list(str(score))]
        total_width = len(digits) * self.image_width
        x_pos = self.rect.x - (total_width - self.rect.width) // 2  # Adjust the x position

        for digit in digits:
            if 0 <= digit < len(self.images):
                self.rects.append(pygame.Rect(x_pos, self.rect.y, self.image_width, self.rect.height))
                x_pos += self.image_width
            else:
                print(f"Invalid digit: {digit}")

        for i, rect in enumerate(self.rects):
            if i < len(digits) and 0 <= digits[i] < len(self.images):
                self.image = self.images[digits[i]]
                self.rect = rect

# class Score(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         pygame.sprite.Sprite.__init__(self)
#         self.images = []
#         for i in range(10):
#             img = pygame.image.load(IMAGE_PATH + f"{i}.png")
#             self.images.append(img)
#         self.image_width = self.images[0].get_width()  # Assuming all digits have the same width
#         self.rects = []
#         self.image = self.images[0]  # Default image
#         self.rect = self.image.get_rect()  # Create a rect
#         self.update_position(x, y)
#
#     def update_position(self, x, y):
#         self.rects.clear()
#         self.rect.topleft = [x, y]
#
#     def update(self, score):
#         digits = [int(x) for x in list(str(score))]
#         total_width = len(digits) * self.image_width
#
#         for i, digit in enumerate(digits):
#             x_pos = self.rect.x + (self.rect.width - total_width) // 2 + i * self.image_width
#             self.rects.append(pygame.Rect(x_pos, self.rect.y, self.image_width, self.rect.height))
#
#         for i, _rect in enumerate(self.rects):
#             self.image = self.images[digits[i]]
#             self.rect = _rect
#
