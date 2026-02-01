import pygame

class UI:
    def __init__(self, game, images, init_pos):
        self.game = game
        self.images = images
        for img in self.images:
            img.set_alpha(150)
        self.pos = init_pos
        self.spacing = 35 #space between each inventory slot
        self.hotbar_positions = [x * self.spacing for x in range(10)] #individual positions for hotbar

        self.selected = 0

    def update(self, event):
        #update hotbar selection
        if event.type == pygame.MOUSEWHEEL:
            self.selected = (self.selected + event.y) % 10
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.selected = 0
            if event.key == pygame.K_2:
                self.selected = 1
            if event.key == pygame.K_3:
                self.selected = 2
            if event.key == pygame.K_4:
                self.selected = 3
            if event.key == pygame.K_5:
                self.selected = 4
            if event.key == pygame.K_6:
                self.selected = 5
            if event.key == pygame.K_7:
                self.selected = 6
            if event.key == pygame.K_8:
                self.selected = 7
            if event.key == pygame.K_9:
                self.selected = 8
            if event.key == pygame.K_0:
                self.selected = 9
        #updates to player inventory

        inventory = self.game.player.inventory
        #updates to world container inventories

    def render_inventory(self, surf):
        slot_num = 1
        for pos in self.hotbar_positions:
            if self.selected + 1 == slot_num:
                surf.blit(pygame.transform.scale_by(self.images[1], 2), (self.pos[0] + pos, self.pos[1]))
            else:
                surf.blit(pygame.transform.scale_by(self.images[0], 2), (self.pos[0] + pos, self.pos[1]))
            font = pygame.font.SysFont('Consolas', 8)
            text_surf = font.render(str(slot_num), True, (255, 255, 255))
            text_rect = text_surf.get_rect()
            text_rect.topleft = (self.pos[0] + pos + 3, self.pos[1] + 3)
            surf.blit(text_surf, text_rect)
            slot_num += 1

        