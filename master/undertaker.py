import sys
import zmq
import time

data_keepers_num = int(sys.argv[1])
alive = {}
IP_table = shared_memory.SharedMemory(name="IP_table") #connect to shared memory
context = zmq.Context
socket = context.socket(zmq.SUB)
for IP in IP_table:
    socket.connect ("tcp://%s:%s"% (IP , port))
    alive[IP] = False
start_time = time.time()

while True:
    messege = socket.recv()
    alive[messege] = True
    end_time = time.time()
    if(end_time - start_time > 1):
        timesup()


#clean table / reset timer / reset alive dict
def timesup():
    for IP,state in alive.items():
        if state == False :
            # todo : delete IP from table
        
    for IP in IP_table:
        alive[IP] = False
    start_time = time.time()