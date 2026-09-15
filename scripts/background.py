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
        self.collection = self.game.backgrounds[self.biome] #access to all items for particular background collection
        self.amt_layers = len(self.collection) - 1 #minus 1 for parallax_x
        self.imgs = [pygame.transform.scale_by(img, (self.game.display.get_width() / img.get_width(), self.game.display.get_height() / img.get_height())) for img in self.game.backgrounds[self.biome].values() if isinstance(img, pygame.Surface)]
        
    def render_background(self):
        parallax_x = self.collection['parallax-mod-x']
        parallax_y = self.collection['parallax-mod-y']

        for i, img in enumerate(self.imgs):

            y_offset = i * -30 # 50 pixels between layers
            y = (
                math.ceil((-self.game.scroll[1] // parallax_y))
                - 150
                + y_offset
                )
            width = img.get_width()
            if isinstance(img, pygame.Surface):
                self.game.display.blit(img, (math.ceil((-self.game.scroll[0] // parallax_x % width) - width), y))
                self.game.display.blit(img, (math.ceil((-self.game.scroll[0] // parallax_x % width)), y))
                self.game.display.blit(img, (math.ceil((-self.game.scroll[0] // parallax_x % width) + width), y))
                        
                parallax_x *= 0.52
                parallax_y *= 0.8

    def update_biome(self, new_biome):
        self.biome = new_biome
        self.collection = self.game.background[self.biome]
        self.imgs = [pygame.transform.scale_by(img, (self.game.display.get_width() / img.get_width(), self.game.display.get_height() / img.get_height())) for img in self.game.backgrounds[self.biome].values() if isinstance(img, pygame.Surface)]

class Cloud:
    def __init__(self):
        pass

