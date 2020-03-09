# TODO : complete file to send periodic replication signal
import time
import zmq

port =7000
context = zmq.Context()
print ("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect ("tcp://192.168.1.10:%s" % port)

print ("Sending replicate request ...")
socket.send_pyobj ({"first_ip" : "192.168.1.9"})
#  Get the reply.
message = socket.recv_pyobj()
print ("Received reply [", message, "]")


socket.send_pyobj ({"video_name" : "output.mp4", "video_name1" : "output24000.mp4", "video_name2" : "output24001.mp4", "video_name3" : "output24002.mp4"})

msgAfterSend = socket.recv_pyobj()
print (msgAfterSend)


context1 = zmq.Context()
print ("Connecting to server...")
socket1 = context1.socket(zmq.REP)
socket1.bind("tcp://192.168.1.9:%s" % port)
i=0
msg = socket1.recv_pyobj()
print (msg)
socket1.send_pyobj ("send videos")
while (True):

    msg = socket1.recv_pyobj()
    print (msg)
    file_output = "download"+str(i)+".mp4"

    if os.path.isfile(file_output):
        os.remove(file_output)

    with open(file_output, "wb") as out_file:
        out_file.write(msg)

    i+=1
    socket1.send_pyobj ("download"+str(i)+".mp4 is done")