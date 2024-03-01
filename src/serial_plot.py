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

'''
    plot signal waves widget
    it set 8*2 subfigure layout and plot signals on it when recv 
'''
import time
import threading
import pyqtgraph as pg

class MatplotSignalDemo(QWidget):
    def __init__(self, parent=None):
        super(MatplotSignalDemo, self).__init__(parent)
        self.init_UI()
        # self.plot_example()

    def init_UI(self): 
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.plot_widgets = []
        for _ in range(16):
            plot_widget = pg.PlotWidget()
            layout.addWidget(plot_widget)
            self.plot_widgets.append(plot_widget)

        # 生成初始数据
        self.data = [np.random.normal(size=1024) for _ in range(16)]
        self.x = np.arange(1024)
        
        # 绘制初始波形
        self.curves = [plot_widget.plot(self.x, data) for plot_widget, data in zip(self.plot_widgets, self.data)]

    def plot_data(self, mtx):
        for curve, data in zip(self.curves, mtx):
            data = data[:1024]
            curve.setData(self.x, data)

    def plot_example(self):
        # Update the data with new random values
        data = [np.random.randn(100) for _ in range(16)]

        # Plot the updated data
        self.plot_data(data)

    '''
        plot signals waves on signale groupbox in label_2

        parameters
        --------------
        signals: signals is n * 16 numpy array
                 n maybe 600, because program will process data every 10 frames

    '''
    def update_image(self, signals):
        signals = signals.reshape(16, len(signals)>>4)
        # signals must be n * 16 numppy arrays
        # print(signals.shape[1], len(self.axes))
        # assert(len(signals.shape) == 2)
        # assert(signals.shape[1] == 16)
        self.plot_data(signals)
        

# class MatplotSignal(QWidget):
#     def __init__(self, parent=None):
#         super(MatplotSignal, self).__init__(parent)
#         self.init_UI()
#         self.plot_example()

#     def init_UI(self):
#         layout = QVBoxLayout(self)
#         self.setLayout(layout)

#         self.fig, self.axes = plt.subplots(16, 1, figsize=(15, 15))
#         self.canvas = FigureCanvas(self.fig)
#         layout.addWidget(self.canvas)

#         # self.fig_left, self.axes_left = plt.subplots(8, 1, figsize=(10, 5))
#         # self.fig_right, self.axes_right = plt.subplots(8, 1, figsize=(10, 5))
#         # self.canvas_left = FigureCanvas(self.fig_left)
#         # self.canvas_right = FigureCanvas(self.fig_right)

#         # layout.addWidget(self.canvas_left)
#         # layout.addWidget(self.canvas_right)

#     def plot_data(self, mtx):
#         # print(mtx)
#         start_time = time.time()
#         for i, ax in enumerate(self.axes):
#             ax.clear()
#             ax.set_ylim(-5, 5)

#             ax.plot(mtx[i])
#             ax.set_facecolor('black')

#         self.canvas.draw()

#         end_time = time.time()
#         print("耗时: {:.2f}秒".format(end_time - start_time))

#     def plot_left(self, mtx):
#         for i, ax in enumerate(self.axes_left):
#             ax.clear()
#             ax.set_ylim(-5, 5)
#             ax.plot(mtx[i])
#             ax.set_facecolor('black')

#         self.canvas_left.draw()


#     def plot_right(self, mtx):
#         for i, ax in enumerate(self.axes_right):
#             ax.clear()
#             ax.plot(mtx[i])
#             ax.set_facecolor('black')

#         self.canvas_right.draw()
        

#     def plot_example(self):
#         # Update the data with new random values
#         data = [np.random.randn(100) for _ in range(16)]

#         # Plot the updated data
#         self.plot_data(data)

#     '''
#         plot signals waves on signale groupbox in label_2

#         parameters
#         --------------
#         signals: signals is n * 16 numpy array
#                  n maybe 600, because program will process data every 10 frames

#     '''
#     def update_image(self, signals):
#         signals = signals.reshape(16, len(signals)>>4)
#         # signals must be n * 16 numppy arrays
#         # print(signals.shape[1], len(self.axes))
#         # assert(len(signals.shape) == 2)
#         # assert(signals.shape[1] == 16)
#         self.plot_data(signals)
        
#         # self.plot_left(signals[:8,])
#         # self.plot_right(signals[8:,])
#         # my_thread = threading.Thread(target=self.plot_left, args=(signals[:8,]))
#         # my_thread.start()


import krige_impl
import util
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QPainter, QImage

x_range = 250
y_range = 250
range_step = 1

gridx = np.arange(0.0, x_range, range_step)
gridy = np.arange(0.0, y_range, range_step)

'''

'''
class MatplotSliceDemo(QWidget):
    def __init__(self, parent=None):
        super(MatplotSliceDemo, self).__init__(parent)
        
        self.image_label = QLabel()
        self.all_water = np.zeros((250, 250), dtype=float)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

    def plot_data(self, mtx):
        print(mtx.shape, sys.getsizeof(mtx.data))
        mtx = mtx.astype(np.uint8)
        qimage = QImage(mtx.data, 250, 250, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)


    def init_UI(self):
        self.label = QWidget.QLabel(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)


    def plot_example(self):
        mtx = np.zeros((250, 250))
        fibers = np.array([255,255,255,255,255,255,0,0,0,0,0,0,0,0,0,0])
        for j in (range(16)):
            points[j][2] =fibers[j]
        kg = krige_impl.Kriging(points[:,0], points[:,1], points[:,2], nlags=10)
        mtx, _ = kg.execute('grid', gridx, gridy)
        # util.set_range_uint8(mtx)
        
        self.plot_data(mtx)

    def update_image(self, frame):
        points[:, 2] = frame
        kg = krige_impl.Kriging(points[:,0], points[:,1], points[:,2], nlags=10)
        mtx, _ = kg.execute('grid', gridx, gridy)

        self.plot_data(mtx)


def test_matplotSliceDemo():
    app = QApplication(sys.argv)
    ex = MatplotSliceDemo()
    start = time.perf_counter()

    ex.plot_example()
    ex.show() 
    for _ in range(100):
        np_array = np.random.randint(255, size=(100, 100, 3), dtype=np.uint8)
        # ex.plot_data(np_array)

    end = time.perf_counter()
    print("runtime:", end-start)
    sys.exit(app.exec_())     

# test_matplotSliceDemo()

class MatplotSlice(QWidget):
    def __init__(self, parent=None):
        super(MatplotSlice, self).__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)

        layout.addWidget(self.canvas)
        self.plot_example()


    def plot_example(self):
        mtx = np.zeros((250, 250))
        fibers = np.array([1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0])
        points[:,2] = fibers
        kg = krige_impl.Kriging(points[:,0], points[:,1], points[:,2], nlags=10)
        mtx, _ = kg.execute('grid', gridx, gridy)
        self.ax.imshow(mtx, cmap='bwr')
        print('get image')
        self.canvas.draw()


    def plot_image(self, frames, type = None):
        mtx = np.zeros(x_range, y_range)
        # image on data
        for frame in frames:
            points[:, 2] = frame
            kg = krige_impl.Kriging(points[:0], points[:1], points[:2], nlags=10)
            mtx, _ = kg.execute('grid', gridx, gridy)
            util.set_range(mtx)


def test_matplotSlice():
    app = QApplication(sys.argv)
    ex = MatplotSlice()
    for _ in range(10):
        ex.plot_example()
        ex.show()
    sys.exit(app.exec_())     

# test_matplotSlice()

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

    
    def plot_image(self, Z):
        self.ax.plot_surface(self.X, self.Y, Z, cmap=cm.Blues)

        # selfax.set_box_aspect((1,4,1)) # 设定坐标轴的长宽高比例
        # ax.grid(False) 

        self.ax.xaxis.set_label_text('X')
        self.ax.yaxis.set_label_text('Y')
        self.ax.zaxis.set_label_text('Z')

        plt.show()