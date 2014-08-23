
"""
game.py

"""

import pyglet


class Game(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)

        self.set_visible()
        print ("Init the window")
