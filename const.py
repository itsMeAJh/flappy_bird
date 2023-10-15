from pygame import image, mixer
from random import randint

# Screen Constants
SCREEN_WIDTH = 287
SCREEN_HEIGHT = 510
FPS = 32
WINDOW_TITLE = "Flappy Bird Game"

# Bird constants
BIRD_WIDTH, BIRD_HEIGHT = 34, 24
INITIAL_BIRD_POS_X = SCREEN_WIDTH / 3
INITIAL_BIRD_POS_Y = SCREEN_HEIGHT / 2

# Pipe constants
PIPE_GAP = 115
HALF_PIPE_GAP = PIPE_GAP / 2
SCROLL_SPEED = 5

# Colors
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

IMAGE_PATH = "assets/image/"

# Image paths
BACKGROUND_IMAGE = image.load(IMAGE_PATH + f"background-{randint(1, 2)}.png")
BASE_IMAGE = image.load(IMAGE_PATH + "base.png")
PIPE_IMAGE = image.load(IMAGE_PATH + f"pipe-{randint(1, 2)}.png")
SCORE_BOARD_IMAGE = image.load(IMAGE_PATH + "score_board.png")
START_BUTTON_IMAGE = image.load(IMAGE_PATH + "start_button.png")
GAME_OVER_IMAGE = image.load(IMAGE_PATH + "game_over.png")
GET_READY_IMAGE = image.load(IMAGE_PATH + "get_ready.png")
OK_BUTTON_IMAGE = image.load(IMAGE_PATH + "ok_button.png")
PAUSE_BUTTON_IMAGE = image.load(IMAGE_PATH + "pause_button.png")
PLAY_BUTTON_IMAGE = image.load(IMAGE_PATH + "play_button.png")
FLAPPY_BIRD_IMAGE = image.load(IMAGE_PATH + "flappy_bird.png")
START_GAME_IMAGE = image.load(IMAGE_PATH + "tap_tap.png")


# Initialize mixer for sounds
mixer.init()

# Sound paths
SOUND_PATH = "assets/audio/"
DIE_SOUND = mixer.Sound(SOUND_PATH + "die.mp3")
FLAP_SOUND = mixer.Sound(SOUND_PATH + "flap.mp3")
HIT_SOUND = mixer.Sound(SOUND_PATH + "hit.mp3")
POINT_SOUND = mixer.Sound(SOUND_PATH + "point.mp3")
SWOOSH_SOUND = mixer.Sound(SOUND_PATH + "swosh.mp3")

# Calculate the bottom height for pipes
HEIGHT_TO_BOTTOM = SCREEN_HEIGHT - BASE_IMAGE.get_height()
OFFSET = HEIGHT_TO_BOTTOM * 0.3

# Generate a random action (not clear how it's used in the code)
RANDOM_ACTION = randint(0, 2)
