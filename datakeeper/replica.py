import time
import zmq
import sys
import os
import signal
import socket as sok

port = 7000
masterIP = sys.argv[1]
MyIp = str(sys.argv[2])
# def get_ip_address():
#     s = sok.socket(sok.AF_INET, sok.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
#     return s.getsockname()[0]
# def get_ip_address():
#     return MyIp

def replicate(IP, video):
    keeperContext = zmq.Context()
    keeperSocket = keeperContext.socket(zmq.REQ)
    print("tcp://" + str(IP))
    keeperSocket.connect("tcp://" + str(IP))
    keeperSocket.send_pyobj("upload")
    msg = keeperSocket.recv_pyobj()
    print(msg)
    keeperSocket.send_pyobj(video)
    msg = keeperSocket.recv_pyobj()
    print(msg)
    file = open(video, 'rb').read()
    keeperSocket.send_pyobj(file)
    msg = keeperSocket.recv_pyobj()
    print(msg)
    #keeperContext.term()

masterContext = zmq.Context()
masterSocket = masterContext.socket(zmq.PAIR)
print("tcp://" + str(MyIp) + ":" + str(port))
masterSocket.bind("tcp://" + str(MyIp) + ":" + str(port))

while True:
    # IP = masterSocket.recv_pyobj()
    # masterSocket.send_pyobj("the ips was received")
    # video = masterSocket.recv_pyobj()
    # masterSocket.send_pyobj("the videos was received")
    
    IP,video = masterSocket.recv_pyobj()
    replicate(IP, video)
