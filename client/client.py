import time
import zmq
#import cv2 as cv
import sys
import os


# determine the port number 
port = 4000
N = int(sys.argv[1])
masterIp =sys.argv[2]
context = zmq.Context()
print ("Connecting to MasterTracker...")
socket = context.socket(zmq.REQ)
for i in range (N):
    socket.connect ("tcp://"+str(masterIp)+":%d" %(port+i))


def upload(message,filename):
    print ("upload")
    context1 = zmq.Context()
    print ("Connecting to DataKeeper to Upload...")
    socket1 = context1.socket(zmq.REQ)
    socket1.connect ("tcp://"+message)
    print ("Sending request upload request ...")
    socket1.send_pyobj ("upload")
    #  Get the reply.
    message = socket1.recv_pyobj()
    print ("Received reply ", message, "....")

    socket1.send_pyobj (filename)
    #  Get the reply.
    message = socket1.recv_pyobj()
    print ("Received reply ", message, "....")

    file = open(filename, 'rb').read()
    socket1.send_pyobj(file)

    msgAfterSend = socket1.recv_pyobj()
    print (msgAfterSend)
    socket1.close()

def download(message,filename):
    print ("download")
    socket.send_pyobj (["replyDownload",message[0]])
    message1 = socket.recv_pyobj()
    print ("Received reply from MasterTracker ", message1, "....")
    context2 = zmq.Context()
    print ("Connecting to DataKeeper to Download...")
    socket2 = context2.socket(zmq.REQ)
    print ("************************************ message => ",message[0])
    socket2.connect ("tcp://"+str(message[0]))
    socket2.send_pyobj ("download")
    #  Get the reply.
    message2 = socket2.recv_pyobj()
    print ("Received reply ", message2, "....")

    socket2.send_pyobj (filename)

    msg = socket2.recv_pyobj()
    print (msg)
    file_output = filename+".mp4"

    if os.path.isfile(file_output):
        os.remove(file_output)

    with open(file_output, "wb") as out_file:
        out_file.write(msg)
    socket2.close()


while (True):
    print ("Enter Your Request")
    request = input()
    if request == "upload" or request == "download" or request == "exit":
        print ("Enter the File Name With .mp4")
        filename= input()
        if os.path.exists(filename) or request == "download":

            # check on the file the file that is on the desk already 
            print ("Sending request to MasterTracker...")
            socket.send_pyobj ([str(request),filename])
            message = socket.recv_pyobj()
            print ("*****************************************************************************************************************************************")
            print ("*********************************************** Receive Response from the master ********************************************************")
            print ("*****************************************************************************************************************************************")
            print  ("This is the message from the master "+str(message))
            if (message[0] == "e" and request == "upload"):
                print ("*****************************************************************************************************************************************")
                print ("******************************************* we have upload request and have error message ***********************************************")
                print("this file is currently on the server please choose a file with an other name or there is no empty servers right now")
                print (message)
                print ("*****************************************************************************************************************************************")
            elif (message[0] == "e" and request == "download"):
                print ("*****************************************************************************************************************************************")
                print ("******************************************* we have download request and have error message *********************************************")
                print("there is no empty port for now")
                print (message)
                print ("*****************************************************************************************************************************************")
            elif (message[0] != "e" and request == "upload"):
                print ("*****************************************************************************************************************************************")
                print ("**************************************************** we have upload request *************************************************************")
                print(message)
                upload(message,str(filename))
                print ("*****************************************************************************************************************************************")
            elif (message[0] != "e" and request == "download"):
                print ("*****************************************************************************************************************************************")
                print ("****************************************************** we have download request *********************************************************")
                print(message)
                download(message,str(filename))
                print ("*****************************************************************************************************************************************")
            elif (request == "exit"):
                print ("you enters "+request)
                break
        else :
            print ("you entered a wrong file name please enter a right one XD")
    else:
        print  ("please enter a valid request between (upload, download, exit) ....")
