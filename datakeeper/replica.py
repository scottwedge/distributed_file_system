import time
import zmq
import sys
import os
import signal
import socket as sok

port = 7000

def get_ip_address():
    s = sok.socket(sok.AF_INET, sok.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def replicate(IPs, videos):
    keeperContext = zmq.Context()
    keeperSocket = keeperContext.socket(zmq.REQ)
    for key in IPs:
        print("tcp://" + str(IPs[key]) + ":" + str(port))
        keeperSocket.connect("tcp://" + str(IPs[key]) + ":" + str(port))
        keeperSocket.send_pyobj("upload")
        msg = keeperSocket.recv_pyobj()
        print(msg)
        for V in videos:
            file = open(videos[V], 'rb').read()
            keeperSocket.send_pyobj(file)
            msg = keeperSocket.recv_pyobj()
            print(msg)
        keeperSocket.disconnet()

ipv4 = get_ip_address()
masterContext = zmq.Context()
masterSocket = masterContext.socket(zmq.REP)
print("tcp://" + str(ipv4) + ":" + str(port))
masterSocket.connect("tcp://" + str(ipv4) + ":" + str(port))

while True:
    IPs = masterSocket.recv_pyobj()
    masterSocket.send_pyobj("the ips was recieved")
    videos = masterSocket.recv_pyobj()
    masterSocket.send_pyobj("the videos was recieved")

    replicate(IPs, videos)