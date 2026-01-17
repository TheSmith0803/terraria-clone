import pygame

class UI:
    def __init__(self, game, images, pos):
        self.images = images
        self.pos = pos

    def update(self):
        pass

    def render_inventory(self, surf):
        surf.blit()
        