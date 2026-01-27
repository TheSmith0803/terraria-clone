import pygame
from .items import Item

class Inventory:
    def __init__(self):

        self.size = 10
        self.contents = []

        self.stack_size = 64

        for i in range(10):
            self.contents.append([Item(None, None), 0])

    def update(self, new_item):
        #add new item to inventory
        for index, item in enumerate(self.contents):
            if item[0].type == None:
                self.contents[index] = [new_item, 1]
                break
            elif item[0].stackable and item[0].type == self.contents[index][0].type and item[1] < self.stack_size:
                self.contents[index][1] += 1
                break
            
