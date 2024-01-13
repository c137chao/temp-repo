import krige_impl
import numpy as np
from matplotlib import pyplot as plt

# 已知采样点的数据，是坐标（x，y）和坐标对应的值
# 矩阵中第一列是x,第二列是y,第三列是坐标对应的值
data = np.array(
    [
       [850, 350, 0],[1650, 550, 0],
       [650, 650, 0],[1050, 750, 0],[1450, 850, 0], [1850, 950, 0], 
       [450, 1050, 1], [850, 1150, 0], [1250, 1250, 0], [1650, 1350, 0], [2050, 1450, 1],
       [650, 1550, 1], [1050, 1650, 1], [1450, 1750, 1], [1850, 1850, 0],
       [850, 1950, 0], [1650, 2150, 0],
    ])

slug_data = np.array(
    [
       [85, 35, 0],[165, 55, 0],
       [65, 65, 0],[105, 75, 1],[145, 85, 0], [185, 95, 0], 
       [45, 105, 0], [85, 115, 1], [165, 135, 1], [205, 145, 0],
       [65, 155, 1], [105, 165, 0], [145, 175, 1], [185, 185, 1], 
       [85, 195, 0], [165, 215, 0],
    ])
ndata = len(data)

import util
import random

def draw_a_random_bubble_on(mtx, x, y):
    if x > 2400 or x < 100:
        return
    if y > 2400 or y < 100:
        return 
    r = random.randint(30, 60)
    for i in range(x-r, x+r):
        for j in range(y-r, y+r):
            if (i-x)**2 + (j-y)**2 <= r**2:
                mtx[j, i] = 1
        

def temp_draw_bubble(vals):
    mtx = np.zeros((2500, 2500))
    for fiber in vals:
        if fiber[2] == 1:
            draw_a_random_bubble_on(mtx, fiber[0], fiber[1])
            for i in range(10):
                draw_a_random_bubble_on(mtx, random.randint(-2000, 2000), fiber[1]+random.randint(-100,100))


    for x in range(2500):
        for y in range(2500):
            if (x-1250)**2 + (y-1250)**2 > 1250 **2:
                mtx[x, y] = 0.5
 
    fig = plt.figure('frame')
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.imshow(mtx, origin="lower", cmap='bwr')
    # ax1.scatter(vals[:,0], vals[:,1], c=vals[:,2])   

    plt.show()

    return None


temp_draw_bubble(data)


# for i in range(ndata):
#     if slug_data[i][2] != 0:
#         x = slug_data[i][0]
#         y = slug_data[i][1]
#         np.append(slug_data, [x+1,y,1])
#         np.append(slug_data, [x,y+1,1])
#         np.append(slug_data, [x-1,y,1])
#         np.append(slug_data, [x,y-1,1])

# plt.figure(figsize=(8, 8))
# plt.scatter(data[:, 0], data[:, 1], c = data[:, 2])
# plt.legend()
# plt.show()

# plt.scatter(slug_data[:, 0], slug_data[:, 1], c = slug_data[:, 2])
# plt.legend()
# plt.show()

# # 网格
# x_range = 259
# y_range = 250
# range_step = 1
# gridx = np.arange(0.0, x_range, range_step) #三个参数的意思：范围0.0 - 0.6 ，每隔0.1划分一个网格
# gridy = np.arange(0.0, y_range, range_step)

# # sep_dict = {'range':70, 'nugget':0, 'psill': 1}


# krig_matrix_1 = krige_impl.Kriging(data[:, 0], data[:, 1], data[:, 2], model='gaussian') 
# krig_matrix_2 = krige_impl.Kriging(slug_data[:, 0], slug_data[:, 1], slug_data[:, 2], model='gaussian') 


# # k2d1_1, _ = ok2d.execute('grid', gridx, gridy)
# k2d1_1, _ = krig_matrix_1.execute('grid', gridx, gridy)

# print(np.round(k2d1_1,2))

# # 绘图
# fig, (ax1) = plt.subplots(1)
# ax1.imshow(k2d1_1, origin="lower", cmap='bwr')
# ax1.set_title("kriging image")
# plt.tight_layout()

# plt.scatter(data[:, 0], data[:, 1], c = data[:, 2])
# plt.legend()
# plt.show()



# gridx = np.arange(0.0, x_range, range_step) 
# gridy = np.arange(0.0, y_range, range_step)

# k2d1_2, _ = krig_matrix_2.execute('grid', gridx, gridy)


# print(np.round(k2d1_2,2))

# # # 绘图
# fig, (ax1) = plt.subplots(1)
# ax1.imshow(k2d1_2, origin="lower", cmap='bwr')
# ax1.set_title("kriging image2")
# plt.tight_layout()

# plt.show()