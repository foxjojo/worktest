import socket
import os
import sys
import struct
import os
import time
import threading
from scapy.all import *

HOST = 'localhost'   # use '' to expose to all networks
PORT = 12345
PASSWORD = "12345"
filepath = "C:\\Users\\Air-wang\\Desktop\\pcap.pcap"
pkts = []
count = 0
pcapnum = 0
pack = 0
LOCK = threading.Lock()


def socket_client(request):
    global filepath
    #request.send(b'1')

    while os.path.exists(filepath) ==False:
        print("bucunzai")
        time.sleep(0.2)

    while 1:
        # filepath = raw_input('please input file path: ')
        print(os.path.isfile(filepath))
        if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包含文件名和文件大小

            fhead = struct.pack('128sl', bytes(os.path.basename(
                filepath), 'utf-8'), os.stat(filepath).st_size)
            request.send(fhead)
            print('client filepath: {0}'.format(filepath))

            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print('{0} file send over...'.format(filepath))
                    break
                request.send(data)
        break


def mainthread():
    global pack
    try:
        """Open specified port and return file-like object"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # set SOL_SOCKET.SO_REUSEADDR=1 to reuse the socket if
        # needed later without waiting for timeout (after it is
        # closed, for example)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, PORT))
        sock.listen(0)   # do not queue connections
        request, addr = sock.accept()
        # print (request.recv(1024), addr)
        if request.recv(1024).decode('utf-8') == PASSWORD:
            request.send(b'1')
            
            LOCK.acquire()
            pack = 1
            LOCK.release()
            


            
            socket_client(request)
        if request.recv(1024).decode('utf-8') == "succes":
            os.remove(filepath)
            request.close()
            sock.close()
        else:
            request.close()
            sock.close()

    except Exception as e:
        sock.close()
        pass

def write_cap(x):
    global pkts
    global pack
    global pcapnum

    pkts.append(x)
    if pack == 1 :  #300 packets save one time
        pname = "C:\\Users\\Air-wang\\Desktop\\pcap.pcap" 
        t = threading.Thread(target=wrpcap, args=(pname, pkts))
        t.start()
        pkts = []
        LOCK.acquire()
        pack = 0
        LOCK.release()

        


def begin_packet():
    sniff(prn=write_cap, filter="tcp port 8080 or tcp port 80")

if __name__ == '__main__':
    t = threading.Thread(target=begin_packet, args=())
    t.start()
    while True:
        mainthread()
        print("h")
