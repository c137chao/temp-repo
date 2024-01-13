import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# pipe_face = np.array()

# print(pipe_face)

# z = np.linspace(0, 1, 100)
# theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
# r = 1
# x = r * np.sin(theta)
# y = r * np.cos(theta)

# fig = plt.figure()
# ax1 = fig.add_subplot(121, projection='3d')
# ax1.plot(x, y, z, alpha=0.5, lw=2)
# ax1.set_xlabel("X")
# ax1.set_ylabel("Y")
# ax1.set_zlabel("Z")
# ax1.set_title("Semi-transparent Cylinder")

# np.random.seed(0)
# inside_points = np.random.rand(30, 3)

# # Scale points so they are inside cylinder:
# inside_points[:, :2] = inside_points[:, :2] - 0.5  # [-0.5, 0.5]
# inside_points[:, 2] = inside_points[:, 2] * 1  # [0, 1]

# ax2 = fig.add_subplot(122, projection='3d')
# ax2.scatter(inside_points[:, 0], inside_points[:, 1], inside_points[:, 2], color='r')
# ax2.set_xlabel("X")
# ax2.set_ylabel("Y")
# ax2.set_zlabel("Z")
# ax2.set_title("Points inside Cylinder")

# plt.show()

fig = plt.figure()  #定义新的三维坐标轴
ax3 = plt.axes(projection='3d')

#定义三维数据
xx = np.arange(-10,10,0.5)
yy = np.arange(-5,5,0.5)
X, Y = np.meshgrid(xx, yy)
Z = np.sin(X)+np.cos(Y)

print("X:", X.shape)
print("Y:", Y.shape)
print("Z:", Z.shape)
ax3.plot_surface(X,Y,Z,cmap='rainbow')
#ax3.contour(X,Y,Z, zdim='z',offset=-2，cmap='rainbow)   #等高线图，要设置offset，为Z的最小值
plt.show()