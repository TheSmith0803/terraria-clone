import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.pos = list(pos)
        self.velocity = [0, 0]
        
        self.gravity = 1

        self.flip = False

    def rect(self):
        return pygame.Rect(*self.pos, *self.size)


    def update(self):
        pass

class Player(PhysicsEntity):
    pass

class NPC(PhysicsEntity):
    pass

class Enemy(PhysicsEntity):
    pass