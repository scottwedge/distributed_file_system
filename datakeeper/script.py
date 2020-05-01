import time
import zmq
import sys
import os
import socket as sok
import multiprocessing
from alarm import *
from keeper import *
from replica import *

# def get_ip_address():
#     s = sok.socket(sok.AF_INET, sok.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
#     return s.getsockname()[0]
# def get_ip_address():
#     return MyIp

#reading arguments
print("reading arguments")
port = 5000
N = int(sys.argv[1])
MasterIP = str(sys.argv[2])
MasterN = sys.argv[3]
MyIp = str(sys.argv[4])
#sending the initializing data to the master
print("sending my ip to master:" + str(MyIp))
context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect("tcp://" + str(MasterIP) + ":" + str(port))
socket.send_pyobj({'IP' : str(MyIp), 'N' : str(N)})


#running the replica process
#os.system("python3.8 replica.py " + str(MasterIP) +" "+ MyIp)

replica_process = multiprocessing.Process(target=replicaKeeper_func,args=(MasterIP,MyIp))
print("starting replica_process ..")
replica_process.start()

alarm_process = multiprocessing.Process(target=alarmKeeper_func,args=(MyIp))
print("starting alarm_process ..")
alarm_process.start()

k_processes = []
for i in range(0,N):
    k_processes.append(multiprocessing.Process(target=mainKeeper_func,args=(MasterIP,MyIp,MasterN)))

for Process in range(0,len(k_processes)):
    print("starting keeper process no."+str(Process)   +"..")
    k_processes[int(Process)].start()
for Process in k_processes:
    Process.join()
alarm_process.join() #wait for infinite processes to end ..
print("this line cannot be reached ever")

#running the N datakeeper for this machine
#print("running the keeper "+ str(N))
#for i in range(N):
#    os.system("python3.8 keeper.py " + str(MasterIP) + " " + str(MasterN) + " " + str(MyIp))


#running the alarm process
#os.system("python3.8 alarm.py "+ MyIp)