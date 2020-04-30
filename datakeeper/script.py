import time
import zmq
import sys
import os
import socket as sok

# def get_ip_address():
#     s = sok.socket(sok.AF_INET, sok.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
#     return s.getsockname()[0]
def get_ip_address():
    return MyIp

#reading arguments
print("reading arguments")
port = 5000
N = int(sys.argv[1])
MasterIP = str(sys.argv[2])
MasterN = sys.argv[3]
MyIp = sys.argv[4]
#sending the initializing data to the master
print("sending my ip to master:" + str(get_ip_address()))
context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect("tcp://" + str(MasterIP) + ":" + str(port))
socket.send_pyobj({'IP' : str(get_ip_address()), 'N' : str(N)})

#running the alarm process
os.system("python3 alarm.py "+ MyIp +" &")

#running the replica process
os.system("python3 replica.py " + str(MasterIP) +" "+ MyIp +" &")

#running the N datakeeper for this machine
print("running the keeper "+ str(N))
for i in range(N):
    os.system("python3 keeper.py " + str(MasterIP) + " " + str(MasterN) + " &")