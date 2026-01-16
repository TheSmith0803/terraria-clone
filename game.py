import pygame
from pygame.locals import *

import math
import sys

from scripts.tilemap import Tilemap
from scripts.entities import PhysicsEntity, Player
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
            'grass/top': load_images('assets\\tiles\\grass')[0],
        }

        self.tilemap = Tilemap(self, 1)

        self.running = True
        self.pos = [40, 275]
        self.movement = [False, False]

        self.delta_time = 0.0

        self.player = Player(self, self.tilemap, self.pos)

    def run(self):
        #game loop
        while self.running:

            self.player.update()
                        
            self.display.fill((20, 100, 200))

            self.tilemap.render_map(self.display)

            self.player.render(self.display)
            
            speed = 1
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[K_a]:
                self.player.moving[0] = True
                self.player.velocity[0] = max(-self.player.grip + self.player.velocity[0], -speed)
            else:
                self.player.moving[0] = False
            if keys_pressed[K_d]:
                self.player.moving[0] = True
                self.player.velocity[0] = min(self.player.grip + self.player.velocity[0], speed)
            else:
                self.player.moving[0] = False

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

                    if event.key == K_w:
                        self.player.velocity[1] = -3
                
                if event.type == pygame.KEYUP:

                    if event.key == K_d:
                        self.player.moving[0] = False
                    if event.key == K_a:
                        self.player.moving[0] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.delta_time = self.clock.tick(60) / 1000.0

if __name__ == '__main__':
    Game().run()
