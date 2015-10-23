
"""
world.py

Created by Jason Elbourne on 2014-09-17.
Copyright (c) 2014 Jason Elbourne. All rights reserved.
"""

import random

import pyglet

from core.config import CONFIG
from core import gfx
from core import utils


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
        self._stoneWall = ("Stone Wall", self.spriteSet[3][0])
        self._stoneFloor = ("Stone Floor", self.spriteSet[4][0])
        self.doorClosed = ("Closed Door", self.spriteSet[5][0])
        self.doorLocked = ("Locked Door", self.spriteSet[5][1])
        self.doorOpen = ("Open Door", self.spriteSet[5][2])

        self.mapTileData = {}

        self._generate_map_level(0)

    def _generate_room(self, chunkX, chunkY, z):
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

        rW = random.randint(2, 4)
        rH = random.randint(2, 4)

        maxRandomX = ((self.cs-(rW*2+1))//2)
        if maxRandomX < 1:
            maxRandomX = 1
        maxRandomY = ((self.cs-(rH*2+1))//2)
        if maxRandomY < 1:
            maxRandomY = 1

        midRoomX = int(rW + random.randint(1, maxRandomX))
        midRoomY = int(rH + random.randint(1, maxRandomY))

        adjX = int((self.cs*self.ss*chunkX))
        adjY = int((self.cs*self.ss*chunkY))

        midRoomCoord = ((midRoomX*self.ss)+adjX, (midRoomY*self.ss)+adjY, z)

        wallCoords = utils.build_ring_coords(midRoomCoord[0],
                                             midRoomCoord[1],
                                             z,
                                             rW,
                                             rH
                                             )

        roomCoords = [midRoomCoord]
        maxR = rW if rW > rH else rH
        for i in range(1, maxR+1):
            irW = i if i <= rW else rW
            irH = i if i <= rH else rH

            roomCoords += utils.build_ring_coords(midRoomCoord[0],
                                                  midRoomCoord[1],
                                                  z,
                                                  irW,
                                                  irH
                                                  )
        return roomCoords, wallCoords

    def _insert_doors(self, wallCoords):
        doorCoords = []
        wc = wallCoords
        numDoors = 1 if len(wc) < 18 else 2 if 18 < len(wc) < 26 else 3
        for i in range(1, numDoors+1):
            doorCoord = None
            j = 0
            while True:
                j += 1
                ## CHANGE
                # doorCoord = random.choice(wallCoords)
                doorIndex = random.randint(0, len(wallCoords)-1)
                doorCoord = wallCoords[doorIndex]
                ## END CHANGE
                if int(doorIndex) > 0 and int(doorIndex+1) < len(wallCoords):
                    before = wallCoords[doorIndex-1]
                    after = wallCoords[doorIndex+1]
                    print (before, doorCoord, after)
                    if doorCoord[0] == before[0] and doorCoord[1] == after[1]:
                        doorCoord = None
                    elif doorCoord[0] == after[0] and doorCoord[1] ==before[1]:
                        doorCoord = None
                    else:
                        break

                if j == len(wallCoords):
                    break
            if doorCoord:
                doorCoords.append(doorCoord)
                wallCoords.remove(doorCoord)

        return wallCoords, doorCoords

    def _generate_map_level(self, level):
        print ("starting to generate map chunks...")
        for x in range(self.chunksWide):
            for y in range(self.chunksHigh):
                self._initialize_chunk(x, y, level)
                print ("-> ({0}, {1}, {2}) Done!".format(x, y, level))

    def _initialize_chunk(self, chunkX, chunkY, z):
        roomFloorTile = False
        collisionTile = False
        setSprite = self._dirt

        roomCoords, wallCoords = self._generate_room(chunkX, chunkY, z)

        floorCoords = list(set(roomCoords) - set(wallCoords))
        roomCoords = list(set(roomCoords))
        wallCoords, doorCoords = self._insert_doors(list(wallCoords))

        for c in range(self.cs):
            for r in range(self.cs):
                roomFloorTile = False
                collisionTile = False
                roomTile = False

                globalX = (c*self.ss) + (self.cs*self.ss*chunkX)
                globalY = (r*self.ss) + (self.cs*self.ss*chunkY)
                coord = (globalX, globalY, z)

                if coord in wallCoords:
                    setSprite = self._stoneWall
                    collisionTile = True
                    roomTile = True
                elif coord in doorCoords:
                    setSprite = self.doorClosed
                    collisionTile = True
                    roomTile = True
                elif coord in floorCoords:
                    setSprite = self._stoneFloor
                    roomFloorTile = True
                    roomTile = True
                elif random.randint(1,100) < 10:
                    setSprite = self._grass
                else:
                    setSprite = self._dirt

                self.mapTileData[coord] = {
                    "spriteImg": setSprite[1],
                    "name": setSprite[0],
                    "collisionTile": collisionTile,
                    "roomFloorTile": roomFloorTile,
                    "roomTile": roomTile
                    }



















