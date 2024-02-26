import socket
import time
import pickle
import util
import krige_impl 

import numpy as np
from matplotlib import pyplot as plt

import taichi as ti

# create two process
# p1 read data from one port with len 8
# p2 read data from another port with len 8

# process data1 + data1
# it should look at {2.73, 2.68, 2.86, .....}

port1 = 9999
port2 = 8888

def recv_data(client_socket):
    data = client_socket.recv(1024)
    received_data = pickle.loads(data)
    print('receive:', received_data)
    # TODO: write received data to buffer

    response = "ok"
    client_socket.send(response.encode())

# create connection
def listen_port(port, buffer):
    server_address = ('localhost', port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind port
    server_socket.bind(server_address)

    # listen....
    server_socket.listen(1)

    print('start listen...')

    client_socket, client_address = server_socket.accept()
    while True:
        recv_data(client_socket)
        # write to data

    client_socket.close()
    server_socket.close()

# create twp process, listen port1 and port2

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

def imaging(client_socket_1, client_socket_2):
    data = None
    raise KeyError("un implement")
    # create p1 and read from socket 1 and read to data[:8]
    # ....

    # create p2 and read from socket 2 and read to data[8:]
    # ...


    # pre-process data
    # ...


    # imaging, now data must be an array like, each array member represent state/value for on fiber
    # ...

demo_seqs = np.array(
  [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1],
    [1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  ]
)

slug_seqs = np.array(
  [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1,1,1,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  ]
)

mask = np.zeros((250, 250),  dtype=bool)
for x in range(mask.shape[0]):
   for y in range(mask.shape[1]):
      mask[x, y] = False
      if util.in_cycle(x, y, 125): 
         mask[x, y] = True
      
print(mask)

def all_water(mtx):
    for x in range(mtx.shape[0]):
        for y in range(mtx.shape[1]):
            r = (x-125)**2 + (y-125)**2
            if r > 125**2:
                mtx[x, y] = 0.5
    mtx[0, 0] = 1

def image_on_fiber(fibers):
    pass


def demo_image_level(seqs):
   fig = plt.figure('frame')

   import liner_image

   mtx = np.zeros((250, 250))
   water_mtx = np.zeros((250, 250))
   all_water(water_mtx)
   for i in range(seqs.shape[1]):
      for j in (range(16)):
        points[j][2] = seqs[j][i]
      liner_image.imagine_layer(points, 125, mtx)
      # slow display
      ax1 = fig.add_subplot(1, 1, 1)
      ax1.imshow(mtx, origin="lower", cmap='bwr')
      ax1.scatter(points[:,0], points[:,1], c=points[:,2])
      # plt.show()
      plt.pause(0.1)
      fig.clf()

x = np.arange(1, 250+1)
y = np.arange(1, 64+1)

pipe_scatter = []
from mpl_toolkits.mplot3d import Axes3D

def demo_image_wave(seqs):
  x_range = 250
  y_range = 250
  range_step = 1
  gridx = np.arange(0.0, x_range, range_step)
  gridy = np.arange(0.0, y_range, range_step)
 
  mtx = np.zeros((250, 250))
  water_mtx = np.zeros((250, 250))
  all_water(water_mtx)
  fig = plt.figure('frame')
  for i in range(seqs.shape[1]):
    for j in (range(16)):
      points[j][2] = seqs[j][i]
    if not np.any(points[:,2]):
      mtx = water_mtx
    else:
      kg = krige_impl.Kriging(points[:,0], points[:,1], points[:,2], nlags=10,)
      mtx, _ = kg.execute('grid', gridx, gridy)
      util.set_range(mtx)
    
    pipe_scatter.append(np.count_nonzero(mtx, axis=0))

    # slow display
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.imshow(mtx, origin="lower", cmap='bwr')
    ax1.scatter(points[:,0], points[:,1], c=points[:,2])
    plt.pause(0.001)
    fig.clf()

center_x = 125
center_y = 125
radius_square = 125 * 125

def demo_image_slug(seqs):
   x_range = 250
   y_range = 250
   range_step = 1
   gridx = np.arange(0.0, x_range, range_step) #三个参数的意思：范围0.0 - 0.6 ，每隔0.1划分一个网格
   gridy = np.arange(0.0, y_range, range_step)

   x, y = np.meshgrid(gridx, gridy)
   distance = ((x - center_x)**2 + (y - center_y)**2)
   fig = plt.figure('frame')

   mtx = np.zeros((250, 250))
   water_mtx = np.zeros((250, 250))
   all_water(water_mtx)
   sep_dict = {'range':45, 'nugget':0, 'psill':2}
   for i in range(seqs.shape[1]):
      for j in (range(16)):
        points[j][2] = seqs[j][i]
      ax1 = fig.add_subplot(1, 1, 1)
      if not np.any(points[:,2]):
        ax1.imshow(water_mtx, origin="lower", cmap='bwr')

      else:
        kg = krige_impl.Kriging(points[:,0], points[:,1], points[:,2],model='spherical', parameters=sep_dict, nlags=10,)
        mtx, _ = kg.execute('grid', gridx, gridy)
        util.set_range(mtx)

        ax1.imshow(mtx, origin="lower", cmap='bwr')

      # liner_image.imagine_layer(points, 125, mtx)
      # plt.show()
        
      plt.pause(0.001)
      fig.clf()

def demo_image_wave_ti(seqs):
   x_range = 250
   y_range = 250
   range_step = 1
   gridx = np.arange(0.0, x_range, range_step) #三个参数的意思：范围0.0 - 0.6 ，每隔0.1划分一个网格
   gridy = np.arange(0.0, y_range, range_step)

   x, y = np.meshgrid(gridx, gridy)
   distance =((x - center_x)**2 + (y - center_y)**2)
   mtx = np.zeros((250, 250))
   water_mtx = np.zeros((250, 250))
   water_mtx[distance > radius_square] = 0.5
   water_mtx[0, 0] = 1
 
   gui = ti.GUI('pipe slice', res = (x_range, y_range))

   sep_dict = {'range':45, 'nugget':0, 'psill':2}
   for i in range(seqs.shape[1]):
      for j in (range(16)):
        points[j][2] = seqs[j][i]
 
      if not np.any(points[:,2]):
        gui.set_image(water_mtx)
      else:
        kg = krige_impl.Kriging(points[:,0], points[:,1], points[:,2], nlags=10)
        mtx, _ = kg.execute('grid', gridx, gridy)
        mtx[distance > radius_square] = 0.5

        gui.set_image(mtx.swapaxes(0, 1))

      gui.show()

def demo_image_slug_ti(seqs):
   x_range = 250
   y_range = 250
   range_step = 1
   gridx = np.arange(0.0, x_range, range_step) #三个参数的意思：范围0.0 - 0.6 ，每隔0.1划分一个网格
   gridy = np.arange(0.0, y_range, range_step)

   x, y = np.meshgrid(gridx, gridy)
   distance =((x - center_x)**2 + (y - center_y)**2)
   mtx = np.zeros((250, 250))
   water_mtx = np.zeros((250, 250))
   water_mtx[distance > radius_square] = 0.5
   water_mtx[0, 0] = 1
 
   gui = ti.GUI('pipe slice', res = (x_range, y_range))

   sep_dict = {'range':45, 'nugget':0, 'psill':2}
   for i in range(seqs.shape[1]):
      for j in (range(16)):
        points[j][2] = seqs[j][i]
 
      if not np.any(points[:,2]):
        gui.set_image(water_mtx)
      else:
        kg = krige_impl.Kriging(points[:,0], points[:,1], points[:,2], model='spherical', parameters=sep_dict, nlags=10)
        mtx, _ = kg.execute('grid', gridx, gridy)
        mtx[distance > radius_square] = 0.5

        gui.set_image(mtx.swapaxes(0, 1))

      gui.show()


def main(): 
    start = time.perf_counter()
    # demo_image_level(demo_seqs)
    # demo_image_wave(demo_seqs)
    demo_image_wave_ti(demo_seqs)
    # demo_image_slug(slug_seqs)
    # demo_image_slug_ti(slug_seqs)
    end = time.perf_counter()
    print("runtime:", end-start)

    # 1. receive data from uart

    # 2. read 0.1ms data and transe to fiber state

    # 3. imageing on different fiber state

    # 4. clear plt and update image
    
from matplotlib import cm

# Using the special variable  
# __name__ 
if __name__=="__main__": 
    main() 
    print(len(pipe_scatter))
    z = np.array(pipe_scatter)
    X, Y = np.meshgrid(x, y[:40])

    plt.style.use('_mpl-gallery')

    # Make data
    # R = np.sqrt(X**2 + Y**2)
    # Z = np.sin(R)

    # Plot the surface
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # ax.plot_surface(X, Y, Z[:40, :], vmin=Z.min() * 2, cmap=cm.Blues)

    ax.set(xticklabels=[],
           yticklabels=[],
           zticklabels=[])

    # plt.show()


    # ax = fig.add_subplot(111, projection='3d') 

    # us = np.linspace(0, 2 * np.pi, 32) 
    # zs = np.linspace(0, 1, 64) 

    # us, zs = np.meshgrid(us, zs) 

    # xs = 10 * np.cos(us) 
    # ys = 10 * np.sin(us) 
    # ax.plot_wireframe(ys, zs, xs, color='black') 

    # plt.show() 

    print("x:", X.shape)
    print("y:", Y.shape)
    print("z:", z.shape)
    print(z)
    # fig = plt.figure()
    # ax = Axes3D(fig)
    ax.plot_surface(X, Y, z[:40, :], cmap=cm.Blues)

    ax.set_xlim(0, 250)
    ax.set_ylim(0, 40)
    ax.set_zlim(0, 250)

    ax.set_box_aspect((1,4,1)) # 设定坐标轴的长宽高比例
    # ax.grid(False) 

    ax.xaxis.set_label_text('X')
    ax.yaxis.set_label_text('Y')
    ax.zaxis.set_label_text('Z')

    plt.show()