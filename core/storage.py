
"""
storage.py
"""


class Storage(object):
    def __init__(self, name, capacity=27, maxWeight=150):
        self.name = name
        self.capacity = capacity
        self.weight = 0
        self.maxWeight = maxWeight

        self.contents = {}

        self.sprite = None

        self.activeItem = None

    def __iter__(self):
        return iter(self.contents.items())

    def __len__(self):
        return len(self.contents)

    def __contains__(self, item):
        return item.ident in self.contents

    def __getitem__(self, item):
        if item.ident in self.contents:
            return self.contents[item.ident]
        return None

    def __setitem__(self, item, value):
        self.contents[item.ident] = value
        return self[item]

    def add(self, item, quantity=1):
        if quantity <= 0:
            raise ValueError("Negative number or zero, Use remove() instead")

        if item in self:
            self[item].quantity += quantity
            self[item].recalc()
        else:
            self[item] = item
            self.activeItem = item

        self.weight += (item.weight * quantity)

    def remove(self, item, quantity=1):
        if item not in self:
            raise KeyError("Item not in contents")
        if quantity <= 0:
            raise ValueError("Negative number or zero, Use add() instead")

        self.weight -= (item.weight * quantity)
        if self.weight < 0:
            self.weight = 0

        if self[item].quantity <= quantity:
            del self.contents[item.ident]
            if self.activeItem == item:
                self.activeItem = None
        else:
            self[item].quanitty -= quantity
            self[item].recalc()


















