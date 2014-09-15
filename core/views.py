

"""
views.py

Created by Jason Elbourne on 2014-08-23.
Copyright (c) 2014 Jason Elbourne. All rights reserved.
"""
import datetime
import random

import pyglet
from pyglet.window import key

from core.static_text import MAIN_MENU_TEXT
from core.config import CONFIG
from core import gfx


class View(object):

    spriteSet = gfx.get_sprite_set()

    def __init__(self, controller):
        super(View, self).__init__()

        self.controller = controller

        self._yCoordToKeyMap = {}
        self.cursor = None
        self.minCursorY = None
        self.maxCursorY = None

        self.fontName = CONFIG["fontName"]
        self.fontSizeSm = CONFIG["fontSizeSm"]
        self.fontSizeMd = CONFIG["fontSizeMd"]
        self.fontSizeLg = CONFIG["fontSizeLg"]
        self.leading = 2
        self.fontSmall = fS = pyglet.font.load(self.fontName, self.fontSizeSm)
        self.fontNormal = fN = pyglet.font.load(self.fontName, self.fontSizeMd)
        self.fontLarge = fL = pyglet.font.load(self.fontName, self.fontSizeLg)
        self.lineHeightSmall = fS.ascent - fS.descent + self.leading
        self.lineHeightNorm = fN.ascent - fN.descent + self.leading
        self.lineHeightLarge = fL.ascent - fL.descent + self.leading

        self.menuSpacing = self.lineHeightLarge

        self.batch = pyglet.graphics.Batch()

    def setup(self):
        pass

    def update(self, dt):
        pass

    def push_handlers(self):
        # We want the handlers for a view to be added to the stack.
        self.controller.window.push_handlers(self)
        self.setup()

    def pop_handlers(self):
        # We are done with view so remove the stack level for the view.
        self.controller.window.pop_handlers()

    def _clear(self):
        # A helper method to mat to the window.clear().
        self.controller.window.clear()

    def on_draw(self):
        # This is the default on_draw for a view.
        # If a view requires multiple layer to be drawn, it should
        # override this method.
        self._clear()
        self.batch.draw()


class MenuView(View):
    def setup(self):
        # Setup what the menu view will need.
        self.cmdMap = {}

    def move_cursor(self, direction):
        # The user input will call this function to move the cursor in
        # a direction. We can update the cursor directly bacause it is
        # a view object.
        if direction >= 1:
            if self.cursor.y + self.menuSpacing <= self.maxCursorY:
                self.cursor.y += self.menuSpacing
            else:
                self.cursor.y = self.minCursorY
        else:
            if self.cursor.y - self.menuSpacing >= self.minCursorY:
                self.cursor.y -= self.menuSpacing
            else:
                self.cursor.y = self.maxCursorY

    def get_selected_command(self):
        # When the user input is to select a menu option we want to getermine
        # what command the cursor is pointing to. This method does that.
        command = None
        yCoord = self.cursor.y
        if yCoord in self._yCoordToKeyMap:
            command = self._yCoordToKeyMap[yCoord]
        return command

    def on_key_press(self, symbol, modifiers):
        # The View Accepts Key Press and calls the controller
        # This is located in a view becuase different views have different
        # inputs. (ie. Touch screen, keyboard)
        if symbol == key.UP:
            # Move the cursor up.
            self.move_cursor(1)
        if symbol == key.DOWN:
            # Move the cursor down.
            self.move_cursor(-1)
        if symbol == key.ENTER:
            # Select the menu item.
            cmd = self.get_selected_command()
            self.cmdMap[str(cmd)]()


class MainMenuView(MenuView):
    def setup(self):
        print ("preparing to display main menu screen...")
        # Setup will construct the view using the appropriate library
        # In this case our view uses Pyglet and builds the view using
        # pyglet.text.Label

        # Map some sting objects (commands) to controller functions
        self.cmdMap = {
            "start": self.controller.start_game,
            "exit": self.controller.exit_game
        }

        # Determine if it is the First of the Year.
        # Consider adding other calendar events. (Chinese new year)
        now = datetime.datetime.now()
        if now.month == 1 and now.day == 1:
            self.mainMenuIntros = ['Happy new year!, You will not beat this \
                game!', ]

        # Set to top starting point on the 'y' axis, (top of screen)
        y = 700
        # Create Title Labels
        for line in MAIN_MENU_TEXT["title"]:
            y -= self.lineHeightLarge
            pyglet.text.Label(line, font_name=self.fontName,
                              font_size=self.fontSizeLg,
                              bold=True, x=32, y=y,
                              batch=self.batch,
                              )
        # Decrease the 'y' axis position for Label
        y -= (self.lineHeightLarge*2)
        # Create Copyright Labels
        for line in MAIN_MENU_TEXT["mainMenuCopyright"]:
            y -= self.lineHeightNorm
            pyglet.text.Label(line, font_name=self.fontName,
                              font_size=self.fontSizeMd,
                              x=32, y=y, batch=self.batch)
        # Decrease the 'y' axis position for Label
        y -= (self.lineHeightLarge*2)
        menuIntros = MAIN_MENU_TEXT["mainMenuIntros"]
        # Randomly select the menu Intro to show
        ## CHANGE
        # line = random.choice(menuIntros)
        line = menuIntros[random.randint(0,  len(menuIntros)-1)]
        ## END CHANGE
        pyglet.text.Label(line, font_name=self.fontName,
                          font_size=self.fontSizeLg, bold=True,
                          x=32, y=y, batch=self.batch)
        # Decrease the 'y' axis position for Label
        y -= (self.lineHeightLarge*2)
        pyglet.text.Label("Select One", font_name=self.fontName,
                          font_size=self.fontSizeMd, bold=True,
                          x=32, y=y, batch=self.batch)
        for line in MAIN_MENU_TEXT["mainMenuItems"]:
            y -= self.menuSpacing
            if not self.cursor:
                # Set the Maximum 'y' axis for the cursor
                self.maxCursorY = y
                # Create the cursor as a Label using the ">" character.
                self.cursor = pyglet.text.Label(">",
                                                font_name=self.fontName,
                                                font_size=self.fontSizeMd,
                                                bold=True, x=32, y=y,
                                                batch=self.batch)
            # Map this 'y' axis to a command string
            self._yCoordToKeyMap[y] = line[1]
            # Create the Labels for the menu items
            pyglet.text.Label(line[0], font_name=self.fontName,
                              font_size=self.fontSizeMd,
                              x=64, y=y, batch=self.batch)
        # Set the minimum 'y' axis for the cursor
        self.minCursorY = y


class GameMapView(View):

    _messagesHudLabels = []

    def _messages_hud(self):
        hudSize = self.controller.get_message_hud_size()
        mapSize = self.controller.get_map_size()
        maxLines = (hudSize[1] // self.lineHeightNorm) - 1
        messages = self.controller.get_messages(maxLines)

        y = mapSize[1]

        for messageLabel in self._messagesHudLabels:
            messageLabel.delete()

        i = 0
        for message in messages:
            i += 1
            alpha = 255//i

            y += self.lineHeightNorm
            self._messagesHudLabels.append(pyglet.text.Label(str(message),
                                        font_name=self.fontName,
                                        font_size=self.fontSizeMd,
                                        x=32, y=y,
                                        color=(255,255,255,alpha),
                                        width=hudSize[0],
                                        batch=self.controller.batch))


    def _player_info_hud(self):
        hudCoords = self.controller.get_player_info_hud_coords()
        y = hudCoords[3] - self.lineHeightLarge
        x = hudCoords[0]

        hudWidth = hudCoords[2] - hudCoords[0]

        col1 = x + 16
        col2 = x + (hudWidth//2)

        self.playerName = pyglet.text.Label(
                                        str(self.controller.player.name),
                                        font_name=self.fontName,
                                        font_size=self.fontSizeLg,
                                        x=col1, y=y,
                                        width=hudCoords[0],
                                        batch=self.controller.batch)
        ## Class
        y -= self.lineHeightSmall
        pyglet.text.Label(
                        "class:",
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col1, y=y,
                        width=(hudCoords[0]//2)-(col1),
                        batch=self.controller.batch)
        self.playerClass = pyglet.text.Label(
                        str(self.controller.player.class_),
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col2, y=y,
                        width=hudCoords[0]//2,
                        batch=self.controller.batch)
        ## Race
        y -= self.lineHeightSmall
        pyglet.text.Label(
                        "race:",
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col1, y=y,
                        width=(hudCoords[0]//2)-(col1),
                        batch=self.controller.batch)
        self.playerRace = pyglet.text.Label(
                        str(self.controller.player.race),
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col2, y=y,
                        width=hudCoords[0]//2,
                        batch=self.controller.batch)
        ## Gender
        y -= self.lineHeightSmall
        pyglet.text.Label(
                        "gender:",
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col1, y=y,
                        width=(hudCoords[0]//2)-(col1),
                        batch=self.controller.batch)
        self.playerGender = pyglet.text.Label(
                        str(self.controller.player.gender),
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col2, y=y,
                        width=hudCoords[0]//2,
                        batch=self.controller.batch)
        ## Strength
        y -= self.lineHeightSmall
        pyglet.text.Label(
                        "strength:",
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col1, y=y,
                        width=(hudCoords[0]//2)-(col1),
                        batch=self.controller.batch)
        self.playerStrength = pyglet.text.Label(
                        str(self.controller.player.strength),
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col2, y=y,
                        width=hudCoords[0]//2,
                        batch=self.controller.batch)
        ## Speed
        y -= self.lineHeightSmall
        pyglet.text.Label(
                        "speed:",
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col1, y=y,
                        width=(hudCoords[0]//2)-(col1),
                        batch=self.controller.batch)
        self.playerSpeed = pyglet.text.Label(
                        str(self.controller.player.speed),
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col2, y=y,
                        width=hudCoords[0]//2,
                        batch=self.controller.batch)
        ## intelligence
        y -= self.lineHeightSmall
        pyglet.text.Label(
                        "intell:",
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col1, y=y,
                        width=(hudCoords[0]//2)-(col1),
                        batch=self.controller.batch)
        self.playerIntelligence = pyglet.text.Label(
                        str(self.controller.player.intelligence),
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col2, y=y,
                        width=hudCoords[0]//2,
                        batch=self.controller.batch)
        ## Wisdom
        y -= self.lineHeightSmall
        pyglet.text.Label(
                        "wisdom:",
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col1, y=y,
                        width=(hudCoords[0]//2)-(col1),
                        batch=self.controller.batch)
        self.playerWisdom = pyglet.text.Label(
                        str(self.controller.player.wisdom),
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col2, y=y,
                        width=hudCoords[0]//2,
                        batch=self.controller.batch)
        ## Steps
        y -= self.lineHeightSmall
        pyglet.text.Label(
                        "steps:",
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col1, y=y,
                        width=(hudCoords[0]//2)-(col1),
                        batch=self.controller.batch)
        self.playerSteps = pyglet.text.Label(
                        str(self.controller.player.steps),
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col2, y=y,
                        width=hudCoords[0]//2,
                        batch=self.controller.batch)
        ## Gold
        y -= self.lineHeightSmall
        pyglet.text.Label(
                        "gold:",
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col1, y=y,
                        width=(hudCoords[0]//2)-(col1),
                        batch=self.controller.batch)
        self.playerGold = pyglet.text.Label(
                        str(self.controller.player.gold),
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col2, y=y,
                        width=hudCoords[0]//2,
                        batch=self.controller.batch)


    def _health_hud(self):
        hudCoords = self.controller.get_health_hud_coords()
        y = hudCoords[3] - self.lineHeightLarge
        x = hudCoords[0]

        hudWidth = hudCoords[2] - hudCoords[0]

        col1 = x + 16
        col2 = x + (hudWidth//2)
        y -= self.lineHeightSmall
        pyglet.text.Label(
                        "Health Information",
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col1, y=y,
                        width=(hudCoords[0]//2)-(col1),
                        batch=self.controller.batch)

        goodColorImg = self.spriteSet[0][4]
        badColorImg = self.spriteSet[0][5]

        y -= self.lineHeightLarge

        self.goodColorSprite = pyglet.sprite.Sprite(
                    goodColorImg,
                    x=col1,
                    y=y,
                    batch=self.controller.batch,
                    group=pyglet.graphics.OrderedGroup(2)
                    )
        self.badColorSprite = pyglet.sprite.Sprite(
                    badColorImg,
                    x=col1,
                    y=y,
                    batch=self.controller.batch,
                    group=pyglet.graphics.OrderedGroup(1)
                    )

    def _map_info_hud(self):
        hudCoords = self.controller.get_map_info_hud_coords()
        y = hudCoords[3] - self.lineHeightLarge
        x = hudCoords[0]

        hudWidth = hudCoords[2] - hudCoords[0]

        col1 = x + 16
        col2 = x + (hudWidth//2)

        tileInfrontData, tileOnData = self.controller.get_tile_hud_data()

        ## Level
        y -= self.lineHeightSmall
        pyglet.text.Label(
                        "level:",
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col1, y=y,
                        width=(hudCoords[0]//2)-(col1),
                        batch=self.controller.batch)
        self.playerLevel = pyglet.text.Label(
                        str(self.controller.player.level),
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col2, y=y,
                        width=hudCoords[0]//2,
                        batch=self.controller.batch)

        y -= self.lineHeightSmall
        self.tileInfrontData = pyglet.text.Label(
                        "In Front:  {}".format(tileInfrontData['name']),
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col1, y=y,
                        width=(hudCoords[0]//2)-(col1),
                        batch=self.controller.batch)
        y -= self.lineHeightSmall
        self.tileOnData = pyglet.text.Label(
                        "Standing On:  {}".format(tileOnData['name']),
                        font_name=self.fontName,
                        font_size=self.fontSizeSm,
                        x=col1, y=y,
                        width=(hudCoords[0]//2)-(col1),
                        batch=self.controller.batch)

    def refresh_message_hud(self):
        self._messages_hud()

    def setup(self):
        print ("preparing to display game map...")

        self._messages_hud()
        self._player_info_hud()
        self._health_hud()
        self._map_info_hud()

    def update(self, dt):
        pass

    def on_key_press(self, symbol, modifiers):
        # The View Accepts Key Press and calls the controller.
        # This is located in a view becuase different views have different
        # inputs. (ie. Touch screen, keyboard)
        ## Move Inputs
        if symbol == key.W:
            self.controller.move_player(90)
        if symbol == key.A:
            self.controller.move_player(180)
        if symbol == key.S:
            self.controller.move_player(270)
        if symbol == key.D:
            self.controller.move_player(0)
        ## Angle Inputs
        if symbol == key.LEFT:
            self.controller.change_player_angle(90)
        if symbol == key.RIGHT:
            self.controller.change_player_angle(-90)
        ## Door Inputs
        if symbol == key.RSHIFT:
            self.controller.open_door()
        if symbol == key.RCTRL:
            self.controller.close_door()
        ## Manipulate Items on Map
        if symbol == key.UP:
            self.controller.pickup_item()
        if symbol == key.DOWN:
            self.controller.drop_item()

    def on_draw(self):
        # GameMapView Requires many layers and so se override on_draw().
        self._clear()
        self.controller.batch.draw()
