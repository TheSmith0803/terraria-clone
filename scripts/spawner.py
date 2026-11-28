from .world import BiomeType
from .entities import *

class Spawner:
    """The spawner class. Handles spawning of entites."""
    def __init__(self, game):

        self.dist_check_count = 0

    def spawn(self):
        slime_spawn_chance = random.randint(1, 1500)
        if slime_spawn_chance == 750 and self.game.world.biome == BiomeType.OVERWORLD:
            print('spawn')
            self.game.ENTITIES.append(Slime(self, self.tilemap, 'green', 'slime', [self.player.pos[0] + random.choice([-400, 400]), self.world.surface_height*16 - 20]))
    
    def distance_check(self):

        if self.dist_check_count == 300:
            self.dist_check_count = -1
            for e in self.game.ENTITIES:
                dist = pygame.Vector2()
        
