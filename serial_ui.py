import sys
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel

class MatrixImageViewer(QMainWindow):
    def __init__(self, rows, cols):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.image_label = QLabel()
        layout.addWidget(self.image_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateMatrix)
        self.timer.start(10)  # 每秒更新一次图像

        self.updateMatrix()

    def updateMatrix(self):
        # 随机生成一个大小为250x250的矩阵
        matrix_data = np.random.randint(0, 256, size=(self.rows, self.cols), dtype=np.uint8)

        # 创建一个QImage以显示矩阵
        q_image = QImage(matrix_data, self.cols, self.rows, self.cols, QImage.Format_Grayscale8)

        # 创建一个QPixmap以显示QImage
        q_pixmap = QPixmap.fromImage(q_image)

        # 在QLabel上显示QPixmap
        self.image_label.setPixmap(q_pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    rows, cols = 250, 250  # 设置矩阵的大小为250x250
    viewer = MatrixImageViewer(rows, cols)
    viewer.show()

    sys.exit(app.exec_())