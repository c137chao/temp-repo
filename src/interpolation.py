import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
y = np.array([0, 1, 0, 2, 1, 2, 3, 2, 4, 3])

# 创建三次样条插值对象
cs = CubicSpline(x, y)

# 生成更多的点进行插值
x_interp = np.linspace(0, 9, 100)
y_interp = cs(x_interp)

# 绘制原始数据点和插值曲线
plt.figure()
plt.plot(x, y, 'o', label='Data Points')
plt.plot(x_interp, y_interp, label='Cubic Spline Interpolation')
plt.title('Cubic Spline Interpolation')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.show()