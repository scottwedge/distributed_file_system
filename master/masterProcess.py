import zmq
import multiprocessing
import socket
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def upload_handler(availability_table):
    # send first avaialble data keeper and wait for success msg from data keeper 
    #then send success to client and add filename to data keeper
    for item in availability_table.items():
        IPport,status = item
        if(status):
            availability_table[IPport] = False
            return IPport
    return "error"
    
def download_handler(availability_table,IP_return_list):
    #recieved download request from client
    retArr=[]
    for item in availability_table.items():
        IPport,status = item
        IP,port=IPport.split(":")
        if(IP in IP_return_list):
            if(status):
                retArr.append(IPport)
    
    return retArr
    
def MasterProcess_func(process_ID,undertaker_table,file_names_tables,availability_table):    
    # process_ID = int(sys.argv[1])
    # IP_table = shared_memory.SharedMemory(name="IP_table") #connect to shared memory
    # shared_mem = sys,argv[2]
    port = str(4000+process_ID)
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://%s:%s"  %( get_ip_address(), port)) #bind server
    # socket_datakeeper = context.socket(zmq.PULL)
    # socket.bind("tcp://%s:%s"  %( get_ip_address(), port))
    
    
    while True:
        request_type,file_name = socket.recv_pyobj()
        IP_return_list = find_file(file_names_tables,file_name)
        if request_type == "upload":
            if(len(IP_return_list) != 0):
                socket.send_pyobj("error")
            else:
                '''
                upload sequence
                '''
                message = upload_handler(availability_table)
                socket.send_pyobj(message)
                # wait for recieve from data keeper
                # send success to client
                # free data keeper -> set IPport in availability_table to True
                '''
                upload sequence end
                '''
                
        elif (request_type == "download"):
            if(len(IP_return_list) != 0):
                '''
                download sequence
                ''' 
                message = download_handler(availability_table,IP_return_list)
                socket.send_pyobj(message)
               
                '''
                download sequence end
                ''' 
            else:
                socket.send_pyobj("error")
        elif request_type == "replydownload":
            availability_table[file_name] = False
            socket.send_pyobj("Fol 3alik ya client")
        elif request_type == "dataKeeperSuccess":
            IPport,oldrequest,filedownloaded=file_name
            availability_table[IPport] = True
            if (oldrequest == "upload"):
                IP,port=IPport.split(":")
                file_names_tables[IP].append(filedownloaded)
            #send success sig to client
            socket.send_pyobj("Fol 3alik ya data keeper")
            
        else:
            socket.send_pyobj("error")

        
    #define  replicate 
def find_file(file_names_tables,file_name):
    return_array = []
    for item in file_names_tables:
        IP,files = item
        for file in files:
            if(file_name == file):
                return_array.append(IP)
    return return_array
