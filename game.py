import pygame
from pygame.locals import *

import sys

from scripts.tilemap import Tilemap

from scripts.utilities import load_image, load_images

class Game:
    def __init__(self):
        
        pygame.init()

        self.screen = pygame.display.set_mode((800, 800))
        self.display = pygame.Surface((400, 400))

        self.clock = pygame.time.Clock()
        
        self.entities = {
            'player': load_image('assets\\entities\\player.png')
        }

        self.tiles = {
            'grass': load_images('assets\\tiles\\grass'),
        }

        self.tilemap = Tilemap(self, 1)

        self.running = True
        self.pos = [10, 10]
        self.movement = [False, False]

    def run(self):
        #game loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        self.running = False

            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[K_d]:
                self.pos[0] += 1
            if keys_pressed[K_a]:
                self.pos[0] -= 1
            if keys_pressed[K_s]:
                self.pos[1] += 1
            if keys_pressed[K_w]:
                self.pos[1] -= 1
                        

            self.display.fill((20, 100, 200))

            self.tilemap.render_tiles()

            self.display.blit(self.entities['player'], self.pos)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
if __name__ == '__main__':
    Game().run()
