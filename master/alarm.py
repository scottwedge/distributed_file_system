import time
import zmq
import random
import numpy as np
import cv2 as cv
import sys
import os

port = "6000"

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print ("Collecting updates from server...")
socket.connect ("tcp://192.168.1.10:%s" % port)
socket.subscribe("")
while (True):
    string = socket.recv_string()
    seconds = time.time()
    print("Seconds since epoch = "+ str(seconds)+"your ip"+str(string))