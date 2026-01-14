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
        
        self.gravity = 1.0

        self.flip = False

    def rect(self):
        return pygame.FRect(*self.pos, *self.size)


    def update(self):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        entity_rect = self.rect()
        self.last_frame_x = entity_rect.centerx
        self.last_frame_y = entity_rect.centery

        self.velocity[1] = min(5, self.velocity[1] + (0.1 * self.gravity)) #gravity
        
        if not self.moving[0]:
            if abs(self.velocity[0]) < self.deadzone:
                self.velocity[0] = 0
            else:
                self.velocity[0] -= self.friction * (1 if self.velocity[0] > 0 else -1)

        self.minkowski_tiles = []
        if self.tilemap.physics_rects_around(entity_rect.center):
            for tile in self.tilemap.physics_rects_around(entity_rect.center):
                minkowski_size = [tile.w + entity_rect.w, tile.h + entity_rect.h]
                minkowski_rect = pygame.FRect((tile.topleft[0] - entity_rect.w / 2, tile.topleft[1] - entity_rect.h / 2), minkowski_size)
                self.minkowski_tiles.append(minkowski_rect)

        self.pos[0] += self.velocity[0]
        entity_rect = self.rect()
        if self.minkowski_tiles:
            for rect in self.minkowski_tiles:
                #x axis
                if (entity_rect.centerx > rect.left and 
                    self.last_frame_x < rect.left and 
                    entity_rect.centery > rect.top and
                    entity_rect.centery < rect.bottom and
                    self.velocity[0] > 0):

                    self.collisions['right'] = True
                    self.pos[0] = self.last_frame_x - (self.img.get_width() / 2)
                    self.velocity[0] = 0
                    break

                if (entity_rect.centerx < rect.right and 
                    self.last_frame_x > rect.right and 
                    entity_rect.centery > rect.top and
                    entity_rect.centery < rect.bottom and
                    self.velocity[0] < 0):

                    self.collisions['left'] = True
                    self.pos[0] = self.last_frame_x - (self.img.get_width() / 2)
                    self.velocity[0] = 0
                    break

        self.last_frame_y = entity_rect.centery

        self.pos[1] += self.velocity[1]
        entity_rect = self.rect()
        if self.minkowski_tiles:
            for rect in self.minkowski_tiles:

                if (entity_rect.centery > rect.top and
                    self.last_frame_y < rect.top and 
                    entity_rect.centerx > rect.left and
                     entity_rect.centerx < rect.right and
                    self.velocity[1] > 0):

                    self.collisions['down'] = True
                    self.pos[1] = self.last_frame_y - (self.img.get_height() / 2)
                    self.velocity[1] = 0
                    break

                if (entity_rect.centery < rect.bottom and
                    self.last_frame_y > rect.bottom and 
                    entity_rect.centerx > rect.left and
                     entity_rect.centerx < rect.right and
                    self.velocity[1] < 0):

                    self.collisions['up'] = True
                    self.pos[1] = self.last_frame_y - (self.img.get_height() / 2)
                    self.velocity[1] = 0
                    break

        if self.velocity[0] > 0:
            self.flip = False
        if self.velocity[0] < 0:
            self.flip = True

    def render(self, surf):
        surf.blit(pygame.transform.flip(self.img, self.flip, False), self.pos)

class Player(PhysicsEntity):
    def __init__(self):
        pass

class NPC(PhysicsEntity):
    pass

class Enemy(PhysicsEntity):
    pass