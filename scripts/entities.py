import pygame

from .physics import swept_aabb
from .items import *
from .tilemap import AUTOTILE_MAP

TILE_OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

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
        self.set_animation('idle')

        self.grip = 0.0700001
        self.air_grip = self.grip * 0.2
        self.friction = 0.0301
        self.deadzone = 0.05
        self.speed = 1.0
        
        self.gravity = 1.0

        self.flip = False

    def rect(self):
        return pygame.FRect(*self.pos, *self.size)

    def set_animation(self, action):
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
    def __init__(self, game, inventory, ui, tilemap, pos):
        super().__init__(game, tilemap, 'player', game.entities['player'], pos, game.entities['player'].get_size())
        self.game = game
        self.inventory = inventory
        self.ui = ui
        self.tilemap = tilemap
        self.pos = pos
        self.world_mpos_raw = None #raw pixel location of cursor
        self.world_mpos_tile = None #for mining tiles and interacting with UI

        #get origin of tile map in order to generate an accurate tilemap for the cursor
        self.tile_pos_origin = None
        self.tile_key_origin = None
        done = False

        for coord in self.tilemap.tile_map.keys():
            self.tile_pos_origin = self.tilemap.tile_map[coord]['pos']
            self.tile_key_origin = coord.split(';')
            self.tile_key_origin[0] = int(self.tile_key_origin[0])
            self.tile_key_origin[1] = int(self.tile_key_origin[1])
            print(self.tile_pos_origin, self.tile_key_origin)
            break

        #FIGURE OUT HOW TO USE THIS ^^^^^ TO MAP THE MOUSE POS TO THE TILE GRID LOL
    
    def mine_tile(self):

        #print(self.world_mpos_tile)

        

        remove_tile = None
        if f'{str(self.world_mpos_tile[0])};{str(self.world_mpos_tile[1])}' in self.tilemap.tile_map.keys():
                remove_tile = f'{str(self.world_mpos_tile[0])};{str(self.world_mpos_tile[1])}'

        #put item into inventory (will drop it in the world later)
        if remove_tile != None:
            self.inventory.update(Item(self.tilemap.tile_map[remove_tile]['type'], self.game.tiles[self.tilemap.tile_map[remove_tile]['type']][self.tilemap.tile_map[remove_tile]['variant']], stackable=True))
            self.tilemap.tile_map.pop(remove_tile)
            for i in self.inventory.contents:
                print(f'type: {i[0].type} ---- amt {i[1]}')

            adjacent_tiles = []
            for tileoffset in TILE_OFFSETS:
                
                curr_tile = (self.world_mpos_tile[0] + tileoffset[0], self.world_mpos_tile[1] + tileoffset[1])
                if f'{curr_tile[0]};{curr_tile[1]}' in self.tilemap.tile_map:
                    adjacent_tiles.append(curr_tile)

            
            if not adjacent_tiles:
                return

            for tile in adjacent_tiles:
                check_tiles = []
                for tile_offset in TILE_OFFSETS:
                    curr_tile = (tile[0] + tile_offset[0], tile[1] + tile_offset[1])
                    if f'{curr_tile[0]};{curr_tile[1]}' in self.tilemap.tile_map:
                        check_tiles.append(tile_offset)
                
                check_tiles = tuple(sorted(check_tiles))

                for autotile in AUTOTILE_MAP.keys():
                    if check_tiles == autotile:
                        self.tilemap.tile_map[f'{tile[0]};{tile[1]}']['variant'] = AUTOTILE_MAP[autotile]




    
    #this will use the raw world coords to check wether or not the cursor is overlapping with a
    #removable object in the scene
    def mine_object(self):
        pass

    def place_tile(self):

        place_tile = None
        offset_tile = None
        direction = None
        """
        for adjacent_tile in TILE_OFFSETS:
            if (f'{str(self.world_mpos_tile[0])};{str(self.world_mpos_tile[1])}' not in self.tilemap.tile_map.keys() and
                f'{self.world_mpos_tile[0] + adjacent_tile[0]};{self.world_mpos_tile[1] + adjacent_tile[1]}' in self.tilemap.tile_map.keys()):
                place_tile =  f'{str(self.world_mpos_tile[0])};{str(self.world_mpos_tile[1])}'
                offset_tile = f'{self.world_mpos_tile[0] + adjacent_tile[0]};{self.world_mpos_tile[1] + adjacent_tile[1]}'
                direction = tile_placement_offsets.index(adjacent_tile)
                print(direction)
                break
        """

                
        
        #get selected ui slot, check if there is a block to place, if not do nothing
        if place_tile != None:

            selected_slot = self.ui.selected
            item = self.inventory.contents[selected_slot][0]

            #USE THESE TILE POSITIONS TO CALCULATE THE NEW POSITIONS FOR PLACED TILES, SORRY THIS IS A MESS - PAST ETHAN
            reference_tile_str = next(iter(self.tilemap.tile_map.keys())) #gets first value in tilemap
            reference_tile_int = [int(reference_tile_str.split(';')[0]), int(reference_tile_str.split(';')[1])]
            place_tile_int = [int(place_tile.split(';')[0]), int(place_tile.split(';')[1])]
            difference = [place_tile_int[0]]
            if item.type == None:
                return
            
            #this will eventually be made to be 'blocks'
            if item.type == 'grass':
                self.inventory.contents[selected_slot][1] -= 1
                
                self.tilemap.tile_map[place_tile] = {'basetype': 'block', 'type': item.type, 'variant': 0, 'pos': (tile_placement_offsets[direction][0] * -self.tilemap.tile_size, tile_placement_offsets[direction][1] * -self.tilemap.tile_size)} #figure out how to get this tile pos lol
            
            #another conditional here for non block types (objects)
            #if item.type == 'object':
            #   do a thing



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


        if self.velocity[0] == 0:
            self.set_animation('idle')
        if self.velocity[0] != 0 and self.collisions['down']:
            self.set_animation('run')
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