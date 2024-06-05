# -*- coding:utf-8 -*-
# This file holds all the colors. It is intended to be imported by wildcard:
# ```from colors import *```
# Wildcard imports are generally frowned upon, but I know what I'm doing.
# This file should avoid importing other local files to avoid circular imports.

from pygame import Color

# These are `pygame.Color` objects to enable easy color math.
# They are in RGBA format. If Alpha is not passed, the color defaults to A=255 (fully opaque).
BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
CYAN = Color(0, 255, 255)
MAGENTA = Color(255, 0, 255)
YELLOW = Color(255, 255, 0)

GAME_BORDER = Color(85, 85, 85)
SMOKE = Color(40, 40, 40)
TANK_BG_COLOR = (64, 0, 0, 255)
