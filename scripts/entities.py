import pygame

class PhysicsEntity:
    def __init__(self, game, tilemap, e_type, pos, size):
        self.game = game
        self.tilemap = tilemap
        self.pos = list(pos)
        self.size = size
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

    def render(self, surf):
        surf.blit(self.game.entities['player'], self.pos)

class Player(PhysicsEntity):
    def __init__(self):
        pass

class NPC(PhysicsEntity):
    pass

class Enemy(PhysicsEntity):
    pass