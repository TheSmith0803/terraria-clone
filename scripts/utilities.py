import os
import pygame

def load_image(path):
    img = pygame.image.load(path).convert()
    img.set_colorkey((0,0,0,0))
    return img

def load_images(path, numeric=False):
    imgs = []
    if numeric:
        sorted_paths = []
        for img in os.listdir(path):
            sorted_paths.append(img)
        
        sorted_paths.sort(key=lambda f: int(os.path.splitext(f)[0]))
        for img in sorted_paths:
            print(img)
            imgs.append(load_image(os.path.abspath(os.path.join(path, img))))

    else:
        for img in os.listdir(path):
            imgs.append(load_image(os.path.abspath(os.path.join(path, img))))w
        
    return imgs

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]

