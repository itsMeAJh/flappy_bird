from pygame import mixer
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
INITIAL_PIPE_POS_X = SCREEN_HEIGHT/2
INITIAL_PIPE_POS_Y = SCREEN_WIDTH*2

# Pipe constants
PIPE_GAP = 115
HALF_PIPE_GAP = PIPE_GAP / 2
SCROLL_SPEED = 5

# Colors
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

IMAGE_PATH = "assets/image/"

# Initialize mixer for sounds
mixer.init()

# Sound paths
SOUND_PATH = "assets/audio/"

# Generate a random action (not clear how it's used in the code)
RANDOM_ACTION = randint(0, 2)
