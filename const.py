from pygame import image, mixer
from random import randint

random_action = randint(0, 2)
window_title = "Flappy Bird Game"
bird_width, bird_height = 34, 24

SCREEN_WIDTH = 287
SCREEN_HEIGHT = 510
FPS = 32
PIPE_GAP = 115

WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
initialBirdPosX = SCREEN_WIDTH / 3
initialBirdPosY = SCREEN_HEIGHT / 2
halfPipeGap = PIPE_GAP / 2
scroll_speed = 5

IMAGE_PATH = "assets/image/"
background_image = image.load(IMAGE_PATH + f"background-{randint(1, 2)}.png")
bird_image = image.load(IMAGE_PATH + "red_bird-1.png")
base_image = image.load(IMAGE_PATH + "base.png")
pipe_image = image.load(IMAGE_PATH + "pipe.png")

mixer.init()
SOUND_PATH = "assets/audio/"
die_sound = mixer.Sound(SOUND_PATH + "die.mp3")
flap_sound = mixer.Sound(SOUND_PATH + "flap.mp3")
hit_sound = mixer.Sound(SOUND_PATH + "hit.mp3")
point_sound = mixer.Sound(SOUND_PATH + "point.mp3")
swosh_sound = mixer.Sound(SOUND_PATH + "swosh.mp3")

height_to_bottom = SCREEN_HEIGHT - base_image.get_height()
offset = height_to_bottom * 0.3
