import pygame


class Debugger:
    def __init__(self, game):
        self.game = game

    def render_collision_boxes(self):
        for rect in self.game.tilemap.physics_rects_around(self.game.player.pos):
            rect.x -= self.game.scroll[0]
            rect.y -= self.game.scroll[1]
            pygame.draw.rect(self.game.display, (255, 0, 0), rect)