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
        self.set_action('idle')

        self.grip = 0.0700001
        self.air_grip = self.grip * 0.2
        self.friction = 0.0301
        self.deadzone = 0.05
        self.speed = 1.0
        
        self.gravity = 1.0

        self.flip = False

    def rect(self):
        return pygame.FRect(*self.pos, *self.size)

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.entities[self.type + "\\" + self.action].copy()

    def update(self):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        entity_rect = self.rect()

        self.velocity[1] = min(5, self.velocity[1] + (0.01 * self.gravity)) #gravity
        
        if not self.moving[0]:
            if abs(self.velocity[0]) < self.deadzone:
                self.velocity[0] = 0
            else:
                self.velocity[0] -= self.friction * (1 if self.velocity[0] > 0 else -1)

        prev_y = entity_rect.bottom
        self.velocity[1] = min(4, self.velocity[1] + 0.1) #gravity
        self.pos[1] += self.velocity[1]
        entity_rect.y = self.pos[1]
        
        #resolve y collisions
        for rect in self.tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.velocity[1] > 0 and prev_y <= rect.top:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if self.velocity[1] < 0:
                    entity_rect.top = rect.bottom 
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
                self.velocity[1] = 0
                break

        self.pos[0] += self.velocity[0]
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
        
        if self.velocity[0] > 0:
            self.flip = False
        if self.velocity[0] < 0:
            self.flip = True

        self.animation.update()

        #print(self.collisions)
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, inventory, tilemap, pos):
        super().__init__(game, tilemap, 'player', game.entities['player'], pos, game.entities['player'].get_size())
        self.game = game
        self.inventory = inventory
        self.tilemap = tilemap
        self.pos = pos

    def mine_tile(self, offset=(0, 0)):
        mpos = list(pygame.mouse.get_pos())
        if mpos[0] != 0:
            mpos[0] /= self.game.x_res_ratio 
        if mpos[1] != 0:    
            mpos[1] /= self.game.y_res_ratio 

        #iterating over every tile every time you click iz bad, 
        #make it deterministic by div mpos by tilepos and see if that tile exists
        #may need to divide offset by 
        mpos_grid = ['','']
        offset_grid = [offset[0] // self.tilemap.tile_size, offset[1] // self.tilemap.tile_size]
        remove_tile = None

        mpos_grid[0] = mpos[0] // self.tilemap.tile_size
        mpos_grid[1] = mpos[1] // self.tilemap.tile_size
        
        for tile in self.tilemap.tile_map:
            if (mpos[0] >= self.tilemap.tile_map[tile]['pos'][0] - offset[0] and
                mpos[1] >= self.tilemap.tile_map[tile]['pos'][1] - offset[1] and
                mpos[0] <= self.tilemap.tile_map[tile]['pos'][0] - offset[0] + self.tilemap.tile_size and
                mpos[1] <= self.tilemap.tile_map[tile]['pos'][1] - offset[1] + self.tilemap.tile_size and 
                self.tilemap.tile_map[tile]['pos'][1] < self.game.world_limit_y_bottom):
                remove_tile = tile
        #put item into inventory (will drop it in the world later)
        

        if remove_tile != None:
            self.inventory.update(Item('grass', self.game.tiles[self.tilemap.tile_map[remove_tile]['type']][self.tilemap.tile_map[remove_tile]['variant']], stackable=True))
            self.tilemap.tile_map.pop(remove_tile)
            for i in self.inventory.contents:
                print(f'type: {i[0].type} ---- amt {i[1]}')

    #maybe put all player based actions in here, like mine tile, switch tool, ect...or maybe all in update? idk lol
    def update_player_actions(self):
        pass

    def update(self):
        

        
        if self.velocity[0] == 0:
            self.set_action('idle')
        if self.velocity[0] != 0 and self.collisions['down']:
            self.animation.img_duration = min(self.animation.img_duration, self.animation.img_duration * abs(self.velocity[0] * 20))
            self.set_action('run')
        if not self.collisions['down']:
            self.animation.frame = 0
        
        super().update()
        

    def render(self, surf, offset=(0, 0)):
        self.offset = offset
        super().render(surf, offset=offset)
        



class NPC(PhysicsEntity):
    pass

class Enemy(PhysicsEntity):
    pass