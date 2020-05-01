import time
import zmq
import sys
import os
import socket as sok


def endRequest(request, filename, socket,MyIp):
    #list order ["dataKeeperSuccess" ,[ip, request(upload, download), filename]]
    print(["dataKeeperSuccess" ,[str(MyIp) + ":" + str(port), request, filename]])
    socket.send_pyobj(["dataKeeperSuccess" ,[str(MyIp) + ":" + str(port), str(request), str(filename)]])
    print ("Ahmed Here")
    msg = socket.recv_pyobj()
    print(msg)

###################################################################################
def download(socket, Msocket,MyIp):
    print("entered the client upload function")
    socket.send_pyobj("send the video name\n")
    FILE_OUTPUT = socket.recv_pyobj()
    print("recieved the video")
    #print(msg)
    socket.send_pyobj("send the video")
    msg = socket.recv_pyobj()
    print("sent the ack")
    # Checks and deletes the output file
    # You cant have a existing file or it will through an error
    if os.path.isfile(FILE_OUTPUT):
        os.remove(FILE_OUTPUT)

    # opens the file 'output.avi' which is accessable as 'out_file'
    with open(FILE_OUTPUT, "wb") as out_file:  # open for [w]riting as [b]inary
        out_file.write(msg)
    print("the video was saved")
    socket.send_pyobj("the file is saved successfully") 
    endRequest("upload", FILE_OUTPUT, Msocket,MyIp)
###################################################################################

############################################
def Upload(socket, Msocket,MyIp):
    print("entered the client download function")
    socket.send_pyobj("send the video name\n")
    msg = socket.recv_pyobj()
    print("filename needed to be downloaded ",msg)
    file = open(msg, 'rb').read()
    socket.send_pyobj(file)
    print("sent the file to client")
    endRequest("download", msg, Msocket,MyIp)
############################################

##################################################
# def get_ip_address():
#     s = sok.socket(sok.AF_INET, sok.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
#     return s.getsockname()[0]
# def get_ip_address():
#     return MyIp
###################################################

################        MAIN        ##################
#READIGN ARGUMENTS

def mainKeeper_func(MasterIP,MyIp,N):
    port = 10000
    MasterPort = 4000
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    print("binding to my ip tcp://" + str(MyIp) + ":" + str(port))
    socket.bind("tcp://" + str(MyIp) + ":" + str(port))

    masterContext = zmq.Context()
    masterSocket = masterContext.socket(zmq.REQ)
    print("connecting to all master processes")
    for i in range(MasterPort, MasterPort + N):
        print("tcp://" + MasterIP + ":" + str(i), " THIS IP FOR SUCCESS")
        masterSocket.connect("tcp://" + MasterIP + ":" + str(i))

    while True:
        message = socket.recv_pyobj()
        print(message)
        #Upload(socket1)
        if (message == "upload"):
            download(socket, masterSocket,MyIp)

        elif (message == "download"):
            Upload(socket, masterSocket,MyIp)



#in success send ip and port, upload or download, filename
#4000
#5000
#6000
#7000
#10000
