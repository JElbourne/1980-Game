
"""
controllers.py

Created by Jason Elbourne on 2014-08-23.
Copyright (c) 2014 Jason Elbourne. All rights reserved.
"""

from functools import partial

import pyglet

from core.views import MainMenuView
from core.views import GameMapView
from core.entity import Player
from core.world import World


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
    batch = pyglet.graphics.Batch()

    def __init__(self, *args, **kwargs):
        super(GameController, self).__init__(*args, **kwargs)

        self.world = None
        self.player = None

        self._visibleMapSprites = []

    def update(self, dt):
        pass

    def setup(self):
        print ("game setting up...")
        # The first view in the game will be the GameMapView
        self.switch_view_class(GameMapView)
        print ("setting up world...")
        self.world = World(self.window.width, self.window.height)

        print ("setting up player...")
        self.player = Player(x=256, y=256, batch=self.batch)
        #
        print ("player is created!")

        self._generate_fov()

        return True

    def _new_player_angle(self, modifier):
        curAngle = self.player.angle
        newAngle = (curAngle + modifier)%360
        return newAngle

    def _new_player_pos(self, angle):
        x, y, z = self.player.sprite.x, self.player.sprite.y, self.player.level
        if angle == 0:
            x += 16
        elif angle == 90:
            y += 16
        elif angle == 180:
            x -= 16
        elif angle == 270:
            y -= 16
        return (x, y, z)

    def _return_collision(self, coords):
        print (self.world.mapTileData[coords])
        return self.world.mapTileData[coords]['collisionTile']

    def _generate_fov(self):
        self._visibleMapSprites = []
        # Python 2.7   iteritems()
        for key, tileData in self.world.mapTileData.items():
            self._visibleMapSprites.append(
                                           pyglet.sprite.Sprite(
                                                img=tileData["sprite"],
                                                x=key[0],
                                                y=key[1],
                                                batch=self.batch,
                                                group=self.world.group
                                                )
                                           )

    def move_player(self, angle):
        coords = self._new_player_pos(angle)
        print (coords)
        if not self._return_collision(coords):
            self.player.move(coords)

    def change_player_angle(self, modifier):
        newAngle = self._new_player_angle(modifier)
        self.player.change_angle(newAngle)

    def push_handlers(self):
        if self.setup():
            # If self.setup() did complete add the Game handlers to the stack.
            self.window.push_handlers(self)
        else:
            # If not switch back to the MainMenuController
            self.switch_controller_class(MainMenuController)
