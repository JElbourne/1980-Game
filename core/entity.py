
"""
entity.py
"""

import pyglet


class Enitity(object):
    group = pyglet.graphics.OrderedGroup(3)
    def __init__(self, name, hp, lightLevel, level):
        self.name = name
        self.hp = hp
        self.maxHp = hp
        self.lightLevel = lightLevel
        self.maxLightLevel = lightLevel
        self.level = level

        self.sprite = None

    def move(self, pos):
        if self.sprite:
            self.sprite.x, self.sprite.y = pos


class Character(Enitity):

    group = pyglet.graphics.OrderedGroup(4)

    def __init__(self, armour=20, speed=30, strength=10, hunger=10, gold=0,
                 angle=0, race="human", class_="Rogue", alignment="Neutral",
                 gender="Male", intelligence=10, wisdom=10, **kwargs):
        super(Character, self).__init__(name="Vladic", hp="17", lightLevel=8,
                                        level=0, **kwargs)
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

        self.angle = angle

        # counters
        self.steps = 0
        self.kills = 0
        self.friends = 0


class Player(Character):

    group = pyglet.graphics.OrderedGroup(5)

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        pass
