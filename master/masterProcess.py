import sys
import zmq

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

process_ID = int(sys.argv[1])
IP_table = shared_memory.SharedMemory(name="IP_table") #connect to shared memory

port = str(4000+process_ID)
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://%s:%s"  %( get_ip_address(), port)) #bind server

#define upload , download , replicate 
