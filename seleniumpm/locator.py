import copy

class Locator(object):

    def __init__(self, by, value):
        self.by = by
        self.value = value

    def append(self, relative_path):
        self.value += relative_path

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def copy(self):
        return copy.deepcopy(self)
