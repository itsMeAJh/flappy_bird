from pygame import image

SCREEN_WIDTH = 287
SCREEN_HEIGHT = 510
FPS = 32
PIPE_GAP = 125

WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
initialBirdPosX = SCREEN_WIDTH / 3
initialBirdPosY = SCREEN_HEIGHT / 2
halfPipeGap = PIPE_GAP / 2
scroll_speed = 5

IMAGE_PATH = "assets/image/"
BACKGROUND = image.load(IMAGE_PATH + "background-1.png")
BIRD = image.load(IMAGE_PATH + "red_bird-1.png")
BASE = image.load(IMAGE_PATH + "base.png")
PIPE = image.load(IMAGE_PATH + "pipe.png")

free_height = SCREEN_HEIGHT - BASE.get_height()
offset = free_height * 0.4
