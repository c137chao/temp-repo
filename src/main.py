import socket
import pickle

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
