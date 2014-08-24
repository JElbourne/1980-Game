
"""
game.py

Created by Jason Elbourne on 2014-08-23.
Copyright (c) 2014 Jason Elbourne. All rights reserved.
"""

import pyglet

from core.controllers import MainMenuController


class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
        print ("Window Created...")
        self.controller = None
        # The first controller wil be the Main Menu Controller.
        controller = MainMenuController(self)
        self.switch_controller(controller)

        # Set the pyglet Window to visible
        self.set_visible()

    def switch_controller(self, new_controller):
        # Switch from one controller to another, ie. Main Menu to the Game.
        if self.controller:
            self.controller.pop_handlers()
        self.controller = new_controller
        self.controller.push_handlers()

    def on_close(self):
        # Runs if the window is closed by the User.
        print ("Closed Window manually, Good Bye!")
        pyglet.app.exit()

    def update(self, dt):
        # if this is called we will call the controller's update method.
        if self.controller:
            self.controller.update(dt)
