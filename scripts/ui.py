import pygame

class UI:
    def __init__(self, game, inventory, images, init_pos):
        self.images = images
        self.pos = init_pos
        self.spacing = 25 #space between each inventory slot
        self.positions = [x * self.spacing for x in range(10)]

    def update(self):
        #updates to player inventory

        self.game.player.inventory
        #updates to world container inventories

    def render_inventory(self, surf):
        slot_num = 1
        for pos in self.positions:
            slot_rect = surf.blit(pygame.transform.scale_by(self.images[0], 1.25), (self.pos[0] + pos, self.pos[1]))
            font = pygame.font.SysFont('Consolas', 8)
            text_surf = font.render(str(slot_num), True, (255, 255, 255))
            text_rect = text_surf.get_rect()
            text_rect.topleft = (self.pos[0] + pos + 1, self.pos[1] + 1)
            surf.blit(text_surf, text_rect)
            slot_num += 1

        