import zmq
import time
'''
process responsible for dealing with alive messages and deleting dead devices
'''

def undertaker_func(undertaker_table,file_names_tables):
    # IP_table = shared_memory.SharedMemory(name="IP_table") #connect to shared memory
    print("undertaker process started")
    context = zmq.Context()
    port="6000" #back door for recieving alive messages from data keepers
    socket = context.socket(zmq.SUB)
    socket.subscribe("")
    for item in undertaker_table.items():
        IP,mylist = item
        socket.connect ("tcp://%s:%s"% (IP , port))
    start_time = time.time()
    #print ("************************************************************************this is the start time ::",start_time)
    print("timer initialized at "+str(start_time))
    while True:
        recieved_IP = socket.recv_string() 
        undertaker_table[recieved_IP][0] =True #set alive
        #print(str(recieved_IP)+" sends alive message")
        end_time = time.time()
        #print ("**********************************************************************this is the end time ::",end_time)
        #if a second has passed 
        #clean table / reset timer / reset is alive variables 
        if(int((end_time)- int(start_time)) > 1):
            for item in undertaker_table.items():
                IP,mylist = item
                if(mylist[0] == False):
                    print("deleting device "+str(IP)+" from the system")
                    del file_names_tables[IP]
                    del undertaker_table [IP]
                    
            for IP,mylist in undertaker_table:
                undertaker_table[IP][0] = False
        start_time = time.time() #reset timer

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
