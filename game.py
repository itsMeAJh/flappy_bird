from math import ceil
from const import *
import sprite_sheet
import pygame


class Game(object):
    def __init__(self):
        self.base_vel = 0
        self.background_scroll = 0
        self.game_over = False

        self.number_images = []
        self.score_numbers_images = []
        for i in range(10):
            img = pygame.image.load(IMAGE_PATH + f"{i}.png")
            img1 = pygame.image.load(IMAGE_PATH + f"{i}s.png")
            self.number_images.append(img)
            self.score_numbers_images.append(img1)

        self.game_over_rect = GAME_OVER_IMAGE.get_rect()
        self.score_board_rect = SCORE_BOARD_IMAGE.get_rect()
        self.start_again_rect = START_BUTTON_IMAGE.get_rect()

    def render_bg(self, surface):
        # surface.blit(BACKGROUND_IMAGE.convert_alpha(), (0, 0))
        background_rect = BACKGROUND_IMAGE.get_rect()
        tiles = ceil(SCREEN_WIDTH / BACKGROUND_IMAGE.get_width()) + 1
        for i in range(0, tiles):
            background_rect.topleft = (i * BACKGROUND_IMAGE.get_width() + self.background_scroll, 0)
            surface.blit(BACKGROUND_IMAGE.convert_alpha(), background_rect)

        self.background_scroll -= 2
        if abs(self.background_scroll) > BACKGROUND_IMAGE.get_width():
            self.background_scroll = 0

    def render_base(self, surface):
        base_rect = BASE_IMAGE.get_rect()
        tiles = ceil(SCREEN_WIDTH / BASE_IMAGE.get_width()) + 1
        for i in range(0, tiles):
            base_rect.bottomleft = (i * BASE_IMAGE.get_width() + self.base_vel, SCREEN_HEIGHT)
            surface.blit(BASE_IMAGE.convert_alpha(), base_rect)

        self.base_vel -= SCROLL_SPEED
        if abs(self.base_vel) > BASE_IMAGE.get_width():
            self.base_vel = 0

    def render_score(self, surface, score):
        digits = [int(digit) for digit in str(score)]
        digit_width = sum(self.number_images[digit].get_width() for digit in digits)
        offset_x = (SCREEN_WIDTH - digit_width) / 2
        score_y = SCREEN_HEIGHT * 0.12

        for digit in digits:
            digit_image = self.number_images[digit]
            surface.blit(digit_image, (offset_x, score_y))
            offset_x += digit_image.get_width()

    @staticmethod
    def show_initial_screen(surface):
        flappy_bird_rect = FLAPPY_BIRD_IMAGE.get_rect()
        tap_img_rect = START_GAME_IMAGE.get_rect()
        flappy_bird_rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT*0.2]
        tap_img_rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT*0.6]

        surface.blit(FLAPPY_BIRD_IMAGE, flappy_bird_rect)
        surface.blit(START_GAME_IMAGE, tap_img_rect)

    def show_game_over_screen(self, surface):
        self.game_over_rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT*0.2]
        self.score_board_rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT*0.5]
        self.start_again_rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT*0.8]

        surface.blit(GAME_OVER_IMAGE, self.game_over_rect)
        surface.blit(SCORE_BOARD_IMAGE, self.score_board_rect)
        surface.blit(START_BUTTON_IMAGE, self.start_again_rect)


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
        self.hit_time = 0
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
                self.hit_time = pygame.time.get_ticks()  # Set the hit time
                self.any_collision_occurred = True  # Set the hit occurred flag

    def update(self):
        # gravity acting on bird
        if self.flying:
            self.vel += 0.7
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
                self.vel = -10
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
