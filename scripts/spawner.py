import math

from .world import BiomeType
from .entities import *

class Spawner:
    """The spawner class. Handles spawning of entites."""
    def __init__(self, game, world, tilemap, player, entities):
        self.game = game
        self.world = world
        self.tilemap = tilemap
        self.player = player
        self.entities = entities
        self.dist_check_count = 0

    def spawn(self):
        slime_spawn_chance = random.randint(1, 200)
        if slime_spawn_chance == 100 and self.world.biome == BiomeType.OVERWORLD:
            print('spawn')
            self.entities.append(Slime(self.game, self.tilemap, 'green', 'slime', [self.player.pos[0] + random.choice([-self.game.display_res[0], self.game.display_res[0]]), self.world.surface_height*16 - 20]))
    
    def distance_check(self):

        if self.dist_check_count == 120:
            self.dist_check_count = -1
            for indx, e in enumerate(self.entities):
                dist = pygame.Vector2(self.player.entity_rect.center[0] - e.entity_rect.center[0], self.player.entity_rect.center[1] - e.entity_rect.center[1])
                magnitude = math.sqrt(dist[0]*dist[0] + dist[1]*dist[1])
                print(magnitude)
                if magnitude > self.game.display.get_width():
                    print('goteem')
                    self.game.ENTITIES.pop(indx)

        self.dist_check_count += 1
        
