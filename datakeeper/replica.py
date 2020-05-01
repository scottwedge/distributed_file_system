import time
import zmq
import sys
import os
import signal
import socket as sok


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

def replicaKeeper_func(masterIP,MyIp):
    port = 7000
    masterContext = zmq.Context()
    masterSocket = masterContext.socket(zmq.PAIR)
    print("tcp://" + str(MyIp) + ":" + str(port))
    masterSocket.bind("tcp://" + str(MyIp) + ":" + str(port))

    while True:
        # IP = masterSocket.recv_pyobj()
        # masterSocket.send_pyobj("the ips was recieved")
        # video = masterSocket.recv_pyobj()
        # masterSocket.send_pyobj("the videos was recieved")
        
        IP,video = masterSocket.recv_pyobj()
        replicate(IP, video)