

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


class View(object):
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
        line = menuIntros[random.randint(0,  len(menuIntros)-1)]
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
    def setup(self):
        print ("preparing to display game map...")

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
