import socket
from sys import path
from threading import Thread
import os
import json
import tqdm
UTF8 = "utf-8"
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udp_host = socket.gethostname()		        
udp_port = 12345			        
sock.bind((udp_host,udp_port))
def FTP(data,addr):
    #This condition will check if client want to get list of files
    data = data.decode(UTF8)
    data = json.loads(data)
    print(data[0])
    check = data[0]
    if check == "0x0000":
        file_names = os.listdir("C:\\Users\\Marhaba\Desktop\\Computer Netwroks\\Lab_08\\File-Transfer-Protocol-Using-TCP\\Files")
        if len(file_names) > 0:
            ResponseToClientFilesList= []
            ResponseToClientFilesList.append("0x0010")
            #Calculating totall size of files in bytes
            dir = "C:\\Users\\Marhaba\Desktop\\Computer Netwroks\\Lab_08\\File-Transfer-Protocol-Using-TCP\\Files"
            totalSize = 0
            for dirpath, dirnames, filenames in os.walk(dir):
                for file in filenames:
                    file_path = os.path.join(dirpath, file)
                    if not os.path.islink(file_path):
                        totalSize += os.path.getsize(file_path)
            ResponseToClientFilesList.append(totalSize)
            ResponseToClientFilesList.append("Individual File Names --->")
            for file in file_names:
                ResponseToClientFilesList.append(file)
            ResponseToClientFilesList= json.dumps(ResponseToClientFilesList)
            sock.sendto(ResponseToClientFilesList.encode("utf-8"),addr)
        else:
            ResponseToClientFilesList= []
            ResponseToClientFilesList.append("0x0010")
            ResponseToClientFilesList.append("0")
            ResponseToClientFilesList.append("No files are found")
            ResponseToClientFilesList= json.dumps(ResponseToClientFilesList)
            sock.sendto(ResponseToClientFilesList.encode("utf-8"),addr)
    elif check == "0x0001":
        file_name_for_download = data[1]
        file_names = os.listdir("C:\\Users\\Marhaba\Desktop\\Computer Netwroks\\Lab_08\\File-Transfer-Protocol-Using-TCP\\Files")
        count = file_names.count(file_name_for_download)
        if count > 0:
            BufferSize = 100 # 100 Bytes for uploading data to client
            #file size 
            fileSize = os.path.getsize("C:\\Users\\Marhaba\Desktop\\Computer Netwroks\\Lab_08\\File-Transfer-Protocol-Using-TCP\\Files\\"+file_name_for_download)
            ResponseToClientDownloadFile= []
            ResponseToClientDownloadFile.append("0x0011")
            ResponseToClientDownloadFile.append(file_name_for_download)
            sizeFile = str(fileSize)
            ResponseToClientDownloadFile.append(sizeFile)
            ResponseToClientDownloadFile= json.dumps(ResponseToClientDownloadFile)
            #Sending file name and size to client
            sock.sendto(ResponseToClientDownloadFile.encode("utf-8"),addr)

            # Sending file from here and will use tqdm for progress bar
            progress_bar = tqdm.tqdm(range(fileSize), f"Sending {file_name_for_download}", unit="B", unit_scale=True, unit_divisor=1024)
            with open("C:\\Users\\Marhaba\Desktop\\Computer Netwroks\\Lab_08\\File-Transfer-Protocol-Using-TCP\\Files\\"+file_name_for_download, "rb") as file:
                while True:
                    # bytes are reading from file 100
                    bytes_read = file.read(BufferSize)
                    if not bytes_read:
                        break
                    #using sendall to assure transimission in busy network
                    sock.sendto(bytes_read,addr)
                    #Updating progress bar
                    progress_bar.update(len(bytes_read))
            
        else:
            ResponseToClientFilesList= []
            ResponseToClientFilesList.append("0x0011")
            ResponseToClientFilesList.append("No such file is avaiable for download")
            ResponseToClientFilesList.append("0")
            ResponseToClientFilesList= json.dumps(ResponseToClientFilesList)
            sock.sendto(ResponseToClientFilesList.encode("utf-8"),addr)
               
def main(): 
    while True:
        print ("Waiting for client...")
        data,addr = sock.recvfrom(1024)
        print(data.decode(UTF8))
        print(f"Client port number {addr}")
        FTP(data,addr)        
if __name__=='__main__':
    main()
        

    