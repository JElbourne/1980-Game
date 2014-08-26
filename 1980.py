#!/usr/bin/env python3.4
# encoding: utf-8

"""
1980.py

Created by Jason Elbourne on 2014-08-22.
Copyright (c) 2014 Jason Elbourne. All rights reserved.
"""

import pyglet

from core.game import Game
from core.config import CONFIG


def main():

    # Chunk of 12 * sprite of 16 * 3 chunks High = 576 pixels High
    # Chunk of 12 * sprite of 16 * 4 chunks Wide = 768 pixels Wide
    # Plus HUD spacing making a total size of 1260x690 pixels

    # Create the Game Instance
    game = Game(width=CONFIG["windowWidth"],
                height=CONFIG["windowHeight"],
                caption=CONFIG["appName"],
                visible=False
                )
    print ("Game instance created with window size: {}x{}".format(game.width,
                                                                  game.height))
    # Start the pyglet app
    pyglet.app.run()


if __name__ == "__main__":
    main()
