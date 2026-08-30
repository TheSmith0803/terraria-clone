import pygame

class UI:
    def __init__(self, game, images):
        self.game = game
        self.images = images
        self.images[0].set_alpha(150)
        self.images[1].set_alpha(150)
        
        self.x_offset = 8
        self.y_offset = 10
        self.hotbar_origin = (self.x_offset, self.y_offset)
        self.hotbar_spacing = 35 #space between each inventory slot
        self.hotbar_positions = [x * self.hotbar_spacing for x in range(10)] #individual positions for hotbar

        self.amt_hearts = 5
        self.healthbar_spacing = 15
        self.healthbar_origin = (self.game.display.get_width() - self.healthbar_spacing * self.amt_hearts - 10, 10)
        self.healthbar_positions = [x * self.healthbar_spacing for x in range(self.amt_hearts)]

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
        #inventory = self.game.player.inventory

        #updates to world container inventories

    def render_hotbar(self, surf):
        slot_num = 1
        for pos in self.hotbar_positions:
            if self.selected + 1 == slot_num:
                surf.blit(pygame.transform.scale_by(self.images[1], 2), (self.hotbar_origin[0] + pos, self.hotbar_origin[1]))
            else:
                surf.blit(pygame.transform.scale_by(self.images[0], 2), (self.hotbar_origin[0] + pos, self.hotbar_origin[1]))
            font = pygame.font.SysFont('Consolas', 8)
            text_surf = font.render(str(slot_num), True, (255, 255, 255))
            text_rect = text_surf.get_rect()
            text_rect.topleft = (self.hotbar_origin[0] + pos + 3, self.hotbar_origin[1] + 3)
            surf.blit(text_surf, text_rect)
            slot_num += 1

    def render_healthbar(self, surf):
        self.healthbar_positions = [x * self.healthbar_spacing for x in range(self.amt_hearts)]
        self.healthbar_origin = (self.game.display.get_width() - self.healthbar_spacing * self.amt_hearts - 10, 10)
        health = self.game.player.health
        for index, pos in enumerate(self.healthbar_positions):
            heart_num = index + 1
            max_health = 20 * heart_num
            if health >= max_health or health > max_health - 10:
                surf.blit(self.images[2], (self.healthbar_origin[0] + pos, self.healthbar_origin[1]))
                continue
            elif health <= max_health - 10 and health > max_health - 20:
                surf.blit(self.images[3], (self.healthbar_origin[0] + pos, self.healthbar_origin[1]))
                continue
            elif health <= max_health - 20:
                surf.blit(self.images[4], (self.healthbar_origin[0] + pos, self.healthbar_origin[1]))

    #press tab to open players personal inventory
    def render_player_inventory(self, surf):
        pass
    
    #will render in the inventory of anything else (chests mostly)
    def render_misc_inventory(self, surf, inventory_obj):
        pass

        