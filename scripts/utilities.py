import os
import pygame

def load_image(path):
    img = pygame.image.load(path).convert()
    #img.set_colorkey((0,0,0))
    return img

def load_images(path):
    imgs = []
    for img in os.listdir(path):
        print(img)
        imgs.append(load_image(os.path.abspath(os.path.join(path, img))))
        
    return imgs
