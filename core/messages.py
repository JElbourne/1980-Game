
"""
messages.py
"""


class MessageLog(object):
    def __init__(self):
        self.messages = []

    def add(self, message):
        self.messages.append(str(message))


    def latest(self, limit):
        if len(self.messages) > limit:
            return self.messages[:-(limit):-1]
        return self.messages[::-1]
