from math import ceil
from const import *
from random import randint
import pygame
import os


class GameObject(object):
    def __init__(self):
        self.init_game_object()
        self.init_game_images()
        self.init_game_sounds()

    def init_game_object(self):
        self.game_over = False
        self.score = 0
        self.best_score = 0
        self.base_vel = 0
        self.background_scroll = 0
        self.pipe_frequency = 1500  # milliseconds
        self.last_pipe = pygame.time.get_ticks()
        self.is_pipe_pass = False
        self.initial_screen = True

    def init_game_images(self):
        self.images = {}
        images_name = os.listdir(IMAGE_PATH)
        for image in images_name:
            img = image.replace(".png", "")
            self.images[img] = ImageLoader.load_image(image)
        self.background_image = ImageLoader.load_random_background()
        self.pipe_image = ImageLoader.load_random_pipe()

    def init_game_sounds(self):
        self.sounds = {}
        sounds_name = os.listdir(SOUND_PATH)
        for sound in sounds_name:
            audio = sound.replace(".mp3", "")
            self.sounds[audio] = SoundLoader.load_sound(sound)


class Game(GameObject):
    def __init__(self):
        GameObject.__init__(self)

        self.game_over_rect = self.images['game_over_text'].get_rect()
        self.score_board_rect = self.images['score_board'].get_rect()
        self.start_again_rect = self.images['start_button'].get_rect()

    def render_bg(self, surface: pygame.surface.Surface, game_over: bool):
        # surface.blit(BACKGROUND_IMAGE.convert_alpha(), (0, 0))
        background_rect = self.background_image.get_rect()
        tiles = ceil(SCREEN_WIDTH / self.background_image.get_width()) + 1
        for i in range(0, tiles):
            background_rect.topleft = (i * self.background_image.get_width() + self.background_scroll, 0)
            surface.blit(self.background_image.convert_alpha(), background_rect)

        if not game_over:
            self.background_scroll -= SCROLL_SPEED - 3
            if abs(self.background_scroll) > self.background_image.get_width():
                self.background_scroll = 0

    def render_base(self, surface: pygame.surface.Surface, game_over: bool):
        base_rect = self.images['base'].get_rect()
        tiles = ceil(SCREEN_WIDTH / self.images['base'].get_width()) + 1
        for i in range(0, tiles):
            base_rect.bottomleft = (i * self.images['base'].get_width() + self.base_vel, SCREEN_HEIGHT)
            surface.blit(self.images['base'].convert_alpha(), base_rect)

        if not game_over:
            self.base_vel -= SCROLL_SPEED
            if abs(self.base_vel) > self.images['base'].get_width():
                self.base_vel = 0

    def render_score(self, surface: pygame.surface):
        digits = [int(digit) for digit in str(self.score)]
        digit_width = sum(self.images[str(digit)].get_width() for digit in digits)
        offset_x = (SCREEN_WIDTH - digit_width) / 2
        score_y = SCREEN_HEIGHT * 0.12

        for digit in digits:
            digit_image = self.images[str(digit)]
            surface.blit(digit_image, (offset_x, score_y))
            offset_x += digit_image.get_width()

    def read_score(self):
        try:
            with open("best_score.txt", "r") as f:
                self.best_score = int(f.read())
        except Exception as e:
            print("There is no best_score.txt file")
            return e

    def write_score(self):
        if self.score > self.best_score:
            self.best_score = self.score
        with open("best_score.txt", "w") as f:
            f.write(str(self.best_score))

    def show_my_score(self, surface: pygame.surface.Surface):
        digits = [int(digit) for digit in str(self.score)]
        digit_width = sum(self.images[str(digit)+'s'].get_width() for digit in digits)
        offset_x = (SCREEN_WIDTH - digit_width) * 0.80
        score_y = SCREEN_HEIGHT * 0.450
        for digit in digits:
            digit_image = self.images[str(digit) + 's']
            surface.blit(digit_image, (offset_x, score_y))
            offset_x += digit_image.get_width()

    def show_my_best_score(self, surface: pygame.surface.Surface):
        digits = [int(digit) for digit in str(self.best_score)]
        digit_width = sum(self.images[str(digit)+'s'].get_width() for digit in digits)
        offset_x = (SCREEN_WIDTH - digit_width) * 0.80
        score_y = SCREEN_HEIGHT * 0.53

        for digit in digits:
            digit_image = self.images[str(digit) + 's']
            surface.blit(digit_image, (offset_x, score_y))
            offset_x += digit_image.get_width()

    def show_initial_screen(self, surface: pygame.surface.Surface):
        flappy_bird_rect = self.images['flappy_bird_text'].get_rect()
        get_ready_rect = self.images['get_ready_text'].get_rect()
        tap_img_rect = self.images['start_game'].get_rect()
        flappy_bird_rect.center = [SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.2]
        get_ready_rect.center = [SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.32]
        tap_img_rect.center = [SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.6]

        surface.blit(self.images['flappy_bird_text'], flappy_bird_rect)
        surface.blit(self.images['get_ready_text'], get_ready_rect)
        surface.blit(self.images['start_game'], tap_img_rect)

    def show_game_over_screen(self, surface: pygame.surface.Surface):
        self.game_over_rect.center = [SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.2]
        self.score_board_rect.center = [SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.5]
        self.start_again_rect.center = [SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.8]

        surface.blit(self.images['game_over_text'], self.game_over_rect)
        surface.blit(self.images['score_board'], self.score_board_rect)
        surface.blit(self.images['start_button'], self.start_again_rect)

    def reset(self):
        self.score = 0
        self.base_vel = 0
        self.background_scroll = 0
        self.game_over = False
        self.initial_screen = True
        self.is_pipe_pass = False

    def restart_button_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_again_rect.left < event.pos[0] < self.start_again_rect.right \
                    and self.start_again_rect.top < event.pos[1] < self.start_again_rect.bottom:
                return True


class ImageLoader:
    @staticmethod
    def load_image(image_name: str):
        return pygame.image.load(IMAGE_PATH + image_name).convert_alpha()

    @staticmethod
    def load_random_background():
        return pygame.image.load(IMAGE_PATH + f"background-{randint(1, 2)}.png")

    @staticmethod
    def load_random_pipe():
        return pygame.image.load(IMAGE_PATH + f"pipe-{randint(1, 2)}.png")


class SoundLoader:
    @staticmethod
    def load_sound(sound_name: str):
        return pygame.mixer.Sound(SOUND_PATH + sound_name)

