import socket
import pymysql
import threading
import struct
import os
THREADCOUNT = 10
LOCK = threading.Lock()
#python3.6

def ConnectMysql():
    conn = pymysql.connect(host='127.0.0.1',
                           user='root',
                           passwd='root',
                           db='mysql',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)
    global cur
    cur = conn.cursor()
    cur.execute("use clientip")
    return cur


def deal_data(host, port, password):
    global THREADCOUNT, fp
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 建立连接:
    conn.connect((host, int(port)))
    conn.send(password.encode())
    if conn.recv(1024).decode('utf-8') == '1':
        print("succes")
        while 1:
            fileinfo_size = struct.calcsize('128sl')
            
            buf = conn.recv(fileinfo_size)
            print(buf)
            if buf:
                
                filename, filesize = struct.unpack('128sl', buf)

                fn = str(filename, encoding="utf-8").strip('\0')
                new_filename = os.path.join('./', 'new_' + fn)
                print('file new name is {0}, filesize if {1}'.format(new_filename,
                                                                     filesize))

                recvd_size = 0  # 定义已接收文件的大小
                fp = open(new_filename, 'wb')
                print('start receiving...')

                while not recvd_size == filesize:
                    print(recvd_size)
                    if filesize - recvd_size > 1024:
                        data = conn.recv(1024)
                        recvd_size += len(data)
                    else:
                        data = conn.recv(filesize - recvd_size)
                        recvd_size = filesize
                    fp.write(data)
                '''
                try:
                    fp.write(data)
                except Exception as e:
                    pass
                '''
                    #fp.write(data)
                fp.close()
                print('end receive...')
            conn.send(str('succes').encode())
            conn.close()
            break
    LOCK.acquire()
    THREADCOUNT = THREADCOUNT - 1
    LOCK.release()

if __name__ == '__main__':
    cur = ConnectMysql()
    ipid = 0
    stat = True
    while stat:
        try:
            sql = "select* from `data` where id =" + str(ipid)
            print(sql)
            cur.execute(sql)  # where id =  + str(ipid))

            data = cur.fetchone()
            if(data == None):
                break

            print(data)
            if THREADCOUNT <= 10:
                t = threading.Thread(target=deal_data, args=(
                    data['ip'], data['port'], data['password']))
                t.start()
                LOCK.acquire()
                THREADCOUNT = THREADCOUNT + 1
                LOCK.release()
                ipid = ipid + 1

        except Exception as e:
            stat = False
        # 创建新线程来处理TCP连接:
       


#linux 定时执行脚本 **/1***/usr/local/etc/rc.d/httpd restart
#每一小时重启
#windows 任务计划程序
