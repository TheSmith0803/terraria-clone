import pygame
import os, math

#will only apply to entities and projectiles
def swept_aabb(px, py, vx, vy, minkowski_box):

    #find the distance between the objects on the near and far sides for x and y
    x_inv_entry, y_inv_entry = float(), float()
    x_inv_exit, y_inv_exit   = float(), float()

    if vx > 0.0:
        x_inv_entry = minkowski_box.x - px
        x_inv_exit = (minkowski_box.x + minkowski_box.w) - px
    else:
        x_inv_entry = (minkowski_box.x + minkowski_box.w) - px
        x_inv_exit = minkowski_box.x - px
    
    if vy > 0.0:
        y_inv_entry = minkowski_box.y - py
        y_inv_exit = (minkowski_box.y + minkowski_box.h) - py 
    else:
        y_inv_entry = (minkowski_box.y + minkowski_box.h) - py
        y_inv_exit = minkowski_box.y - py

    #find time of collision and time of leaving for each axis (if statement is to prevent divide by zero)
    x_entry, y_entry = float(), float()
    x_exit, y_exit   = float(), float()

    if vx == 0.0:
        x_entry = float("-inf")
        x_exit = float('inf')
    else:
        x_entry = x_inv_entry / vx
        x_exit = x_inv_exit / vx
    
    if vy == 0.0:
        y_entry = float("-inf")
        y_exit = float('inf')
    else:
        y_entry = y_inv_entry / vy
        y_exit = y_inv_exit / vy

    x_entry = min(x_entry, x_exit)
    x_exit  = max(x_entry, x_exit)

    y_entry = min(y_entry, y_exit)
    y_exit  = max(y_entry, y_exit)

    #find earliest and latest times of collisionfloat
    entry_time = max(x_entry, y_entry)
    exit_time = min(x_exit, y_exit)

    #if no collision occurs
    if (entry_time > exit_time or 
        entry_time < 0.0 or 
        entry_time > 1.0):
        normalx = 0.0
        normaly = 0.0
        return normalx, normaly, 1.0
    #if a collision does occur
    else:

        if x_entry > y_entry:
            normalx = -1.0 if vx > 0 else 1.0
            normaly = 0.0
        else:
            normalx = 0.0
            normaly = -1.0 if vy > 0 else 1.0
        
        #this will need to be handled, 
        #as variable assignment by reference isnt possible (dumb python)
        return normalx, normaly, entry_time

