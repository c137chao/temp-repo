import numpy as np
import krige_impl as kg
import random
import util

from matplotlib import pyplot as plt

x_range = 250
y_range = 250

image_size = 250

rand_bubble_cnt = 10
BUBBLE_MAX_FRAMES = 10

class FiberState:
    GAS = 0
    WATER = 1
    SLUG = 2
    BUBBLE = 3

def compress_singals(signals):
        if util.all_in_gas(signals):
            return FiberState.GAS
        
        if util.all_in_water(signals):
            return FiberState.WATER
        
        if util.max_gas_length(signals) > BUBBLE_MAX_FRAMES:
            return FiberState.SLUG
        
        else:
            return FiberState.BUBBLE
        

def draw_a_random_bubble_on(mtx, x, y, r):
    cell = image_size // 25
    if x < cell or x > image_size - cell:
        return
    if y < cell or image_size - cell:
        return
        
    for i in range(x - r, x + r):
        for j in range(y-r, y+r):
            if (i-x)**2 + (j-y)**2 <= r**2:
                mtx[j, i] = 1
     
def draw_bubbles(mtx, bubbles):
        for bubble in bubbles:
            draw_a_random_bubble_on(bubble[0], bubble[1])
            for i in range(rand_bubble_cnt):
                draw_a_random_bubble_on(random.randint(-200,200), bubble[1]+random.randint(-10,10))

def build_image(all_signals, mtx):
    index = 0
    image_type = FiberState.NONE

    all_bubbles = []
    for i in range(len(all_signals)): 
        state = compress_singals(all_signals[i])
        if state > image_type:
            image_type = state
        if state == FiberState.BUBBLE:
            all_bubbles.append(util.points[i][:1])
    

    draw_bubbles(mtx, all_bubbles)

class FibersImage:
    def __init__(self, size):
        self.edge = size 
        self.bubbles = []
        self.slug_length = 0
        self.mtx = np.zeros((size, size))
    
    def get_image_matrix(self):
        return self.mtx
    
    def draw_a_random_bubble_on(self, x, y, r):
        cell = self.edgs // 25
        if x < cell or x > self.edge - cell:
            return
        if y < cell or y > self.edge - cell:
            return
        
        for i in range(x - r, x + r):
            for j in range(y-r, y+r):
                if (i-x)**2 + (j-y)**2 <= r**2:
                    self.mtx[j, i] = 1
     
    def draw_bubbles(self):
        for bubble in self.bubbles:
            self.draw_a_random_bubble_on(bubble[0], bubble[1])
            # TODO
            for i in range(rand_bubble_cnt):
                self.draw_a_random_bubble_on(random.randint(-200,200), bubble[1]+random.randint(-10,10))
       
    def compress_singals(signals):
        if util.all_in_gas(signals):
            return FiberState.GAS
        
        if util.all_in_water(signals):
            return FiberState.WATER
        
        if util.max_gas_length(signals) > BUBBLE_MAX_FRAMES:
            return FiberState.SLUG
        
        else:
            return FiberState.BUBBLE
        
    # build image according signals. signals is a sequence with 0 or 1   
    def build_image(self, all_signals):
       index = 0
       image_type = fibers.FiberState.NONE
       for i in range(len(all_signals)): 
           state = self.compress_singals(all_signals[i])
           if state > image_type:
               image_type = state
           if state == fibers.FiberState.BUBBLE:
               self.bubbles.append(fibers.points[i][:1])
       
       # check and image 


       self.draw_bubbles()

           
      # switch(self.compress_singals())