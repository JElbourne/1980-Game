
"""
gfx.py

Created by Jason Elbourne on 2014-08-23.
Copyright (c) 2014 Jason Elbourne. All rights reserved.
"""

import pyglet

from core.config import CONFIG

pyglet.resource.path = CONFIG["resourcePath"]
sprites = pyglet.resource.image(CONFIG["textureFile"])
spriteSize = CONFIG["spriteSize"]

spr = sprites.width//spriteSize  # spr = sprites per row
spc = sprites.height//spriteSize  # spc = sprites per column

## Full Image We import
#  1| 2| 3| 4| 5| 6| 7| 8
#  9|10|11|12|13|14|15|16
# 17|18|19|20|21|22|23|24

imgGrid = pyglet.image.ImageGrid(sprites, spr, spc)

# Result of Image Grid
# [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]


def get_sprite_set():
    spriteSet = [imgGrid[i: i+spr] for i in range(0, len(imgGrid), spr)][::-1]
    return spriteSet

# Result of spriteSet
# [ [1,2,3,4,5,6,7,8], [9,10,11,12,13,14,15,16], [17,18,19,20,21,22,23,24] ]
