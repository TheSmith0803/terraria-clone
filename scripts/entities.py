import pygame

from .physics import swept_aabb

class PhysicsEntity:
    def __init__(self, game, tilemap, img, pos, size):
        self.game = game
        self.tilemap = tilemap
        self.pos = list(pos)
        self.img = img
        self.size = size
        self.velocity = [0, 0]
        self.moving = [False, False]
        

        self.grip = 0.0700001
        self.air_grip = self.grip * 0.2
        self.friction = 0.0301
        self.deadzone = 0.05
        self.speed = 1.0
        
        self.gravity = 1.0

        self.flip = False

    def rect(self):
        return pygame.FRect(*self.pos, *self.size)


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

        #print(self.collisions)
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.img, self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))

class Player(PhysicsEntity):
    def __init__(self, game, tilemap, pos):
        super().__init__(game, tilemap, game.entities['player'], pos, game.entities['player'].get_size())
        self.game = game
        self.tilemap = tilemap
        self.pos = pos

    def mine_tile(self, offset=(0, 0)):
        mpos = list(pygame.mouse.get_pos())
        if mpos[0] != 0:
            mpos[0] /= self.game.x_res_ratio 
        if mpos[1] != 0:    
            mpos[1] /= self.game.y_res_ratio 

        remove_tile = None
        for tile in self.tilemap.tile_map:
            if (mpos[0] >= self.tilemap.tile_map[tile]['pos'][0] - offset[0] and
                mpos[1] >= self.tilemap.tile_map[tile]['pos'][1] - offset[1] and
                mpos[0] <= self.tilemap.tile_map[tile]['pos'][0] - offset[0] + self.tilemap.tile_size and
                mpos[1] <= self.tilemap.tile_map[tile]['pos'][1] - offset[1] + self.tilemap.tile_size and 
                self.tilemap.tile_map[tile]['pos'][1] < self.game.world_limit_y_bottom):
                remove_tile = tile

        if remove_tile != None:
            self.tilemap.tile_map.pop(remove_tile)

    #maybe put all player based actions in here, like mine tile, switch tool, ect...or maybe all in update? idk lol
    def update_player_actions(self):
        pass

    def set_action(self, action):
        pass

    def update(self):
        super().update()

    def render(self, surf, offset=(0, 0)):
        self.offset = offset
        super().render(surf, offset=offset)
        



class NPC(PhysicsEntity):
    pass

class Enemy(PhysicsEntity):
    pass