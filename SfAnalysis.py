
import pynlpir
import sys
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root',
                       passwd='root', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("use sf")

TF = {}


def Analysis(s):
    print(s)
    if s == None:
        return
    pynlpir.open()
    try:
        segments = pynlpir.segment(s)
    except Exception as ee:
        return
    for segment in segments:
        try:
            TF[segment[0]]
        except Exception as e:
            TF[segment[0]] = 1
            break
        TF[segment[0]] = TF[segment[0]] + 1

    pynlpir.close()

if __name__ == '__main__':
    for id in range(1, 45106):
        cur.execute("select introduce from `novel` where id = " + id.__str__())
        data = cur.fetchone()
        Analysis(data[0])

    for x in TF.items():
        print(x[0]+str(x[1]))
        cur.execute("insert into ana (keyy, countt) values (%s, %s)", (x[0], str(x[1])))
        cur.connection.commit()

