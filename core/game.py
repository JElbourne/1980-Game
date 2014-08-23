
"""
game.py

"""

import pyglet

from core.controllers import MainMenuController


class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

        self.controller = None
        controller = MainMenuController(self)
        self.switch_controller(controller)

        self.set_visible()

        print ("Init the window")

    def switch_controller(self, new_controller):
        if self.controller:
            self.controller.pop_handler()
        self.controller = new_controller
        self.controller.push_handler()

    def on_close(self):
        print ("Closed Window,Bye!")
        pyglet.app.exit()
