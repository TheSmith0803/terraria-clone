import pygame
from pygame.locals import *

class Background:
    def __init__(self, game, biome):
        possible_biomes = ['forest', 'jungle', 'desert', 'underground']

        if biome not in possible_biomes:
            raise RuntimeError(f'{biome} is not a valid biome!') 

        self.bg = None
        self.biome = biome
        self.game = game
        self.img = self.game.backgrounds

    def render_background(self):
        self.bg = self.game.display.blit(self.game.backgrounds[self.biome], (-self.game.scroll[0] /3, -100))

    def update_biome(self, new_biome):
        self.biome = new_biome

class Cloud:
    def __init__(self):
        pass

