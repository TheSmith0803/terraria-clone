import pygame
from pygame.locals import *
import random

class Background:
    def __init__(self, game, biome):
        possible_biomes = ['forest', 'jungle', 'desert', 'underground']
        forest_backgrounds = ['pine']
        if biome not in possible_biomes:
            raise RuntimeError(f'{biome} is not a valid biome!') 

        self.bg = None
        self.biome = biome
        self.game = game
        self.collection = self.game.backgrounds[self.biome]
        self.imgs = [pygame.transform.scale_by(img, (self.game.display.get_width() / img.get_width(), self.game.display.get_height() / img.get_height())) for img in self.game.backgrounds[self.biome].values()]
        
    def render_background(self):
        parralax = 5
        for img in self.imgs:
            self.bg = self.game.display.blit(img, (-self.game.scroll[0] / parralax, -100))
            parralax *= 0.5

    def update_biome(self, new_biome):
        self.biome = new_biome
        self.collection = self.game.background[self.biome]
        self.imgs = [pygame.transform.scale_by(img, (self.game.display.get_width() / img.get_width(), self.game.display.get_height() / img.get_height())) for img in self.game.backgrounds[self.biome].values()]

class Cloud:
    def __init__(self):
        pass

