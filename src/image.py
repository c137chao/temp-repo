import numpy as np
import krige_impl as kg
import fibers
import random
import util

from matplotlib import pyplot as plt

x_range = 250
y_range = 250

rand_bubble_cnt = 10

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
            return fibers.FiberState.GAS
        
        if util.all_in_water(signals):
            return fibers.FiberState.WATER
        
        if util.max_gas_length(signals) > fibers.BUBBLE_MAX_FRAMES:
            return fibers.FiberState.SLUG
        
        else:
            return fibers.FiberState.BUBBLE
        
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

           
    #    switch(self.compress_singals())