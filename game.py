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
from scripts.background import Background
from scripts.utilities import load_image, load_images, Animation
from scripts.console import Console
from scripts.objects import InteractableObjects, Chest
from scripts.debugger import Debugger
from scripts.items import *

class Game:
    def __init__(self):
        
        pygame.init()

        self.mixer = pygame.mixer.init()

        #these variables are for calculating cursor pos with scaling
        self.window_size = (800, 800)
        self.display_res = (self.window_size[0] // 2, self.window_size[1] // 2)
        self.x_res_ratio = self.window_size[0] / self.display_res[0]
        self.y_res_ratio = self.window_size[1] / self.display_res[1]

        self.screen = pygame.display.set_mode(self.window_size)
        self.display = pygame.Surface(self.display_res)
        
        self.font = pygame.font.SysFont('Consolas', 15)

        self.entities = {
            #player sprite and animations for player
            'player': load_image('assets\\entities\\newplayer.png'),
            'player\\idle': Animation(load_images('assets\\entities\\player\\idle'), img_dur=6),
            'player\\run': Animation(load_images('assets\\entities\\player\\run'), img_dur=5)
        }

        self.ui_assets = {
            'slot': load_image('assets\\ui\\inventory-slot.png'),
            'selected-slot': load_image('assets\\ui\\inventory-slot-selected.png'),
            'full-heart': load_image('assets\\ui\\full-heart.png'),
            'half-heart': load_image('assets\\ui\\half-heart.png'),
            'empty-heart': load_image('assets\\ui\\empty-heart.png'),
        }

        self.tiles = {
            #grass tiles
            BlockType.GRASS: load_images('assets\\tiles\\grass', numeric=True),
            BlockType.DIRT: load_images('assets\\tiles\\dirt', numeric=True)
        }
        
        #everything else lol
        self.containers = {
            'chest': load_image('assets\\chests\\chest-regular.png'),
            #'cursor': load_image(),
        }

        self.weapons = {
            'wood sword': load_image('assets\\weapons\\wood-sword.png')
        }

        self.backgrounds = {
            'forest': {
                'pine-background': load_image('assets\\background\\forest\\pine-background.png'),
                'pine-midground': load_image('assets\\background\\forest\\pine-midground.png'),
                'pine-foreground': load_image('assets\\background\\forest\\pine-foreground.png'),
                'parallax-mod-x': 8,
                'parallax-mod-y': 2,
            },
        }
        
        self.tilemap = Tilemap(self)
        self.world = World(self, 'debug', self.tilemap)
        self.world_size_pix = (self.world.map_size[0] * self.tilemap.tile_size, self.world.map_size[1] * self.tilemap.tile_size)

        if os.path.exists("map.dig"):
            print("loading world")
            self.world.load_world()
        else:
            print('generating world')
            self.world.generate_world()

        self.running = True

        self.pos = [(self.world.map_size[0] // 2) * self.tilemap.tile_size, (self.world.surface_height*16)-20] #surface hieght in terms of tiles so x16 needed, also -16 so not spawn in ground (character is 16 pix tall)
        self.movement = [False, False]

        self.scroll = [0, 0]
        
        self.ui = UI(self,[img for img in self.ui_assets.values()])
        self.background = Background(self, 'forest')
        self.player = Player(self, self.ui, self.tilemap, self.pos)
        self.inputs = Input(self, self.tilemap, self.player)
        self.entites = [] #will hold all active entities

        self.camera = Camera(self, self.display, self.scroll, self.world, self.player, self.entites)
        self.console = Console(self)
        self.debugger = Debugger(self)
        #self.player.speed, self.player.grip, self.player.friction = 10, 10, 10
        self.clock = pygame.time.Clock()
        
    def run(self):
        #game loop
        angle = 0
        while self.running:
            #frame ticker for stuffs sometimes
            #calculate delta time
            self.delta_time = self.clock.tick(60) / 1000.0
            self.player.update(offset=self.scroll)#player must be updated before camera to avoid funny jittery bisuiness

            #goofy player death
            if self.player.dead:
                print('YOU DIED')
                pygame.quit()
                sys.exit()
                self.running = False

            self.camera.update()#takes care of all the scroll code

            self.display.fill((min(max(0, 20 + self.player.pos[1] // 6 - 400), 255),
                               min(max(0, 100 + self.player.pos[1] // 6 - 400), 255),
                               min(max(0, 200 + self.player.pos[1] // 6 - 400), 255)))
            self.background.render_background()
            self.tilemap.render_map(self.display, offset=self.scroll)
            self.player.render(self.display, offset=self.scroll)

            self.inputs.update()
            for event in pygame.event.get():
                self.inputs.update_events(event=event)    
                self.ui.update(event=event)
                    
            #render ui stuff at the end of the fram
            font_surf = self.font.render(f'Player pos\nX: {int(self.player.pos[0]) // self.tilemap.tile_size}\nY: {int(self.player.pos[1]) // self.tilemap.tile_size}', False, (100,100,255))
            self.display.blit(font_surf, (10, 45))
            self.ui.render_hotbar(self.display)
            self.ui.render_healthbar(self.display)
            self.player.inventory.render_contents(self.display)
            angle+=1
            angle%=359
            self.display.blit(pygame.transform.rotate(pygame.transform.scale_by(self.weapons['wood sword'], 1), angle), (self.display.get_width()//2-6, self.display.get_height()//2 - 6))

            #self.debugger.render_collision_boxes()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            #print(self.delta_time)
            pygame.display.set_caption(
                f"FPS: {self.clock.get_fps():.1f}"
            )
            
            

            #print(self.player.velocity, self.player.pos)
            #print(self.player.velocity)
            #print(self.player.pos)
            
if __name__ == '__main__':
    Game().run()
