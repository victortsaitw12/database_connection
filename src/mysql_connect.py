import pymysql

conn = pymysql.connect(host='10.149.7.17', port=3306, user='nwe', passwd='nwe1234', db='mes_db')

cur = conn.cursor()
cur.execute("SELECT * FROM dbauthorization")
rows = cur.fetchall()
for row in rows:
        print(row)
