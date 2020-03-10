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
    socket.send_pyobj (["replyDownload,",message[0]])
    message = socket.recv_pyobj()
    print ("Received reply from MasterTracker ", message, "....")
    context2 = zmq.Context()
    print ("Connecting to DataKeeper to Download...")
    socket2 = context2.socket(zmq.REP)
    socket2.connect ("tcp://"+message[0])
    socket2.send_pyobj ("download")
    #  Get the reply.
    message = socket2.recv_pyobj()
    print ("Received reply ", message, "....")

    socket2.send_pyobj (filename)

    msg = socket.recv_pyobj()
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
    print ("Enter the File Name With .mp4")
    filename= input()
    print ("Sending request to MasterTracker...")
    socket.send_pyobj ([str(request),filename])
    message = socket.recv_pyobj()
    if (message[0] == "e" and request == "upload"):
        print("this file is currently on the server please choose a file with an other name")
    elif (message[0] == "e" and request == "download"):
        print("there is no empty port for now")
    elif (request == "upload"):
        print(message)
        upload(message,str(filename))
    elif (request == "download"):
        print(message)
        download(message,str(filename))
    elif (request == "exit"):
        print("you entered this request " + request + " bye bye")
        break

