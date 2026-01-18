import os
import pygame

def load_image(path):
    img = pygame.image.load(path).convert()
    img.set_colorkey((0,0,0))
    return img

def load_images(path):
    imgs = []
    for img in os.listdir(path):
        print(img)
        imgs.append(load_image(os.path.abspath(os.path.join(path, img))))
        
    return imgs

class Animation:
    def __init__(self, sprite_sheet, sprite_res=(16, 16), img_dur=5, loop=True):
        self.sheet = sprite_sheet
        self.res = sprite_res
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.sheet, self.sheet, self.res, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

