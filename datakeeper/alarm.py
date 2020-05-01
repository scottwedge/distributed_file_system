import time
import zmq
import sys
import os
import signal
import socket as sok

# def get_ip_address():
#     s = sok.socket(sok.AF_INET, sok.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
#     return s.getsockname()[0]
MyIp = sys.argv[1]
# def get_ip_address():
#     return MyIp

port = 6000
ipv4 = str(MyIp)
context = zmq.Context()
socket = context.socket(zmq.PUB)
ip = "tcp://" + str(ipv4) + ":" + str(port)
print(ip)
socket.bind(ip)
socket.send_pyobj(ipv4)



i = 0
while True:
    time.sleep(0.5)

    #sending the ipv4
    print (ipv4)
    socket.send_string(str(ipv4))



