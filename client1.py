import socket
import time 
import json
import tqdm
BufferSize = 100 # 100 Bytes for downloading data from server

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


UTF8 = "utf-8"



udp_host = socket.gethostname()
udp_port = 12345			       
msg =["Hello server i need some files for download!"]

msg = json.dumps(msg)
sock.sendto(msg.encode("utf-8"),(udp_host,udp_port))

print("Enter 1 for request list of files")
print("Enter 2 for download a file")
check = input()
if check == "1":
    Get_List_of_File = []
    Get_List_of_File.append("0x0000")
    Get_List_of_File = json.dumps(Get_List_of_File)
    sock.sendto(Get_List_of_File.encode("utf-8"),(udp_host,udp_port))
    data,addr = sock.recvfrom(1024)
    data = json.loads(data)   
    print(data)
elif check == "2":
    Download_File = []
    Download_File.append("0x0001")
    file_name = input("Enter file name for download --->")
    Download_File.append(file_name)
    Download_File = json.dumps(Download_File)
    Download_File = Download_File.encode(UTF8)
    #Sending file name to server for download
    sock.sendto(Download_File,(udp_host,udp_port))
    data,addr = sock.recvfrom(1024)
    data = data.decode(UTF8)
    data = json.loads(data)
    fileType = data[0]
    fileName = data[1]
    fileSize = data[2]
    if fileType == "0x0011" and fileSize == "0":
        print(data)
    else:
        print(data)     
        #From server started downloading
        fileSize = int(fileSize)
        progress = tqdm.tqdm(range(fileSize), f"Receiving {fileName}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(fileName, "wb") as file:
            singal = 0
            while True:
                #downloading data from server 
                data,addr = sock.recvfrom(fileSize)
                if len(data)==94: 
                    #Writing data into file 
                    file.write(data)
                    progress.update(len(data))  
                    break
                #Writing data into file 
                file.write(data)
                progress.update(len(data))
        sock.close()
    


