import numpy as np
import util
import matplotlib.pyplot as plt
import taichi as ti

total_diff_k = 0
total_diff_r = 0

# 创建x坐标值
x = np.linspace(0, 250, 250)

# 创建平滑曲线的y坐标值，例如使用sin函数
def generate_waves():
    all_wave = []

    all_wave.append(10 * np.sin(x/40+100) + 5 * np.cos(x/200 + 150) + 5 * np.sin(x/40 + 12) + 67)
    all_wave.append(5 * np.sin(x/60 + 5) + 6 * np.cos(x/150 + 140) + 6 * np.sin(x/50 + 25) + 90)
    all_wave.append(2 * np.sin(x/150+ 21) + 7 * np.cos(x/50 + 100) + 5 * np.sin(x/40 + 60) + 125)
    all_wave.append(7 * np.sin(x/40+ 21) + 5 * np.cos(x/100 + 60) + 5 * np.sin(x/400 + 82) + 165)
    all_wave.append(5 * np.sin(x/30+12) + 14 * np.cos(x/60 + 36) + 5 * np.sin(x/40 + 32) + 170)

    np.random.seed(0)

    for i in range(50):
        from random import randint
        all_wave.append(randint(40, 180) + 10 * np.sin(x/randint(30, 60) + 70 + randint(0, 20))+  \
                                           5 * abs(np.cos(x/randint(60, 150) + 30 + randint(30, 100))) + \
                                           randint(3, 7) * abs(np.sin(x/randint(30, 90) + randint(70, 100))) - \
                                           randint(5, 7) * abs(np.cos(x/randint(40, 100) + randint(50, 100))))
    # wave = 10 * np.sin(x/40) + 5 * np.cos(x/100 + 3) + 5 * np.sin(x/40 + 2) + 125

    return all_wave

n = 250  

# 使用NumPy的arange函数创建从1到n的一维数组
values = np.arange(1, n + 1)

x_range = 250
y_range = 250
range_step = 1

gridx = np.arange(0.0, x_range, range_step)
gridy = np.arange(0.0, y_range, range_step)

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

show = False
total = np.array([0, 0, 0, 0, 0])
stats = np.array([0, 0, 0, 0, 0])

def liner_ratio():
    from scipy.interpolate import griddata
    mtx_linear = np.zeros((250, 250), dtype=float)
    mtx_linear = griddata(points[:, :2], points[:, 2], (gridx[None, :], gridy[:, None]), method='linear')
    util.set_range(mtx_linear)
    return util.get_gas_holding(mtx_linear)


def origin_kriging(ax):
    from pykrige.ok import OrdinaryKriging

    ok3d = OrdinaryKriging(points[:, 0], points[:, 1], points[:, 2], variogram_model='power') # 模型
    mtx, _ = ok3d.execute("grid", gridx, gridy)
    mtx = np.where(mtx > 0.4, 1.0, 0.0)

    util.set_range(mtx)

    if show:
        im = ax.imshow(mtx, extent=(0, 1, 0, 1), origin='lower', cmap='bwr')
        ax.set_title(f'origin_kriging')
        plt.colorbar(im, ax=ax)

    # ax2.plot(mtx, cmap='bwr')

    # plt.imshow(mtx, cmap='bwr', interpolation='nearest')
    # plt.show()

    return util.get_gas_holding(mtx)


# from skimage.measure import compare_ssim

from skimage.metrics import structural_similarity as compare_ssim

def my_wave_kriging(ax, cmp):
    import krige_impl
    import cv2

    kg = krige_impl.Kriging(points[:,0], points[:,1], points[:,2],  nlags=10,)
    mtx_wave_krig, _ = kg.execute('grid', gridx, gridy)
    # mtx_wave_krig = cv2.GaussianBlur(mtx_wave_krig, (5, 5), 0)
    util.set_range(mtx_wave_krig)

    # plt.figure("改进克里金")

    if show:
        im = ax.imshow(mtx_wave_krig,origin='lower', cmap='bwr')
        ax.set_title(f'opti krig')
        ax.scatter(points[:,0], points[:,1], c=points[:,2]) 

        plt.colorbar(im, ax=ax)

    # ax3.plot(mtx_wave_krig, cmap='bwr')

    # plt.imshow(mtx_wave_krig, cmap='bwr', interpolation='nearest')
    # plt.show()
    import cv2
    global total_diff_k 
    cv2.GaussianBlur(mtx_wave_krig, (5, 5), 0)
    ssim = compare_ssim(mtx_wave_krig, cmp, full=False, data_range = 1)
    total_diff_k +=  ssim


    return util.get_gas_holding(mtx_wave_krig)


def rbf_insertation(ax, cmp):
    from scipy.interpolate import Rbf
    import cv2

    rbf = Rbf(points[:, 0], points[:, 1], points[:, 2])

    x_grid, y_grid = np.meshgrid(gridx, gridy)
    z_grid = rbf(x_grid, y_grid)

    z_grid = np.where(z_grid > 0.4, 1.0, 0.0)
    util.set_range(z_grid)

    if show:
        im = ax.imshow(z_grid, extent=(0, 1, 0, 1), origin='lower', cmap='bwr')
        ax.set_title(f'rbf')
        plt.colorbar(im, ax=ax)

    global total_diff_r 
    # total_diff_r +=  np.count_nonzero(cmp != z_grid)
    ssim = compare_ssim(z_grid, cmp, full=False, data_range = 1)
    total_diff_r += ssim


    # plt.figure("高斯径向基")
    # plt.imshow(z_grid, cmap='bwr', interpolation='nearest')
    # plt.show()

    return util.get_gas_holding(z_grid)

def indist(ax):
    from scipy.interpolate import griddata

    # idw
    zi = griddata(points[:, :2], points[:, 2], (gridx[None, :], gridy[:, None]), method='cubic')
    zi = np.where(zi > 0.5, 1.0, 0.0)
    util.set_range(zi)

    if show:
        im = ax.imshow(zi, extent=(0, 1, 0, 1), origin='lower', cmap='bwr')
        plt.colorbar(im, ax=ax)
        
    # plt.figure("idw")

    # plt.imshow(zi, cmap='bwr', interpolation='nearest')
    # plt.show()

    return util.get_gas_holding(zi)


e = 0

def compare_waves(all_wave):
    print('-------------------------------------------------------------------------')
    print('| 真实值 | 原始克里金插值 | 改进克里金插值 | 线性插值 | rbf插值 | 反距离插值 |') 
    print('-------------------------------------------------------------------------')
    for wave in all_wave:
        waves = np.tile(wave, (n, 1))
        # 使用NumPy的tile函数复制values数组来创建n * n的二维数组
        origin = np.tile(values, (n, 1))
        origin = np.rot90(origin, k=1)

        origin[origin < waves] = 0.0
        origin[origin >= waves] = 1.0

        origin = np.flipud(origin)
        
        # fig, axes = plt.subplots(1, 5, figsize=(15, 15))
        axes = np.array([0,0,0,0,0])

        origin = origin.astype(float)
        util.set_range(origin)

        base_gas_holding = (util.get_gas_holding(origin))    
        if show:
            ax = axes[0]
            im = ax.imshow(origin, extent=(0, 1, 0, 1), origin='lower', cmap='bwr')
            plt.colorbar(im, ax=ax)

        # plt.imshow(origin, cmap='bwr', interpolation='nearest')
        # plt.show()
        # print(wave)

        for i in range(len(points)):
            if wave[points[i, 0]] < points[i, 1]:
                points[i, 2] = 1 
            else:
                points[i, 2] = 0

        # print(points)

        # ori_krig_ratio = "{:.4f}".format(origin_kriging())
        ori_krig_ratio = (origin_kriging(axes[1]))
        my_krig_ratio = (my_wave_kriging(axes[2], origin))
        rbf_ratio = (rbf_insertation(axes[3], origin))
        indist_ratio = (indist(axes[4]))
        level_ratio = (liner_ratio())


        if show:
            plt.tight_layout()
            plt.show()

        mis = np.array([abs(ori_krig_ratio-base_gas_holding), abs(my_krig_ratio-base_gas_holding), abs(level_ratio-base_gas_holding), abs(rbf_ratio-base_gas_holding), abs(indist_ratio - base_gas_holding)])    
        stats = stats + mis
        total[np.argmin(mis)] += 1

        target = abs(my_krig_ratio-base_gas_holding)

        if target > e:
            e = target

        print('|', f"{base_gas_holding:.4f}", '| ', f"{ori_krig_ratio:.4f}", '|', f"{my_krig_ratio:.4f}", '|', f"{level_ratio:.4f}", '|', f"{rbf_ratio:.4f}", '|', f"{indist_ratio:.4f}")
        # print('|', base_gas_holding, '| ', ori_krig_ratio-base_gas_holding, '|', my_krig_ratio-base_gas_holding, '|', level_ratio-base_gas_holding, '|', rbf_ratio-base_gas_holding, '|', indist_ratio)
        # print('|', base_gas_holding, '| ', ori_krig_ratio-base_gas_holding, '|', my_krig_ratio-base_gas_holding, '|', level_ratio-base_gas_holding, '|', rbf_ratio-base_gas_holding, '|', indist_ratio)


    print('-------------------------------------------------------------------------')

    print(e)
    print(total)
    print(stats)

    print(total_diff_k / 50)
    print(total_diff_r / 50)

    plt.clf()

    labels = ['ori-krig', 'opt-krig', 'linear', 'rbf', 'idw']
    colors = ['red', 'green', 'blue', 'purple', 'yellow']  # 每个柱子的颜色

    plt.bar(range(len(total)), total, color=colors)
    plt.xticks(range(len(labels)), labels)

    plt.show()
    

labels = ['ori-krig', 'opt-krig', 'linear', 'rbf', 'idw']
colors = ['red', 'green', 'blue', 'purple', 'yellow']  # 每个柱子的颜色

plt.bar(range(5), [15, 26, 0, 14, 0], color=colors)
plt.xticks(range(len(labels)), labels)

plt.show()