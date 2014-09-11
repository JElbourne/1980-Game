
"""
entity.py

Created by Jason Elbourne on 2014-08-23.
Copyright (c) 2014 Jason Elbourne. All rights reserved.
"""

import pyglet

from core import gfx
from core.storage import Storage

class Entity(object):
    spriteSet = gfx.get_sprite_set()
    group = pyglet.graphics.OrderedGroup(3)

    def __init__(self, name, hp, lightLevel, level, angle):
        self.name = name
        self.hp = hp
        self.maxHp = hp
        self.lightLevel = lightLevel
        self.maxLightLevel = lightLevel
        self.level = level
        self.angle = angle

        self.x = 0
        self.y = 0

        self.sprite = None

    def move(self, coords):
        # A change position method to update the instance sprite position
        self.x = coords[0]
        self.y = coords[1]
        self.level = coords[2]
        if self.sprite:
            self.sprite.x = self.x
            self.sprite.y = self.y

    def change_angle(self, angle):
        # A change angle method to update the instance variable
        self.angle = angle
        self._update_sprite_angle()

    def get_coords(self):
        return self.x, self.y, self.level


class Character(Entity):

    group = pyglet.graphics.OrderedGroup(4)

    def __init__(self, armour=20, speed=30, strength=10, hunger=10, gold=0,
                 race="human", class_="Rogue", alignment="Neutral",
                 gender="Male", intelligence=10, wisdom=10, **kwargs):
        super(Character, self).__init__(name="Vladic", hp="17", lightLevel=8,
                                        level=0, angle=0, **kwargs)
        self.armour = armour
        self.maxArmour = armour
        self.speed = speed
        self.strength = strength
        self.hunger = hunger
        self.maxHunger = hunger
        self.gold = gold
        self.race = race
        self.class_ = class_
        self.alignment = alignment
        self.gender = gender
        self.intelligence = intelligence
        self.wisdom = wisdom

        # counters
        self.steps = 0
        self.kills = 0
        self.friends = 0


class Player(Character):

    group = pyglet.graphics.OrderedGroup(5)

    def __init__(self, x, y, batch, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)

        # Set the different player sprites from the spriteSet
        self._playerSpriteR = self.spriteSet[0][0]
        self._playerSpriteU = self.spriteSet[0][1]
        self._playerSpriteL = self.spriteSet[0][2]
        self._playerSpriteD = self.spriteSet[0][3]

        self.x = x
        self.y = y

        self.spriteImg = self._playerSpriteU

        self.backpack = Storage(name="backpack")


    def _update_sprite_angle(self):
        # Update the sprite used based on the current angle.
        if self.angle == 0:
            self.sprite.image = self._playerSpriteR
        elif self.angle == 90:
            self.sprite.image = self._playerSpriteU
        elif self.angle == 180:
            self.sprite.image = self._playerSpriteL
        elif self.angle == 270:
            self.sprite.image = self._playerSpriteD


class Item(Entity):
    """
    Items are things you can actually pick up and use.
    """

    group = pyglet.graphics.OrderedGroup(4)

    def __init__(self, ident, description, quantity, value,
                 weight, x, y, spriteX, spriteY, batch, **kwargs):
        super(Item, self).__init__(**kwargs)
        self.ident = ident
        self.description = description
        self.quantity = quantity
        self.weight = weight
        self.x = x
        self.y = y

        self.value = value
        self.netValue = int(self.value) * int(self.quantity)

        self.spriteImg = self.spriteSet[spriteY][spriteX]


    def recalc(self):
        ## To be call to update the netValue based on a change in either a value or quantity.
        self.netValue = int(self.value) * int(self.quantity)



























