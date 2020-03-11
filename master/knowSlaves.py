'''
get ips of all data keepers and init and run undertaker and n processes
'''
import socket
import sys
# import os
import zmq
# from multiprocessing import shared_memory
import multiprocessing
from undertaker import *
from masterProcess import *

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

data_keepers_num = -1
port_num = "5000" #backdoor for recieving system ips
port_num_DataKeepers = 10000 #starting port for datakeepers process
if (len(sys.argv) > 1):
    data_keepers_num = int(sys.argv[1])
print("identifying "+str(data_keepers_num)+" data keepers in the system")
if (len(sys.argv) > 2):
    master_processes_num = int(sys.argv[2])
else:
    master_processes_num=data_keepers_num #use same N as data keepers
print("master will have "+str(master_processes_num)+" processes ")

manager = multiprocessing.Manager()
undertaker_table = manager.dict()
file_names_tables = manager.dict()
avaiability_table = manager.dict()
context = zmq.Context()
reciever = context.socket(zmq.PULL)
#reciever.connect("tcp://192.168.1.14:%s"  %(port_num))
reciever.bind("tcp://%s:%s"  %( get_ip_address(), port_num))

'''
write ips in shared memory after recieving them from devices in the system
'''
print("recieving data keepers IPs ..")
for i in range(0,data_keepers_num):
    All = reciever.recv_pyobj()
    print("device "+str(i+1)+" recieved :"+All['IP'])
    #print(All['IP'])
    #print(All['N'])
    ip = All['IP']
    Num_of_ports = int(All['N'])
    undertaker_table[ip]=[False,Num_of_ports]  #initialize all devices not alive
                                               #until they send their first heart beat
    file_names_tables[ip] = []
    print(file_names_tables[ip],len(file_names_tables))
    for j in range(0,Num_of_ports):
        temp_key = ip + ":" + str(port_num_DataKeepers+j)
        avaiability_table[temp_key] = True

'''
start N processes +undertaker
'''
# os.system("python undertaker.py "+data_keepers_num)
# for i in range(0,data_keepers_num):
#     os.system("python masterProcess.py ",i)

undertaker_process = multiprocessing.Process(target=undertaker_func,args=(undertaker_table,file_names_tables))
print("starting undertaker process..")
undertaker_process.start()
m_processes = []
for i in range(0,master_processes_num):
    m_processes.append(multiprocessing.Process(target=MasterProcess_func,args=(i,undertaker_table,file_names_tables,avaiability_table)))

#m_processes.append(undertaker_process)
#print("initializing "+str(len(m_processes))+" processes")
for Process in range(0,len(m_processes)):
    print("starting master process no."+str(Process)   +"..")
    m_processes[int(Process)].start()
for Process in m_processes:
    Process.join()
undertaker_process.join() #wait for infinite processes to end ..
print("this line cannot be reached ever")
