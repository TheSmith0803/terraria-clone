import pygame

from .physics import swept_aabb
from .items import *
from .inventory import Inventory
from .data.enemy_data import *

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
        self.is_enemy = False
        self.action = ''

        self.acceleration = 1
        self.air_acceleration = self.acceleration * 0.2
        self.friction = 1
        self.deadzone = 5
        self.speed = 50
        
        self.gravity = 5
        self.terminal_velocity = 160

        self.flip = False

    def rect(self):
        return pygame.FRect(*self.pos, *self.size)

    def set_animation(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.entity_sprites[self.type + "\\" + self.action].copy()

    def update(self):
        self.entity_rect = self.rect()        
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        self.velocity[1] = min(self.terminal_velocity, self.velocity[1] + self.gravity) #gravity
        
        prev_y_bottom = self.entity_rect.bottom

        self.pos[1] += self.velocity[1] * self.game.delta_time
        self.entity_rect.y = self.pos[1]


        #resolve y collisions
        for rect in self.tilemap.physics_rects_around(self.pos, self.size):
            if self.entity_rect.colliderect(rect):
                if self.velocity[1] > 0 and prev_y_bottom <= rect.top:
                    self.entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                else:
                    self.collisions['down'] = False                    
                if self.velocity[1] < 0:
                    self.entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = self.entity_rect.y
                self.velocity[1] = 0
                break

            #variable to ensure that contact is only checked once
            touching_top = (self.entity_rect.bottom == rect.top 
                            and self.entity_rect.left < rect.right 
                            and self.entity_rect.right > rect.left)
            if touching_top:
                self.collisions['down'] = True
                self.pos[1] = self.entity_rect.y
                self.velocity[1] = 0
                break
            else:
                self.collisions['down'] = False

        self.pos[0] += self.velocity[0] * self.game.delta_time
        self.entity_rect.x = self.pos[0]

        #resolve x collisions
        for rect in self.tilemap.physics_rects_around(self.pos, self.size):
            if self.entity_rect.colliderect(rect):
                if self.velocity[0] > 0:
                    self.entity_rect.right = rect.left 
                    self.collisions['right'] = True
                if self.velocity[0] < 0:
                    self.entity_rect.left = rect.right 
                    self.collisions['left'] = True
                self.pos[0] = self.entity_rect.x
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
    def __init__(self, game, ui, tilemap, pos):
        super().__init__(game, tilemap, 'player', game.entity_sprites['player'], pos, game.entity_sprites['player'].get_size())
        self.game = game
        self.ui = ui
        self.inventory = Inventory(game, self.ui)
        self.inventory.open = False
        self.tilemap = tilemap
        self.pos = pos
        self.world_mpos_raw = None #raw pixel location of cursor
        self.world_mpos_tile = None #for mining tiles and interacting with UI
        self.set_animation('idle')

        self.jump_power = 150

        self.health_cap = self.ui.amt_hearts * 20 #each heart worth 20 health
        self.health = 100
        self.health_regen_rate = 90
        self.frames = 1 #for spacing out heath regen
        self.dead = False
        
        self.fall_counter = 0
        self.fall_damage = True

        #get origin of tile map in order to generate an accurate tilemap for the cursor
        self.tile_pos_origin = None
        self.tile_key_origin = None

        for coord in self.tilemap:
            self.tile_pos_origin = coord
            break
    
    def process_action_lmb(self):
        if self.inventory.selected_item.category in (None, ItemCategory.TOOL, ItemCategory.BLOCK, ItemCategory.ORE):
            self.mine_tile()
        if self.inventory.selected_item.category is ItemCategory.WEAPON:
            self.attack()
            
    # LMB FUNCTIONS
    def attack(self):
        print('attack!')

    def mine_tile(self):
        item = self.tilemap.rmv_tile((int(self.world_mpos_tile[0]), int(self.world_mpos_tile[1])))
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
        #health regen
        if self.health < self.health_cap:
            self.frames += 1
            if self.frames % self.health_regen_rate == 0: # 90 frames (every second and a half)
                self.health += 1
                print(self.health)

        if self.frames > 100000:
            self.frames = 1
        
        mpos = list(pygame.mouse.get_pos())
        if mpos[0] != 0:
            mpos[0] /= self.game.x_res_ratio 
        if mpos[1] != 0:    
            mpos[1] /= self.game.y_res_ratio 
        
        self.world_mpos_raw = [mpos[0] + offset[0], mpos[1] + offset[1]]
        self.world_mpos_tile = [self.world_mpos_raw[0] // self.tilemap.tile_size, self.world_mpos_raw[1] // self.tilemap.tile_size]

        if not self.collisions['down']:
            if self.velocity[1] == self.terminal_velocity:
                self.fall_counter += self.velocity[1]
            else:
                self.fall_counter = 0
        
        if self.fall_damage:
            max_fall_dist = 6000
            self.fall_dmg_modifer = 0.0022
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
        
        if abs(self.velocity[0]) < self.deadzone and not self.moving[0]:
            self.velocity[0] = 0
        if abs(self.velocity[1]) < self.deadzone and not self.moving[1]:
            self.velocity[1] = 0

        if self.health < 0:
            self.health = 0
        
        super().update()

        #collisions with entity
        for e in self.game.ENTITIES:
            if e.is_enemy and self.entity_rect.colliderect(e.rect()):
                push_dir = pygame.Vector2(self.entity_rect.center[0] - e.entity_rect.center[0], self.entity_rect.center[1] - e.entity_rect.center[1])
                push_dir.normalize()
                push_dir *= e.pushback
                
                #push player away from entity and visa versa
                self.velocity[0] = push_dir[0]
                e.velocity[0] = -push_dir[0]
                if not self.collisions['down']:
                    self.velocity[1] = push_dir[1]
                if not e.collisions['down']:
                    e.velocity[1] = -push_dir[1]
                if e.damage_cooldown == 0:
                    self.health -= e.damage
                    e.damage_cooldown = e.damage_wait_time

        
    def render(self, surf, offset=(0, 0)):
        self.offset = offset
        super().render(surf, offset=offset)

class NPC(PhysicsEntity):
    def __init__(self, game, tilemap, e_name, inventory, pos):
        super().__init__(game, tilemap, e_name, game.entity_sprites[e_name], pos, game.entity_sprites[e_name].get_size())
        self.game = game
        self.tilemap = tilemap
        self.entity_name = e_name
        self.inventory = inventory
        self.pos = pos
        

class Slime(PhysicsEntity):
    def __init__(self, game, tilemap, color, e_name, pos, inventory=None):
        super().__init__(game, tilemap, f"{color}_{e_name}", game.entity_sprites[f"{color}_{e_name}"], pos, game.entity_sprites[f"{color}_{e_name}"].get_size())
        self.set_animation('idle')
        self.game = game
        self.tilemap = tilemap
        self.entity_name = f"{color}_{e_name}"

        self.damage_cooldown = 0
        self.damage_wait_time = ENEMY_DATA[self.entity_name]['attack_cooldownn']

        self.is_enemy = True
        #super fun enemy attributes
        self.health   = ENEMY_DATA[self.entity_name]['health']
        self.damage   = ENEMY_DATA[self.entity_name]['damage']
        self.pushback = ENEMY_DATA[self.entity_name]['pushback']

        if inventory is not None:
            self.inventory = inventory

        self.pos = pos

    def update(self):
        super().update()

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1
        if self.damage_cooldown < 0:
            self.damage_cooldown = 0

        if not self.collisions['down']:
            self.animation.frame = 0

    def render(self, surf, offset=(0, 0)):
        print(self.pos[0] - offset[0] < self.game.display.get_width())
        print(self.pos[1] - offset[1] < self.game.display.get_height())
        print()
        if (self.pos[0] - offset[0] < self.game.display.get_width() and 
            self.pos[0] - offset[0] + self.size[0] > 0 and
            self.pos[1] - offset[1] < self.game.display.get_height() and
            self.pos[1] - offset[1] + self.size[1] > 0):
            super().render(surf, (int(offset[0]),int(offset[1])))
        else:
            pass
