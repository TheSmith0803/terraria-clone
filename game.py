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
            #player sprite and animations for player
            'player': load_image('assets\\entities\\player.png')
        }

        self.tiles = {
            #grass tiles
            'grass': load_images('assets\\tiles\\grass'),
        }

        self.tilemap = Tilemap(self, 1)
        self.tilemap.generate_map()
        self.running = True
        self.pos = [40, 275]
        self.movement = [False, False]

        self.delta_time = 0.0

        self.player = Player(self, self.tilemap, self.pos)

    def run(self):
        #game loop
        while self.running:
            
            mpos = pygame.mouse.get_pos()
            mouse_btns = pygame.mouse.get_pressed()

            mposx = (mpos[0] // self.tilemap.tile_size) // 2
            mposy = (mpos[1] // self.tilemap.tile_size) // 2
            mpos = (mposx, mposy)

            #for removing tiles
            try:
                if mouse_btns[0] and self.tilemap.tile_map[str(mpos[0]) + ';' + str(mpos[1])]:
                    self.tilemap.tile_map.pop(str(mpos[0]) + ';' + str(mpos[1] - 1))
                    print(f'removed tile: {str(mpos[0]) + ';' + str(mpos[1])}')
                    print(self.tilemap.tile_map)
                else:
                    pass
            except KeyError:
                pass
            self.player.update()
                        
            self.display.fill((20, 100, 200))
            
            self.tilemap.render_map(self.display)
            mouse_over_rect = pygame.Rect(((mpos[0] / 2) * self.tilemap.tile_size * 2, (mpos[1] / 2) * self.tilemap.tile_size * 2) , self.tiles['grass'][0].get_size())
            #pygame.draw.rect(self.display, (255, 0, 0), mouse_over_rect)
            self.player.render(self.display)

            

            speed = 1
            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[K_a] or keys_pressed[K_d]:
                self.player.moving[0] = True
            else:
                self.player.moving[0] = False

            if keys_pressed[K_a]:
                if self.player.collisions['down']:
                    self.player.velocity[0] = max(-self.player.grip + self.player.velocity[0], -speed)
                else:
                    self.player.velocity[0] = max(-self.player.air_grip + self.player.velocity[0], -speed)

            if keys_pressed[K_d]:
                if self.player.collisions['down']:
                    self.player.velocity[0] = min(self.player.grip + self.player.velocity[0], speed)
                else:
                    self.player.velocity[0] = min(self.player.air_grip + self.player.velocity[0], speed)

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
