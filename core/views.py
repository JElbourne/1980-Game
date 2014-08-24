

"""
views.py
"""

import pyglet


class View(pyglet.event.EventDispatcher):
    def __init__(self, controller):
        super(View, self).__init__()

        self.controller = controller

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
        print ("IN Main Menu View")

    def on_key_press(self, key, modifiers):
        pass


