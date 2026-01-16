import pygame

from .physics import swept_aabb

class PhysicsEntity:
    def __init__(self, game, tilemap, img, pos, size):
        self.game = game
        self.tilemap = tilemap
        self.pos = list(pos)
        self.size = size
        self.img = img
        self.velocity = [0, 0]
        self.moving = [False, False]

        self.friction = 0.001
        self.deadzone = 0.05
        
        self.gravity = 1.0

        self.flip = False

    def rect(self):
        return pygame.FRect(*self.pos, *self.size)


    def update(self):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}
        entity_rect = self.rect()

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
        
        px, py = entity_rect.center
        vx, vy = self.velocity

        earliest_time = 1.0
        hit_normal = (0, 0)
        nx, ny = 0.0, 0.0

        for tile in self.minkowski_tiles:
            nx, ny, entry_time = swept_aabb(px, py, vx, vy, tile)
            if entry_time < earliest_time:
                earliest_time = entry_time
                hit_normal = (nx, ny)

        self.pos[0] += self.velocity[0] * earliest_time
        self.pos[1] += self.velocity[1] * earliest_time

        remaining = 1.0 - earliest_time
        dot = vx * nx + vy * ny
        self.velocity[0] -= dot * nx
        self.velocity[1] -= dot * ny


        self.pos[0] += self.velocity[0] * remaining
        self.pos[1] += self.velocity[1] * remaining

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
        pass

class NPC(PhysicsEntity):
    pass

class Enemy(PhysicsEntity):
    pass