import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSizePolicy
from PyQt5.QtCore import QTimer

class MultiPlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建一个窗口部件作为主窗口的中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建一个垂直布局
        layout = QVBoxLayout(central_widget)

        # 初始化x数据
        self.x = np.linspace(0, 10, 1000)

        # 创建一个列表用于存储所有的曲线
        self.curves = []

        # 创建十六个PlotWidget并添加到布局中
        for i in range(16):
            plot_widget = pg.PlotWidget()
            plot_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            layout.addWidget(plot_widget)

            # 初始化y数据
            y = np.sin(self.x + i)
            # 在每个plot_widget中添加一个曲线
            curve = plot_widget.plot(self.x, y)
            self.curves.append(curve)

        # 创建一个定时器用于定期更新波形
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(50)  # 每50毫秒更新一次

    def update_plots(self):
        for i in range(16):
            # 更新y数据
            y = np.roll(np.sin(self.x + i), -1)  # 将y数据向左移动一个单位
            y[-1] = np.sin(self.x[-1] + 0.1 + i)  # 计算新的最后一个数据点

            # 更新曲线数据
            self.curves[i].setData(self.x, y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MultiPlotWindow()
    window.setWindowTitle('Multi-plot Real-time Plot')
    window.show()
    sys.exit(app.exec_())
