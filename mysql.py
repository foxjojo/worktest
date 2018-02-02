import pymysql
conn = pymysql.connect(host = '10.203.75.46',user = 'myroot',passwd = 'root',db = 'mysql', unix_socket = '/var/lib/mysql/mysql.sock', charset = 'utf8')
cur = conn.cursor()
cur.execute("use PythonSpide")
#cur.execute("insert into pages (title, content) values (\"Test pages\",\"6545464654654564564654\")")
#cur.connection.commit()
cur.execute("select * from pages")
for x in cur.fetchall():
	print(x)
#cur.close()
#conn.close()
