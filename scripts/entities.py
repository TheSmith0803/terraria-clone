import pygame

class PhysicsEntity:
    def __init__(self, game, tilemap, img, pos, size):
        self.game = game
        self.tilemap = tilemap
        self.pos = list(pos)
        self.size = size
        self.img = img
        self.velocity = [0, 0]
        self.moving = [False, False]

        self.friction = 0.03
        self.deadzone = 0.05
        
        self.gravity = 1

        self.flip = False

    def rect(self):
        return pygame.Rect(*self.pos, *self.size)


    def update(self):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        entity_rect = self.rect()
        
        if not self.moving[0]:
            if abs(self.velocity[0]) < self.deadzone:
                self.velocity[0] = 0
            else:
                self.velocity[0] -= self.friction * (1 if self.velocity[0] > 0 else -1)

        self.minkowski_tiles = []
        if self.tilemap.physics_rects_around(entity_rect.center):
            for tile in self.tilemap.physics_rects_around(entity_rect.center):
                entity_rect = self.rect()
                minkowski_size = [tile.w + entity_rect.w, tile.h + entity_rect.h]
                minkowski_rect = pygame.Rect((tile.topleft[0] - entity_rect.w / 2, tile.topleft[1] - entity_rect.h / 2), minkowski_size)
                self.minkowski_tiles.append(minkowski_rect)

        self.velocity[1] = min(5, self.velocity[1] + 0.1) 
                
        if self.minkowski_tiles:
            for rect in self.minkowski_tiles:
                #update palyers position
                entity_rect = self.rect()
                
                if entity_rect.center[0] > rect.left and  entity_rect.center[0] < rect.right and self.velocity[0] > 0:
                    self.collisions['right'] = True
                    self.velocity[0] = 0
                if entity_rect.center[0] > rect.right and entity_rect.center[0] < rect.left and self.velocity[0] < 0:
                    self.collisions['left'] = True
                    self.velocity[0] = 0

                self.pos[0] += self.velocity[0]
                

                if entity_rect.center[1] <= rect.top and self.velocity[1] > 0:
                    self.collisions['bottom'] = True
                    self.velocity[1] = 0
                if entity_rect.center[1] < rect.bottom and self.velocity[1] < 0:
                    self.collisions['top'] = True
                    self.velocity[1] = 0
                
                self.pos[1] += self.velocity[1]
        else:
            self.pos[0] += self.velocity[0]
            self.pos[1] += self.velocity[1]
        

        if self.velocity[0] > 0:
            self.flip = False
        if self.velocity[0] < 0:
            self.flip = True

        print(self.collisions)

    def render(self, surf):
        surf.blit(pygame.transform.flip(self.img, self.flip, False), self.pos)

class Player(PhysicsEntity):
    def __init__(self):
        pass

class NPC(PhysicsEntity):
    pass

class Enemy(PhysicsEntity):
    pass