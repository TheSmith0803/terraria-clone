import pygame
from pygame.locals import *

import math
import sys
import time
import os

from scripts.camera import Camera
from scripts.world import World
from scripts.tilemap import Tilemap
from scripts.entities import Player
from scripts.input import Input
from scripts.ui import UI
from scripts.inventory import Inventory
from scripts.utilities import load_image, load_images, Animation
from scripts.console import Console
from scripts.objects import InteractableObjects, Chest

class Game:
    def __init__(self):
        
        pygame.init()

        self.mixer = pygame.mixer.init()

        #these variables are for calculating cursor pos with scaling
        self.window_size = (800, 800)
        self.display_res = (self.window_size[0] / 2, self.window_size[1] / 2)
        self.x_res_ratio = self.window_size[0] / self.display_res[0]
        self.y_res_ratio = self.window_size[1] / self.display_res[1]

        self.screen = pygame.display.set_mode(self.window_size)
        self.display = pygame.Surface(self.display_res)
        
        self.font = pygame.font.SysFont('Consolas', 15)

        self.entities = {
            #player sprite and animations for player
            'player': load_image('assets\\entities\\player.png'),
            'player\\idle': Animation(load_images('assets\\entities\\player\\idle'), img_dur=6),
            'player\\run': Animation(load_images('assets\\entities\\player\\run'), img_dur=5)
        }

        self.inventory_assets = {
            'slot': load_image('assets\\ui\\inventory-slot.png'),
            'selected-slot': load_image('assets\\ui\\inventory-slot-selected.png')
        }

        self.tiles = {
            #grass tiles
            'grass': load_images('assets\\tiles\\grass', numeric=True),
            'dirt': load_images('assets\\tiles\\dirt', numeric=True)
        }
        
        #everything else lol
        self.assets = {
            'background': load_image('assets\\shitty-background.png'),
            'chest': load_image('assets\\chests\\chest-regular.png'),
            #'cursor': load_image(),
        }

        #figure out how to keep this visible but maintain aspect ratio
        self.assets['background'] = pygame.transform.scale_by(self.assets['background'], (self.display.get_width() / self.assets['background'].get_width(), self.display.get_height() / self.assets['background'].get_height()))

        
        self.tilemap = Tilemap(self)
        self.world = World(self, 'small', self.tilemap)
        self.world_size_pix = (self.world.map_size[0] * self.tilemap.tile_size, self.world.map_size[1] * self.tilemap.tile_size)
        print(self.world_size_pix)
        self.world.generate_world()

        self.running = True

        self.pos = [0, 0]
        self.movement = [False, False]

        self.scroll = [0, 0]
        self.delta_time  = 0.0

        
        self.ui = UI(self,[img for img in self.inventory_assets.values()])
        self.player_inventory = Inventory(self, self.ui)
        self.player_inventory.open = False #only for player inventory maybe?
        self.player = Player(self, self.player_inventory, self.ui, self.tilemap, self.pos)
        self.inputs = Input(self, self.player)
        self.entites = [] #will hold all active entities

        self.camera = Camera(self, self.display, self.scroll, self.world, self.player, self.entites)
        self.console = Console(self)
        #self.player.speed, self.player.grip, self.player.friction = 10, 10, 10
        self.clock = pygame.time.Clock()

    def _tile(self, coords: tuple) -> str: #maybe ill use this?
        return f"{coords[0]};{coords[1]}"

    def run(self):
        #game loop
        while self.running:
            #calculate delta time
            self.delta_time = self.clock.tick(60) / 1000.0
            #print(self.delta_time)
            #self.scroll = [int(self.scroll[0]), int(self.scroll[1])]
            self.player.update(offset=self.scroll)#player must be updated before camera to avoid funny jittery bisuiness

            if self.player.dead:
                print('YOU DIED')
                pygame.quit()
                sys.exit()
                self.running = False

            self.camera.update()#takes care of all the scroll code

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.display.fill((20, 100, 200))
            bg = self.display.blit(self.assets['background'], (-self.scroll[0] /3, -100))
            self.tilemap.render_map(self.display, offset=self.scroll)
            self.player.render(self.display, offset=self.scroll)

            self.inputs.update()
            for event in pygame.event.get():
                self.inputs.update_events(event=event)                
                self.ui.update(event=event)
                    
            #render ui stuff at the end of the fram
            font_surf = self.font.render(f'Player pos\nX: {int(self.player.pos[0]) // self.tilemap.tile_size}\nY: {-int(self.player.pos[1]) // self.tilemap.tile_size}', False, (255,255,255))
            self.display.blit(font_surf, (10, 45))
            self.ui.render_hotbar(self.display)
            self.player.inventory.render_contents(self.display)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()

            #fps timer
            #frame_ratio = 60 / (1/self.delta_time)
            
            #print(frame_ratio)
            pygame.display.set_caption(
                f"FPS: {1 / self.delta_time:.2f}"
            )
            #if not frame_ratio > 1:
            #this is really dumb and wont work on every system
            #print(self.player.velocity, self.player.pos)
            #print(self.player.velocity)
            #print(self.player.pos)
            
if __name__ == '__main__':
    Game().run()
