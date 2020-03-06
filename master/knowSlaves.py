'''
get ips of all data keepers and init and run undertaker and n processes
'''
import socket
import sys
import os
import numpy as np
from multiprocessing import shared_memory

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

data_keepers_num = -1
port_num = "5000"
if (len(sys.argv) > 1):
    data_keepers_num = int(sys.argv[1])


context = zmq.Context()
reciever = context.socket(zmq.PULL)
reciever.connect("tcp://%s:%s"  %( get_ip_address(), port))
ips = np.array([])
for i in range(0,data_keepers_num):
    message = reciever.recv_string()
    ips.append(ips,message)

'''
write ips in shared memory
'''
#create ip table
shm = shared_memory.SharedMemory(name="IP_table",create=True, size=ips.nbytes)
# Now create a NumPy array backed by shared memory
shared_ips = np.ndarray(ips.shape, dtype=ips.dtype, buffer=shm.buf)
shared_ips[:] = ips[:]  # Copy the original data into shared memory

#TODO :create tables of data keepers files (shared memory)
'''
init N processes + undertaker *who's first?
'''
os.system("python undertaker.py "+data_keepers_num)
for i in range(0,data_keepers_num):
    os.system("python masterProcess.py ",i)
