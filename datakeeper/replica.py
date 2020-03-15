import time
import zmq
import sys
import os
import signal
import socket as sok

port = 7000
masterIP = sys.argv[1]

def get_ip_address():
    s = sok.socket(sok.AF_INET, sok.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def replicate(IP, video):
    keeperContext = zmq.Context()
    keeperSocket = keeperContext.socket(zmq.REQ)
    print("tcp://" + str(IP))
    keeperSocket.connect("tcp://" + str(IP))
    keeperSocket.send_pyobj("upload")
    msg = keeperSocket.recv_pyobj()
    print(msg)
    file = open(video, 'rb').read()
    keeperSocket.send_pyobj(file)
    msg = keeperSocket.recv_pyobj()
    print(msg)
    #keeperContext.term()

masterContext = zmq.Context()
masterSocket = masterContext.socket(zmq.PAIR)
print("tcp://" + str(get_ip_address()) + ":" + str(port))
masterSocket.bind("tcp://" + str(get_ip_address()) + ":" + str(port))

while True:
    # IP = masterSocket.recv_pyobj()
    # masterSocket.send_pyobj("the ips was recieved")
    # video = masterSocket.recv_pyobj()
    # masterSocket.send_pyobj("the videos was recieved")
    
    IP,video = masterSocket.recv_pyobj()
    replicate(IP, video)