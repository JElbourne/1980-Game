#!/usr/bin/env python3.4
# encoding: utf-8

"""
1980.py

Created by Jason Elbourne on 2014-08-22.
Copyright (c) 2014 Jason Elbourne. All rights reserved.
"""

import pyglet

from core.game import Game


def main():
    game = Game(width=1280,
                height=768,
                caption="1980 Game",
                visible=False
                )

    pyglet.app.run()


if __name__ == "__main__":
    main()