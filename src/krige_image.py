import numpy as np
import krige_impl

from matplotlib import pyplot as plt

import random

x_range = 250
y_range = 250


water_mtx = np.zeros((250, 250))
for x, y in range(water_mtx.shape):
    r = (x-125)**2 + (y-125)**2
    if r > 125**2:
        water_mtx[x, y] = 0.5
        
water_mtx[0, 0] = 1


def draw_a_random_bubble_on(mtx, x, y, r):
    if x > 240 or x < 10:
        return
    if y > 240 or y < 10:
        return 
    # r = random.randint(3, 7)
    for i in range(x-r, x+r):
        for j in range(y-r, y+r):
            if (i-x)**2 + (j-y)**2 <= r**2:
                mtx[j, i] = 1


def image_wave(signals):
   range_step = 1
   gridx = np.arange(0.0, x_range, range_step)
   gridy = np.arange(0.0, y_range, range_step)
 
   fig = plt.figure('frame')

   mtx = np.zeros((250, 250))
#    if signals.any():
       
   for i in range(signals.shape[1]):
      for j in (range(16)):
        fibers.points[j][2] = signals[j][i]
      if not np.any(fibers.points[:,2]):
        mtx = water_mtx
      else:
        # print(points)
        kg = krige_impl.Kriging(fibers.points[:,0], fibers.points[:,1], fibers.points[:,2], nlags=10)
        mtx, _ = kg.execute('grid', gridx, gridy)

      # slow display
      ax1 = fig.add_subplot(1, 1, 1)
      ax1.imshow(mtx, origin="lower", cmap='bwr')
      ax1.scatter(fibers.points[:,0], fibers.points[:,1], c=fibers.points[:,2])
      # plt.show()
      plt.pause(0.01)
      fig.clf()


class KrigeImage:
    def __init__(self):
       self.matrix = np.zeros((250, 250))
    
    def get_image_matrix(self):
        return self.matrix

    def generate(fibers):
        pass
    # ...

    

    def draw_a_random_bubble_on(self, x, y, r):
        if x > 240 or x < 10:
            return
        if y > 240 or y < 10:
            return 
        # r = random.randint(3, 7)
        for i in range(x-r, x+r):
            for j in range(y-r, y+r):
                if (i-x)**2 + (j-y)**2 <= r**2:
                    self.mtx[j, i] = 1

    def draw_bubbles(self, bubbles):
        for bubble in bubbles:
            self.draw_a_random_bubble_on(bubble[0], bubble[1])
            for i in range(10):
                self.draw_a_random_bubble_on(random.randint(-200, 200), bubble[1]+random.randint(-10,10))
    
    

