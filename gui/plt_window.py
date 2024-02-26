import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import liner_image
import numpy as np

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
        self.figure = plt.figure()
        self.ax1 = self.figure.add_subplot(8,2,1);
        self.ax2 = self.figure.add_subplot(8,2,2);
        self.ax3 = self.figure.add_subplot(8,2,3);
        self.ax4 = self.figure.add_subplot(8,2,4);
        self.ax5 = self.figure.add_subplot(8,2,5);
        self.ax6 = self.figure.add_subplot(8,2,6);
        self.ax7 = self.figure.add_subplot(8,2,7);
        self.ax8 = self.figure.add_subplot(8,2,8);
        self.ax9 = self.figure.add_subplot(8,2,9);
        self.ax10 = self.figure.add_subplot(8,2,10);
        self.ax11 = self.figure.add_subplot(8,2,11);
        self.ax12 = self.figure.add_subplot(8,2,12);
        self.ax13 = self.figure.add_subplot(8,2,13);
        self.ax14 = self.figure.add_subplot(8,2,14);
        self.ax15 = self.figure.add_subplot(8,2,15);
        self.ax16 = self.figure.add_subplot(8,2,16);
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.plot_image(None)

    def plot_image(self, signals):
        x = np.arange(1, 100)
        ax1 = self.figure.add_subplot(8, 2, 1);
        ax1.plot(x, x)

        ax2 = self.figure.add_subplot(8, 2, 2);
        ax2.plot(x, 2*x)

        ax3 = self.figure.add_subplot(8, 2, 3);
        ax3.plot(x, x*x)

        ax4 = self.figure.add_subplot(8, 2, 4);
        ax4.plot(x, x*x*x)


class MatplotImage2d(QWidget):
    def __init__(self, parent=None):
        super(MatplotImage2d, self).__init__(parent)
        self.figure = plt.figure(figsize=(3, 2), dpi=10)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.plot_example()

    def plot_example(self):
        ax = self.figure.add_subplot(111)
        mtx = np.zeros((250, 250))
        fibers = np.array([1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0])
        for j in (range(16)):
            points[j][2] =fibers[j]
        liner_image.imagine_layer(points, 125, mtx)
        ax.imshow(mtx, origin="lower", cmap='bwr')
        self.canvas.draw()


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.figure = plt.figure(figsize=(3, 2), dpi=10)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.plot_example()

    def plot_example(self):
        ax = self.figure.add_subplot(111)
        ax.plot([1, 2, 3, 4, 5], [2, 3, 5, 7, 11])  # Your plot data here
        ax.set_title('Matplotlib Plot')
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(0, 0, 100, 100)

        tab_widget = QTabWidget(self)

        # Create MatplotlibWidget and add it to a tab
        matplotlib_widget = MatplotlibWidget(self)
        tab_widget.addTab(matplotlib_widget, "Matplotlib Tab")

        self.setCentralWidget(tab_widget)

        # Plot example data on the MatplotlibWidget
        matplotlib_widget.plot_example()

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # mainWin = MainWindow()
    # mainWin.show()
    # sys.exit(app.exec_())
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 3, 1)  
    fig.add_subplot(232, facecolor="blue")  
    fig.add_subplot(233, facecolor="yellow")  
    fig.add_subplot(234, sharex=ax1) 
    fig.add_subplot(235, facecolor="red") 
    fig.add_subplot(236, facecolor="green")  
    plt.show()