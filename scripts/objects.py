class Object:
    def __init__(self, img, pos):
        self.states = 2
        self.img = img
        self.pos = pos

    def update(self):
        pass

    def render(self):
        pass

class Chest(Object):
    def __init__(self):
        pass