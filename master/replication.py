# TODO : complete file to send periodic replication signal
import time
import zmq

def replication_func(availability_table,file_names_tables):
    port_num =7000 #back door for replication
    data_keepers_num = -1
    if (len(sys.argv) > 1):
        data_keepers_num = int(sys.argv[1])
    print("identifying "+str(data_keepers_num)+" data keepers in the replication system")
    maxNumOfReplications=min(3,data_keepers_num) #less than 3 if we have less than 3 data keepers
    context = zmq.Context()
    ## TODO: fix connection , you can't bind same ip & port multiple times
    sockets={}
    for i in range(data_keepers_num):
        print ("binding replication port of datakeeper no. "+str(i+1))
        sockets[ip] = context.socket(zmq.Push)
        sockets[ip].bind ("tcp://%s:%s"  %( get_ip_address(), str(port_num)))

    while True:
        ## DONE: check for file if present in IPs<maxNumOfReplications
        ## DONE: get ip:port available for the other datakeeper IPs
        ## DONE: send to data keeper [ip:port , file name]
        for item in file_names_tables.items():
            IP,files = item
            for file in files:
                if(Need_to_replicate(file)):
                    #get another IP other than found
                    nextIP=getNextOtherIP(IP,file_names_tables,file)
                    #get free port to send to
                    nextPort=getFirstNextFreePort(nextIP,availability_table)
                    availability_table[nextPort] = False
                    print(file_name + "is taken now for replication..")
                    sockets[IP].send_pyobj([nextPort,file]) #send to the datakeeper having the file to send it to other data keeper given
                    wait(1)


#returns true if file does Need_to_replicate exist in tables<maxNumOfReplications
def Need_to_replicate(file_name):
    pass
    ## TODO: implement

#get ip doesn't have the same file
def getNextOtherIP(IP,file_names_tables,file):
    pass
    ## TODO: implement

def getFirstNextFreePort(nextIP,availability_table):
    pass
    ## TODO: implement
