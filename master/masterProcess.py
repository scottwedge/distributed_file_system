import sys
import zmq
import multiprocessing
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

# def upload_handler(file_name):
#     # recieved upload request from client
    
# def download_handler(file_name):
#     #recieved download request from client
    
def MasterProcess(process_ID,undertaker_table,file_names_tables):    
    # process_ID = int(sys.argv[1])
    # IP_table = shared_memory.SharedMemory(name="IP_table") #connect to shared memory
    # shared_mem = sys,argv[2]
    port = str(4000+process_ID)
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://%s:%s"  %( get_ip_address(), port)) #bind server
    
    
    while true():
        request_type,file_name = socket.recv_pyobj()
        if request_type == "upload":
            # reply = upload_handler()
        else if request_type == "download":
            # reply = download_handler()
        
    #define  replicate 
