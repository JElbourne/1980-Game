
"""
messages.py

Created by Jason Elbourne on 2014-09-17.
Copyright (c) 2014 Jason Elbourne. All rights reserved.
"""


class MessageLog(object):
    def __init__(self):
        self.messages = []

    def add(self, message):
        self.messages.append(str(message))

    def latest(self, limit):
        if len(self.messages) > limit:
            return self.messages[:-(limit+1):-1]
        return self.messages[::-1]
