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

class Bubble:
    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b

    def in_bubble(self, x, y):
        return ((x-self.x) ** 2) / (self.a ** 2) + ((y-self.y) ** 2) / (self.b ** 2) <= 1
    
    def __str__(self) -> str:
        return f"({self.x},{self.y}), rx:{self.a}, ry:{self.b}"

    def show(self):
        fig, ax = plt.subplots()

        ellipse = patches.Ellipse((self.x, self.y), self.a, self.b, angle=45, linewidth=2,
                                edgecolor='r', facecolor='none')
        ax.add_patch(ellipse)

        # print(self)
        plt.axis('scaled')
        plt.show()

# 
class Generator:
    def __init__(self, pattern, frequence):
        self.pattern = pattern
        self.data = np.zeros(len(frequence))
        self.frequence = frequence
        self.bubbles = list()

    def generate_bubble(self, rx, ry):
        center_x = int(random.uniform(3*rx, len(self.frequence)-3*rx))
        center_y = 0
        # theta = np.linspace(0, 2 * np.pi, 100)
        # x = center_x + rx * np.cos(theta)
        # y = center_y + ry * np.sin(theta)

        self.bubbles.append(Bubble(center_x, center_y, rx, ry))

    def generate_wave(self):
        return 1 / 4 * np.sin(self.frequence)

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
            for i in range(len(self.data)):
                if self.data < y:
                    seq[i] = 1
        elif self.pattern == FlowPattern.BUBBLE:
            pass

        elif self.pattern == FlowPattern.SHOT:
            pass

        else:
            pass
        
        return seq
    
    def show_wave(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, 100)
        ax.set_ylim(-20, 20)

        line, = ax.plot(self.frequence*3, 10*self.data)
        # 更新函数，用于生成波浪动画
        def update(frame):
            wave =  np.roll(10*self.data, frame)
            line.set_ydata(wave)
            return line,

        # 创建动画
        ani = animation.FuncAnimation(fig, update, frames=10, blit=True)
        plt.show()


    def show_bubble(self):
        fig, ax = plt.subplots()
        ax.set_xlim(0, 1000)
        ax.set_ylim(-125, 125)
        for bubble in self.bubbles:
            # bubble.show()
            ellipse = patches.Ellipse((bubble.x, bubble.y), bubble.a, bubble.y, angle=45, linewidth=2,
                                edgecolor='r', facecolor='none')
            ax.add_patch(ellipse)

        plt.axis('scaled')
        plt.show()
          

freq = np.linspace(0, 100, 1000)
gen = Generator(FlowPattern.WAVE, frequence=freq)
gen.generate()
gen.show_wave()