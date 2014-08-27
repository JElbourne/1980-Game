
"""
world.py
"""

import random

import pyglet

from core.config import CONFIG
from core import gfx

class World(object):

    """
    This is an example if chunkSize = 12 sprites

    |-----12-----||-----24-----||----36-----||-----48-----||-----60-----|

    Width if 60 tiles @ 16px = 960 px wide map (5 chunks wide)
    Height if 36 tile @ 16 px = 576 px high map (3 chunks high)

    """

    spriteSet = gfx.get_sprite_set()
    group = pyglet.graphics.OrderedGroup(0)

    def __init__(self, window_width, window_height):
        self.windowWidth = window_width
        self.windowHeight = window_height

        self.cs = CONFIG["chunkSize"]
        self.ss = CONFIG["spriteSize"]

        self.chunksWide = (self.windowWidth//(self.cs*self.ss))-1
        self.chunksHigh = self.windowHeight//(self.cs*self.ss)

        print (self.chunksWide, self.chunksHigh)

        self._grass = ("Grass", self.spriteSet[1][0])
        self._dirt = ("Dirt", self.spriteSet[2][0])

        self.mapTileData = {}

        self._generate_map_level(0)

    def _generate_room(self, z):
        ## A Chunk (12x12)
        #===========
        # |-|-|-|-|-|-|-|-|-|-|-|-|
        # |-|-|-|-|-|-|-|-|-|-|-|-|
        # |-|-|-|-|-|-|-|-|-|-|-|-|
        # |-|-|-|-|-|-|-|-|-|-|-|-|
        # |-|-|-|-|-|-|-|-|-|-|-|-|
        # |-|-|-|-|-|-|-|-|-|-|-|-|
        # |-|-|-|-|-|-|-|-|-|-|-|-|
        # |-|-|-|-|-|-|-|-|-|-|-|-|
        # |-|-|-|-|-|-|-|-|-|-|-|-|
        # |-|-|-|-|-|-|-|-|-|-|-|-|
        # |-|-|-|-|-|-|-|-|-|-|-|-|
        # |-|-|-|-|-|-|-|-|-|-|-|-|

        ## Radius Explained (ring)
        #
        #       R=1             R=2             R=3
        #       x x x           x x x x x       x x x x x x x
        #       x o x           x x x x x       x x x x x x x
        #       x x x           x x o x x       x x x x x x x
        #                       x x x x x       x x x o x x x
        #                       x x x x x       x x x x x x x
        #                                       x x x x x x x
        #                                       x x x x x x x

        rW = random.randint(2,4+1)
        rH = random.randint(2,4+1)

        midRoomX = rW + random.randint(1,((self.cs-(rW*2+1))//2))
        midRoomY = rH + random.randint(1,((self.cs-(rH*2+1))//2))

        midRoomCoord = ( int(midRoomX*self.ss), int(midRoomY*self.ss), z)

        wallCoords = utils.build_ring_coords(midRoomCoord[0], 
                                             midRoomCoord[1], 
                                             z, 
                                             rW,
                                             rH
                                             )

        roomCoords = [midRoomCoord]
        maxR = rW if rW>rH else rH
        for i in range(1, maxR+1):
            irW = i if i <= rW else rW
            irH = i if i <= rH else rH

            roomCoords += utils.build_ring_coords(midRoomCoord[0], 
                                             midRoomCoord[1], 
                                             z, 
                                             irW,
                                             irH
                                             )
        return roomCoords, wllCoords


    def _generate_map_level(self, level):
        print ("starting to generate map chunks...")
        for x in range(self.chunksWide):
            for y in range(self.chunksHigh):
                self._initialize_chunk(x, y, level)
                print ("-> ({0}, {1}, {2}) Done!".format(x, y, level))

    def _initialize_chunk(self, x, y, z):
        for c in range(self.cs):
            for r in range(self.cs):
                globalX = (c*self.ss) + (self.cs*self.ss*x)
                globalY = (r*self.ss) + (self.cs*self.ss*y)
                coords = (globalX, globalY, z)

                self.mapTileData[coords] = {
                    "sprite": self._dirt[1],
                    "name": self._dirt[0],
                    "collisionTile": False,
                    "roomFloorTile": False
                    }



















