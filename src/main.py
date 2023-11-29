import socket
import time
import pickle
import krige_impl 

import numpy as np
from matplotlib import pyplot as plt


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
    #    [125, 125, 0], 
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
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1,1,1,1,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0],
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

def demo_image_wave(seqs):
   x_range = 259
   y_range = 250
   range_step = 1
   gridx = np.arange(0.0, x_range, range_step) #三个参数的意思：范围0.0 - 0.6 ，每隔0.1划分一个网格
   gridy = np.arange(0.0, y_range, range_step)
 
   fig = plt.figure('frame')

   mtx = np.zeros((250, 250))
   water_mtx = np.zeros((250, 250))
   all_water(water_mtx)
   for i in range(seqs.shape[1]):
      for j in (range(16)):
        points[j][2] = seqs[j][i]
      if not np.any(points[:,2]):
        mtx = water_mtx
      else:
        # print(points)
        kg = krige_impl.Kriging(points[:,0], points[:,1], points[:,2], model='linear',nlags=10,)
        mtx, _ = kg.execute('grid', gridx, gridy)

      # slow display
      ax1 = fig.add_subplot(1, 1, 1)
      ax1.imshow(mtx, origin="lower", cmap='bwr')
      ax1.scatter(points[:,0], points[:,1], c=points[:,2])
      # plt.show()
      plt.pause(0.1)
      fig.clf()

def demo_image_slug(seqs):
   x_range = 259
   y_range = 250
   range_step = 1
   gridx = np.arange(0.0, x_range, range_step) #三个参数的意思：范围0.0 - 0.6 ，每隔0.1划分一个网格
   gridy = np.arange(0.0, y_range, range_step)
 
   fig = plt.figure('frame')

   mtx = np.zeros((250, 250))
   water_mtx = np.zeros((250, 250))
   all_water(water_mtx)
#    import liner_image
   sep_dict = {'range':40, 'nugget':0, 'psill':1}
   for i in range(seqs.shape[1]):
      for j in (range(16)):
        points[j][2] = seqs[j][i]
    #   print(points)
      ax1 = fig.add_subplot(1, 1, 1)
      if not np.any(points[:,2]):
        ax1.imshow(water_mtx, origin="lower", cmap='bwr')
      else:
        # print(points)
        kg = krige_impl.Kriging(points[:,0], points[:,1], points[:,2], model='spherical', parameters=sep_dict, nlags=10,)
        mtx, _ = kg.execute('grid', gridx, gridy)
        ax1.imshow(mtx, origin="lower", cmap='bwr')

      # liner_image.imagine_layer(points, 125, mtx)
      # slow display
      ax1.scatter(points[:,0], points[:,1], c=points[:,2])
      # plt.show()
      plt.pause(0.1)
      fig.clf()
 
def main(): 
    start = time.perf_counter()
    demo_image_level(demo_seqs)
    # demo_image_wave(demo_seqs)
    # demo_image_slug(slug_seqs)
    end = time.perf_counter()
    print("runtime:", end-start)

    # 1. receive data from uart

    # 2. read 0.1ms data and transe to fiber state

    # 3. imageing on different fiber state

    # 4. clear plt and update image
    
  
# Using the special variable  
# __name__ 
if __name__=="__main__": 
    main() 