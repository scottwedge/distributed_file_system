import time
import zmq
import cv2
import sys
import os
import socket as sok

def get_ip_address():
    s = sok.socket(sok.AF_INET, sok.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

#reading arguments
N = int(sys.argv[1])
port = int(sys.argv[2])
MasterIP = str(sys.argv[3])
MasterN = str(sys.argv[4])

#sending the initializing data to the master
context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.bind("tcp://" + str(MasterIP) + ":5000")
socket.send_pyobj({'IP' : str(get_ip_address()), 'N' : str(N)})

# #running the alarm process
# os.system("python3 alarm.py &")

# #running the replica process
# os.system("python3 replica.py &")

#running the N datakeeper for this machine
for i in range(port, port + N):
    os.system("python3 keeper.py " + str(i) + " " + str(MasterIP) + " " + MasterN + " &")