import pygame
from pygame.locals import *
import random
import math

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
        self.amt_layers = len(self.collection) - 1 #minus 1 for parallax
        self.imgs = [pygame.transform.scale_by(img, (self.game.display.get_width() / img.get_width(), self.game.display.get_height() / img.get_height())) for img in self.game.backgrounds[self.biome].values() if isinstance(img, pygame.Surface)]
        
    def render_background(self):
        parallax = self.collection['parallax-mod']
        for img in self.imgs:
            width = img.get_width()
            if isinstance(img, pygame.Surface):
                tile = math.ceil(self.game.display.get_width() / width)
                self.game.display.blit(img, (math.ceil((-self.game.scroll[0] // parallax % width) - width), -100))
                self.game.display.blit(img, (math.ceil((-self.game.scroll[0] // parallax % width)), -100))
                self.game.display.blit(img, (math.ceil((-self.game.scroll[0] // parallax % width) + width), -100))
                        
                parallax *= 0.52

    def update_biome(self, new_biome):
        self.biome = new_biome
        self.collection = self.game.background[self.biome]
        self.imgs = [pygame.transform.scale_by(img, (self.game.display.get_width() / img.get_width(), self.game.display.get_height() / img.get_height())) for img in self.game.backgrounds[self.biome].values() if isinstance(img, pygame.Surface)]

class Cloud:
    def __init__(self):
        pass

