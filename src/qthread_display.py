import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import liner_image
import numpy as np

from matplotlib import cm

class MatplotSignal(QWidget):
    def __init__(self, parent=None):
        super(MatplotSignal, self).__init__(parent)
        self.init_UI()
        self.plot_example()

    def init_UI(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.fig, self.axes = plt.subplots(8, 2, figsize=(10, 10))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        
    def plot_data(self, mtx):
        # print(mtx)
        # start_time = time.time()
        for i, ax in enumerate(self.axes.flat):
            ax.clear()
            ax.plot(mtx[i])
            ax.set_facecolor('black')

        self.canvas.draw()
        # end_time = time.time()
        # print("耗时: {:.2f}秒".format(end_time - start_time))


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
        print(signals.shape[1], len(self.axes))
        # assert(len(signals.shape) == 2)
        # assert(signals.shape[1] == 16)

        self.plot_data(signals)


class signal_thread(QWidget):
    def __init__(self, parent=None):
        super(MatplotSignal, self).__init__(parent)
        self.init_UI()
       
    def init_UI(self):
        self.signal_plot = MatplotSignal(None)
        self.signal_plot.setGeometry(QtCore.QRect(10, 10, 501, 481))
