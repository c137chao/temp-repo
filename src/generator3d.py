from enum import Enum
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

class FlowPattern(Enum):
    LEVEL = 1
    WAVE  = 2
    BUBBLE = 3
    SHOT = 4

class Bubble3D:
    def __init__(self, x, y, z, a, b, c):
        self.x0 = x
        self.y0 = y
        self.z0 = z
        self.a = a
        self.b = b
        self.c = c

    def in_bubble(self, x, y, z):
        return ((x-self.x0) ** 2) / (self.a ** 2) + ((y-self.y0) ** 2) / (self.b ** 2) + ((z-self.z0) ** 2)/(self.b**2) <= 1
    
    def __str__(self) -> str:
        return f"(x-{self.x})^2  / {self.a}^2 + (y-{self.y})^2 / {self.b}^2 + (z-{self.z})^2 / {self.c}^2 = 1"

    def show(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # generate np array
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = self.x0 + self.a * np.outer(np.cos(u), np.sin(v))
        y = self.y0 + self.b * np.outer(np.sin(u), np.sin(v))
        z = self.z0 + self.c * np.outer(np.ones(np.size(u)), np.cos(v))


        ax.plot_surface(x, y, z, color='b', alpha=0.6)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # show
        plt.show()

# 
class Generator3D:
    def __init__(self, pattern, frequence):
        self.pattern = pattern
        self.data = np.zeros(len(frequence))
        self.frequence = frequence
        self.bubbles = list()

    def generate_bubble(self, rx, ry, rz):
        pass
        

    def generate_wave(self):
        pass
        # return 1 / 4 * np.sin(self.frequence)

    # frequence can be a np array
    # ex: np.linespace(start, stop, number)
    def generate(self):
        if self.pattern == FlowPattern.LEVEL:
            self.data = np.zeros(len(self.frequence))

        elif self.pattern == FlowPattern.WAVE:
            self.data = self.generate_wave()
        
        elif self.pattern == FlowPattern.BUBBLE:
            for i in range(10):
                self.generate_bubble(int(random.uniform(32, 128)), int(random.uniform(32, 96)))
        
        elif self.pattern == FlowPattern.SHOT:
            return None
        
        else:
            return None
    
        
    def get_sequence_at_point(self, x, y):
        seq = np.zeros(len(self.frequence))
        if self.pattern == FlowPattern.WAVE:
            pass
        elif self.pattern == FlowPattern.BUBBLE:
            pass

        elif self.pattern == FlowPattern.SHOT:
            pass

        else:
            pass
        
        return seq
    
    def show_wave(self):
        pass


    def show_bubble(self):
        pass
          