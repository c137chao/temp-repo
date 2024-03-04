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



import sys
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPixmap, QColor

class GrayscaleImage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Grayscale Image")
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 800, 600)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(100)  # 每100毫秒更新一次图像

    def update_image(self):
        matrix = np.random.randint(0, 256, (400, 600), dtype=np.uint8)  # 随机生成一个400x600的二维矩阵
        img = self.matrix_to_image(matrix)
        pixmap = QPixmap.fromImage(img)
        self.label.setPixmap(pixmap)

    def matrix_to_image(self, matrix):
        height, width = matrix.shape
        img = QImage(width, height, QImage.Format_RGB32)

        for y in range(height):
            for x in range(width):
                value = matrix[y, x]
                color = QColor(value, 0, 255 - value)  # 根据灰度值设置红蓝颜色
                img.setPixelColor(x, y, color)

        return img

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GrayscaleImage()
    window.show()
    sys.exit(app.exec_())
