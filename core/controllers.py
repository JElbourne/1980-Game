
"""
controllers.py
"""


import pyglet


class Controller(object):
    def __init__(self, window):
        self.window = window
        self.current_view = None


class MainMenuController(Controller):
    pass
