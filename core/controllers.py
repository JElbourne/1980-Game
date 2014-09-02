
"""
controllers.py

Created by Jason Elbourne on 2014-08-23.
Copyright (c) 2014 Jason Elbourne. All rights reserved.
"""

from functools import partial
import random

import pyglet

from core.views import MainMenuView
from core.views import GameMapView
from core.entity import Player
from core.world import World
from core.config import CONFIG
from core import utils

class Controller(object):
    def __init__(self, window):
        self.window = window
        self.current_view = None

    def setup(self):
        pass

    def update(self, dt):
        # if this is called we will call the current_view's update method.
        if self.current_view:
            self.current_view.update(dt)

    def switch_view(self, new_view):
        if self.current_view:
            self.current_view.pop_handlers()
        self.current_view = new_view
        self.current_view.push_handlers()
        return pyglet.event.EVENT_HANDLED

    def switch_view_class(self, new_view_class):
        self.switch_view(new_view_class(self))
        return pyglet.event.EVENT_HANDLED

    def switch_controller(self, new_controller):
        self.window.switch_controller(new_controller)
        return pyglet.event.EVENT_HANDLED

    def switch_controller_class(self, controller_class):
        self.switch_controller(controller_class(self.window))
        return pyglet.event.EVENT_HANDLED

    def push_handlers(self):
        self.window.push_handlers(self)
        self.setup()

    def pop_handlers(self):
        # We are done with view so remove the stack level for the view.
        if self.current_view:
            self.current_view.pop_handlers()
        self.window.pop_handlers()


class MainMenuController(Controller):
    def __init__(self, *args, **kwargs):
        super(MainMenuController, self).__init__(*args, **kwargs)
        # Use partial to prepare the function to switch view. Much Faster.
        self.setup = partial(self.switch_view_class, MainMenuView)
        ## TODO add more menu options and views. ie. Options, Controls, Help

    def start_game(self):
        # Start Game has been selected so we run the method to switch
        # controllers over to Game Controller.
        self.switch_controller_class(GameController)

    def exit_game(self):
        # Exit game has been selected so we should take hte oportunity to
        # clean up and save any data then exist the application.
        print ("Shutting down the Game, Good Bye!")
        pyglet.app.exit()


class GameController(Controller):
    batch = pyglet.graphics.Batch()

    def __init__(self, *args, **kwargs):
        super(GameController, self).__init__(*args, **kwargs)

        self.world = None
        self.player = None

        self._visibleMapSprites = []
        self._litCoords = []

    def update(self, dt):
        pass

    def setup(self):
        print ("game setting up...")
        # The first view in the game will be the GameMapView
        self.switch_view_class(GameMapView)
        print ("setting up world...")
        self.world = World(self.window.width, self.window.height)

        spawnCoord = self._pick_random_spawn_coords(level=0)

        print ("setting up player...")
        self.player = Player(x=spawnCoord[0], y=spawnCoord[1],batch=self.batch)
        #
        print ("player is created!")

        self._generate_fov()

        return True

    def _pick_random_spawn_coords(self, level=0):
        cSW = self.world.chunksWide * self.world.cs
        cSH = self.world.chunksHigh * self.world.cs
        maxLoop = cSW * cSH
        j = 0
        while True:
            j += 1

            coordX = random.randint(3,cSW-2)
            coordY = random.randint(3,cSH-2)
            spawnCoord = (coordX*self.world.ss, coordY*self.world.ss, level)
            if spawnCoord in self.world.mapTileData:
                tileData = self.world.mapTileData[spawnCoord]
                if tileData["roomFloorTile"]:
                    break

            if j >= maxLoop:
                spawnCoord = (256,256,level)
                break
        return spawnCoord

    def _new_player_angle(self, modifier):
        curAngle = self.player.angle
        newAngle = (curAngle + modifier) % 360
        return newAngle

    def _new_player_pos(self, angle):
        x, y, z = self.player.sprite.x, self.player.sprite.y, self.player.level
        if angle == 0:
            x += 16
        elif angle == 90:
            y += 16
        elif angle == 180:
            x -= 16
        elif angle == 270:
            y -= 16
        return (x, y, z)

    def _return_collision(self, coord):
        mapWide = self.world.chunksWide * self.world.cs * self.world.ss
        mapHigh = self.world.chunksHigh * self.world.cs * self.world.ss
        return (0 > coord[0] > mapWide
                or 0 > coord[1] > mapHigh
                or self.world.mapTileData[coord]['collisionTile'])

    def _return_is_lit(self, coord):
        return coord in self._litCoords

    def _set_lit(self,coord):
        mapWide = self.world.chunksWide * self.world.cs * self.world.ss
        mapHigh = self.world.chunksHigh * self.world.cs * self.world.ss
        if (0 < coord[0] < mapWide or 0 < coord[1] < mapHigh):
            self._litCoords.append(coord)

    def _cast_light(self, coord, row, start, end, radius, xx, xy, yx, yy, id):
        if start < end:
            return
        radiusSquared = radius * radius
        for j in range(row, radius+1):
            dx, dy = -j-1, -j
            blocked = False
            while dx <=0:
                pass

    def _generate_fov(self):

        multi = [
                [1, 0, 0,-1,-1, 0, 0, 1],
                [0, 1,-1, 0, 0,-1, 1, 0],
                [0, 1, 1, 0, 0,-1,-1, 0],
                [1, 0, 0, 1,-1, 0, 0,-1],
                ]

        self._visibleMapSprites = []

        visibleCoords = []

        entityPosition = self.player.get_coords()

        for octant in range(8):
        self._cast_light(
                         entityPosition,
                         1,
                         1.0,
                         0.0,
                         self.player.lightLevel,
                         multi[0][octant],
                         multi[1][octant],
                         multi[2][octant],
                         multi[3][octant],
                         0
                         )

        visibleCoords.append(entityPosition)
        if entityPosition:
            for r in range(1, self.player.lightLevel+1):
                visibleCoords += utils.build_ring_coords(entityPosition[0],
                                             entityPosition[1],
                                             entityPosition[2],
                                             r,
                                             r
                                             )
            for coord in visibleCoords:
                if coord in self.world.mapTileData:
                    tileData = self.world.mapTileData[coord]
                    if tileData["roomTile"]:
                        self._visibleMapSprites.append(
                                               pyglet.sprite.Sprite(
                                                    img=tileData["sprite"],
                                                    x=coord[0],
                                                    y=coord[1],
                                                    batch=self.batch,
                                                    group=self.world.group
                                                    )
                                               )


        # # Python 2.7   iteritems()
        # for key, tileData in self.world.mapTileData.items():
        #     self._visibleMapSprites.append(
        #                                    pyglet.sprite.Sprite(
        #                                         img=tileData["sprite"],
        #                                         x=key[0],
        #                                         y=key[1],
        #                                         batch=self.batch,
        #                                         group=self.world.group
        #                                         )
        #                                    )

    def move_player(self, angle):
        coords = self._new_player_pos(angle)
        print (coords)
        if not self._return_collision(coords):
            self.player.move(coords)

    def change_player_angle(self, modifier):
        newAngle = self._new_player_angle(modifier)
        self.player.change_angle(newAngle)

    def open_door(self):
        ss = CONFIG['spriteSize']
        (x,y,z) = self.player.sprite.x, self.player.sprite.y, self.player.level
        coordOptions = [(x+ss, y, z), (x-ss, y, z), (x, y+ss, z), (x, y-ss, z)]
        for coord in coordOptions:
            if coord in self.world.mapTileData:
                tileData = self.world.mapTileData[coord]
                if tileData['name'] == self.world.doorClosed[0]:
                    tileData['sprite'] = self.world.doorOpen[1]
                    tileData['name'] = self.world.doorOpen[0]
                    tileData['collisionTile'] = False
                    self._generate_fov()

    def close_door(self):
        ss = CONFIG['spriteSize']
        (x,y,z) = self.player.sprite.x, self.player.sprite.y, self.player.level
        coordOptions = [(x+ss, y, z), (x-ss, y, z), (x, y+ss, z), (x, y-ss, z)]
        for coord in coordOptions:
            if coord in self.world.mapTileData:
                tileData = self.world.mapTileData[coord]
                if tileData['name'] == self.world.doorOpen[0]:
                    tileData['sprite'] = self.world.doorClosed[1]
                    tileData['name'] = self.world.doorClosed[0]
                    tileData['collisionTile'] = True
                    self._generate_fov()





    def push_handlers(self):
        if self.setup():
            # If self.setup() did complete add the Game handlers to the stack.
            self.window.push_handlers(self)
        else:
            # If not switch back to the MainMenuController
            self.switch_controller_class(MainMenuController)
