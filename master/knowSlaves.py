'''
get ips of all data keepers and init and run undertaker and n processes
'''

#an item in the shared mem will look like this:
# {IP:[alive,[{processes(port_num):available}],[file_names]]}

import socket
import sys
# import os
import zmq
# import numpy as np
# from multiprocessing import shared_memory
import multiprocessing
import undertaker
import masterProcess

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

data_keepers_num = -1
port_num = "5000"
port_num_DataKeepers = 10000
if (len(sys.argv) > 1):
    data_keepers_num = int(sys.argv[1])

manager = multiprocessing.Manager()
undertaker_table = manager.dict()
file_names_tables = manager.dict()
avaiability_table = manager.dict()
context = zmq.Context()
reciever = context.socket(zmq.PULL)
reciever.connect("tcp://%s:%s"  %( get_ip_address(), port_num))
'''
write ips in shared memory
'''
for i in range(0,data_keepers_num):
    ip,Num_of_ports = reciever.recv_pyobj()
    undertaker_table[ip]=[False,Num_of_ports]  
    file_names_tables[ip] = []
    for j in range(0,Num_of_ports):
        temp_key = ip + ":" + str(port_num_DataKeepers+j)
        avaiability_table[temp_key] = True
'''
init N processes + undertaker *who's first?
'''

# os.system("python undertaker.py "+data_keepers_num)
# for i in range(0,data_keepers_num):
#     os.system("python masterProcess.py ",i)
    
undertaker_process = multiprocessing.Process(target=undertaker,args=(undertaker_table,file_names_tables))
undertaker_process.start()
undertaker_process.join()
m_processes = []
for i in range(0,data_keepers_num):
    m_processes.append(multiprocessing.Process(target=masterProcess,args=(i,undertaker_table,file_names_tables,avaiability_table)))
    m_processes[i].start()
    m_processes[i].join()
