
"""
world.py
"""

import pyglet

from core.config import CONFIG


class World(object):

    """
    This is an example if chunkSize = 12 sprites

    |-----12-----||-----24-----||----36-----||-----48-----||-----60-----|

    Width if 60 tiles @ 16px = 960 px wide map (5 chunks wide)
    Height if 36 tile @ 16 px = 576 px high map (3 chunks high)

    """

    group = pyglet.graphics.OrderedGroup(0)

    def __init__(self, window_width, window_height):
        self.windowWidth = window_width
        self.windowHeight = window_height

        cs = CONFIG["chunkSize"]
        ss = CONFIG["spriteSize"]

        self.chunksWide = (self.windowWidth//(cs*ss))-1
        self.chunksHigh = self.windowHeight//(cs*ss)

        print (self.chunksWide, self.chunksHigh)
