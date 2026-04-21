import pygame
from pygame.locals import *

class Background:
    def __init__(self, img):
        self.biomes = ['forest', 'jungle', 'desert', 'underground']

        self.img = img
        self.current_biome = self.biomes[0]

    def render_background(self):
        #render the background with a parralax effect
        #this will require a lot of pixel art lol, with repeating patterns for the background
        pass

    def update_biome(self, new_biome):
        pass
