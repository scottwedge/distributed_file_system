# TODO : complete file to send periodic replication signal
import time
import zmq
import sys

def replication_func(availability_table,file_names_tables):
    replication_port =7000 #back door for replication
    data_keepers_num = -1
    if (len(sys.argv) > 1):
        data_keepers_num = int(sys.argv[1])
    print("identifying "+str(data_keepers_num)+" data keepers in the replication system")
    maxNumOfReplications=min(3,data_keepers_num) #less than 3 if we have less than 3 data keepers
    context = zmq.Context()
    replication_socket = context.socket(zmq.PAIR)
    #sockets={}
    # for i in range(data_keepers_num):
    #     print ("binding replication port of datakeeper no. "+str(i+1))
    #     sockets[ip] = context.socket(zmq.Push)
    #     sockets[ip].bind ("tcp://%s:%s"  %( get_ip_address(), str(port_num)))

    while True:
        ## DONE: check for file if present in IPs<maxNumOfReplications
        ## DONE: get ip:port available for the other datakeeper IPs
        ## DONE: send to data keeper [ip:port , file name]
        for item in file_names_tables.items():
            IP,files = item
            for file in files:
                if(Need_to_replicate(file,file_names_tables,maxNumOfReplications)):
                    replication_socket.connect("tcp://"+str(IP)+":"+str(replication_port))
                    #get another IP other than found
                    nextIP=getNextOtherIP(IP,file_names_tables,file)
                    #get free port to send to
                    nextPort=getFirstNextFreePort(nextIP,availability_table)
                    availability_table[nextPort] = False
                    print(file + "is taken now for replication..")
                    # sockets[IP].send_pyobj([nextPort,file]) #send to the datakeeper having the file to send it to other data keeper given
                    replication_socket.send_pyobj([nextPort,file])
                    replication_socket.close() # socket.disconnect() may work
                    time.sleep(1)


#returns true if file does Need_to_replicate exist in tables<maxNumOfReplications
def Need_to_replicate(file_name,file_names_tables,maxNumOfReplications):
    temp_counter = 0
    for item in file_names_tables.items():
        IP,files = item
        for file in files:
            if(file_name == file):
                temp_counter+=1
    if (temp_counter >= maxNumOfReplications): # should be == but used >= to avoid potential issues
        return False
    else:
        return True
    ## Done: implement
    ## TODO: test

#get ip doesn't have the same file
def getNextOtherIP(IP,file_names_tables,file_name):
    for item in file_names_tables.items():
        file_exists_in_current_data_keeper = False
        IPfromlist,files = item
        if (IP != IPfromlist):
            for file in files:
                if(file_name == file):
                    file_exists_in_current_data_keeper = True
            if (file_exists_in_current_data_keeper == False):
                return IPfromlist
    return "error : (getNextOtherIP)this line can't be reached" # all IPs have this file
    
    ## Done: implement
    ## TODO: test

def getFirstNextFreePort(nextIP,availability_table):
    for item in availability_table.items():
        IPport,status = item
        IP,port=IPport.split(":")
        if (IP == nextIP and status == True):
            return IPport
    return "error : no free port available"
    ## Done: implement
    ## TODO: test
