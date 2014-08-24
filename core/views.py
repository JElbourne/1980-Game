

"""
views.py

Created by Jason Elbourne on 2014-08-23.
Copyright (c) 2014 Jason Elbourne. All rights reserved.
"""
import datetime
import random

import pyglet

from core.static_text import MAIN_MENU_TEXT


class View(pyglet.event.EventDispatcher):
    def __init__(self, controller):
        super(View, self).__init__()

        self.controller = controller

        self._yCoordToKeyMap = {}
        self.cursor = None
        self.minCursorY = None
        self.maxCursorY = None

        self.fontName = "Courier New"
        self.fontSizeSm = 12
        self.fontSizeMd = 16
        self.fontSizeLg = 20
        self.leading = 2
        self.fontSmall = fS = pyglet.font.load(self.fontName, self.fontSizeSm)
        self.fontNormal = fN = pyglet.font.load(self.fontName, self.fontSizeMd)
        self.fontLarge = fL = pyglet.font.load(self.fontName, self.fontSizeLg)
        self.lineHeightSmall = fS.ascent - fS.descent + self.leading
        self.lineHeightNorm  = fN.ascent - fN.descent + self.leading
        self.lineHeightLarge = fL.ascent - fL.descent + self.leading

        self.menuSpacing = self.lineHeightLarge

        self.batch = pyglet.graphics.Batch()

    def setup(self):
        pass

    def update(self, dt):
        pass

    def push_handlers(self):
        self.controller.window.push_handlers(self)
        self.setup()

    def pop_handlers(self):
        self.controller.window.pop_handlers()

    def _clear(self):
        self.controller.window.clear()

    def on_draw(self):
        self._clear()
        self.batch.draw()

    def on_key_pressed(self, key, modifiers):
        self.dispatch_event("on_key_press", key, modifiers)

View.register_event_type('on_key_press')


class MenuView(View):
    def setup(self):
        self.cmdMap = {}

    def move_cursor(self, direction):
        pass

    def get_selected_command(self):
        pass


class MainMenuView(MenuView):
    def setup(self):
        self.cmdMap = {
            "start": self.controller.start_game,
            "exit": self.controller.exit_game
        }

        now = datetime.datetime.now()
        if now.month == 1 and now.day == 1:
            self.mainMenuIntros = ['Happy new year!, You will not beat this \
                game!', ]

        y = 700
        for line in MAIN_MENU_TEXT["title"]:
            y -= self.lineHeightLarge
            pyglet.text.Label(line, font_name=self.fontName,
                              font_size=self.fontSizeLg,
                              bold=True, x=32, y=y,
                              batch=self.batch,
                              )

        y -= (self.lineHeightLarge*2)
        for line in MAIN_MENU_TEXT["mainMenuCopyright"]:
            y -= self.lineHeightNorm
            pyglet.text.Label(line, font_name=self.fontName,
                              font_size=self.fontSizeMd,
                              x=32, y=y, batch=self.batch)

        y -= (self.lineHeightLarge*2)
        menuIntros = MAIN_MENU_TEXT["mainMenuIntros"]
        line = menuIntros[random.randint(0,  len(menuIntros)-1)]
        pyglet.text.Label(line, font_name=self.fontName,
                          font_size=self.fontSizeLg, bold=True,
                          x=32, y=y, batch=self.batch)

        y -= (self.lineHeightLarge*2)
        pyglet.text.Label("Select One", font_name=self.fontName,
                          font_size=self.fontSizeMd, bold=True,
                          x=32, y=y, batch=self.batch)
        for line in MAIN_MENU_TEXT["mainMenuItems"]:
            y -= self.menuSpacing
            if not self.cursor:
                # Last is to write the cursor:
                self.maxCursorY = y
                self.cursor = pyglet.text.Label(">",
                                                font_name=self.fontName,
                                                font_size=self.fontSizeMd,
                                                bold=True, x=32, y=y,
                                                batch=self.batch)

            self._yCoordToKeyMap[y] = line[1]
            pyglet.text.Label(line[0], font_name=self.fontName,
                              font_size=self.fontSizeMd,
                              x=64, y=y, batch=self.batch)

        self.minCursorY = y

    def on_key_press(self, key, modifiers):
        pass
