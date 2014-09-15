
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
from core.entity import Item
from core.world import World
from core.messages import MessageLog
from core.config import CONFIG

from config import item_config


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

        self._visibleMapSprites = {}
        self._itemsData = {}
        self._litCoords = []
        self._memoryCoords = []
        self._entities = []

        pyglet.clock.schedule_interval(self._decay_torches, 10)

    def update(self, dt):
        pass

    def setup(self):
        print ("game setting up...")

        self.messages = MessageLog()
        self._add_message("Welcome to your doom!")

        print ("setting up world...")
        self.world = World(self.window.width, self.window.height)

        spawnCoord = self._pick_random_spawn_coords(level=0)

        print ("setting up player...")
        self.player = Player(x=spawnCoord[0], y=spawnCoord[1],batch=self.batch)
        self._entities.append(self.player)

        print ("player is created!")

        itemIds = item_config.level_items[0]
        for itemId in itemIds:
            if itemId in item_config.item_types:
                item = item_config.item_types[itemId]
                itemSpawnCoord = self._pick_random_spawn_coords(level=0)
                item["x"] = itemSpawnCoord[0]
                item["y"] = itemSpawnCoord[1]
                item["level"] = itemSpawnCoord[2]
                item["batch"] = self.batch
                itemInstance = Item(**item)
                self._entities.append(itemInstance)
                self._itemsData[itemSpawnCoord] = itemInstance


        self._generate_fov()

        # The first view in the game will be the GameMapView
        self.switch_view_class(GameMapView)

        return True

    def _decay_torches(self, dt):
        for item in self._entities:
            if item.name == "Torch":
                if item.lightLevel > 0:
                    item.lightLevel -= 1

    def _add_message(self, message):
        self.messages.add(str(message))
        if self.current_view:
            self.current_view.refresh_message_hud()

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
        if coord in self.world.mapTileData:
            return self.world.mapTileData[coord]['collisionTile']
        return True

    def _return_is_lit(self, coord):
        return coord in self._litCoords

    def _set_lit(self,coord):
        if coord in self.world.mapTileData:
            self._litCoords.append(coord)

    def _cast_light(self, cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
        if start < end:
            return

        ss = self.world.ss
        z = self.player.level
        radiusSquared = radius * radius
        for j in range(row, radius+1):
            dx, dy = -j-1, -j
            blocked = False
            while dx <=0:
                dx += 1
                x, y = (cx + ((dx*xx+dy*xy)*ss), cy + ((dx * yx + dy * yy)*ss))
                lSlope, rSlope = (dx-0.5)/(dy+0.5), (dx+0.5)/(dy-0.5)
                if start <  rSlope:
                    continue
                elif end > lSlope:
                    break
                else:
                    if dx*dx + dy*dy < radiusSquared:
                        self._set_lit((x, y, z))
                    if blocked:
                        if self._return_collision((x, y, z)):
                            newStart = rSlope
                            continue
                        else:
                            blocked = False
                            start = newStart
                    else:
                        if self._return_collision((x, y, z)) and j < radius:
                            blocked = True
                            self._cast_light( cx,cy,j+1,start,lSlope,radius,
                                             xx,xy,yx,yy, id+1)
                            newStart = rSlope
            if blocked:
                break

    def _generate_fov(self):
        self._litCoords = []
        entityCoords = {}
        for entity in self._entities:
            entityPosition = entity.get_coords()

            if entity.lightLevel <= 0:
                entityCoords[entityPosition] = entity
                print (entityPosition)
            else:
                entity.sprite = pyglet.sprite.Sprite(
                    entity.spriteImg,
                    x=entity.x,
                    y=entity.y,
                    batch=self.batch,
                    group=entity.group
                    )

                visionSections = 8
                lightLevel = entity.lightLevel
                multi = [
                        [1, 0, 0,-1,-1, 0, 0, 1],
                        [0, 1,-1, 0, 0,-1, 1, 0],
                        [0, 1, 1, 0, 0,-1,-1, 0],
                        [1, 0, 0, 1,-1, 0, 0,-1],
                        ]

                inRoom = self.world.mapTileData[entityPosition]["roomTile"]
                if not inRoom and entity.__class__.__name__ == "Player":
                    visionSections = 2
                    lightLevel = int(entity.lightLevel//1.6)
                    if entity.angle == 0:
                        multi = [[0, 0], [-1, -1], [1, -1], [0, 0]]
                    elif entity.angle == 90:
                        multi = [[-1, 1], [0, 0], [0, 0], [-1, -1]]
                    elif entity.angle == 180:
                        multi = [[0, 0], [1, 1], [-1, 1], [0, 0]]
                    else:
                        multi = [[1, -1], [0, 0], [0, 0], [1, 1]]

                for section in range(visionSections):
                    self._cast_light(
                                     entityPosition[0],
                                     entityPosition[1],
                                     1,
                                     1.0,
                                     0.0,
                                     lightLevel,
                                     multi[0][section],
                                     multi[1][section],
                                     multi[2][section],
                                     multi[3][section],
                                     0
                                     )

                self._litCoords.append(entityPosition)

        for coord in self._litCoords:
            tileData = None
            if coord in self.world.mapTileData:
                tileData = self.world.mapTileData[coord]
                group = self.world.group
            if coord in entityCoords:
                entity = entityCoords[coord]
                group = entity.group
                tileData = entity.__dict__

            if tileData:
                spriteData = pyglet.sprite.Sprite(
                                            img=tileData["spriteImg"],
                                            x=coord[0],
                                            y=coord[1],
                                            batch=self.batch,
                                            group=group
                                            )
                self._visibleMapSprites[coord] = spriteData

        memoryCoords = self._visibleMapSprites.keys() - self._litCoords

        for tileCoord in memoryCoords:
            if tileCoord in self._visibleMapSprites:
                tile = self._visibleMapSprites[tileCoord]
                tile.opacity = 20


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

    def get_map_size(self):
        width = self.world.chunksWide * self.world.cs * self.world.ss
        height = self.world.chunksHigh * self.world.cs * self.world.ss
        return width, height

    def get_message_hud_size(self):
        mapSize = self.get_map_size()
        return mapSize[0], self.window.height - mapSize[1]

    def get_player_info_hud_coords(self):
        mapSize = self.get_map_size()
        sectionHeight = self.window.height//3

        startX = mapSize[0]
        stopX = self.window.width

        startY = self.window.height - sectionHeight
        stopY = self.window.height

        return startX, startY, stopX, stopY

    def get_map_info_hud_coords(self):
        mapSize = self.get_map_size()
        sectionHeight = self.window.height//3

        startX = mapSize[0]
        stopX = self.window.width

        startY = 0
        stopY = sectionHeight

        return startX, startY, stopX, stopY

    def get_messages(self, limit):
        return self.messages.latest(limit)

    def move_player(self, angle):
        coords = self._new_player_pos(angle)
        print (coords)
        if not self._return_collision(coords):
            self.player.move(coords)
            self.player.change_angle(angle)
            self._generate_fov()

    def change_player_angle(self, modifier):
        newAngle = self._new_player_angle(modifier)
        self.player.change_angle(newAngle)
        self._generate_fov()

    def open_door(self):
        ss = CONFIG['spriteSize']
        (x,y,z) = self.player.sprite.x, self.player.sprite.y, self.player.level
        coordOptions = [(x+ss, y, z), (x-ss, y, z), (x, y+ss, z), (x, y-ss, z)]
        for coord in coordOptions:
            if coord in self.world.mapTileData:
                tileData = self.world.mapTileData[coord]
                if tileData['name'] == self.world.doorClosed[0]:
                    tileData['spriteImg'] = self.world.doorOpen[1]
                    tileData['name'] = self.world.doorOpen[0]
                    tileData['collisionTile'] = False
                    self._generate_fov()
                    self._add_message("You opened the door!")

    def close_door(self):
        ss = CONFIG['spriteSize']
        (x,y,z) = self.player.sprite.x, self.player.sprite.y, self.player.level
        coordOptions = [(x+ss, y, z), (x-ss, y, z), (x, y+ss, z), (x, y-ss, z)]
        for coord in coordOptions:
            if coord in self.world.mapTileData:
                tileData = self.world.mapTileData[coord]
                if tileData['name'] == self.world.doorOpen[0]:
                    tileData['spriteImg'] = self.world.doorClosed[1]
                    tileData['name'] = self.world.doorClosed[0]
                    tileData['collisionTile'] = True
                    self._generate_fov()
                    self._add_message("You closed the door!")

    def pickup_item(self):
        thereIsRoom = True
        coords = self.player.get_coords()
        if coords in self._itemsData:
            item = self._itemsData[coords]
            if item.weight <= self.player.strength:
                backpack = self.player.backpack
                if (backpack.weight + item.weight) <= backpack.maxWeight:
                    if item not in backpack:
                        thereIsRoom = backpack.capacity > len(backpack)
                    if thereIsRoom:
                        item.sprite.batch = None
                        backpack.add(item)
                        del self._itemsData[coords]
                        self._entities.remove(item)
                        self._add_message("You picked up a {}!".format(item.name))


    def drop_item(self):
        coords = self.player.get_coords()
        backpack = self.player.backpack
        if backpack.activeItem:
            item = backpack.activeItem
            item.move(coords)
            item.lightLevel = item.maxLightLevel
            print (item.maxLightLevel, item.lightLevel)
            item.sprite.batch = self.batch
            backpack.remove(item)
            self._itemsData[coords] = item
            self._entities.append(item)
            self._add_message("You dropped up a {}!".format(item.name))

    def push_handlers(self):
        if self.setup():
            # If self.setup() did complete add the Game handlers to the stack.
            self.window.push_handlers(self)
        else:
            # If not switch back to the MainMenuController
            self.switch_controller_class(MainMenuController)
