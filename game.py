import pygame
from pygame.locals import *

import math
import sys

from scripts.world import World
from scripts.tilemap import Tilemap
from scripts.entities import PhysicsEntity, Player
from scripts.inventory import Inventory
from scripts.utilities import load_image, load_images, Animation

class Game:
    def __init__(self):
        
        pygame.init()

        #these variables are for calculating cursor pos with scaling
        self.window_size = (800, 800)
        self.display_res = (self.window_size[0] / 2, self.window_size[1] / 2)
        self.x_res_ratio = self.window_size[0] / self.display_res[0]
        self.y_res_ratio = self.window_size[1] / self.display_res[1]  

        self.screen = pygame.display.set_mode(self.window_size)
        self.display = pygame.Surface(self.display_res)

        self.clock = pygame.time.Clock()
        
        self.entities = {
            #player sprite and animations for player
            'player': load_image('assets\\entities\\player.png'),
            'player\\idle': Animation(load_images('assets\\entities\\player\\idle'), img_dur=6),
            'player\\run': Animation(load_images('assets\\entities\\player\\run'), img_dur=6)
        }

        self.tiles = {
            #grass tiles
            'grass': load_images('assets\\tiles\\grass'),
        }

        #everything else lol
        self.assets = {
            'background': load_image('assets\\shitty-background.png'),
            'chest': load_image('assets\\chests\\chest-regular.png'),
            #'cursor': load_image(),
        }
        
        self.tilemap = Tilemap(self, 'small')
        
        self.tilemap.generate_map()
        
        #can be attached to world size later if i feel like it lol
        self.world_limit_y_top = -500
        self.world_limit_y_bottom = 1000

        self.running = True
        self.pos = [self.display.get_width() / 2, self.display.get_height() / 2]
        self.movement = [False, False]

        self.scroll = [0, 0]

        self.delta_time = 0.0

        self.inventory = Inventory()
        self.player = Player(self, self.inventory, self.tilemap, self.pos)

    def run(self):
        #game loop
        while self.running:
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 10

            #locks the camera when world limit is reached
            if self.scroll[1] <= self.world_limit_y_top and (self.player.rect().centery - self.scroll[1]) < self.display.get_height() / 2:
                self.scroll[1] = self.world_limit_y_top
            elif self.scroll[1] >= self.world_limit_y_bottom and (self.player.rect().centery - self.scroll[1]) > self.display.get_height() / 2:
                self.scroll[1] = self.world_limit_y_bottom
            else:
                self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 10

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.display.fill((20, 100, 200))
            self.display.blit(pygame.transform.scale_by(self.assets['background'], 0.5), (0,0))

            self.player.update()
            self.tilemap.render_map(self.display, offset=render_scroll)
            self.player.render(self.display, offset=render_scroll)

            
            keys_pressed = pygame.key.get_pressed()

            #player clontrols
            if keys_pressed[K_a] or keys_pressed[K_d]:
                self.player.moving[0] = True
            else:
                self.player.moving[0] = False

            #player x axis logic
            if keys_pressed[K_a]:
                if self.player.collisions['down']:
                    self.player.velocity[0] = max(-self.player.grip + self.player.velocity[0], -self.player.speed)
                else:
                    self.player.velocity[0] = max(-self.player.air_grip + self.player.velocity[0], -self.player.speed) 
            if keys_pressed[K_d]:
                if self.player.collisions['down']:
                    self.player.velocity[0] = min(self.player.grip + self.player.velocity[0], self.player.speed)
                else:
                    self.player.velocity[0] = min(self.player.air_grip + self.player.velocity[0], self.player.speed)

            if pygame.mouse.get_pressed()[0]:
                self.player.mine_tile(offset=render_scroll)

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
                        print("poop")

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.delta_time = self.clock.tick(60) / 1000.0

if __name__ == '__main__':
    Game().run()
