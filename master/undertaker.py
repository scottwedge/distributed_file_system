# import sys
import zmq
import time
def undertaker(undertaker_table,file_names_tables):
    # data_keepers_num = int(sys.argv[1])
    # alive = {}
    # IP_table = shared_memory.SharedMemory(name="IP_table") #connect to shared memory
    context = zmq.Context
    port="6000"
    socket = context.socket(zmq.SUB)
    for item in undertaker_table.items():
        IP,mylist = item
        socket.connect ("tcp://%s:%s"% (IP , port))
        # alive[IP] = False
    start_time = time.time()
    
    while True:
        recieved_IP = socket.recv_string() 
        undertaker_table[recieved_IP][0] =True
        end_time = time.time()
        if(end_time - start_time > 1):
            for item in undertaker_table.items():
                IP,mylist = item
                if(mylist[0] == False):
                    del file_names_tables[IP]
                    del undertaker_table [IP]
                    
            for IP,mylist in undertaker_table:
                undertaker_table[IP][0] = False
            start_time = time.time()

#clean table / reset timer / reset alive dict
'''
def timesup(undertaker_table,file_names_tables):
    for item in undertaker_table.items():
        IP,mylist = item
        if(mylist[0] == False):
            del file_names_tables[IP]
            del undertaker_table [IP]
            
    for IP,mylist in undertaker_table:
        undertaker_table[IP][0] = False
    start_time = time.time()
'''