import pygame

class PhysicsEntity:
    def __init__(self, game, pos, velocity, offset=(0, 0)):
        self.game = game
        self.pos = pos
        self.velocity = velocity

        self.flip = False

    def update(self):
        pass    