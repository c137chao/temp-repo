import krige_impl
import numpy as np
from matplotlib import pyplot as plt

# 已知采样点的数据，是坐标（x，y）和坐标对应的值
# 矩阵中第一列是x,第二列是y,第三列是坐标对应的值
data = np.array(
    [
       [85, 35, 2],[165, 55, 2],
       [65, 65, 2],[105, 75, 2],[145, 85, 2], [185, 95, 2], 
       [45, 105, 1], [85, 115, 0], [125, 125, 1], [165, 135, 1], [205, 145, 1],
       [65, 155, 0], [105, 165, 0], [145, 175, 0], [185, 185, 0],
         [85, 195, 0], [165, 215, 0],
    ])

slug_data = np.array(
    [
       [85, 35, 0],[165, 55, 0],
       [65, 65, 0],[105, 75, 1],[145, 85, 1], [185, 95, 0], 
       [45, 105, 0], [85, 115, 1], [125, 125, 1], [165, 135, 1], [205, 145, 0],
       [65, 155, 0], [105, 165, 1], [145, 175, 1], [185, 185, 0], 
       [85, 195, 0], [165, 215, 0],
    ])
ndata = len(data)

for i in range(ndata):
    if slug_data[i][2] != 0:
        x = slug_data[i][0]
        y = slug_data[i][1]
        np.append(slug_data, [x+1,y,1])
        np.append(slug_data, [x,y+1,1])
        np.append(slug_data, [x-1,y,1])
        np.append(slug_data, [x,y-1,1])

plt.figure(figsize=(8, 8))
plt.scatter(data[:, 0], data[:, 1], c = data[:, 2])
plt.legend()
plt.show()

plt.scatter(slug_data[:, 0], slug_data[:, 1], c = slug_data[:, 2])
plt.legend()
plt.show()

# 网格
x_range = 259
y_range = 250
range_step = 1
gridx = np.arange(0.0, x_range, range_step) #三个参数的意思：范围0.0 - 0.6 ，每隔0.1划分一个网格
gridy = np.arange(0.0, y_range, range_step)

# sep_dict = {'range':70, 'nugget':0, 'psill': 1}


krig_matrix_1 = krige_impl.Kriging(data[:, 0], data[:, 1], data[:, 2], model='gaussian') 
krig_matrix_2 = krige_impl.Kriging(slug_data[:, 0], slug_data[:, 1], slug_data[:, 2], model='gaussian') 


# k2d1_1, _ = ok2d.execute('grid', gridx, gridy)
k2d1_1, _ = krig_matrix_1.execute('grid', gridx, gridy)

print(np.round(k2d1_1,2))

# 绘图
fig, (ax1) = plt.subplots(1)
ax1.imshow(k2d1_1, origin="lower", cmap='bwr')
ax1.set_title("kriging image")
plt.tight_layout()

plt.scatter(data[:, 0], data[:, 1], c = data[:, 2])
plt.legend()
plt.show()



gridx = np.arange(0.0, x_range, range_step) 
gridy = np.arange(0.0, y_range, range_step)

k2d1_2, _ = krig_matrix_2.execute('grid', gridx, gridy)


print(np.round(k2d1_2,2))

# # 绘图
fig, (ax1) = plt.subplots(1)
ax1.imshow(k2d1_2, origin="lower", cmap='bwr')
ax1.set_title("kriging image2")
plt.tight_layout()

plt.show()