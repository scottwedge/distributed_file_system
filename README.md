# Distributed_file_system
linux distributed file system with 1 master, N clients, and N dataKeepers.                                                                                                                                                                                    
To run this project on a single machie you need to create number of IPs to represent a different machines for the datakeeper and the master.


# To generate different IPs
    1- call "ip addr" to know what is the dev of your ip
    if your ip == 192.168.1.9/24 from ip addr
    and your dev = enp0s.
    2- call "sudo ip addr add 192.168.1.10/24 dev enp0s3"
    and now you can type "hostname -I" to check that you have now 2 ips
    
    
# To run master files 

  python3.8 knowSlaves.py #NumberofDatakeepers #NumberofProcessesinTheMaster 
 
  
# To run datakeeper files
  python3.8 script.py #NumberofProcessesinDatakeeper MasterIP #NumberofProcessesinTheMaster DatakeeperIP
  
  # To run client files
   python3.8 client.py #NumberofProcessesinTheMaster MasterIP
   
# Prerequisites
1- install python3.8                                                                                                        
2- install zmq                                                                                                              
3- install multiprocessing                                                                                                   
4- install sockect                                                                                                          
