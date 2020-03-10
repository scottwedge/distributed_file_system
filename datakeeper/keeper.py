import time
import zmq
import cv2
import sys
import os
import socket as sok

#READIGN ARGUMENTS
port = 10000
MasterIP = sys.argv[1]
N = int(sys.argv[2])
MasterPort = 4000

def done(request, filename, socket):
    #list order ["dataKeeperSuccess" ,[ip, request(upload, download), filename]]
    socket.send_pyobj(["dataKeeperSuccess",[str(get_ip_address()) + ":" + str(port), request, filename]])
    msg = socket.recv_pyobj()
    print(msg)

###################################################################################
def download(socket, Msocket):
    socket.send_pyobj("send the video name\n")
    FILE_OUTPUT = socket.recv_pyobj()
    #print(msg)
    socket.send_pyobj("send the video")

    msg = socket.recv_pyobj()

    # Checks and deletes the output file
    # You cant have a existing file or it will through an error
    if os.path.isfile(FILE_OUTPUT):
        os.remove(FILE_OUTPUT)

    # opens the file 'output.avi' which is accessable as 'out_file'
    with open(FILE_OUTPUT, "wb") as out_file:  # open for [w]riting as [b]inary
        out_file.write(msg)

    socket.send_pyobj("the file is saved successfully") 
    done("upload", msg, Msocket)
###################################################################################

############################################
def Upload(socket, Msocket):
    socket.send_pyobj("send the video name\n")
    msg = socket.recv_pyobj()
    print(msg)
    file = open(msg, 'rb').read()
    socket.send_pyobj(file)
    done("download", msg, Msocket)
############################################

##################################################
def get_ip_address():
    s = sok.socket(sok.AF_INET, sok.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
###################################################

################        MAIN        ##################
context = zmq.Context()
socket = context.socket(zmq.REP)
print("binding to my ip tcp://" + str(get_ip_address()) + ":" + str(port))
socket.bind("tcp://" + str(get_ip_address()) + ":" + str(port))

masterContext = zmq.Context()
masterSocket = masterContext.socket(zmq.REQ)
print("connecting to all master processes")
for i in range(MasterPort, MasterPort + N):
    print("tcp://" + MasterIP + ":" + str(i), " THIS IP FOR SUCCESS")
    socket.connect("tcp://" + MasterIP + ":" + str(i))

while True:
    message = socket.recv_pyobj()
    print(message)
    #Upload(socket1)
    if (message == "upload"):
        download(socket, masterSocket)

    elif (message == "download"):
        Upload(socket, masterSocket)



#in success send ip and port, upload or download, filename
#4000
#5000
#6000
#7000
#10000