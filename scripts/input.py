import pygame
from pygame.locals import *
import sys


class Input:
    def __init__(self, game, player):
        self.game = game
        self.player = player

    def update(self):
        keys_pressed = pygame.key.get_pressed()
        pygame.key.get_just_pressed

        #player clontrols
        if keys_pressed[K_a] or keys_pressed[K_d]:
            self.player.moving[0] = True
        else:
            self.player.moving[0] = False

        #player x axis logic
        if keys_pressed[K_a]:
            if self.player.collisions['down']:
                self.player.velocity[0] = max(-self.player.grip + self.player.velocity[0], -self.player.speed)
            else:
                self.player.velocity[0] = max(-self.player.air_grip + self.player.velocity[0], -self.player.speed)
        if keys_pressed[K_d]:
            if self.player.collisions['down']:
                self.player.velocity[0] = min(self.player.grip + self.player.velocity[0], self.player.speed)
            else:
                self.player.velocity[0] = min(self.player.air_grip + self.player.velocity[0], self.player.speed)

        #player mouse logic if interacting with inventories
        if self.player.inventory.open:
            if pygame.mouse.get_just_pressed()[0]:
                pass
            if pygame.mouse.get_just_pressed()[2]:
                pass
        else:
            if pygame.mouse.get_pressed()[0]:
                self.player.mine_tile()
            if pygame.mouse.get_pressed()[2]:
                self.player.place_tile()

    def update_events(self, event):
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                self.game.running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                self.running = False

            if event.key == K_w:
                self.player.velocity[1] = -self.player.jump_power
                print("poop")
            
            if event.key == K_TAB:
                self.player.inventory.open = not self.player.inventory.open

            if event.key == K_o:
                self.tilemap.save()
            