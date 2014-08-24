

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
        self.controller.window.push_handlers()
        self.setup()

    def pop_handlers(self):
        self.controller.window.pop_handler()

    def _clear(self):
        self.controller.window.clear()

    def on_draw(self):
        self._clear()
        self.batch.draw()

    def on_key_pressed(self, key, modifiers):
        self.dispatch_event("on_key_press", key, modifiers)

View.register_event_type('on_key_pressed')
