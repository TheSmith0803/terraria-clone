import pygame

from .physics import swept_aabb
from .items import *

class PhysicsEntity:
    def __init__(self, game, tilemap, e_type, img, pos, size):
        self.game = game
        self.tilemap = tilemap
        self.pos = list(pos)
        self.img = img
        self.size = size
        self.velocity = [0, 0]
        self.moving = [False, False]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        self.type = e_type
        self.action = ''

        self.grip = 0.8
        self.air_grip = self.grip * 0.2
        self.friction = 0.8
        self.deadzone = .5
        self.speed = 50
        
        self.gravity = 3
        self.terminal_velocity = 160

        self.flip = False

    def rect(self):
        return pygame.FRect(*self.pos, *self.size)

    def set_animation(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.entities[self.type + "\\" + self.action].copy()

    def update(self):
        entity_rect = self.rect()        
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        self.velocity[1] = min(self.terminal_velocity, self.velocity[1] + self.gravity) #gravity
        
        prev_y_bottom = entity_rect.bottom

        self.pos[1] += self.velocity[1] * self.game.delta_time
        entity_rect.y = self.pos[1]


        #resolve y collisions
        for rect in self.tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.velocity[1] > 0 and prev_y_bottom <= rect.top:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                else:
                    self.collisions['down'] = False                    
                if self.velocity[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
                self.velocity[1] = 0
                break

            #variable to ensure that contact is only checked once
            touching_top = (entity_rect.bottom == rect.top 
                            and entity_rect.left < rect.right 
                            and entity_rect.right > rect.left)
            if touching_top:
                self.collisions['down'] = True
                self.pos[1] = entity_rect.y
                self.velocity[1] = 0
                break
            else:
                self.collisions['down'] = False

        self.pos[0] += self.velocity[0] * self.game.delta_time
        entity_rect.x = self.pos[0]

        #resolve x collisions
        for rect in self.tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.velocity[0] > 0:
                    entity_rect.right = rect.left 
                    self.collisions['right'] = True
                if self.velocity[0] < 0:
                    entity_rect.left = rect.right 
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
                self.velocity[0] = 0
                break

        #this is to make sure you dont bounce back in the other direction if friction is high
        #must happen after above collision calculations
        if not self.moving[0] and self.collisions['down']:
            if self.velocity[0] > 0:
                self.velocity[0] -= self.friction * (1 if self.velocity[0] > 0 else -1)
                if self.velocity[0] < 0:
                    self.velocity[0] = 0
            if self.velocity[0] < 0:
                self.velocity[0] -= self.friction * (1 if self.velocity[0] > 0 else -1)
                if self.velocity[0] > 0:
                    self.velocity[0] = 0

        if self.velocity[0] > 0:
            self.flip = False
        if self.velocity[0] < 0:
            self.flip = True
        
        #just in case you are somehow flipped right up against a wall
        if self.velocity[0] == 0 and self.collisions['left']:
            self.flip = True
        if self.velocity[1] == 0 and self.collisions['right']:
            self.flip = False
            
        self.animation.update()

        #print(self.collisions)
    def render(self, surf, offset=(0, 0)):
        screen_x = round(self.pos[0] - offset[0])
        screen_y = round(self.pos[1] - offset[1])
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (screen_x, screen_y))

class Player(PhysicsEntity):
    def __init__(self, game, inventory, ui, tilemap, pos):
        super().__init__(game, tilemap, 'player', game.entities['player'], pos, game.entities['player'].get_size())
        self.game = game
        self.inventory = inventory
        self.ui = ui
        self.tilemap = tilemap
        self.pos = pos
        self.world_mpos_raw = None #raw pixel location of cursor
        self.world_mpos_tile = None #for mining tiles and interacting with UI
        self.set_animation('idle')

        self.jump_power = 140
        self.health = 100
        self.dead = False
        
        self.fall_counter = 0

        #get origin of tile map in order to generate an accurate tilemap for the cursor
        self.tile_pos_origin = None
        self.tile_key_origin = None

        for coord in self.tilemap.tile_map.keys():
            self.tile_pos_origin = self.tilemap.tile_map[coord]['pos']
            self.tile_key_origin = coord.split(';')
            self.tile_key_origin[0] = int(self.tile_key_origin[0])
            self.tile_key_origin[1] = int(self.tile_key_origin[1])
            break

        #FIGURE OUT HOW TO USE THIS ^^^^^ TO MAP THE MOUSE POS TO THE TILE GRID LOL
    
    def mine_tile(self):
        item = self.tilemap.rmv_tile(self.world_mpos_tile)
        if item == None:
            return
        else:
            self.inventory.update(item)

    def place_tile(self):

        if self.inventory.contents[self.ui.selected][0].type == None:
            return
        else:
            placed = self.tilemap.insert_tile(self.world_mpos_tile, self.inventory.contents[self.ui.selected][0]) #place item in world
            if placed:
                self.inventory.contents[self.ui.selected][1] -= 1 #sub item from invetory
            else:
                return


    #maybe put all player based actions in here, like mine tile, switch tool, ect...or maybe all in update? idk lol
    def update_player_actions(self):
        pass

    def update(self, offset):
        
        mpos = list(pygame.mouse.get_pos())
        if mpos[0] != 0:
            mpos[0] /= self.game.x_res_ratio 
        if mpos[1] != 0:    
            mpos[1] /= self.game.y_res_ratio 
        
        self.world_mpos_raw = [mpos[0] + offset[0], mpos[1] + offset[1]]
        self.world_mpos_tile = [int((self.world_mpos_raw[0] - self.tile_pos_origin[0]) // self.tilemap.tile_size) + self.tile_key_origin[0], int((self.world_mpos_raw[1] - self.tile_pos_origin[1]) // self.tilemap.tile_size) + self.tile_key_origin[1]]


        if not self.collisions['down']:
            if self.velocity[1] == self.terminal_velocity:
                self.fall_counter += self.velocity[1]
            else:
                self.fall_counter = 0
        
        max_fall_dist = 12000
        self.fall_dmg_modifer = 0.001
        if self.fall_counter > max_fall_dist and self.collisions['down']:
            before = self.health
            self.health -= self.fall_counter * self.fall_dmg_modifer
            self.health = round(self.health)
            print(f'{before} - {self.fall_counter * self.fall_dmg_modifer} = {self.health}')
            self.fall_counter = 0

        if self.velocity[0] == 0:
            self.set_animation('idle')
        if self.velocity[0] != 0 and self.collisions['down']:
            self.set_animation('run')
        if not self.collisions['down']:
            self.animation.frame = 0

        if self.health <= 0:
            self.dead = True
        
        super().update()
        
    def render(self, surf, offset=(0, 0)):
        self.offset = offset
        super().render(surf, offset=offset)
        



class NPC(PhysicsEntity):
    pass

class Enemy(PhysicsEntity):
    pass