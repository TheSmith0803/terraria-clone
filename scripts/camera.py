
class Camera:
    def __init__(self, game, display, scroll, world, player, entities):
        self.display = display
        self.game = game
        self.scroll = scroll
        self.world = world
        self.player = player
        self.entities = entities

    def update(self):
        #locks the camera when world limit is reached
            if self.scroll[0] <= self.world.lh_world_lim and (self.player.rect().centerx - self.scroll[0]) < self.display.get_width() / 2:
                self.scroll[0] = self.world.lh_world_lim 
            elif self.scroll[0] >= self.world.rh_world_lim and (self.player.rect().centerx - self.scroll[0]) > self.display.get_width() / 2:
                self.scroll[0] = self.world.rh_world_lim
            else:
                self.scroll[0] = (self.player.rect().centerx - self.display.get_width() / 2)
            
            #locks the camera when world limit is reached
            if self.scroll[1] <= self.world.upr_world_lim and (self.player.rect().centery - self.scroll[1]) < self.display.get_height() / 2:
                self.scroll[1] = self.world.upr_world_lim
            elif self.scroll[1] >= self.world.lwr_world_lim and (self.player.rect().centery - self.scroll[1]) > self.display.get_height() / 2:
                self.scroll[1] = self.world.lwr_world_lim
            else:
                self.scroll[1] = (self.player.rect().centery - self.display.get_height() / 2)