import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import liner_image
import numpy as np

from matplotlib import cm


points = np.array(
    [
       [165, 215, 0],
       [85, 195, 0], 
       [185, 185, 0], 
       [145, 175, 0], 
       [105, 165, 0], 
       [65, 155, 0], 
       [205, 145, 0],
       [165, 135, 0], 
       [85, 115, 0], 
       [45, 105, 0], 
       [185, 95, 0], 
       [145, 85, 0], 
       [105, 75, 0],
       [65, 65, 0],
       [165, 55, 0],
       [85, 35, 0],
    ])

class MatplotSignal(QWidget):
    def __init__(self, parent=None):
        super(MatplotSignal, self).__init__(parent)

        self.fig, self.axes = plt.subplot(8, 2, figsize=(10, 4))
        for ax in self.axes:
            ax.set_facecolor('black')  # 设置背景颜色为黑色
            ax.grid(True, color='white', linestyle='dotted') 
            ax.set_xlim(0, 10240)  # 设置x轴范围
            ax.set_ylim(0, 5)  # 设置y轴范围

            self.axs.append(ax)


        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.plot_image(None)

    def plot_image(self, signals):
        plt.figure(facecolor='black', edgecolor='green')

        x = np.arange(0, 1024)
        y = np.random.randint(5, 6, size=1024)
        for ax in self.axs:
            ax.plot(x, y, color='green')

import krige_impl

class MatplotImage2d(QWidget):
    def __init__(self, parent=None):
        super(MatplotImage2d, self).__init__(parent)
        self.fig, self.ax = plt.subplots(figsize=(500, 400))
        self.figure = plt.figure(figsize=(3, 2), dpi=10)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.plot_example(None)

    def plot_example(self, data, bbox=None):
        ax = self.figure.add_subplot(111)
        if bbox:
            pass
        x_range = 250
        y_range = 250
        range_step = 1
        gridx = np.arange(0.0, x_range, range_step) #三个参数的意思：范围0.0 - 0.6 ，每隔0.1划分一个网格
        gridy = np.arange(0.0, y_range, range_step)
        mtx = np.zeros((250, 250))
        fibers = np.array([1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0])
        for j in (range(16)):
            points[j][2] =fibers[j]
        kg = krige_impl.Kriging(points[:,0], points[:,1], points[:,2], nlags=10,)
        mtx, _ = kg.execute('grid', gridx, gridy)
        for i in range(0, 250):
            for j in range(0, 250):
                if i**2+j**2>(125**2):
                    mtx[i, j] = 0.5
        ax.imshow(mtx, origin="lower", cmap='bwr')
        self.canvas.draw()

class MatplotImage3d(QWidget):
    def __init__(self, parent=None):
        super(MatplotImage3d, self).__init__(parent)
        self.xlen = 250
        self.ylen = 64
        x = np.arange(1,  self.xlen+1)
        y = np.arange(1,  self.ylen+1)
        self.X, self.Y = np.meshgrid(x, y)
        
        self.fig, self.ax = plt.subplots(subplot_kw={"projection": "3d"})   
        self.canvas = FigureCanvas(self.fig)
        self.ax.set(xticklabels=[],
           yticklabels=[],
           zticklabels=[])
        self.ax.set_xlim(0,  self.xlen)
        self.ax.set_ylim(0,  self.ylen)
        self.ax.set_zlim(0, 250)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    
    def plot_example(self, Z):
        self.ax.plot_surface(self.X, self.Y, Z, cmap=cm.Blues)

        # selfax.set_box_aspect((1,4,1)) # 设定坐标轴的长宽高比例
        # ax.grid(False) 

        self.ax.xaxis.set_label_text('X')
        self.ax.yaxis.set_label_text('Y')
        self.ax.zaxis.set_label_text('Z')

        plt.show()