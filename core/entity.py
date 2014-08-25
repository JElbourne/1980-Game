
"""
entity.py
"""


class Enitity(object):
    def __init__(self, name, hp, lightLevel, level):
        self.name = name
        self.hp = hp
        self.maxHp = hp
        self.lightLevel = lightLevel
        self.maxLightLevel = lightLevel
        self.level = level

        self.sprite = None


class Character(Enitity):
    def __init__(self, armour, speed, strength, hunger, gold, angle, **kwargs):
        super(Character, self).__init__(**kwargs)
        self.armour = armour
        self.maxArmour = armour
        self.speed = speed
        self.strength = strength
        self.hunger = hunger
        self.maxHunger = hunger
        self.gold = gold

        self.angle = angle

        # counters
        self.steps = 0
        self.kills = 0
        self.friends = 0


class Player(Character):
    def __init__(self, race, class_, alignment, gender, intelligence, wisdom, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.race = race
        self.class_ = class_
        self.alignment = alignment
        self.gender = gender

        self.intelligence = intelligence
        self.wisdom = wisdom
