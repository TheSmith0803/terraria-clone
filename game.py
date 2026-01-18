import pygame
from pygame.locals import *

import math
import sys

from scripts.world import World
from scripts.tilemap import Tilemap
from scripts.entities import PhysicsEntity, Player
from scripts.utilities import load_image, load_images, Animation

class Game:
    def __init__(self):
        
        pygame.init()

        self.screen = pygame.display.set_mode((800, 800))
        self.display = pygame.Surface((400, 400))

        self.clock = pygame.time.Clock()
        
        self.entities = {
            #player sprite and animations for player
            'player': load_image('assets\\entities\\player.png'),
            'player/idle': Animation(load_image('assets\\entities\\player\\idle\\player-idle.png'), img_dur=5)
        }

        self.tiles = {
            #grass tiles
            'grass': load_images('assets\\tiles\\grass'),
        }

        #everything else lol
        self.assets = {
            'background': load_image('assets\\shitty-background.png'),
            #'cursor': load_image(),
        }

        self.tilemap = Tilemap(self, 1)
        self.tilemap.generate_map()
        self.running = True
        self.pos = [40, 105]
        self.movement = [False, False]

        self.scroll = [0, 0]

        self.delta_time = 0.0

        self.player = Player(self, self.tilemap, self.pos)

    def run(self):
        #game loop
        while self.running:
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 10
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 10
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            mpos = pygame.mouse.get_pos()
            mouse_btns = pygame.mouse.get_pressed()

            mposx = (mpos[0] // self.tilemap.tile_size) // 2 + (render_scroll[0] // self.tilemap.tile_size)
            mposy = (mpos[1] // self.tilemap.tile_size)  // 2 + (render_scroll[1] // self.tilemap.tile_size)
            mpos = (mposx, mposy)

            #for removing tiles
            try:
                if mouse_btns[0] and str(mpos[0]) + ';' + str(mpos[1] + 1) in self.tilemap.tile_map.keys():
                    self.tilemap.tile_map.pop(str(mpos[0]) + ';' + str(mpos[1] + 1))
                    print(f'removed tile: {str(mpos[0]) + ';' + str(mpos[1])}')
                else:
                    pass
            except KeyError:
                pass

            self.display.fill((20, 100, 200))
            self.display.blit(pygame.transform.scale_by(self.assets['background'], 0.5), (0,0))

            self.player.update()
            
            self.tilemap.render_map(self.display, offset=render_scroll)
            self.player.render(self.display, offset=render_scroll)

            print(self.player.pos)

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

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print('ok')
                    print(mpos)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.delta_time = self.clock.tick(60) / 1000.0

if __name__ == '__main__':
    Game().run()
