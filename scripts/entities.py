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

        self.grip = 0.07
        self.friction = 0.03
        self.deadzone = 0.05
        
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
    def render(self, surf):
        surf.blit(pygame.transform.flip(self.img, self.flip, False), self.pos)

class Player(PhysicsEntity):
    def __init__(self, game, tilemap, pos):
        super().__init__(game, tilemap, game.entities['player'], pos, game.entities['player'].get_size())

class NPC(PhysicsEntity):
    pass

class Enemy(PhysicsEntity):
    pass