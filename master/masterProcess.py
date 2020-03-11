import zmq
import multiprocessing
import socket

'''
process invoked N times to handle clients requests
'''
def MasterProcess_func(process_ID,undertaker_table,file_names_tables,availability_table):
    print("master process no. "+str(process_ID)+" started")
    # process_ID = int(sys.argv[1])
    # IP_table = shared_memory.SharedMemory(name="IP_table") #connect to shared memory
    port = str(4000+process_ID) #port for reciebing requests
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://%s:%s"  %( get_ip_address(), port)) #bind server
    # socket_datakeeper = context.socket(zmq.PULL)
    # socket.bind("tcp://%s:%s"  %( get_ip_address(), port))
    print(len(file_names_tables),file_names_tables)
    print(len(availability_table),availability_table)
    while True:
        #wait for new request
        print("#####################################################################################")
        print("waiting for new request")
        request_type,file_name = socket.recv_pyobj()
        print(str(process_ID)+" process recieved a request of type :"+request_type)
        print(file_name)

        print(file_names_tables,file_name)
        IP_return_list = find_file(file_names_tables,file_name) #search file name in all data keepers
        if request_type == "upload":
            print("IP_return_list : ",IP_return_list)
            if(len(IP_return_list) != 0):
                socket.send_pyobj("error : file already uploaded before")
                print("master response : error // file already uploaded before")
            else:
                '''
                upload sequence
                '''
                message = upload_handler(availability_table)
                print("master response :"+message +" is free to upload to")
                socket.send_pyobj(message)
                # wait for recieve from data keeper
                # send success to client
                # free data keeper -> set IPport in availability_table to True

        elif (request_type == "download"):
            print("IP_return_list : ",IP_return_list)
            if(len(IP_return_list) != 0):
                '''
                download sequence
                '''
                message = download_handler(availability_table,IP_return_list)
                print("master response :"+str(len(message)) +" are free to download from")
                socket.send_pyobj(message) #send array of free IP:Port to client

            else:
                socket.send_pyobj("error : file not found in any data keeper")
                print("master response : error // file not found in any data keeper")
        elif request_type == "replydownload":
            availability_table[file_name] = False
            print(file_name + "is taken now..")
            socket.send_pyobj("Fol 3alik ya client")
        elif request_type == "dataKeeperSuccess":
            IPport,oldrequest,filedownloaded=file_name
            print(file_name)
            availability_table[IPport] = True
            if (oldrequest == "upload"):
                IP,port=IPport.split(":")
                file_names_tables[IP].append(filedownloaded)
                print("file_names_tables[IP] = ",file_names_tables[IP])
            #TODO : send success sig to client
            socket.send_pyobj("Fol 3alik ya data keeper")

        else:
            socket.send_pyobj("error // request type not known")
            print("master response : error // request type not known")

def find_file(file_names_tables,file_name):
    print(file_names_tables,file_name)
    return_array = []
    for item in file_names_tables.items():
        IP,files = item
        for file in files:
            if(file_name == file):
                return_array.append(IP)
    return return_array

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def upload_handler(availability_table):
    #print("availability table in upload"+availability_table)
    # send first avaialble data keeper and wait for success msg from data keeper
    #then send success to client and add filename to data keeper
    for item in availability_table.items():
        #print("for item"+item+ "in availability_table.items()")
        IPport,status = item
        #print(IPport,status)
        if(status):
            #print(availability_table[IPport])
            availability_table[IPport] = False
            return IPport
    return "-1"

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
