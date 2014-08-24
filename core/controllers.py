
"""
controllers.py

Created by Jason Elbourne on 2014-08-23.
Copyright (c) 2014 Jason Elbourne. All rights reserved.
"""

from functools import partial

import pyglet

from core.views import MainMenuView
from core.views import GameMapView


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
    def __init__(self, *args, **kwargs):
        super(GameController, self).__init__(*args, **kwargs)

        self.world = None
        self.player = None

    def update(self, dt):
        pass

    def setup(self):
        print ("game setting up...")
        # The first view in the game will be the GameMapView
        self.switch_view_class(GameMapView)
        return True

    def push_handlers(self):
        if self.setup():
            # If self.setup() did complete add the Game handlers to the stack.
            self.window.push_handlers(self)
        else:
            # If not switch back to the MainMenuController
            self.switch_controller_class(MainMenuController)
