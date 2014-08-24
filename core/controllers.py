
"""
controllers.py

Created by Jason Elbourne on 2014-08-23.
Copyright (c) 2014 Jason Elbourne. All rights reserved.
"""

from functools import partial

import pyglet

from core.views import MainMenuView


class Controller(object):
    def __init__(self, window):
        self.window = window
        self.current_view = None

    def setup(self):
        pass

    def update(self, dt):
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

    def pop_handelrs(self):
        if self.current_view:
            self.current_view.pop_handlers()
        self.window.pop_handlers()


class MainMenuController(Controller):
    def __init__(self, *args, **kwargs):
        super(MainMenuController, self).__init__(*args, **kwargs)

        self.setup = partial(self.switch_view_class, MainMenuView)

    def start_game(self):
        pass

    def exit_game(self):
        print ("Shutting down the Game, Good Bye!")
        pyglet.app.exit()
